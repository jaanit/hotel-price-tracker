import logging

def setup_logger(name='HotelScraper'):
    """Configure and return a logger with both file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('scraper.log')
    
    # Create formatters and add it to handlers
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    c_format = logging.Formatter(log_format)
    f_format = logging.Formatter(log_format)
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    return logger