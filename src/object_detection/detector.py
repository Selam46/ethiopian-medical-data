import torch
import cv2
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime
import sys

logger = logging.getLogger(__name__)

class ObjectDetector:
    def __init__(self, model_path=None):
        self.project_root = Path(__file__).parent.parent.parent
        self.yolo_dir = self.project_root / "models" / "yolov5"
        
        # Add YOLOv5 to path
        if str(self.yolo_dir) not in sys.path:
            sys.path.append(str(self.yolo_dir))
        
        try:
            # Import YOLOv5 modules
            from models.common import DetectMultiBackend
            from utils.general import check_img_size
            
            # Set device first
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            logger.info(f"Using device: {self.device}")
            
            # Load YOLO model
            if model_path:
                self.model = DetectMultiBackend(model_path, device=self.device)
            else:
                # Use YOLOv5s.pt from the models directory
                weights_path = self.yolo_dir / 'yolov5s.pt'
                if not weights_path.exists():
                    logger.info("Downloading YOLOv5s weights...")
                    torch.hub.download_url_to_file(
                        'https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5s.pt',
                        str(weights_path)
                    )
                self.model = DetectMultiBackend(weights_path, device=self.device)
            
            # Set model parameters
            self.conf_thres = 0.25  # Confidence threshold
            self.iou_thres = 0.45   # NMS IOU threshold
            self.imgsz = check_img_size((640, 640), s=self.model.stride)  # Check image size
            
            # Move model to device
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise
        
    def process_image(self, image_path):
        """Process a single image and return detections"""
        try:
            # Import here to ensure YOLOv5 is in path
            from utils.general import non_max_suppression
            from utils.augmentations import letterbox
            
            # Load and preprocess image
            img0 = cv2.imread(str(image_path))
            if img0 is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Padded resize
            img = letterbox(img0, self.imgsz, stride=self.model.stride)[0]
            
            # Convert
            img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
            img = torch.from_numpy(img).to(self.device)
            img = img.float()
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if len(img.shape) == 3:
                img = img[None]  # expand for batch dim
            
            # Inference
            pred = self.model(img)
            if isinstance(pred, (list, tuple)):
                pred = pred[0]  # get first element if list/tuple
            
            # NMS
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres)
            
            # Process detections
            detections = []
            if len(pred[0]):
                # Rescale boxes from img_size to im0 size
                pred[0][:, :4] = self._scale_coords(img.shape[2:], pred[0][:, :4], img0.shape).round()
                
                # Convert detections to list of dictionaries
                for *xyxy, conf, cls in pred[0]:
                    detection = {
                        'image_path': str(image_path),
                        'class_id': int(cls),
                        'class_name': self.model.names[int(cls)],
                        'confidence': float(conf),
                        'bbox_x1': float(xyxy[0]),
                        'bbox_y1': float(xyxy[1]),
                        'bbox_x2': float(xyxy[2]),
                        'bbox_y2': float(xyxy[3]),
                        'processed_date': datetime.now()
                    }
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            raise
            
    def _scale_coords(self, img1_shape, coords, img0_shape):
        """
        Rescale coords (xyxy) from img1_shape to img0_shape
        """
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
        
        coords[:, [0, 2]] -= pad[0]  # x padding
        coords[:, [1, 3]] -= pad[1]  # y padding
        coords[:, :4] /= gain
        self._clip_coords(coords, img0_shape)
        return coords
        
    def _clip_coords(self, boxes, shape):
        """
        Clip bounding xyxy bounding boxes to image shape (height, width)
        """
        boxes[:, [0, 2]] = boxes[:, [0, 2]].clamp(0, shape[1])  # clip x
        boxes[:, [1, 3]] = boxes[:, [1, 3]].clamp(0, shape[0])  # clip y
        return boxes
        
    def process_directory(self, image_dir):
        """Process all images in a directory"""
        try:
            image_dir = Path(image_dir)
            logger.info(f"Processing images in directory: {image_dir}")
            
            # Create directory if it doesn't exist
            image_dir.mkdir(parents=True, exist_ok=True)
            
            all_detections = []
            image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))
            
            logger.info(f"Found {len(image_files)} images to process")
            
            for image_path in image_files:
                logger.info(f"Processing image: {image_path.name}")
                try:
                    detections = self.process_image(image_path)
                    all_detections.extend(detections)
                except Exception as e:
                    logger.error(f"Error processing {image_path.name}: {str(e)}")
                    continue
            
            # Convert to DataFrame
            if all_detections:
                df = pd.DataFrame(all_detections)
                logger.info(f"Successfully processed {len(image_files)} images with {len(df)} detections")
                return df
            else:
                logger.warning("No detections found in any images")
                return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error processing directory: {str(e)}")
            raise

    def save_detections(self, df, db_manager, table_name='object_detections'):
        """Save detection results to database"""
        try:
            if df.empty:
                logger.warning("No detections to save")
                return
                
            logger.info(f"Saving {len(df)} detections to database")
            
            # Ensure all required columns are present
            required_columns = [
                'image_path', 'class_id', 'class_name', 'confidence',
                'bbox_x1', 'bbox_y1', 'bbox_x2', 'bbox_y2', 'processed_date'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Save to database
            db_manager.save_dataframe(df, table_name, if_exists='append')
            logger.info(f"Successfully saved {len(df)} detections to table '{table_name}'")
            
        except Exception as e:
            logger.error(f"Error saving detections to database: {str(e)}")
            raise