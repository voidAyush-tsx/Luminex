from datetime import datetime, timedelta
from collections import deque


class SimpleRateLimiter:
    def __init__(self, max_requests_per_minute: int = 60, max_requests_per_day: int = 1000) -> None:
        self.max_per_minute = max_requests_per_minute
        self.max_per_day = max_requests_per_day
        self.minute_requests = deque()  # type: ignore[var-annotated]
        self.day_requests = deque()  # type: ignore[var-annotated]

    def can_make_request(self) -> bool:
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        while self.minute_requests and self.minute_requests[0] < minute_ago:
            self.minute_requests.popleft()
        day_ago = now - timedelta(days=1)
        while self.day_requests and self.day_requests[0] < day_ago:
            self.day_requests.popleft()
        if len(self.minute_requests) >= self.max_per_minute:
            return False
        if len(self.day_requests) >= self.max_per_day:
            return False
        return True

    def record_request(self) -> None:
        now = datetime.now()
        self.minute_requests.append(now)
        self.day_requests.append(now)


