import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def setup_image_directories():
    """Set up image directories and move images from raw to media"""
    try:
        # Setup paths
        project_root = Path(__file__).parent.parent.parent
        raw_dir = project_root / "data" / "raw" / "images"
        media_dir = project_root / "data" / "media"
        
        # Create media directory if it doesn't exist
        media_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all images from raw directory
        image_files = list(raw_dir.glob("*.jpg")) + list(raw_dir.glob("*.png"))
        logger.info(f"Found {len(image_files)} images in raw directory")
        
        # Copy images to media directory
        for image_path in image_files:
            dest_path = media_dir / image_path.name
            shutil.copy2(image_path, dest_path)
            logger.info(f"Copied {image_path.name} to media directory")
            
        logger.info(f"Successfully copied {len(image_files)} images to media directory")
        
    except Exception as e:
        logger.error(f"Error preparing images: {str(e)}")
        raise

if __name__ == "__main__":
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    setup_image_directories() 