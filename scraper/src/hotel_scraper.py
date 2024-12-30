# ./scraper/src/hotel_scraper.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import random
from datetime import datetime
from fake_useragent import UserAgent

class KayakHotelScraper:
    def __init__(self, city, check_in_date, check_out_date):
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
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.binary_location = '/usr/bin/chromium'
        
        # Additional options for stability
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--disable-browser-side-navigation')
        
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
            
            # Additional browser configuration
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": user_agent,
                "platform": "Windows"
            })
            
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            self.driver.implicitly_wait(10)
            print("Webdriver initialized successfully")
            
        except Exception as e:
            print(f"Error initializing webdriver: {str(e)}")
            raise
    
    def get_page(self, url):
        """Get page with retry logic and random delays"""
        try:
            # Random delay between requests
            time.sleep(random.uniform(3, 5))
            print(f"Attempting to load URL: {url}")
            
            self.driver.get(url)
            
            # Wait for initial page load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll down the page gradually to trigger lazy loading
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait to load page
                time.sleep(random.uniform(2, 3))
                
                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            print("Page loaded successfully")
            return self.driver.page_source
                
        except Exception as e:
            print(f"Error loading page: {str(e)}")
            raise

    def construct_search_url(self):
        """Construct the search URL for Kayak"""
        formatted_city = self.city.replace(' ', '-').lower()
        check_in = self.check_in_date.strftime('%Y-%m-%d')
        check_out = self.check_out_date.strftime('%Y-%m-%d')
        return f"{self.base_url}/hotels/{formatted_city}/{check_in}/{check_out}/2adults"


    def extract_hotel_basic_info(self, hotel_element):
        """Extract basic hotel information from a hotel element"""
        try:
            hotel_info = {}
            
            # Get hotel name
            try:
                name_elem = hotel_element.find_element(By.CSS_SELECTOR, 'a[class*="FLpo-big-name"]')
                hotel_info['name'] = name_elem.text.strip()
            except NoSuchElementException:
                hotel_info['name'] = 'N/A'
            
            # Get price
            try:
                price_elem = hotel_element.find_element(By.CSS_SELECTOR, 'div[class*="c1XBO"]')
                hotel_info['price'] = price_elem.text.strip()
            except NoSuchElementException:
                try:
                    price_elem = hotel_element.find_element(By.CSS_SELECTOR, 'div[class*="Ptt7-price"]')
                    hotel_info['price'] = price_elem.text.strip()
                except NoSuchElementException:
                    hotel_info['price'] = 'N/A'
            
            # Get rating
            try:
                rating_elem = hotel_element.find_element(By.CSS_SELECTOR, 'div[class*="opAh"]')
                hotel_info['rating'] = rating_elem.text.strip()
            except NoSuchElementException:
                hotel_info['rating'] = 'N/A'
            
            # Get location
            try:
                location_elem = hotel_element.find_element(By.CSS_SELECTOR, 'div[class*="upS4-big-name"]')
                hotel_info['location'] = location_elem.text.strip()
            except NoSuchElementException:
                hotel_info['location'] = 'N/A'

            # Get image URL
            try:
                img_elem = hotel_element.find_element(By.CSS_SELECTOR, 'img[class*="e9fk-photo"]')
                hotel_info['image_url'] = img_elem.get_attribute('src')
            except NoSuchElementException:
                hotel_info['image_url'] = 'N/A'
            
            # Get hotel link
            try:
                link_elem = hotel_element.find_element(By.CSS_SELECTOR, 'a[class*="FLpo-big-name"]')
                hotel_info['hotel_link'] = link_elem.get_attribute('href')
            except NoSuchElementException:
                hotel_info['hotel_link'] = 'N/A'



            
            # Try to get additional info like amenities
            try:
                amenities_elem = hotel_element.find_element(By.CSS_SELECTOR, 'div[class*="BNDX"]')
                hotel_info['amenities'] = amenities_elem.text.strip()
            except NoSuchElementException:
                hotel_info['amenities'] = 'N/A'
            
            return hotel_info
                
        except Exception as e:
            print(f"Error extracting hotel info: {str(e)}")
            return None



    def scrape_hotels(self):
        """Main method to scrape hotel data"""
        try:
            url = self.construct_search_url()
            self.get_page(url)
            print(f"Accessed URL: {self.driver.current_url}")
            
            # Wait longer for full page load
            time.sleep(random.uniform(10, 12))
            
            print("Initial page load complete. Looking for hotel elements...")
            
            # Find all hotel elements directly
            hotel_elements = []
            try:
                # Wait for any hotel element to be present
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="yuAt yuAt-pres-rounded"]'))
                )
                
                # Get all hotel elements
                hotel_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div[class*="yuAt yuAt-pres-rounded"]')
                print(f"Found {len(hotel_elements)} hotels")
                
            except TimeoutException:
                print("Timeout waiting for hotel elements")
                return []
                
            if not hotel_elements:
                print("Could not find any hotel elements")
                return []
                
            print(f"Processing {len(hotel_elements)} hotels...")
            
            for index, hotel_element in enumerate(hotel_elements):
                try:
                    hotel_info = self.extract_hotel_basic_info(hotel_element)
                    if hotel_info:
                        self.hotels_data.append(hotel_info)
                        print(f"Processed hotel {index + 1}/{len(hotel_elements)}: {hotel_info.get('name', 'Unknown')}")
                except Exception as e:
                    print(f"Error processing hotel {index + 1}: {str(e)}")
                    continue
            
            return self.hotels_data
                
        except Exception as e:
            print(f"Error in scrape_hotels: {str(e)}")
            print("Page title:", self.driver.title)
            print("Current URL:", self.driver.current_url)
            return []


    def save_results(self, filename='hotel_data.json'):
        """Save scraped data to JSON file"""
        try:
            os.makedirs('/app/data', exist_ok=True)
            filepath = os.path.join('/app/data', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.hotels_data, f, ensure_ascii=False, indent=2)
            print(f"Data saved successfully to {filepath}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")

    def close(self):
        """Clean up resources"""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                print("Driver closed successfully")
            except Exception as e:
                print(f"Error closing driver: {str(e)}")