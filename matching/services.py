"""
Haversine distance calculation and matching algorithms.
"""
import math
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r


def calculate_donor_score(donor, request_latitude, request_longitude):
    """
    Calculate matching score for a donor based on:
    - Availability (+50)
    - Donation recency (+0 to +40)
    - Distance (+10 to +30)
    
    Returns total score
    """
    score = 0

    # Availability score
    if donor.is_available:
        score += 50

    # Donation recency score
    if donor.last_donation_date:
        days_since_donation = (timezone.now().date() - donor.last_donation_date).days
        
        if days_since_donation < 30:
            score += 0
        elif days_since_donation <= 90:
            score += 20
        else:
            score += 40
    else:
        # Never donated - eligible for donation
        score += 40

    # Distance score
    distance = haversine_distance(
        request_latitude, request_longitude,
        donor.latitude, donor.longitude
    )
    
    if distance < 5:
        score += 30
    elif distance < 15:
        score += 20
    else:
        score += 10

    return score, distance


def find_matching_donors(blood_group, request_latitude, request_longitude, limit=50):
    """
    Find matching donors for a blood request.
    
    Returns list of donors ranked by score (descending)
    """
    # Find all donors with matching blood group who are available
    donors = User.objects.filter(
        blood_group=blood_group,
        is_available=True
    )

    # Calculate scores for each donor
    donor_scores = []
    for donor in donors:
        score, distance = calculate_donor_score(
            donor, request_latitude, request_longitude
        )
        donor_scores.append({
            'donor': donor,
            'score': score,
            'distance': distance
        })

    # Sort by score (descending)
    donor_scores.sort(key=lambda x: x['score'], reverse=True)

    # Return top donors
    return donor_scores[:limit]
