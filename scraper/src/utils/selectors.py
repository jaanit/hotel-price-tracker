"""CSS Selectors for Kayak hotel search and detail pages"""

# Main containers and hotel cards
HOTEL_CARD = 'div.S0Ps-resultInner'
HOTEL_CONTAINER = 'div.S0Ps-middleSection'
HOTEL_PHOTO = 'img.e9fk-photo'
HOTEL_DESCRIPTION = 'div.b40a-desc-text'

# Basic hotel information from search page
HOTEL_NAME = 'a.FLpo-big-name'
HOTEL_LOCATION = 'div.upS4-big-name'
HOTEL_RATING = 'div.wdjx-positive'
HOTEL_REVIEWS = 'div.xdhG-rating-description-and-count'
HOTEL_STARS = 'span.Ius0'

# Price information
PRICE_SECTION = 'div.zV27-price-section'
PRICE_AMOUNT = 'div.c1XBO'
PROVIDER_LOGO = 'img.c7Fuo-provider-logo'
PRICE_DEALS = 'div.qSC7'

# Room information from detail page
ROOM_SECTION = 'div.LK1E-groupedRoomType'
ROOM_CARD = 'div.c5l3f'
ROOM_TYPE = 'div.c_Hjx-group-header-title'
ROOM_PRICE = 'span.C9NJ-amount'
ROOM_PROVIDER = 'img.c2pAq-logo'
ROOM_INFO = 'div.c_Hjx-header-details'
ROOM_SIZE = 'span.c_Hjx-amenity:contains("sq ft")'
ROOM_VIEW = 'span.c_Hjx-amenity:contains("view")'

# Bed configuration
BED_CONFIG = 'div.c_Hjx-detail-amenity'
BED_TYPE = 'span.c_Hjx-amenity'
BED_COUNT = 'div.c_Hjx-amenity'

# Amenities selectors
AMENITIES_SECTION = 'section.Vdvb'
FEATURED_AMENITIES = '.t8Xi-amenity-name'
AMENITY_CATEGORY = '.BxLB-category-name'
AMENITY_ITEM = '.BxLB-amenity'
AMENITY_NAME = '.BxLB-amenity-name'

# Categories container
CATEGORIES_CONTAINER = 'div.DbSA-categories-container'

# Featured amenities at top
FEATURED_AMENITIES = 'ul.kml-row'

# Individual amenity sections
AMENITY_SECTIONS = {
    'basics': '.BxLB-category-name:contains("Basics")',
    'general': '.BxLB-category-name:contains("General")',
    'kitchen': '.BxLB-category-name:contains("Kitchen")',
    'bathroom': '.BxLB-category-name:contains("Bathroom")',
    'bedroom': '.BxLB-category-name:contains("Bedroom")',
    'outdoor': '.BxLB-category-name:contains("Outdoor")',
    'services': '.BxLB-category-name:contains("Services")',
    'family': '.BxLB-category-name:contains("Family friendly")',
    'accessibility': '.BxLB-category-name:contains("Accessibility")',
    'dining': '.BxLB-category-name:contains("Dining")',
    'media': '.BxLB-category-name:contains("Media")',
    'workspace': '.BxLB-category-name:contains("Workspace")',
    'activities': '.BxLB-category-name:contains("Things to do")'
}

# Categories of amenities
BASIC_AMENITIES = 'div.BxLB-categories-container div:contains("Basics")'
ROOM_AMENITIES = 'div.BxLB-categories-container div:contains("In the room")'
BATHROOM_AMENITIES = 'div.BxLB-categories-container div:contains("Bathroom")'
SERVICES_AMENITIES = 'div.BxLB-categories-container div:contains("Services")'
OUTDOOR_AMENITIES = 'div.BxLB-categories-container div:contains("Outdoor")'

# Policies and conditions
CANCELLATION_POLICY = 'div.BZag-freebie:contains("cancellation")'
BREAKFAST_INFO = 'div.BZag-freebie:contains("breakfast")'
SPECIAL_CONDITIONS = 'div.BZag-freebie'
CHECK_IN_OUT = 'div.c5NJT'

# Navigation and pagination
NEXT_PAGE = 'button[aria-label="Next page"]'
PREV_PAGE = 'button[aria-label="Previous page"]'
PAGE_NUMBERS = 'div.Joiu-buttons button'
CURRENT_PAGE = 'button#active'
SHOW_MORE = 'button.c1oRo-show-more'

# Popup handling
CLOSE_BUTTON = 'button[aria-label="Close"]'
DISMISS_BUTTON = '.dismiss-button'

# Property features
PROPERTY_FEATURES = {
    'wifi': 'span.BxLB-amenity-name:contains("Wi-Fi")',
    'parking': 'span.BxLB-amenity-name:contains("Parking")',
    'breakfast': 'span.BxLB-amenity-name:contains("Breakfast")',
    'pool': 'span.BxLB-amenity-name:contains("Pool")',
    'spa': 'span.BxLB-amenity-name:contains("Spa")',
    'fitness': 'span.BxLB-amenity-name:contains("Fitness")',
    'restaurant': 'span.BxLB-amenity-name:contains("Restaurant")',
    'bar': 'span.BxLB-amenity-name:contains("Bar")',
    'business': 'span.BxLB-amenity-name:contains("Business")',
}


# Amenities selectors
AMENITIES_SECTION = 'section.Vdvb'
AMENITIES_CATEGORY = 'div.kml-col-12-12.kml-col-6-12-m'
CATEGORY_NAME = 'p.BxLB-category-name'
AMENITY_ITEM = 'span.BxLB-amenity-name'
TOP_AMENITIES = 'span.t8Xi-amenity-name'

# Categories container
CATEGORIES_CONTAINER = 'div.DbSA-categories-container'

# Featured amenities at top
FEATURED_AMENITIES = 'ul.kml-row'

# Individual amenity sections
AMENITY_SECTIONS = {
    'basics': '.BxLB-category-name:contains("Basics")',
    'general': '.BxLB-category-name:contains("General")',
    'kitchen': '.BxLB-category-name:contains("Kitchen")',
    'bathroom': '.BxLB-category-name:contains("Bathroom")',
    'bedroom': '.BxLB-category-name:contains("Bedroom")',
    'outdoor': '.BxLB-category-name:contains("Outdoor")',
    'services': '.BxLB-category-name:contains("Services")',
    'family': '.BxLB-category-name:contains("Family friendly")',
    'accessibility': '.BxLB-category-name:contains("Accessibility")',
    'dining': '.BxLB-category-name:contains("Dining")',
    'media': '.BxLB-category-name:contains("Media")',
    'workspace': '.BxLB-category-name:contains("Workspace")',
    'activities': '.BxLB-category-name:contains("Things to do")'
}