import datetime
from dataclasses import dataclass


@dataclass
class Review:
    review_id: str
    business_id: str
    user_id: str
    stars: float
    review_date: datetime.date
    votes_funny: int
    votes_useful: int
    votes_cool: int
    review_text: str

    def __str__(self):
        return self.review_id

    def __repr__(self):
        return self.review_id

    def __hash__(self):
        return hash(self.review_id)
