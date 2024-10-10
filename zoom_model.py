from pydantic import BaseModel, HttpUrl, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime
from profile_model import Profile
from meeting_model import Meeting


class ZoomModel(BaseModel):
    profile: Profile
    pastMeetings: List[Meeting]

    model_config = ConfigDict(extra="ignore")
