import os

# Browser settings
CHROME_BINARY_PATH = '/usr/bin/chromium'
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'

# Data settings
DATA_DIR = '/app/data'
DEFAULT_OUTPUT_FILE = 'hotel_data.json'

# Scraping settings
DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 2

# Selectors for different elements
SELECTORS = {
    'hotel_card': 'div[class*="yuAt yuAt-pres-rounded"]',
    'hotel_name': 'a.FLpo-big-name',
    'hotel_location': '.upS4-big-name',
    'hotel_price': '.zV27-price-section .c1XBO, .Ptt7-price',
    'hotel_rating': '.wdjx',
    'hotel_reviews': '.xdhG-rating-description-and-count',
    'hotel_description': '.b40a-desc-text, .b40a-desc-wrap--full',
    'hotel_address': '.c3xth-address',
    'room_card': '.c5l3f',
    'hotel_image': '.e9fk-photo',
}

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)