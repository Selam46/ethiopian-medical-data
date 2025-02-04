import os
import subprocess
import logging
from pathlib import Path

class DBTRunner:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.logger = logging.getLogger(__name__)
        
    def run_dbt_command(self, command):
        """Run a DBT command"""
        try:
            result = subprocess.run(
                f"dbt {command}",
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.logger.error(f"DBT command failed: {result.stderr}")
                raise Exception(f"DBT command failed: {command}")
                
            self.logger.info(f"DBT command successful: {command}")
            return result.stdout
            
        except Exception as e:
            self.logger.error(f"Error running DBT command: {str(e)}")
            raise
            
    def run_transformation(self):
        """Run the complete DBT transformation pipeline"""
        try:
            # Install dependencies
            self.run_dbt_command("deps")
            
            # Run the models
            self.run_dbt_command("run")
            
            # Run tests
            self.run_dbt_command("test")
            
            # Generate documentation
            self.run_dbt_command("docs generate")
            
            self.logger.info("DBT transformation pipeline completed successfully")
            
        except Exception as e:
            self.logger.error(f"DBT transformation pipeline failed: {str(e)}")
            raise 