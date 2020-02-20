from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from PIL import Image, ExifTags


def file_uploads(myfile, media_path):
    fs = FileSystemStorage()
    upload_root = "{0}/{1}".format(media_path, myfile.name)
    filename = fs.save(upload_root, myfile)
    uploaded_file_url = fs.url(filename)
    resize_image(os.path.join(settings.MEDIA_ROOT, upload_root))
    return uploaded_file_url


def resize_image(upload_root):
    image = Image.open(upload_root)

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == "Orientation":
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)

    image_width, image_height = image.size
    width = 0
    height = 0

    if image_width > 1920:
        idx = image_width / 1920
        width = int(image_width / idx)
        height = int(image_height / idx)

    image = image.resize((width, height), Image.ANTIALIAS)

    image.save(upload_root, format="jpeg")
