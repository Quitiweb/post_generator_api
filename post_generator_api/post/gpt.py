import os
import time
from urllib.error import HTTPError

import openai
from django.conf import settings
from dotenv import load_dotenv
from openai.error import RateLimitError

from .models import Post, Title
from .tools.prompts import (
    gpt_image_v2, gpt_multiple_titles, gpt_titles_non_related, gpt_post, gpt_template,
    url_block,
)
from .tools.utils import save_images_from_url

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_openai_models():
    """
    Esta función es solo para ver por consola los modelos de openai existentes
    """
    res = openai.Model.list()
    for r in res.data:
        print(r.id)


def generate_image(title):
    response = openai.Image.create(
        prompt=gpt_image_v2.format(title),
        n=4,
        size="1024x1024"
    )
    image_urls = []
    for data in response["data"]:
        image_urls.append(data['url'])

    return image_urls


def generate_titles_gpt(category, ntitles=30, tokens=0):
    description = gpt_multiple_titles.format(ntitles, category.name)
    titles = Title.objects.filter(category=category)
    if titles:
        description += gpt_titles_non_related.format([t.name + ", " for t in titles])

    result, tokens = call_gpt(description, tokens)

    # Eliminar las dobles comillas y la barra inclinada al principio y al final
    cleaned_string = result.strip("\"")

    # Reemplazar las barras inclinadas restantes
    # cleaned_string = cleaned_string.replace("\\", "")

    return cleaned_string, tokens


def generate_post_gpt(title, tokens):
    description = gpt_post.format(gpt_template, title.name)
    title.used = True
    title.save()

    result, tokens = call_gpt(description, tokens)

    # Generar imagen del título por API e IA
    image_urls = generate_image(title.name)

    post = Post.objects.create(
        title=title,
        category=title.category,
        description=result,
    )
    save_images_from_url(post, image_urls)

    # TODO: Featured image
    #   CODIGO AQUI
    #

    # Split del código por cabeceras e inserción de las imágenes
    fpost = ""
    # TODO: Comprobar que el split por H2 devuelve más de X resultados
    select_img = 0
    for stext in result.split("</h2>"):
        fpost += stext
        select_img += 1
        img_url = ""

        if select_img >= 4:
            continue
        if select_img == 1:
            img_url = os.path.join(settings.MEDIA_ROOT, post.img1.url)
        if select_img == 2:
            img_url = os.path.join(settings.MEDIA_ROOT, post.img2.url)
        if select_img == 3:
            img_url = os.path.join(settings.MEDIA_ROOT, post.img3.url)

        fpost += url_block.format(img_url)

    post.description = fpost
    post.save()

    return fpost, tokens


def call_gpt(description, tokens):
    result = ""
    retries = 5
    ntries = 0
    error = True
    response = None

    while (ntries < retries) and error:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": description},
                    # {"role": "user", "content": conversation},
                ]
            )
            error = False
        except (HTTPError, RateLimitError) as e:
            error = True
            ntries += 1
            print("Error de openai: {}".format(e))
            print()
            for i in range(5, -1, -1):
                print("Reintentando en: {}".format(i))
                time.sleep(1)

    if not error:
        for option in response.choices:
            result += option.message.content

        tokens = response["usage"]["total_tokens"]

    return result, tokens
