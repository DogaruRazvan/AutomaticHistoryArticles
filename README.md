📜 Daily History Engine | AI-Powered Data Pipeline
This repository houses the Data Ingestion & Processing Core for the Daily History EdTech platform. It is a specialized ETL (Extract, Transform, Load) pipeline designed to convert raw historical data into immersive, interactive storytelling experiences.

🏗️ System Architecture
The engine functions as a decoupled microservice (deployed via Railway Cron Jobs), ensuring the Java Spring Boot backend remains focused on business logic and user management while this service handles heavy data lifting.

🛠️ Key Features & Tech Stack
Extraction Layer: High-performance interfacing with the MediaWiki API to fetch significant historical events based on chronological triggers.

LLM Intelligence Layer: Leverages Large Language Models (OpenAI/Anthropic) via specialized prompt engineering to:

Synthesize dry historical facts into engaging "Daily Stories."

Generate structured metadata (titles, summaries, tags, and SEO descriptions).

Automated Translation: Multi-language support layer (English-first) using automated translation pipelines to prepopulate the PostgreSQL global schema.

Media Cloud Pipeline: Integrated Cloudinary SDK for automated image fetching, optimization, and CDN delivery (strictly no local storage).

Data Integrity: Strict schema enforcement using Pydantic models to ensure 100% compatibility with the Spring Boot DTOs.

Security: Secured via X-Internal-API-Key headers for protected inter-service communication.
/src
 ├── agents/         # Prompt engineering & LLM orchestration
 ├── scrapers/       # MediaWiki & historical source connectors
 ├── models/         # Pydantic schemas for data validation
 ├── services/       # Translation, Cloudinary, and Push logic
 └── main.py         # Main execution entry point (Cron-ready)

 🚀 Execution Workflow
Fetch: Identify the "Event of the Day" through targeted historical queries.

Enrich: The LLM rewrites the event into a narrative format optimized for mobile UX (short paragraphs, high impact).

Localize: Translation layers generate localized versions for international markets.

Optimize: Visual assets are processed through Cloudinary for 60 FPS fluid rendering (WebP/AVIF formats).

Ingest: Validated data is pushed via a secure POST request to the Java Backend Ingestion API.

⚙️ Quick Start

# Install dependencies
pip install -r requirements.txt

# Environment Setup
cp .env.example .env # Configure OpenAI, Cloudinary, and Internal API Keys

# Run the pipeline manually
python src/main.py

💡 CTO Performance Notes
Scalability: The pipeline is stateless. If we need to process 1,000 years of history in one go, we can spin up multiple containers without data collision.

Performance: All images are delivered via CDN with auto-format/auto-quality to maintain that 60 FPS React Native target.

Reliability: Implemented exponential backoff for API calls to handle rate-limiting from external sources.
