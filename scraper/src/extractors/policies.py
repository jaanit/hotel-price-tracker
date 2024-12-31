from selenium.common.exceptions import StaleElementReferenceException
from ..utils.retry import wait_for_elements

class PoliciesExtractor:
    @staticmethod
    def extract(room_element, logger):
        """Extract all policies from a room element"""
        policies = {
            'cancellation': None,
            'checkin': None,
            'checkout': None,
            'special_conditions': []
        }
        
        try:
            policy_elements = wait_for_elements(
                room_element,
                '.BZag-freebie, .lUp8 .BNDX',
                parent=room_element
            )
            
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
            logger.warning(f"Error extracting policies: {str(e)}")
            
        return policies