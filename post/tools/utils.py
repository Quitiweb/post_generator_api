#
# Tools and functions to use anywhere
#
import os
import requests

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .prompts import url_block


def remove_html_tags(text):
    # Remove the specific text ```html``` and ``` from the string
    cleaned_text = text.replace("```html", "").replace("```", "")
    return cleaned_text.strip()


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


def insert_images_into_text(post, text, domain):
    """
    Split del código por cabeceras e inserción de las imágenes
    :param post: objeto de tipo Post
    :param domain: la url del dominio, p.e: host.com
    :param text: el texto con cabeceras <h2> donde irán insertadas las imágenes
    :return: el texto con las imágenes insertadas
    """
    fpost = ""
    select_img = 0

    # TODO: Comprobar que el split por H2 devuelve más de X resultados
    for stext in text.split("</h2>"):
        fpost += stext + "</h2>"
        select_img += 1
        img_url = domain

        if select_img >= 4:
            continue
        if select_img == 1:
            img_url += os.path.join(settings.MEDIA_ROOT, post.img1.url)
        if select_img == 2:
            img_url += os.path.join(settings.MEDIA_ROOT, post.img2.url)
        if select_img == 3:
            img_url += os.path.join(settings.MEDIA_ROOT, post.img3.url)

        fpost += url_block.format(img_url)

    return fpost
