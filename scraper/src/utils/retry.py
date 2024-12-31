import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.settings import DEFAULT_TIMEOUT, MAX_RETRIES, RETRY_DELAY

def find_element_with_retry(parent, selector, max_retries=MAX_RETRIES):
    """Find element with retry logic for stale elements"""
    for attempt in range(max_retries):
        try:
            return parent.find_element(By.CSS_SELECTOR, selector)
        except StaleElementReferenceException:
            if attempt == max_retries - 1:
                raise
            time.sleep(RETRY_DELAY)
        except NoSuchElementException:
            return None

def wait_for_element(driver, selector, timeout=DEFAULT_TIMEOUT, parent=None):
    """Wait for single element to be present"""
    try:
        return WebDriverWait(parent or driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    except TimeoutException:
        return None

def wait_for_elements(driver, selector, timeout=DEFAULT_TIMEOUT, parent=None):
    """Wait for elements and return them when available"""
    try:
        return WebDriverWait(parent or driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
    except TimeoutException:
        return []

def wait_for_page_load(driver, timeout=DEFAULT_TIMEOUT):
    """Wait for page to finish loading"""
    try:
        return WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
    except TimeoutException:
        return False

def scroll_into_view(driver, element):
    """Scroll element into view using JavaScript"""
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Let the page settle
    except Exception:
        pass