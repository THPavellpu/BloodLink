"""
Common constants for the API.
"""

BLOOD_TYPES = [
    'O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'
]

URGENCY_LEVELS = ['Low', 'Medium', 'High']

# Distance in kilometers for donor matching
DISTANCE_FILTERS = {
    'very_close': 5,      # < 5 km
    'close': 15,          # < 15 km
    'moderate': 50,       # < 50 km
}

# Days for checking donation recency
DONATION_RECENCY_DAYS = {
    'ineligible': 30,     # < 30 days
    'moderate': 90,       # 30-90 days
    'eligible': 90,       # > 90 days
}
