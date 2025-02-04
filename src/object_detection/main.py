import os
import sys
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root / "src"))

from object_detection.setup import YOLOSetup
from object_detection.detector import ObjectDetector
from database.db_manager import DatabaseManager
from log_utils.logger import setup_logger

def main():
    # Set up logging
    logger = setup_logger()
    
    try:
        # Setup paths
        media_dir = project_root / "data" / "media"
        
        logger.info("=== Starting Object Detection Pipeline ===")
        
        # Setup YOLO
        logger.info("Setting up YOLO...")
        yolo_setup = YOLOSetup()
        yolo_setup.setup_yolo()
        
        # Initialize components
        detector = ObjectDetector()
        db_manager = DatabaseManager()
        
        # Process images
        logger.info("Processing images...")
        detections_df = detector.process_directory(media_dir)
        
        # Save results
        logger.info("Saving detection results...")
        db_manager.connect()
        try:
            detector.save_detections(detections_df, db_manager)
        finally:
            db_manager.disconnect()
        
        logger.info("=== Object Detection Pipeline Completed Successfully ===")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 