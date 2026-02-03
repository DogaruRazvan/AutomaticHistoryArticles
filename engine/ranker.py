class ScoringEngine:
    def __init__(self):
        self.impact_map = {
            "world war": 50, "revolution": 45, "independence": 40,
            "constitution": 35, "treaty": 30, "empire": 25
        }

    def calculate(self, item: dict) -> float:
        score = 10.0
        text = item.get("text", "").lower()

        # Analiză profunzime Wikipedia
        pages = item.get("pages", [])
        score += len(pages) * 7

        # Cuvinte cheie
        for word, bonus in self.impact_map.items():
            if word in text:
                score += bonus

        # IMPORTANT: Limitare strictă la 100 pentru a nu mai da eroare în Streamlit
        return float(min(score, 100.0))