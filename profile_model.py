from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime


class CustomAttribute(BaseModel):
    key: str
    name: str
    value: str

    model_config = ConfigDict(extra="ignore")


class Profile(BaseModel):
    id: str
    first_name: str
    last_name: str
    display_name: str
    email: Optional[EmailStr]
    type: int
    role_name: str
    pmi: int
    use_pmi: bool
    vanity_url: Optional[str] = None
    personal_meeting_url: Optional[str] = None
    timezone: str
    verified: int
    dept: Optional[str]
    created_at: datetime
    last_login_time: datetime
    last_client_version: str
    pic_url: Optional[str] = None
    cms_user_id: str
    jid: str
    group_ids: List[str]
    im_group_ids: List[str]
    account_id: str
    language: str
    phone_number: Optional[str]
    status: str
    job_title: Optional[str]
    location: Optional[str]
    # custom_attributes: List[CustomAttribute] # Dictionaries can not be inserted as a property into Neo4j, would have to be it's own node.
    login_types: List[int]
    role_id: str
    account_number: int
    cluster: str
    user_created_at: datetime

    model_config = ConfigDict(extra="ignore")
