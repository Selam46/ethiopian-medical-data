import subprocess
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class YOLOSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.models_dir = self.project_root / "models"
        self.yolo_dir = self.models_dir / "yolov5"
        
    def setup_yolo(self):
        """Set up YOLOv5 and install dependencies"""
        try:
            logger.info("Setting up YOLO environment...")
            
            # Create models directory
            self.models_dir.mkdir(exist_ok=True)
            
            # Clone YOLOv5 if not already present
            if not self.yolo_dir.exists():
                logger.info("Cloning YOLOv5 repository...")
                subprocess.run([
                    "git", "clone",
                    "https://github.com/ultralytics/yolov5.git",
                    str(self.yolo_dir)
                ], check=True)
            
            # Install YOLOv5 requirements
            logger.info("Installing YOLOv5 requirements...")
            requirements_file = self.yolo_dir / "requirements.txt"
            subprocess.run([
                "pip", "install", "-r", str(requirements_file)
            ], check=True)
            
            logger.info("YOLO setup completed successfully")
            
        except Exception as e:
            logger.error(f"Error setting up YOLO: {str(e)}")
            raise 