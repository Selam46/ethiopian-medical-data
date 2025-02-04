# Data Analysis Notebooks

This directory contains Jupyter notebooks for analyzing the Ethiopian medical data.

## Available Notebooks

### 1. Message Analysis
- `message_analysis.ipynb`: Analyzes Telegram messages
  - Message frequency over time
  - Language distribution
  - Word count statistics
  - URL analysis
  - Channel activity comparison

### 2. Object Detection Analysis
- `object_detection_analysis.ipynb`: Analyzes detection results
  - Detection confidence distribution
  - Object class distribution
  - Detection counts per image
  - Temporal analysis of detections

### 3. Data Quality Analysis
- `data_quality.ipynb`: Assesses data quality
  - Missing value analysis
  - Data completeness
  - Language detection accuracy
  - Image quality metrics



3. Navigate to the desired notebook

## Required Dependencies

- pandas
- matplotlib
- seaborn
- numpy
- sqlalchemy
- opencv-python
- plotly (for interactive visualizations)

## Data Sources

The notebooks analyze data from:
1. PostgreSQL database tables:
   - cleaned_messages
   - object_detections
2. Raw data files in data/raw/
3. Processed data in data/processed/

## Best Practices

1. **Environment**
   - Use the project's virtual environment
   - Keep dependencies updated

2. **Data Access**
   - Use database connection strings from .env
   - Don't store credentials in notebooks

3. **Visualization**
   - Use consistent color schemes
   - Include clear titles and labels
   - Add explanatory markdown cells

4. **Code Organization**
   - Keep cells focused and modular
   - Include error handling
   - Add comments for complex operations

## Contributing

When adding new notebooks:
1. Follow the naming convention
2. Update this README
3. Include clear documentation
4. Add requirements if needed

## Note

- Notebooks are for analysis only
- Production code should be in the src/ directory
- Keep notebooks synced with git
- Clear outputs before committing