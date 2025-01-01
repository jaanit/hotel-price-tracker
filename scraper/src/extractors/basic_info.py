from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from ..utils.retry import find_element_with_retry
from ..utils.selectors import (
    HOTEL_NAME, HOTEL_LOCATION, HOTEL_RATING,
    HOTEL_REVIEWS, HOTEL_STARS, PRICE_AMOUNT,
    HOTEL_DESCRIPTION
)

class BasicInfoExtractor:
    @staticmethod
    def extract(hotel_element, logger):
        """Extract basic hotel information from search result element"""
        try:
            hotel_info = {}
            
            # Get hotel name and URL
            try:
                name_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_NAME)
                if name_elem:
                    hotel_info['name'] = name_elem.text.strip()
                    hotel_info['detail_url'] = name_elem.get_attribute('href')
                else:
                    logger.warning("Could not find hotel name/URL")
                    return None
            except NoSuchElementException:
                logger.warning("Could not find hotel name/URL")
                return None
            
            # Get location
            try:
                location_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_LOCATION)
                if location_elem:
                    hotel_info['location'] = location_elem.text.strip()
            except NoSuchElementException:
                hotel_info['location'] = None

            # Get description
            try:
                # Looking for description in parent elements
                parent = hotel_element.find_element(By.XPATH, "./..")
                desc_elem = parent.find_element(By.CSS_SELECTOR, HOTEL_DESCRIPTION)
                if desc_elem:
                    hotel_info['description'] = desc_elem.text.strip()
            except NoSuchElementException:
                hotel_info['description'] = None

            # Get stars
            try:
                stars_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_STARS)
                if stars_elem:
                    stars_text = stars_elem.text.strip()
                    hotel_info['stars'] = stars_text.split()[0] if stars_text else None
            except NoSuchElementException:
                hotel_info['stars'] = None

            # Get price
            try:
                price_elem = hotel_element.find_element(By.CSS_SELECTOR, PRICE_AMOUNT)
                if price_elem:
                    hotel_info['price'] = price_elem.text.strip()
            except NoSuchElementException:
                hotel_info['price'] = None

            # Get rating and reviews
            try:
                rating_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_RATING)
                reviews_elem = hotel_element.find_element(By.CSS_SELECTOR, HOTEL_REVIEWS)
                
                if rating_elem:
                    hotel_info['rating'] = rating_elem.text.strip()
                if reviews_elem:
                    reviews_text = reviews_elem.text.strip()
                    # Parse reviews count from format "Very good (12185)"
                    hotel_info['reviews'] = reviews_text
                    if '(' in reviews_text and ')' in reviews_text:
                        count = reviews_text.split('(')[1].split(')')[0]
                        hotel_info['review_count'] = count
            except NoSuchElementException:
                pass
            
            logger.info(f"Successfully extracted basic info for: {hotel_info.get('name', 'Unknown')}")
            return hotel_info
            
        except Exception as e:
            logger.error(f"Error extracting hotel info: {str(e)}")
            return None