import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get database credentials
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('DB_NAME', 'medical_data')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD')
        
        if not self.db_password:
            raise ValueError("Database password not found in environment variables")
        
        self.engine = None
        
    def connect(self):
        """Create database connection"""
        try:
            if not self.engine:
                # URL encode the password to handle special characters
                encoded_password = quote_plus(self.db_password)
                
                # Print current environment variables (without password)
                logger.info("Database connection parameters:")
                logger.info(f"Host: {self.db_host}")
                logger.info(f"Port: {self.db_port}")
                logger.info(f"Database: {self.db_name}")
                logger.info(f"User: {self.db_user}")
                
                # Create connection string with encoded password
                conn_str = f"postgresql://{self.db_user}:{encoded_password}@{self.db_host}:{self.db_port}/{self.db_name}"
                
                # Create engine
                self.engine = create_engine(
                    conn_str,
                    echo=False,
                    pool_pre_ping=True
                )
                
                # Test connection
                with self.engine.connect() as conn:
                    result = conn.execute(text("SELECT 1"))
                    result.fetchone()
                    logger.info("Database connection successful")
                
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            # Print the actual connection string (with password masked)
            safe_conn_str = f"postgresql://{self.db_user}:****@{self.db_host}:{self.db_port}/{self.db_name}"
            logger.error(f"Attempted connection string: {safe_conn_str}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            logger.info("Database connection closed")
    
    def save_dataframe(self, df, table_name, if_exists='replace'):
        """Save DataFrame to database"""
        try:
            if not self.engine:
                self.connect()
            
            logger.info(f"Saving DataFrame to table '{table_name}'")
            logger.info(f"DataFrame shape: {df.shape}")
            
            df.to_sql(
                table_name,
                self.engine,
                if_exists=if_exists,
                index=False
            )
            
            # Verify the save
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.scalar()
                logger.info(f"Successfully saved {count} rows to table '{table_name}'")
            
        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
            raise