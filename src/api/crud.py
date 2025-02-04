from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_messages(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    channel: str = None,
    language: str = None
) -> List[models.Message]:
    try:
        logger.info("Attempting to fetch messages from database")
        query = db.query(models.Message)
        
        if channel:
            query = query.filter(models.Message.channel == channel)
        if language:
            query = query.filter(models.Message.language == language)
        
        # Log the SQL query
        logger.info(f"SQL Query: {query}")
        
        messages = query.offset(skip).limit(limit).all()
        logger.info(f"Successfully fetched {len(messages)} messages")
        return messages
        
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        raise

def get_detections(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    class_name: str = None,
    min_confidence: float = None
) -> List[models.ObjectDetection]:
    try:
        logger.info("Attempting to fetch detections from database")
        query = db.query(models.ObjectDetection)
        
        if class_name:
            query = query.filter(models.ObjectDetection.class_name == class_name)
        if min_confidence:
            query = query.filter(models.ObjectDetection.confidence >= min_confidence)
        
        # Log the SQL query
        logger.info(f"SQL Query: {query}")
        
        detections = query.offset(skip).limit(limit).all()
        logger.info(f"Successfully fetched {len(detections)} detections")
        return detections
        
    except Exception as e:
        logger.error(f"Error fetching detections: {str(e)}")
        raise