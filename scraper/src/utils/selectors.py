"""CSS Selectors for Kayak hotel search and detail pages."""

# Main Search Result Containers
HOTEL_CARD = 'div.S0Ps-resultInner'
HOTEL_CONTAINER = 'div.S0Ps-middleSection'

# Search page image selectors
SEARCH_PHOTO_CONTAINER = '.e9fk-photoContainer'  # Container for search page images
SEARCH_PHOTO_WRAP = '.e9fk-photoWrap'  # Wrapper for picture element
SEARCH_PHOTO = '.e9fk-photo'  # Main image element

# Detail page image selectors
DETAIL_PHOTO_CONTAINER = '.c1E0k-photo-container'  # Main container for detail page photos
DETAIL_PHOTO_WRAPPER = '.vdGX.vdGX-mod-layout-mosaic'  # Grid layout wrapper
DETAIL_PHOTO_ITEM = '.f800.f800-mod-pres-default'  # Individual photo container
DETAIL_PHOTO = '.f800-image'  # Actual image element in detail page

# Basic Hotel Information
HOTEL_NAME = 'a.FLpo-big-name'
HOTEL_LOCATION = 'div.upS4-big-name'
HOTEL_RATING = 'div.wdjx-positive'
HOTEL_REVIEWS = 'div.xdhG-rating-description-and-count'
HOTEL_STARS = 'span.Ius0'
HOTEL_DESCRIPTION = 'div.b40a-desc-text'

# Price Information
PRICE_SECTION = 'div.zV27-price-section'
PRICE_AMOUNT = 'div.c1XBO, span.C9NJ-amount'
PROVIDER_LOGO = 'img.c7Fuo-provider-logo'
DEALS_CONTAINER = 'div.qSC7'

# Room Information
ROOM_SECTION = 'div.LK1E-groupedRoomType'
ROOM_CARD = 'div.c5l3f'
ROOM_TYPE = 'div.c_Hjx-group-header-title'
ROOM_PRICE = 'span.C9NJ-amount'
ROOM_PROVIDER = 'img.c2pAq-logo'
ROOM_INFO = 'div.c_Hjx-header-details'
ROOM_SIZE = 'span.c_Hjx-amenity:contains("sq ft")'
ROOM_VIEW = 'span.c_Hjx-amenity:contains("view")'

# Bed Configuration
BED_CONFIG = 'div.c_Hjx-detail-amenity'
BED_TYPE = 'span.c_Hjx-amenity'

# Updated Amenities Selectors
AMENITIES_SECTION = '.tYfO[data-section-name="amenities"]'  # Main amenities container
AMENITIES_TOP_SECTION = '.tYfO-top-amenities'  # Top visible amenities section
AMENITY_ITEM = '.tYfO-amenity-name'  # Individual amenity in top section
AMENITY_EXPANDED_ITEM = '.BxLB-amenity-name'  # Individual amenity in expanded view
SHOW_ALL_AMENITIES_BTN = '.tYfO-toggle-all-button button'  # Show all amenities button
AMENITY_MODAL = '.DbSA-categories-container'  # Container for all amenities when expanded

# Amenity Categories in Modal
AMENITY_CATEGORY_ITEM = '.BxLB-category-name'  # Category header in expanded view
AMENITY_LIST = 'ul.kml-row'  # List of amenities

# Policies and Conditions
CANCELLATION_POLICY = 'div.BZag-freebie:contains("cancellation")'
BREAKFAST_INFO = 'div.BZag-freebie:contains("breakfast")'
SPECIAL_CONDITIONS = 'div.BZag-freebie'
CHECK_IN_OUT = 'div.c5NJT'

# Navigation and Pagination
PAGINATION_CONTAINER = 'div.Pf_g-pagination'
NEXT_PAGE = 'button[aria-label="Next page"]'
PREV_PAGE = 'button[aria-label="Previous page"]'
PAGE_NUMBERS = 'div.Joiu-buttons button'
CURRENT_PAGE = 'button#active'

# Property Features (Key Amenities)
PROPERTY_FEATURES = {
    'wifi': 'span.tYfO-amenity-name:contains("Wi-Fi")',  # Updated selector
    'parking': 'span.tYfO-amenity-name:contains("Parking")',
    'breakfast': 'span.tYfO-amenity-name:contains("Breakfast")',
    'pool': 'span.tYfO-amenity-name:contains("Pool")',
    'spa': 'span.tYfO-amenity-name:contains("Spa")',
    'fitness': 'span.tYfO-amenity-name:contains("Fitness")',
    'restaurant': 'span.tYfO-amenity-name:contains("Restaurant")',
    'bar': 'span.tYfO-amenity-name:contains("Bar")',
    'business': 'span.tYfO-amenity-name:contains("Business")',
}

# Amenity Categories
AMENITY_SECTIONS = {
    'basics': 'p.BxLB-category-name:contains("Basics")',
    'general': 'p.BxLB-category-name:contains("General")',
    'kitchen': 'p.BxLB-category-name:contains("Kitchen")',
    'bathroom': 'p.BxLB-category-name:contains("Bathroom")',
    'bedroom': 'p.BxLB-category-name:contains("Bedroom")',
    'outdoor': 'p.BxLB-category-name:contains("Outdoor")',
    'services': 'p.BxLB-category-name:contains("Services")',
    'family': 'p.BxLB-category-name:contains("Family friendly")',
    'accessibility': 'p.BxLB-category-name:contains("Accessibility")',
    'dining': 'p.BxLB-category-name:contains("Dining")',
    'media': 'p.BxLB-category-name:contains("Media")',
    'workspace': 'p.BxLB-category-name:contains("Workspace")',
    'activities': 'p.BxLB-category-name:contains("Things to do")',
    'transportation': 'p.BxLB-category-name:contains("Parking and transportation")',
}

# Popup Handling
CLOSE_BUTTON = 'button[aria-label="Close"]'
DISMISS_BUTTON = '.dismiss-button'