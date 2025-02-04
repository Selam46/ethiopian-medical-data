from telethon import TelegramClient, events
import os
import logging
from datetime import datetime
import asyncio
from typing import List, Dict
import json
from pathlib import Path

class TelegramScraper:
    def __init__(self, session_name: str = "medical_scraper"):
        """Initialize the Telegram scraper with API credentials."""
        self.api_id = os.getenv("API_ID")
        self.api_hash = os.getenv("API_HASH")
        self.phone = os.getenv("PHONE_NUMBER")
        self.client = TelegramClient(session_name, self.api_id, self.api_hash)
        self.channels = [
            "DoctorsET",
            "lobelia4cosmetics",
            "yetenaweg",
            "EAHCI"
        ]
        
        # Create necessary directories
        self.raw_messages_path = Path("data/raw/messages")
        self.raw_images_path = Path("data/raw/images")
        
        # Create directories if they don't exist
        self.raw_messages_path.mkdir(parents=True, exist_ok=True)
        self.raw_images_path.mkdir(parents=True, exist_ok=True)
        
    async def initialize(self):
        """Start the client and authenticate."""
        await self.client.start(phone=self.phone)
        logging.info("Telegram client initialized successfully")
        
    async def scrape_channel(self, channel: str, limit: int = 100) -> Dict:
        """Scrape messages and media from a specific channel."""
        channel_data = {
            "messages": [],
            "images": []
        }
        
        try:
            entity = await self.client.get_entity(channel)
            messages = await self.client.get_messages(entity, limit=limit)
            
            for message in messages:
                # Extract message data
                msg_data = {
                    "id": message.id,
                    "date": message.date.isoformat(),
                    "text": message.text,
                    "has_media": message.media is not None
                }
                channel_data["messages"].append(msg_data)
                
                # Download media if present
                if message.media:
                    if hasattr(message.media, 'photo'):
                        path = f"data/raw/images/{channel}_{message.id}.jpg"
                        await message.download_media(path)
                        channel_data["images"].append(path)
                        
            return channel_data
            
        except Exception as e:
            logging.error(f"Error scraping channel {channel}: {str(e)}")
            return channel_data
            
    async def scrape_all_channels(self):
        """Scrape all channels."""
        all_data = {}
        
        for channel in self.channels:
            logging.info(f"Scraping channel: {channel}")
            messages = await self.scrape_channel(channel)
            all_data[channel] = messages
            
        # Save the data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.raw_messages_path / f"scrape_{timestamp}.json"
        
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(all_data, f, indent=4)
            
        logging.info("Scraping completed successfully")
        
    async def download_media(self, message, channel_name):
        """Download media from a message."""
        if message.media:
            try:
                # Create channel-specific directory
                channel_dir = self.raw_images_path / channel_name
                channel_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{message.id}.jpg"
                path = channel_dir / filename
                
                await self.client.download_media(message, str(path))
                return str(path)
            except Exception as e:
                logging.error(f"Error downloading media: {str(e)}")
                return None
        return None
