from haversine import haversine
from math import trunc


def get_distance(latitude, longitude, accout_spot):
    shop_spot = (float(latitude), float(longitude))
    distance = haversine(shop_spot, accout_spot, unit="km")

    if distance >= 1:
        distance = round(distance, 1)
        return f"{distance}km"
    else:
        distance = distance * 1000
        distance = trunc(distance)
        return f"{distance}m"
