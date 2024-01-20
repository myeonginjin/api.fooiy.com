from common import index as Common


def get_android_picker(feeds):
    results = []
    if feeds.exists():
        current_feed_id = feeds[0].id
        current_longitude = feeds[0].longitude
        current_latitude = feeds[0].latitude
        current_feed_image = feeds[0].to_image[0].image.url
        current_count = 0
        for feed in feeds:
            if (
                feed.longitude == current_longitude
                and feed.latitude == current_latitude
            ):
                current_count += 1

            else:
                results.append(
                    {
                        "id": current_feed_id,
                        "longitude": current_longitude,
                        "latitude": current_latitude,
                        "feed_image": current_feed_image,
                        "feeds_count": current_count,
                    }
                )
                current_feed_id = feed.id
                current_longitude = feed.longitude
                current_latitude = feed.latitude
                current_feed_image = feed.to_image[0].image.url
                current_count = 1

        results.append(
            {
                "id": current_feed_id,
                "longitude": current_longitude,
                "latitude": current_latitude,
                "feed_image": current_feed_image,
                "feeds_count": current_count,
            }
        )

    return results


def check_feed_is_cafe(feed):
    try:
        return feed.shop.category.first().name == Common.global_variables.category_cafe
    except:
        return False


def get_ios_picker(feeds):
    results = []
    if feeds.exists():
        current_feed_id = feeds[0].id
        current_longitude = feeds[0].longitude
        current_latitude = feeds[0].latitude
        current_category_is_cafe = check_feed_is_cafe(feeds[0])
        current_count = 0
        for feed in feeds:
            if (
                feed.longitude == current_longitude
                and feed.latitude == current_latitude
            ):
                current_count += 1

            else:
                results.append(
                    {
                        "id": current_feed_id,
                        "longitude": current_longitude,
                        "latitude": current_latitude,
                        "category_is_cafe": current_category_is_cafe,
                        "feeds_count": current_count,
                    }
                )
                current_feed_id = feed.id
                current_longitude = feed.longitude
                current_latitude = feed.latitude
                current_category_is_cafe = check_feed_is_cafe(feed)
                current_count = 1

        results.append(
            {
                "id": current_feed_id,
                "longitude": current_longitude,
                "latitude": current_latitude,
                "category_is_cafe": current_category_is_cafe,
                "feeds_count": current_count,
            }
        )

    return results
