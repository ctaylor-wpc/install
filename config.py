# config.py
# Configuration file for pricing, SKUs, and other constants

# Google Sheet and Drive Configuration
SHEET_ID = "1kEOIdxYqPKx6R47sNdaY8lWR8PmLc6bz_PyHtYH1M7Q"
PDF_FOLDER_ID = "1UinHT5ZXjDrGXwfX-WBwge28nnHLfgq8"

# Scopes for Google API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Origin addresses for distance calculation
ORIGIN_ADDRESSES = {
    "Frankfort": "3690 East West Connector, Frankfort KY 40601",
    "Lexington": "2700 Palumbo Drive Lexington KY 40509"
}

# Installation material pricing
INSTALL_MATERIALS_PRICING = {
    "tablet_unit_price": 0.75,
    "soil_conditioner_unit_price": 9.99,
    "deer_guard_unit_price": 3.99,
    "tree_stake_unit_price": 36.00
}

# Mulch pricing and SKU configuration
MULCH_CONFIG = {
    "Soil Conditioner Only": {"price": 9.99, "sku": "07SOILC02"},
    "Hardwood": {"price": 8.99, "sku": "7HARDRVM"},
    "Eastern Red Cedar": {"price": 8.99, "sku": "RVM CEDAR"},
    "Pine Bark": {"price": 8.99, "sku": "07PINEBM02"},
    "Pine Bark Mini Nuggets": {"price": 8.99, "sku": "07PINEBMN02"},
    "Pine Bark Nuggets": {"price": 8.99, "sku": "07PINEBN02"},
    "Grade A Cedar": {"price": 16.99, "sku": "CEDAR"},
    "Redwood": {"price": 16.99, "sku": "REDWOODM"},
    "Pine Straw": {"price": 15.99, "sku": "07PINESTRAW"}
}

# Default mulch if type not found
DEFAULT_MULCH = {"price": 8.99, "sku": "7HARDRVM"}

# Mileage rate for delivery calculation
DELIVERY_MILEAGE_RATE = 2.25  # per mile, round trip

# Tax rate
TAX_RATE = 0.06

# Installation multipliers by type
INSTALLATION_MULTIPLIERS = {
    "Shrubs Only: 97%": 0.97,
    "1-3 trees: 97%": 0.97,
    "4-6 trees: 91%": 0.91,
    "7+ Trees: 85%": 0.85
}

# Plant size options
PLANT_SIZE_OPTIONS = [
    "1.25", "1.5", "1.75", "2", "5-6", "6-7", 
    "1G", "2G", "3G", "5G", "7G", "10G", "15G", "30G", 
    "Slender Upright"
]

# Mulch type options
MULCH_TYPE_OPTIONS = [
    "Soil Conditioner Only", "Hardwood", "Grade A Cedar", 
    "Eastern Red Cedar", "Redwood", "Pine Bark", 
    "Pine Bark Mini Nuggets", "Pine Bark Nuggets", "Pine Straw"
]

# Installation type options
INSTALLATION_TYPE_OPTIONS = [
    "Shrubs Only: 97%", 
    "1-3 trees: 97%", 
    "4-6 trees: 91%", 
    "7+ Trees: 85%"
]

# Utilities options for customer form
UTILITIES_OPTIONS = [
    "Underground Dog Fence",
    "Septic Tank",
    "Septic Field",
    "Geothermal",
    "Landscape Lighting",
    "Gas to Outdoor Kitchen or Grill",
    "Irrigation Lines",
    "Propane Tank",
    "Well or Spring",
    "Stump or Existing Tree",
    "No Obstacles Near Planting",
]

# Lookup table for plant sizes - mulch, soil, and tablet quantities
PLANT_SIZE_DATA = {
    "1.25": {"mulch": (2, 2, 1), "soil": 0.5, "tablets": 4},
    "1.5": {"mulch": (2, 2, 1), "soil": 0.5, "tablets": 4},
    "1.75": {"mulch": (3, 3, 2), "soil": 1, "tablets": 5},
    "2": {"mulch": (3, 3, 3), "soil": 2, "tablets": 6},
    "5-6": {"mulch": (3, 3, 2), "soil": 1, "tablets": 5},
    "6-7": {"mulch": (3, 3, 3), "soil": 2, "tablets": 6},
    "Slender Upright": {"mulch": (2, 2, 1), "soil": 0.5, "tablets": 4},
    "1G": {"mulch": (0.5, 0.5, 0.25), "soil": 0.25, "tablets": 2},
    "2G": {"mulch": (0.5, 0.5, 0.25), "soil": 0.25, "tablets": 2},
    "3G": {"mulch": (0.5, 0.5, 0.25), "soil": 0.5, "tablets": 3},
    "5G": {"mulch": (1, 1, 0.5), "soil": 0.5, "tablets": 4},
    "7G": {"mulch": (1, 1, 1), "soil": 1, "tablets": 5},
    "10G": {"mulch": (2, 2, 2), "soil": 1, "tablets": 6},
    "15G": {"mulch": (2, 2, 2), "soil": 2, "tablets": 8},
    "30G": {"mulch": (3, 3, 3), "soil": 3, "tablets": 12}
}

# Mulch categories for lookup
MULCH_CATEGORIES = {
    "category_a": ["Soil Conditioner Only", "Hardwood", "Eastern Red Cedar", 
                   "Pine Bark", "Pine Bark Mini Nuggets", "Pine Bark Nuggets"],
    "category_b": ["Grade A Cedar", "Redwood"],
    "category_c": ["Pine Straw"]
}