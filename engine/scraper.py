import httpx
import cloudinary
import cloudinary.uploader
from datetime import datetime
from typing import Optional, List  # Am adăugat List
from core.config import config
from core.logger import setup_logger

logger = setup_logger("Scraper")


class WikiScraper:
    def __init__(self):
        self.headers = {"User-Agent": config.USER_AGENT}
        cloudinary.config(
            cloud_name=config.CLOUDINARY_CLOUD_NAME,
            api_key=config.CLOUDINARY_API_KEY,
            api_secret=config.CLOUDINARY_API_SECRET,
            secure=True
        )

    async def fetch_today(self):
        now = datetime.now()
        url = f"{config.WIKI_BASE_URL}/feed/onthisday/events/{now.month}/{now.day}"
        async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                return data.get('selected', []) + data.get('events', [])
            except Exception as e:
                logger.error(f"Wiki Fetch Error: {e}")
                return []

    async def fetch_gallery_urls(self, title_slug: str, limit: int = 5) -> List[str]:
        """Caută o galerie de imagini pentru un subiect dat."""
        if not title_slug: return []
        title_slug_encoded = title_slug.replace(' ', '_')
        image_urls = []

        async with httpx.AsyncClient(headers=self.headers, timeout=15.0) as client:
            try:
                # Endpoint-ul de media-list e cel mai bun pentru galerii
                res = await client.get(f"{config.WIKI_BASE_URL}/page/media-list/{title_slug_encoded}")
                if res.status_code == 200:
                    items = res.json().get('items', [])
                    for item in items:
                        if item.get('type') == 'image':
                            # Luăm varianta cea mai mare din srcset sau src
                            img_src = item.get('srcset', [{}])[0].get('src') or item.get('title')
                            if img_src:
                                # Curățăm URL-ul (Wikipedia trimite uneori cu //)
                                full_url = f"https:{img_src}" if img_src.startswith("//") else img_src
                                # Evităm iconițele mici (SVG) care strică designul
                                if ".svg" not in full_url.lower():
                                    image_urls.append(full_url)

                        if len(image_urls) >= limit: break
            except Exception as e:
                logger.warning(f"Gallery fetch error for {title_slug}: {e}")

        # --- FALLBACK: Dacă nu avem galerie, încercăm imaginea principală (Summary) ---
        if not image_urls:
            try:
                res = await client.get(f"{config.WIKI_BASE_URL}/page/summary/{title_slug_encoded}")
                if res.status_code == 200:
                    data = res.json()
                    main_img = data.get('originalimage', {}).get('source')
                    if main_img: image_urls.append(main_img)
            except:
                pass

        # --- FINAL FALLBACK: Imagine generică dacă e gol ---
        if not image_urls:
            logger.info("ℹ️ Nu s-au găsit imagini pe Wiki. Se folosește fallback-ul generic.")
            # Pune aici un URL cu o imagine de pergament/istorie din Cloudinary-ul tău
            image_urls.append(
                "https://images.unsplash.com/photo-1524850041227-6177e2f47000?q=80&w=1000&auto=format&fit=crop")

        return image_urls

    def upload_to_cloudinary(self, image_url: str, public_id: str) -> Optional[str]:
        try:
            logger.info(f"📤 Se urcă imaginea pe Cloudinary: {public_id}")
            result = cloudinary.uploader.upload(
                image_url,
                public_id=f"history_app/{public_id}",
                overwrite=True,
                transformation=[
                    {'width': 1200, 'crop': "limit"},  # Puțin mai mare pentru galerii
                    {'quality': "auto"},
                    {'fetch_format': "auto"}
                ]
            )
            return result.get('secure_url')
        except Exception as e:
            logger.error(f"Cloudinary Error: {e}")
            return None