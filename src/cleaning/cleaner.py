import json
import logging
from pathlib import Path
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self, raw_data_path):
        self.raw_data_path = Path(raw_data_path)
        
    def load_raw_data(self):
        """Load raw data from JSON file"""
        try:
            # Find all JSON files in the directory
            logger.info(f"Looking for JSON files in: {self.raw_data_path}")
            json_files = list(self.raw_data_path.glob('*.json'))
            logger.info(f"All files in directory: {[f.name for f in json_files]}")
            
            # Filter for scrape files
            scrape_files = [f for f in json_files if f.name.startswith('scrape_')]
            logger.info(f"Found {len(scrape_files)} JSON files matching pattern")
            
            if not scrape_files:
                raise FileNotFoundError("No scrape files found")
            
            # Use the most recent file
            latest_file = max(scrape_files, key=lambda x: x.stat().st_mtime)
            logger.info(f"Using most recent file: {latest_file}")
            
            # Read and parse JSON file
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Successfully loaded JSON data")
                return data
                
        except Exception as e:
            logger.error(f"Error loading raw data: {str(e)}")
            raise
            
    def convert_to_dataframe(self, raw_data):
        """Convert raw data to DataFrame"""
        try:
            rows = []
            for channel, channel_data in raw_data.items():
                # Extract messages from the channel data
                messages = channel_data.get('messages', [])
                logger.info(f"Processing channel {channel}: {len(messages)} messages")
                
                for msg in messages:
                    row = {
                        'channel': channel,
                        'message_id': msg.get('id'),
                        'date': msg.get('date'),
                        'text': msg.get('text', ''),
                        'has_media': msg.get('has_media', False),
                        'media_path': msg.get('media_path', '')
                    }
                    rows.append(row)
            
            if not rows:
                raise ValueError("No valid messages found in the data")
            
            df = pd.DataFrame(rows)
            logger.info(f"Successfully converted data to DataFrame with {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"Error converting to DataFrame: {str(e)}")
            raise
            
    def clean_data(self, df):
        """Clean the DataFrame"""
        try:
            # Create a copy to avoid modifying the original
            cleaned = df.copy()
            
            # Convert date strings to datetime
            cleaned['date'] = pd.to_datetime(cleaned['date'])
            
            # Sort by date
            cleaned = cleaned.sort_values('date')
            
            # Fill missing values
            cleaned['text'] = cleaned['text'].fillna('')
            cleaned['has_media'] = cleaned['has_media'].fillna(False)
            cleaned['media_path'] = cleaned['media_path'].fillna('')
            
            # Remove any duplicate messages
            cleaned = cleaned.drop_duplicates(subset=['message_id'])
            
            # Add derived columns
            cleaned['word_count'] = cleaned['text'].str.split().str.len()
            cleaned['contains_url'] = cleaned['text'].str.contains('http|www', case=False, na=False)
            cleaned['language'] = cleaned['text'].apply(
                lambda x: 'amharic' if any('\u1200' <= c <= '\u137F' for c in str(x)) else 'english'
            )
            
            logger.info(f"Successfully cleaned data, resulting in {len(cleaned)} rows")
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            raise