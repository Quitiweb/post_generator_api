#
# Tools and functions to use anywhere
#
import requests

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


def save_images_from_url(post_model, urls):
    select_img = 0
    for url in urls:
        img = requests.get(url).content

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(img)
        img_temp.flush()

        if select_img >= 4:
            continue
        if select_img == 0:
            post_model.featured.save("featured.jpg", File(img_temp), save=True)
        if select_img == 1:
            post_model.img1.save("img1.jpg", File(img_temp), save=True)
        if select_img == 2:
            post_model.img2.save("img2.jpg", File(img_temp), save=True)
        if select_img == 3:
            post_model.img3.save("img2.jpg", File(img_temp), save=True)
        select_img += 1
