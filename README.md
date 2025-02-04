# Ethiopian Medical Data Analysis Project

This project collects, processes, and analyzes medical data from Ethiopian Telegram channels, performs object detection on medical images, and exposes the data through a REST API.

## Project Structure

ethiopian_medical_data/
├── src/
│ ├── api/
│ │ ├── init.py
│ │ ├── database.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── crud.py
│ │ └── main.py
│ ├── cleaning/
│ │ ├── __init__.py
│ │ ├── cleaner.py
│ ├── database/
│ │ ├── init.py
│ │ └── db_manager.py
│ ├── log_utils/
│ │ ├── init.py
│ │ └── logger.py
│ ├── object_detection/
│ │ ├── __init__.py
│ │ ├── detector.py
│ │ ├── setup.py
│ │ └── main.py
│ └── run_api.py
├── data/
│ ├── raw/
│ │ ├── messages/
│ │ └── images/
│ ├── processed/
│ └── media/
├── logs/
├── models/
│ ├── run_api.py
├── .env
└── requirements.txt

## Features

1. **Data Collection**
   - Scrapes medical data from Ethiopian Telegram channels
   - Stores raw data in JSON format

2. **Data Cleaning**
   - Processes raw JSON data
   - Extracts relevant information
   - Performs language detection (Amharic/English)
   - Calculates message statistics

3. **Object Detection**
   - Uses YOLOv5 for object detection in medical images
   - Processes images from Telegram messages
   - Stores detection results in database

4. **REST API**
   - Exposes processed data through FastAPI
   - Provides endpoints for messages and detections
   - Includes statistical analysis endpoints

## Setup

1. **Environment Setup**


# Clone the repository

git clone [repository-url]

cd ethiopian_medical_data

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

2. **Database Configuration**


# Create .env file with database credentials
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_data

3. **YOLOv5 Setup**

# Install YOLOv5 dependencies
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
cd ..


## Usage

1. **Data Processing Pipeline**

# Run the data cleaning pipeline
python src/cleaning/cleaner.py

# Run object detection
python src/object_detection/main.py

2. **API Server**

# Start the FastAPI server
python src/run_api.py

## API Endpoints

- `GET /`: Welcome message
- `GET /messages/`: List all messages
  - Query parameters:
    - `skip`: Number of records to skip
    - `limit`: Number of records to return
    - `channel`: Filter by channel name
    - `language`: Filter by language
- `GET /messages/{message_id}`: Get specific message
- `GET /detections/`: List all object detections
  - Query parameters:
    - `skip`: Number of records to skip
    - `limit`: Number of records to return
    - `class_name`: Filter by detected object class
    - `min_confidence`: Filter by minimum confidence score
- `GET /detections/{detection_id}`: Get specific detection
- `GET /stats/`: Get overall statistics

## Database Schema

1. **cleaned_messages**
   - message_id (PK)
   - channel
   - date
   - text
   - has_media
   - media_path
   - word_count
   - contains_url
   - language

2. **object_detections**
   - id (PK)
   - image_path
   - class_id
   - class_name
   - confidence
   - bbox_x1
   - bbox_y1
   - bbox_x2
   - bbox_y2
   - processed_date

## Requirements

- Python 3.8+
- PostgreSQL 12+
- CUDA-capable GPU (recommended for object detection)

## Dependencies

Main dependencies include:
- FastAPI
- SQLAlchemy
- PyTorch
- YOLOv5
- OpenCV
- Pandas
- Pydantic

See `requirements.txt` for complete list.

## Logging

- All operations are logged in the `logs/` directory
- Log files are named with timestamps
- Includes INFO, WARNING, and ERROR level logs

## Error Handling

- Comprehensive error handling throughout the pipeline
- Detailed error messages in logs
- API returns appropriate HTTP status codes
