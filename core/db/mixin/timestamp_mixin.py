from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional

class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def set_updated_at(self):
        """Set the `updated_at` field to the current time."""
        self.updated_at = lambda: datetime.now(timezone.utc)