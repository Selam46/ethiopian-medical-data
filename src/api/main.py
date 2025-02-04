from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, models, schemas
from .database import engine, get_db
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Ethiopian Medical Data API",
    description="API for accessing Ethiopian medical data from Telegram channels",
    version="1.0.0"
)

@app.get("/messages/", response_model=List[schemas.Message])
async def read_messages(
    skip: int = 0,
    limit: int = 100,
    channel: Optional[str] = None,
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get messages with optional filtering"""
    try:
        logger.info("Processing request to /messages/")
        messages = crud.get_messages(db, skip=skip, limit=limit, channel=channel, language=language)
        return messages
    except Exception as e:
        logger.error(f"Error processing messages request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/detections/", response_model=List[schemas.ObjectDetection])
async def read_detections(
    skip: int = 0,
    limit: int = 100,
    class_name: Optional[str] = None,
    min_confidence: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Get object detections with optional filtering"""
    try:
        logger.info("Processing request to /detections/")
        detections = crud.get_detections(
            db, 
            skip=skip, 
            limit=limit, 
            class_name=class_name,
            min_confidence=min_confidence
        )
        return detections
    except Exception as e:
        logger.error(f"Error processing detections request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))