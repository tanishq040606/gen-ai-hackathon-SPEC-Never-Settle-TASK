import re

class SummarizerAgent:
    def summarize(self, chunks, max_points=5):
        text = " ".join(chunks)
        text = re.sub(r"\s+", " ", text)

        sentences = re.split(r"(?<=[.!?])\s+", text)

        filtered = [
            s.strip()
            for s in sentences
            if 60 < len(s) < 300
        ]

        return filtered[:max_points]