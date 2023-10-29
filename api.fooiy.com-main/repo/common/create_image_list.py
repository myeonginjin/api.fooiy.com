def create_image_list(image_1, image_2, image_3, image_4=None, image_5=None):
    images = []

    if image_1:
        images.append(image_1)
    if image_2:
        images.append(image_2)
    if image_3:
        images.append(image_3)
    if image_4:
        images.append(image_4)
    if image_5:
        images.append(image_5)

    return images
