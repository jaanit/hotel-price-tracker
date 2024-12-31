# ./scraper/src/hotel_scraper.py

import os
import time
import json
import random
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from fake_useragent import UserAgent

def setup_logger():
    """Configure and return a logger with both file and console handlers"""
    logger = logging.getLogger('HotelScraper')
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

class KayakHotelScraper:
    def __init__(self, city, check_in_date, check_out_date):
        self.logger = setup_logger()
        self.city = city
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.base_url = "https://www.kayak.com"
        self.hotels_data = []
        self.setup_driver()

    def setup_driver(self):
        """Configure Selenium WebDriver with appropriate options"""
        chrome_options = Options()
        
        # Basic Chrome options
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.binary_location = '/usr/bin/chromium'
        
        # Anti-bot detection options
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set realistic user agent
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')

        service = Service(executable_path='/usr/bin/chromedriver')
        
        try:
            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
            
            # Additional configurations
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": user_agent,
                "platform": "Windows"
            })
            
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            self.driver.implicitly_wait(10)
            self.logger.info("WebDriver initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise

    def wait_for_element(self, selector, timeout=10, parent=None):
        """Wait for element and return it when available"""
        try:
            element = WebDriverWait(parent or self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except:
            return None

    def find_element_with_retry(self, parent, selector, max_retries=3):
        """Find element with retry logic for stale elements"""
        for attempt in range(max_retries):
            try:
                return parent.find_element(By.CSS_SELECTOR, selector)
            except StaleElementReferenceException:
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)
            except NoSuchElementException:
                return None

    def construct_search_url(self):
        """Construct the search URL for Kayak"""
        check_in = self.check_in_date.strftime('%Y-%m-%d')
        check_out = self.check_out_date.strftime('%Y-%m-%d')
        return f"{self.base_url}/hotels/errachidia-c52508/{check_in}/{check_out}/2adults?sort=rank_a"

    def get_page(self, url):
        """Get page with retry logic and random delays"""
        try:
            self.logger.info(f"Loading URL: {url}")
            self.driver.get(url)
            
            # Wait for initial page load
            time.sleep(5)
            
            # Scroll page to trigger lazy loading
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_count = 0
            while scroll_count < 3:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_count += 1
            
            # Final wait for dynamic content
            time.sleep(3)
            
            self.logger.info("Page loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading page: {str(e)}")
            return False

    def extract_hotel_basic_info(self, hotel_element):
        """Extract basic hotel information from search result element"""
        try:
            hotel_info = {}
            
            # Get hotel name and URL
            try:
                name_elem = self.find_element_with_retry(hotel_element, 'a.FLpo-big-name')
                if name_elem:
                    hotel_info['name'] = name_elem.text.strip()
                    hotel_info['detail_url'] = name_elem.get_attribute('href')
            except:
                self.logger.warning("Could not find hotel name/URL")
                return None
            
            # Get location
            location_elem = self.find_element_with_retry(hotel_element, '.upS4-big-name')
            if location_elem:
                hotel_info['location'] = location_elem.text.strip()
            
            # Get price
            try:
                price_elem = self.find_element_with_retry(hotel_element, '.zV27-price-section .c1XBO') or \
                           self.find_element_with_retry(hotel_element, '.Ptt7-price')
                if price_elem:
                    hotel_info['price'] = price_elem.text.strip()
            except:
                hotel_info['price'] = None

            # Get rating
            try:
                rating_elem = self.find_element_with_retry(hotel_element, '.wdjx')
                reviews_elem = self.find_element_with_retry(hotel_element, '.xdhG-rating-description-and-count')
                if rating_elem:
                    hotel_info['rating'] = rating_elem.text.strip()
                if reviews_elem:
                    hotel_info['reviews'] = reviews_elem.text.strip()
            except:
                pass
            
            return hotel_info
            
        except Exception as e:
            self.logger.error(f"Error extracting hotel info: {str(e)}")
            return None

    def scrape_hotels(self, limit=None):
        """Main method to scrape hotel data"""
        try:
            # Get the search results page
            url = self.construct_search_url()
            if not self.get_page(url):
                return []
            
            # Find all hotel elements
            hotel_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class*="yuAt yuAt-pres-rounded"]'))
            )
            
            total_hotels = len(hotel_elements)
            self.logger.info(f"Found {total_hotels} hotels")
            
            if limit:
                hotel_elements = hotel_elements[:limit]
                self.logger.info(f"Processing first {limit} hotels")
            
            # Process each hotel
            for index, hotel_element in enumerate(hotel_elements, 1):
                try:
                    self.logger.info(f"Processing hotel {index}/{len(hotel_elements)}")
                    
                    # Get basic info
                    hotel_info = self.extract_hotel_basic_info(hotel_element)
                    
                    if hotel_info and hotel_info.get('detail_url'):
                        # Get detailed info
                        details = self.extract_hotel_details(hotel_info['detail_url'])
                        
                        if details:
                            hotel_info.update(details)
                            self.hotels_data.append(hotel_info)
                            self.logger.info(f"Successfully processed: {hotel_info['name']}")
                    
                    # Random delay between hotels
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    self.logger.error(f"Error processing hotel {index}: {str(e)}")
                    continue
            
            self.logger.info(f"Successfully processed {len(self.hotels_data)} hotels")
            return self.hotels_data
            
        except Exception as e:
            self.logger.error(f"Error in scrape_hotels: {str(e)}")
            return []

    def extract_hotel_details(self, detail_url):
        """Extract detailed information from hotel detail page"""
        try:
            self.logger.info(f"Fetching details from: {detail_url}")
            if not self.get_page(detail_url):
                return None
            
            details = {}
            
            # Extract room details
            details['rooms'] = self.extract_room_details()
            
            # Extract amenities
            details['amenities'] = self.extract_amenities()
            
            # Extract description
            desc_elem = self.wait_for_element('.b40a-desc-text, .b40a-desc-wrap--full')
            if desc_elem:
                details['description'] = desc_elem.text.strip()
            
            # Extract address
            address_elem = self.wait_for_element('.c3xth-address')
            if address_elem:
                details['full_address'] = address_elem.text.strip()
            
            return details
            
        except Exception as e:
            self.logger.error(f"Error extracting hotel details: {str(e)}")
            return None

    def extract_room_details(self):
        """Extract room information from the detail page"""
        rooms = []
        try:
            room_elements = self.driver.find_elements(By.CSS_SELECTOR, '.c5l3f')
            
            for room in room_elements:
                room_info = {
                    'type': None,
                    'price': None,
                    'provider': None,
                    'cancellation': None,
                    'inclusions': []
                }
                
                try:
                    # Room type
                    type_elem = self.find_element_with_retry(room, '.c5NJT div')
                    if type_elem:
                        room_info['type'] = type_elem.text.strip()
                    
                    # Price
                    price_elem = self.find_element_with_retry(room, '.D9i2-price .C9NJ-amount')
                    if price_elem:
                        room_info['price'] = price_elem.text.strip()
                    
                    # Provider
                    provider_elem = self.find_element_with_retry(room, '.c2pAq-logo')
                    if provider_elem:
                        room_info['provider'] = provider_elem.get_attribute('alt')
                    
                    # Cancellation and inclusions
                    inclusions_elem = self.find_element_with_retry(room, '.BZag-freebie')
                    if inclusions_elem:
                        inclusion_text = inclusions_elem.text.strip()
                        if 'cancellation' in inclusion_text.lower():
                            room_info['cancellation'] = inclusion_text
                        else:
                            room_info['inclusions'].append(inclusion_text)
                    
                    if any(room_info.values()):
                        rooms.append(room_info)
                        
                except Exception as e:
                    self.logger.warning(f"Error extracting room details: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error extracting rooms: {str(e)}")
            
        return rooms

    def extract_amenities(self):
        """Extract amenities from the detail page"""
        amenities = {
            'general': [],
            'room': [],
            'services': []
        }
        
        try:
            amenity_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                '[aria-label="Amenities"] .BNDX, .BNDX-mod-presentation-default')
            
            for element in amenity_elements:
                try:
                    amenity_text = element.text.strip()
                    if amenity_text:
                        # Categorize amenity
                        if any(word in amenity_text.lower() for word in 
                              ['wifi', 'parking', 'pool', 'restaurant', 'gym']):
                            amenities['general'].append(amenity_text)
                        elif any(word in amenity_text.lower() for word in 
                               ['bed', 'tv', 'bathroom', 'air']):
                            amenities['room'].append(amenity_text)
                        else:
                            amenities['services'].append(amenity_text)
                except StaleElementReferenceException:
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error extracting amenities: {str(e)}")
            
        return amenities

    def save_results(self, filename='hotel_data.json'):
        """Save scraped data to JSON file"""
        try:
            os.makedirs('/app/data', exist_ok=True)
            filepath = os.path.join('/app/data', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.hotels_data, f, ensure_ascii=False, indent=2)
                self.logger.info(f"Data saved successfully to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")

    def close(self):
        """Clean up resources"""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing WebDriver: {str(e)}")

    def find_elements_safe(self, selector, parent=None, timeout=10):
        """Safely find multiple elements with wait and retry logic"""
        try:
            elements = WebDriverWait(parent or self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            return elements
        except:
            return []

    def get_text_safe(self, element, selector):
        """Safely get text from an element with retry logic"""
        try:
            el = self.find_element_with_retry(element, selector)
            return el.text.strip() if el else None
        except:
            return None

    def get_attribute_safe(self, element, selector, attribute):
        """Safely get attribute from an element with retry logic"""
        try:
            el = self.find_element_with_retry(element, selector)
            return el.get_attribute(attribute) if el else None
        except:
            return None

    def refresh_and_retry(self, url):
        """Refresh the page and retry loading with backoff"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.driver.refresh()
                time.sleep(2 ** retry_count)  # Exponential backoff
                return True
            except Exception as e:
                retry_count += 1
                self.logger.warning(f"Refresh attempt {retry_count} failed: {str(e)}")
                if retry_count == max_retries:
                    return False

    def wait_for_ajax(self, timeout=10):
        """Wait for all AJAX requests to complete"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script('return jQuery.active == 0')
            )
            return True
        except:
            return False

    def extract_policies(self, room_element):
        """Extract all policies from a room element"""
        policies = {
            'cancellation': None,
            'checkin': None,
            'checkout': None,
            'special_conditions': []
        }
        
        try:
            policy_elements = self.find_elements_safe('.BZag-freebie, .lUp8 .BNDX', room_element)
            
            for element in policy_elements:
                try:
                    policy_text = element.text.strip()
                    if 'cancellation' in policy_text.lower():
                        policies['cancellation'] = policy_text
                    elif 'check-in' in policy_text.lower():
                        policies['checkin'] = policy_text
                    elif 'check-out' in policy_text.lower():
                        policies['checkout'] = policy_text
                    else:
                        policies['special_conditions'].append(policy_text)
                except StaleElementReferenceException:
                    continue
                    
        except Exception as e:
            self.logger.warning(f"Error extracting policies: {str(e)}")
            
        return policies

    def extract_bed_info(self, room_element):
        """Extract bed configuration information"""
        bed_info = {
            'type': None,
            'count': None,
            'extra': []
        }
        
        try:
            bed_elements = self.find_elements_safe('.c5NJT-bed-types, .BZag-bed-types', room_element)
            
            for element in bed_elements:
                try:
                    bed_text = element.text.strip().lower()
                    if 'bed' in bed_text:
                        # Parse bed information
                        parts = bed_text.split()
                        for i, part in enumerate(parts):
                            if part.isdigit() and i + 1 < len(parts) and 'bed' in parts[i + 1]:
                                bed_info['count'] = int(part)
                                bed_info['type'] = ' '.join(parts[i + 1:])
                                break
                    else:
                        bed_info['extra'].append(bed_text)
                except StaleElementReferenceException:
                    continue
                    
        except Exception as e:
            self.logger.warning(f"Error extracting bed info: {str(e)}")
            
        return bed_info

    def extract_price_details(self, price_element):
        """Extract detailed price information"""
        price_info = {
            'amount': None,
            'currency': None,
            'per_night': None,
            'total': None,
            'taxes_fees': None
        }
        
        try:
            # Get main price
            price_text = self.get_text_safe(price_element, '.D9i2-price, .c1XBO')
            if price_text:
                # Parse price components
                parts = price_text.strip().split()
                if len(parts) >= 2:
                    price_info['currency'] = parts[0][0]  # Currency symbol
                    price_info['amount'] = parts[0][1:]  # Amount without currency
                    
                    if 'night' in price_text.lower():
                        price_info['per_night'] = True
                
                # Check for total price
                total_elem = self.find_element_with_retry(price_element, '.D9i2-total')
                if total_elem:
                    price_info['total'] = total_elem.text.strip()
                
                # Check for taxes and fees
                taxes_elem = self.find_element_with_retry(price_element, '.D9i2-taxes-fees')
                if taxes_elem:
                    price_info['taxes_fees'] = taxes_elem.text.strip()
                    
        except Exception as e:
            self.logger.warning(f"Error extracting price details: {str(e)}")
            
        return price_info