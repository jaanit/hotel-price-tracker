from selenium.common.exceptions import StaleElementReferenceException
from ..utils.retry import find_element_with_retry, wait_for_elements
from .policies import PoliciesExtractor
from .price import PriceExtractor

class RoomExtractor:
    @staticmethod
    def extract_bed_info(room_element, logger):
        """Extract bed configuration information"""
        bed_info = {
            'type': None,
            'count': None,
            'extra': []
        }
        
        try:
            bed_elements = wait_for_elements(
                room_element,
                '.c5NJT-bed-types, .BZag-bed-types',
                parent=room_element
            )
            
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
            logger.warning(f"Error extracting bed info: {str(e)}")
            
        return bed_info

    @staticmethod
    def extract_rooms(driver, logger):
        """Extract room information from the detail page"""
        rooms = []
        try:
            room_elements = wait_for_elements(driver, '.c5l3f')
            
            for room in room_elements:
                room_info = {
                    'type': None,
                    'price': None,
                    'provider': None,
                    'bed_config': None,
                    'policies': None
                }
                
                try:
                    # Room type
                    type_elem = find_element_with_retry(room, '.c5NJT div')
                    if type_elem:
                        room_info['type'] = type_elem.text.strip()
                    
                    # Price
                    price_elem = find_element_with_retry(room, '.D9i2-price .C9NJ-amount')
                    if price_elem:
                        room_info['price'] = PriceExtractor.extract(price_elem, logger)
                    
                    # Provider
                    provider_elem = find_element_with_retry(room, '.c2pAq-logo')
                    if provider_elem:
                        room_info['provider'] = provider_elem.get_attribute('alt')
                    
                    # Bed configuration
                    room_info['bed_config'] = RoomExtractor.extract_bed_info(room, logger)
                    
                    # Policies
                    room_info['policies'] = PoliciesExtractor.extract(room, logger)
                    
                    if any(room_info.values()):
                        rooms.append(room_info)
                        
                except Exception as e:
                    logger.warning(f"Error extracting room details: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error extracting rooms: {str(e)}")
            
        return rooms