from ..utils.retry import find_element_with_retry

class PriceExtractor:
    @staticmethod
    def extract(price_element, logger):
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
            price_text = price_element.text.strip() if price_element else None
            if price_text:
                # Parse price components
                parts = price_text.split()
                if len(parts) >= 2:
                    price_info['currency'] = parts[0][0]  # Currency symbol
                    price_info['amount'] = parts[0][1:]  # Amount without currency
                    
                    if 'night' in price_text.lower():
                        price_info['per_night'] = True
                
                # Check for total price
                total_elem = find_element_with_retry(price_element, '.D9i2-total')
                if total_elem:
                    price_info['total'] = total_elem.text.strip()
                
                # Check for taxes and fees
                taxes_elem = find_element_with_retry(price_element, '.D9i2-taxes-fees')
                if taxes_elem:
                    price_info['taxes_fees'] = taxes_elem.text.strip()
                    
        except Exception as e:
            logger.warning(f"Error extracting price details: {str(e)}")
            
        return price_info