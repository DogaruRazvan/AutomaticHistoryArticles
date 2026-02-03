from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class HistoryEvent(BaseModel):
    year: int
    event_date: date
    title: str
    raw_description: str
    ai_summary: str
    impact_score: float
    source_url: Optional[str] = None
    image_url: Optional[str] = None
    gallery: List[str] = []

class EventList(BaseModel):
    """Clasa care lipsea și cauza eroarea de referință"""
    events: List[HistoryEvent]
    total: int
    scraped_date: date