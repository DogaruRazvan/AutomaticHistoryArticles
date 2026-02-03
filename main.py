import asyncio
import os
from datetime import datetime
from core.logger import setup_logger
from core.config import config
from engine.scraper import WikiScraper
from engine.processor import AIProcessor
from engine.ranker import ScoringEngine
from schema.models import HistoryEvent, EventList

logger = setup_logger("Main")


async def main():
    logger.info("🚀 Pornire Pipeline Premium...")

    if not os.path.exists("archive"):
        os.makedirs("archive")

    scraper = WikiScraper()
    processor = AIProcessor(config.AI_MODEL)
    ranker = ScoringEngine()

    # 1. Fetch & Rank
    raw_data = await scraper.fetch_today()
    if not raw_data: return
    for item in raw_data:
        item['calculated_score'] = ranker.calculate(item)
    raw_data.sort(key=lambda x: x['calculated_score'], reverse=True)
    best_item = raw_data[0]

    # 2. AI Summary
    summary = await processor.summarize_event(best_item.get("text", ""))

    # 3. Media Gallery (Wiki -> Cloudinary)
    pages = best_item.get("pages", [])
    slug = pages[0].get("titles", {}).get("canonical") if pages else "event"

    # Luăm până la 3 poze
    wiki_imgs = await scraper.fetch_gallery_urls(slug, limit=3)

    cloudinary_urls = []
    for idx, img_url in enumerate(wiki_imgs):
        public_id = f"{best_item.get('year')}_{slug.replace(' ', '_')}_{idx}"
        c_url = scraper.upload_to_cloudinary(img_url, public_id)
        if c_url:
            cloudinary_urls.append(c_url)

    # 4. Construire Obiect Final
    top_event = HistoryEvent(
        year=best_item.get("year", 0),
        event_date=datetime.now().date(),
        title=best_item.get("text", "")[:200],
        raw_description=best_item.get("text", ""),
        ai_summary=summary,
        impact_score=best_item['calculated_score'],
        source_url=f"https://en.wikipedia.org/wiki/{slug}" if slug else None,
        image_url=cloudinary_urls[0] if cloudinary_urls else None,
        gallery=cloudinary_urls
    )

    output = EventList(events=[top_event], total=1, scraped_date=datetime.now().date())

    # 5. Salvare dublă (Arhivă + Current)
    today_str = datetime.now().strftime("%Y-%m-%d")
    with open(f"archive/history_{today_str}.json", "w", encoding="utf-8") as f:
        f.write(output.model_dump_json(indent=2))
    with open("output.json", "w", encoding="utf-8") as f:
        f.write(output.model_dump_json(indent=2))

    logger.info(f"✅ Succes! S-au salvat {len(cloudinary_urls)} imagini.")


if __name__ == "__main__":
    asyncio.run(main())