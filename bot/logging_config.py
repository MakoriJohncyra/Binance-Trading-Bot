"""
This file sets up logging - like a diary for our program.
It records what happens so we can check if something goes wrong.
"""

import logging
import sys
from datetime import datetime

def setup_logging():
    """
    Creates and sets up our program's diary system.
    It writes to both a file and shows messages on screen.
    """
    # Create a diary/logger named 'trading_bot'
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.DEBUG)  # Record everything
    
    # Create a file to write logs to (with today's date)
    log_filename = f'trading_bot_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)  # Write all details to file
    
    # Create a screen display for logs
    screen_handler = logging.StreamHandler(sys.stdout)
    screen_handler.setLevel(logging.INFO)  # Only show important messages on screen
    
    # Create a format for our log messages
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Apply the format to both handlers
    file_handler.setFormatter(log_format)
    screen_handler.setFormatter(log_format)
    
    # Connect the handlers to our logger
    logger.addHandler(file_handler)
    logger.addHandler(screen_handler)
    
    logger.info(f"Logging system started. Writing logs to: {log_filename}")
    return logger