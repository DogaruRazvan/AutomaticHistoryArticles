import asyncio
from groq import Groq
from core.config import config
from core.logger import setup_logger

logger = setup_logger("Processor")


class AIProcessor:
    # Schimbă modelul aici cu unul dintre cele de mai jos:
    def __init__(self, model="llama-3.3-70b-specdec"):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = model

    async def summarize_event(self, text: str) -> str:
        prompt = f"""
        Act as a world-class historian and storyteller. Provide an exhaustive, premium narrative for: "{text}".

        REQUIRED STRUCTURE:
        1. ### [Catchy & Epic Headline]
        2. **The Historical Setting**: Describe the world state leading up to this moment. Why did this happen? (Min 100 words)
        3. **The Definitive Moment**: A step-by-step, dramatic retelling of the event itself. Use **bold** for key figures. (Min 150 words)
        4. **The Global Ripple Effect**: How did this change borders, laws, or human thought? (Min 100 words)
        5. **Legacy & Lessons**: Why should we care today? What is the *italicized* lesson?

        FORMATTING: 
        - Use Markdown (H3, Bold, Italics).
        - Use bullet points for key consequences.
        - Ensure the total length is substantial (400-600 words).
        """

        try:
            # Groq nu are nevoie de loop.run_in_executor pentru că librăria lor e foarte eficientă,
            # dar folosim varianta async pentru a nu bloca restul programului.
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a master historian."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,  # Suficient pentru cele 600 de cuvinte
                top_p=1,
                stream=False,
            )
            return completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Groq AI Error: {e}")
            return "History is deep, but our connection is thin. Please check your AI engine."