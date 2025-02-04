from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MessageBase(BaseModel):
    channel: str
    text: str
    has_media: bool
    media_path: Optional[str] = None
    word_count: Optional[int] = None
    contains_url: Optional[bool] = None
    language: str

class MessageCreate(MessageBase):
    message_id: str
    date: datetime

class Message(MessageBase):
    message_id: str
    date: datetime
    
    class Config:
        from_attributes = True

class ObjectDetectionBase(BaseModel):
    image_path: str
    class_id: int
    class_name: str
    confidence: float
    bbox_x1: float
    bbox_y1: float
    bbox_x2: float
    bbox_y2: float

class ObjectDetection(ObjectDetectionBase):
    id: int
    processed_date: datetime
    
    class Config:
        from_attributes = True

class Stats(BaseModel):
    total_messages: int
    messages_by_language: dict
    messages_with_media: int
    average_word_count: float 