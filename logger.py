"""
Centralized Logging Module for Job Automation System
Provides consistent logging across all modules with file and console output
"""

import os
import logging
from datetime import datetime
from typing import Optional


# Log directory and file configuration
LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, 'job_automation.log')

# Global flag to track if logging has been configured
_logging_configured = False


def setup_logging(
    log_level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True
) -> None:
    """
    Configure the centralized logging system
    
    Args:
        log_level: Logging level (default: INFO)
        log_file: Custom log file path (default: job_automation.log)
        console_output: Whether to output to console (default: True)
    """
    global _logging_configured
    
    if _logging_configured:
        return
    
    log_file = log_file or LOG_FILE
    
    # Create formatter with detailed information
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # File handler - appends to the log file
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    _logging_configured = True
    
    # Log initialization
    logger = get_logger('logger')
    logger.info("=" * 80)
    logger.info(f"Logging initialized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    
    Args:
        name: Name for the logger (typically __name__ of the module)
        
    Returns:
        Configured logger instance
    """
    # Ensure logging is set up
    if not _logging_configured:
        setup_logging()
    
    return logging.getLogger(name)


def log_separator(logger: logging.Logger, char: str = "-", length: int = 60) -> None:
    """Log a separator line for visual clarity"""
    logger.info(char * length)


def log_section(logger: logging.Logger, title: str) -> None:
    """Log a section header"""
    logger.info("")
    log_separator(logger, "=")
    logger.info(f"  {title}")
    log_separator(logger, "=")


def log_subsection(logger: logging.Logger, title: str) -> None:
    """Log a subsection header"""
    logger.info("")
    logger.info(f"--- {title} ---")


def log_job_summary(logger: logging.Logger, feed_name: str, job_count: int, feed_url: str) -> None:
    """Log a summary for jobs from a specific feed"""
    logger.info(f"Feed: {feed_name}")
    logger.info(f"  URL: {feed_url}")
    logger.info(f"  Jobs found: {job_count}")


def log_total_summary(logger: logging.Logger, total_jobs: int, feed_count: int) -> None:
    """Log the total summary of all feeds"""
    log_separator(logger)
    logger.info(f"TOTAL: {total_jobs} jobs from {feed_count} feeds")
    log_separator(logger)


# Initialize logging on module import
setup_logging()

