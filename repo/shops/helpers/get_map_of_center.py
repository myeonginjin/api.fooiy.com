def get_map_of_center(
    longitude_left_bottom: str,
    latitude_left_bottom: str,
    longitude_right_top: str,
    latitude_right_top: str,
) -> float:
    return (float(longitude_left_bottom) + float(longitude_right_top)) / 2, (
        float(latitude_left_bottom) + float(latitude_right_top)
    ) / 2
