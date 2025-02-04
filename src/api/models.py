from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Message(Base):
    __tablename__ = "cleaned_messages"
    
    message_id = Column(String, primary_key=True)
    channel = Column(String)
    date = Column(DateTime)
    text = Column(String)
    has_media = Column(Boolean)
    media_path = Column(String)
    word_count = Column(Integer)
    contains_url = Column(Boolean)
    language = Column(String)

class ObjectDetection(Base):
    __tablename__ = "object_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String)
    class_id = Column(Integer)
    class_name = Column(String)
    confidence = Column(Float)
    bbox_x1 = Column(Float)
    bbox_y1 = Column(Float)
    bbox_x2 = Column(Float)
    bbox_y2 = Column(Float)
    processed_date = Column(DateTime) 