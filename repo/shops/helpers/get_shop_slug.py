from django.utils.text import slugify
from common import index as Common


def get_shop_slug(name, address):
    longitude, latitude = Common.convert_address_to_coordinate(address)
    (
        address_depth1,
        address_depth2,
        address_depth3,
    ) = Common.convert_coordinate_to_address(longitude, latitude)
    trimed_name = name.replace(" ", "")
    slug = slugify(
        f"{trimed_name} {address_depth1} {address_depth2} {address_depth3}",
        allow_unicode=True,
    )
    return slug
