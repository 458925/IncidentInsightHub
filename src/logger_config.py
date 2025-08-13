import logging
import sys
from datetime import datetime
import os

def setup_logger(name: str = "IncidentInsightHub", level: str = "INFO") -> logging.Logger:
    """
    Set up a comprehensive logger for the application with both console and file output
    
    Args:
        name: Logger name (used to identify different modules)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance with handlers and formatters
    """
    
    # Create main logger instance with specified name and level
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))  # Convert string level to logging constant
    
    # Prevent adding duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create detailed formatter for file logging (includes module, function, line number)
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create simple formatter for console output (cleaner, less verbose)
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Set up console handler - outputs to stdout with INFO level and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Only show INFO+ messages in console
    console_handler.setFormatter(simple_formatter)
    
    # Set up file handler - creates daily log files with DEBUG level and above
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Create logs directory if it doesn't exist
    
    # Generate daily log filename with current date
    log_filename = f"{log_dir}/incident_hub_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Log all messages to file
    file_handler.setFormatter(detailed_formatter)
    
    # Attach both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Log initial setup confirmation
    logger.info(f"Logger '{name}' initialized with level {level}")
    logger.debug(f"Log file: {log_filename}")
    
    return logger

def get_logger(name: str | None = None) -> logging.Logger:
    """
    Get or create a logger instance with the specified name
    
    Args:
        name: Logger name (defaults to main app name if None)
    
    Returns:
        Logger instance (creates new one if doesn't exist)
    """
    # Use default app name if no specific name provided
    if name is None:
        name = "IncidentInsightHub"
    
    # Return existing logger or create new one with this name
    return logging.getLogger(name)

# Application-wide logger instance
app_logger = setup_logger("IncidentInsightHub", "INFO") 