from selenium.common.exceptions import StaleElementReferenceException
from ..utils.retry import find_element_with_retry, wait_for_elements

class AmenitiesExtractor:
    @staticmethod
    def extract(driver, logger):
        """Extract amenities from the detail page"""
        amenities = {
            'general': [],
            'room': [],
            'services': []
        }
        
        try:
            amenity_elements = wait_for_elements(
                driver,
                '[aria-label="Amenities"] .BNDX, .BNDX-mod-presentation-default'
            )
            
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
            logger.error(f"Error extracting amenities: {str(e)}")
            
        return amenities