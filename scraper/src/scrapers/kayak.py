import json
import time
import random
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from src.core.driver import WebDriverManager
from src.core.logger import setup_logger
from src.utils.retry import (
    wait_for_element, 
    wait_for_elements, 
    wait_for_page_load,
    scroll_into_view
)
from src.utils.selectors import *

class KayakHotelScraper:
    def __init__(self, city, check_in_date, check_out_date):
        self.logger = setup_logger()
        self.city = city
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.base_url = "https://www.kayak.com/hotels"
        self.hotels_data = []
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        try:
            self.driver = WebDriverManager.create_driver()
            self.logger.info("WebDriver initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise

    def construct_search_url(self):
        check_in = self.check_in_date.strftime('%Y-%m-%d')
        check_out = self.check_out_date.strftime('%Y-%m-%d')
        city_formatted = self.city.replace(' ', '-')
        return f"{self.base_url}/{city_formatted}-c52508/{check_in}/{check_out}/2adults?sort=rank_a"

    def handle_popups(self):
        try:
            popup_selectors = [
                'button[aria-label="Close"]',
                '.close-button',
                '.dismiss-button'
            ]
            for selector in popup_selectors:
                try:
                    element = wait_for_element(self.driver, selector, timeout=3)
                    if element and element.is_displayed():
                        element.click()
                        time.sleep(0.5)
                except:
                    continue
        except:
            pass

    def load_page(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Loading URL (attempt {attempt + 1}): {url}")
                self.driver.get(url)
                wait_for_page_load(self.driver)
                self.handle_popups()
                
                # Scroll to load dynamic content
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, 0);")
                
                return True
            except Exception as e:
                self.logger.error(f"Error loading page (attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    return False
                time.sleep(2 ** attempt)
        return False

    def extract_room_price(self, room_elem):
        """Extract price from room element with multiple selectors"""
        try:
            # Try different price selectors in order of preference
            price_selectors = [
                'span.C9NJ-amount',
                'div.C9NJ-amount', 
                'div.Ptt7-price',
                'div.c1XBO',
                'div[class*="price"]'
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = room_elem.find_element(By.CSS_SELECTOR, selector)
                    if price_elem:
                        price_text = price_elem.text.strip()
                        # Extract numeric price
                        price = float(''.join(filter(str.isdigit, price_text.replace(',', ''))))
                        return price
                except:
                    continue
            return None
        except Exception as e:
            self.logger.error(f"Error extracting room price: {str(e)}")
            return None

    def extract_room_details(self):
        """Extract detailed room information"""
        try:
            rooms = []
            # Wait and scroll for room elements
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            
            # Look for room containers
            room_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.LK1E-groupedRoomType')
            self.logger.info(f"Found {len(room_elements)} room elements")
            
            for room_elem in room_elements:
                try:
                    room_info = {
                        'room_type': None,
                        'price': None,
                        'bed_configuration': None,
                        'cancellation_policy': None,
                        'board_type': None,
                        'special_conditions': []
                    }
                    
                    # Scroll to room element
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", room_elem)
                    time.sleep(1)
                    
                    # Room type
                    type_elem = room_elem.find_element(By.CSS_SELECTOR, 'div.c_Hjx-group-header-title')
                    if type_elem:
                        room_info['room_type'] = type_elem.text.strip()
                    
                    # Price from provider section
                    price = self.extract_room_price(room_elem)
                    if price:
                        room_info['price'] = price
                    
                    # Bed configuration
                    bed_elems = room_elem.find_elements(By.CSS_SELECTOR, 'div.c_Hjx-detail-amenity')
                    for elem in bed_elems:
                        if any(word in elem.text.lower() for word in ['bed', 'twin', 'double', 'queen', 'king']):
                            room_info['bed_configuration'] = elem.text.strip()
                            break
                    
                    # Policies and board type
                    policy_elements = room_elem.find_elements(By.CSS_SELECTOR, '.BZag-freebie')
                    for elem in policy_elements:
                        text = elem.text.strip()
                        if 'cancellation' in text.lower():
                            room_info['cancellation_policy'] = text
                        elif 'breakfast' in text.lower():
                            room_info['board_type'] = text
                        elif text:
                            room_info['special_conditions'].append(text)
                    
                    if any(v for v in room_info.values() if v):
                        rooms.append(room_info)
                        self.logger.info(f"Successfully extracted room: {room_info['room_type']}")
                
                except Exception as e:
                    self.logger.error(f"Error extracting room details: {str(e)}")
                    continue
            
            return rooms
            
        except Exception as e:
            self.logger.error(f"Error in extract_room_details: {str(e)}")
            return []


    def extract_amenities(self):
        """Extract all amenities from the detail page"""
        amenities = []
        try:
            # Scroll to load amenities section
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Get all amenity categories
            category_containers = self.driver.find_elements(By.CSS_SELECTOR, '.kml-col-12-12.kml-col-6-12-m')
            
            for container in category_containers:
                try:
                    category_name_elem = container.find_element(By.CSS_SELECTOR, '.BxLB-category-name')
                    category = category_name_elem.text.strip() if category_name_elem else None
                    
                    if category:
                        # Get all amenities in this category
                        amenity_elements = container.find_elements(By.CSS_SELECTOR, '.BxLB-amenity-name')
                        for elem in amenity_elements:
                            amenity = elem.text.strip()
                            if amenity and amenity not in amenities:
                                amenities.append(amenity)
                except:
                    continue
            
            # Also get amenities from the top summary section
            top_amenities = self.driver.find_elements(By.CSS_SELECTOR, '.t8Xi-amenity-name')
            for elem in top_amenities:
                amenity = elem.text.strip()
                if amenity and amenity not in amenities:
                    amenities.append(amenity)
                    
            return amenities
                    
        except Exception as e:
            self.logger.error(f"Error extracting amenities: {str(e)}")
            return []

    def extract_hotel_details(self, detail_url):
        """Get detailed information from hotel page"""
        try:
            self.logger.info(f"Loading detail page: {detail_url}")
            if not self.load_page(detail_url):
                return {}
            
            details = {}
            
            # Extract rooms
            rooms = self.extract_room_details()
            if rooms:
                details['rooms'] = rooms
                self.logger.info(f"Found {len(rooms)} room types")
            
            # Extract amenities
            amenities = self.extract_amenities()
            if amenities:
                details['amenities'] = amenities
                self.logger.info(f"Found {len(amenities)} amenities")
            
            return details
            
        except Exception as e:
            self.logger.error(f"Error extracting hotel details: {str(e)}")
            return {}

 
    def extract_hotel_basic_info(self, hotel_element):
        """Extract basic hotel information"""
        try:
            info = {}
            
            # Extract hotel name and URL
            name_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_NAME)
            if name_elem:
                info['hotel_name'] = name_elem.text.strip()
                info['detail_url'] = name_elem.get_attribute('href')
            
            # Extract location
            location_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_LOCATION)
            if location_elem:
                info['location'] = location_elem.text.strip()
            
            # Extract rating and reviews
            try:
                rating_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_RATING)
                reviews_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_REVIEWS)
                
                info['review_scores'] = {
                    'rating': float(rating_elem.text.strip()),
                    'count': int(''.join(filter(str.isdigit, reviews_elem.text)))
                }
            except:
                info['review_scores'] = {'rating': None, 'count': None}
            
            # Extract price
            try:
                price_elem = hotel_element.find_element(By.CSS_SELECTOR, PRICE_AMOUNT)
                info['price'] = price_elem.text.strip()
            except:
                info['price'] = None
            # extract hotel image
            try:
                img_elem = hotel_element.find_element(By.CSS_SELECTOR, 'img[class*="e9fk-photo"]')
                hotel_info['image_url'] = img_elem.get_attribute('src')
            except NoSuchElementException:
                hotel_info['image_url'] = 'N/A'
            return info
            
        except Exception as e:
            self.logger.error(f"Error extracting basic hotel info: {str(e)}")
            return None

    def scrape_hotels(self, limit=None):
        """Main method to scrape hotel information"""
        try:
            # Load initial search page
            search_url = self.construct_search_url()
            if not self.load_page(search_url):
                return []
            
            # Get all hotel cards first
            hotel_elements = wait_for_elements(self.driver, HOTEL_CARD)
            if not hotel_elements:
                self.logger.error("No hotel elements found")
                return []
            
            self.logger.info(f"Found {len(hotel_elements)} hotels")
            
            # Store basic info and URLs first
            hotels_to_process = []
            for hotel_element in hotel_elements[:limit]:
                try:
                    info = {}
                    # Extract hotel name and URL
                    name_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_NAME)
                    if name_elem:
                        info['hotel_name'] = name_elem.text.strip()
                        info['detail_url'] = name_elem.get_attribute('href')
                    
                    # Extract location
                    location_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_LOCATION)
                    if location_elem:
                        info['location'] = location_elem.text.strip()
                    
                    # Extract rating and reviews
                    try:
                        rating_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_RATING)
                        reviews_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_REVIEWS)
                        
                        info['review_scores'] = {
                            'rating': float(rating_elem.text.strip()),
                            'count': int(''.join(filter(str.isdigit, reviews_elem.text)))
                        }
                    except:
                        info['review_scores'] = {'rating': None, 'count': None}
                    
                    # Extract price
                    price_elem = hotel_element.find_element(By.CSS_SELECTOR, PRICE_AMOUNT)
                    if price_elem:
                        info['price'] = price_elem.text.strip()
                    
                    if info.get('detail_url'):
                        hotels_to_process.append(info)
                    # extract hotel image
                    try:
                        img_elem = hotel_element.find_element(By.CSS_SELECTOR, 'img[class*="e9fk-photo"]')
                        hotel_info['image_url'] = img_elem.get_attribute('src')
                    except NoSuchElementException:
                        hotel_info['image_url'] = 'N/A'
                        
                    
                except Exception as e:
                    self.logger.error(f"Error extracting basic hotel info: {str(e)}")
                    continue
            
            # Now process each hotel's details
            for hotel_info in hotels_to_process:
                try:
                    # Get detailed info
                    details = self.extract_hotel_details(hotel_info['detail_url'])
                    hotel_info.update(details)
                    self.hotels_data.append(hotel_info)
                    
                    # Return to search page
                    self.load_page(search_url)
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    self.logger.error(f"Error processing hotel details: {str(e)}")
                    continue
            
            self.format_output()
            return self.hotels_data
                
        except Exception as e:
            self.logger.error(f"Error in scrape_hotels: {str(e)}")
            return []

    def format_output(self):
        """Format the scraped data into the desired structure"""
        formatted_data = {
            "city": self.city,
            "hotels": self.hotels_data,
            "pagination": {
                "current_page": 1,
                "total_pages": 1
            },
            "metadata": {
                "scraping_date": datetime.now().strftime('%Y-%m-%d'),
                "scraping_time": datetime.now().strftime('%H:%M'),
                "source_url": self.base_url
            }
        }
        self.hotels_data = formatted_data

    def save_results(self, filename='hotel_data.json'):
        try:
            os.makedirs('data', exist_ok=True)
            filepath = os.path.join('data', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.hotels_data, f, ensure_ascii=False, indent=2)
                self.logger.info(f"Data saved successfully to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing WebDriver: {str(e)}")