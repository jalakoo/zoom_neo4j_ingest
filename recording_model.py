from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime


class Recording(BaseModel):
    id: str
    meeting_id: str
    recording_start: datetime
    recording_end: datetime
    file_type: str
    file_extension: str
    file_size: int
    play_url: Optional[str] = None
    download_url: Optional[str] = None
    status: str
    recording_type: str

    model_config = ConfigDict(extra="ignore")
