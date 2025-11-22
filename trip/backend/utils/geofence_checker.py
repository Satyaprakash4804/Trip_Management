import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Haversine distance in meters between two lat/lon pairs.
    """
    R = 6371e3  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) *
         math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def is_inside_geofence(user_lat, user_lng, fence_lat, fence_lng, radius_meters):
    """
    Returns tuple (inside: bool, distance_meters: float)
    """
    dist = calculate_distance(user_lat, user_lng, fence_lat, fence_lng)
    return (dist <= radius_meters), dist
