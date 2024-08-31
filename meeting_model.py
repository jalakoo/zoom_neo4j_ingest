from pydantic import BaseModel, HttpUrl, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class SummaryDetail(BaseModel):
    label: str
    summary: str


class Summary(BaseModel):
    # meeting_host_id: Optional[str] = None
    # meeting_host_email: Optional[EmailStr] = None
    # meeting_uuid: Optional[str] = None
    # meeting_id: Optional[int] = None
    # meeting_topic: Optional[str] = None
    # meeting_start_time: Optional[datetime] = None
    # meeting_end_time: Optional[datetime] = None
    # summary_start_time: Optional[datetime] = None
    # summary_end_time: Optional[datetime] = None
    # summary_created_time: Optional[datetime] = None
    # summary_last_modified_time: Optional[datetime] = None
    # summary_title: str
    # summary_overview: Optional[str] = None
    # summary_details: Optional[List[SummaryDetail]] = None
    # next_steps: Optional[List[str]] = (
    #     None  # Assuming this can be an empty list or contain string items
    # )
    meeting_host_id: str
    meeting_host_email: str
    meeting_uuid: str
    meeting_id: int
    meeting_topic: str
    meeting_start_time: str
    meeting_end_time: str
    summary_start_time: str
    summary_end_time: str
    summary_created_time: str
    summary_last_modified_time: str
    summary_title: str
    summary_overview: Optional[str] = Field(default="")
    summary_details: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")


class Participant(BaseModel):
    id: Optional[str] = None
    user_id: str
    participant_uuid: str
    user_name: str
    device: str
    ip_address: str
    internal_ip_addresses: Optional[List[str]] = None
    location: str
    network_type: str
    microphone: Optional[str] = None
    speaker: Optional[str] = None
    camera: Optional[str] = None
    data_center: str
    full_data_center: str
    connection_type: Optional[str] = None
    join_time: datetime
    leave_time: datetime
    share_application: bool
    share_desktop: bool
    share_whiteboard: bool
    recording: bool
    pc_name: Optional[str] = None
    domain: Optional[str] = None
    mac_addr: Optional[str] = None
    harddisk_id: Optional[str] = None
    version: Optional[str]
    leave_reason: str
    email: Optional[EmailStr] = None
    audio_quality: Optional[str] = None
    video_quality: Optional[str] = None
    screen_share_quality: Optional[str] = None
    registrant_id: Optional[str] = None
    status: str
    os: str
    os_version: Optional[str] = None
    device_name: Optional[str] = None
    groupId: Optional[str] = None
    health: str
    customer_key: Optional[str] = None
    sip_uri: Optional[str] = None
    from_sip_uri: Optional[str] = None
    role: str
    participant_user_id: Optional[str] = None
    audio_call: List[str]  # Assuming this can be an empty list or contain string items

    model_config = ConfigDict(extra="ignore")


class Details(BaseModel):
    uuid: str
    id: int
    topic: str
    type: int
    start_time: datetime
    duration: int
    total_minutes: int
    participants_count: int

    model_config = ConfigDict(extra="ignore")


class Meeting(BaseModel):
    details: Details
    participants: List[Participant]
    recordings: List[str]  # Assuming this can be an empty list or contain string items
    summary: Optional[Summary] = Field(default=None)

    model_config = ConfigDict(extra="ignore")
