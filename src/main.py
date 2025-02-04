import os
from pathlib import Path
from cleaning.cleaner import DataCleaner
from database.db_manager import DatabaseManager
from log_utils.logger import setup_logger

def main():
    # Set up logging
    logger = setup_logger()
    
    try:
        # Setup paths
        project_root = Path(__file__).parent.parent
        data_dir = project_root / "data" / "raw" / "messages"
        processed_dir = project_root / "data" / "processed"
        
        logger.info("=== Starting Data Pipeline ===")
        logger.info(f"Data directory: {data_dir}")
        
        # Initialize components
        cleaner = DataCleaner(raw_data_path=str(data_dir))
        db_manager = DatabaseManager()
        
        # Step 1: Load and Clean Data
        logger.info("Step 1: Loading and Cleaning Data")
        raw_data = cleaner.load_raw_data()
        df = cleaner.convert_to_dataframe(raw_data)
        cleaned_df = cleaner.clean_data(df)
        
        # Step 2: Save to Database
        logger.info("Step 2: Loading to Database")
        db_manager.connect()
        try:
            db_manager.save_dataframe(cleaned_df, 'cleaned_messages', if_exists='replace')
            logger.info("Data loaded to database successfully")
        finally:
            db_manager.disconnect()
        
        logger.info("=== Pipeline Completed Successfully ===")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()