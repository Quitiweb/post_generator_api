import os
import time
from urllib.error import HTTPError

import openai
import requests
from django.conf import settings
from dotenv import load_dotenv
from openai.error import RateLimitError

from .models import Post, Title

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
gpt_one_title = """
Necesito un título, solo un título, relacionado con {} para escribir un post en un blog.
Para el título, quiero un punto de vista científico y/o tecnológico.
Diferente a otros anteriores que haya podido pedirte.
Que atraiga a una gran mayoría de personas nada más leerlo.
"""
gpt_multiple_titles = """
Necesito {} ideas de títulos relacionados con {} para escribir un blog.
En texto plano, en formato CSV, separados por punto y coma.
No los enumeres, solo escribe los títulos línea a línea y, al final de cada línea,
punto y coma.
"""
gpt_titles_non_related = """
Importante que no tengan relación con los títulos siguientes: {} 
"""
gpt_template = """
<html>
<head></head>
<body>
<h2>titulo1</h2><p>descripcion</p><h3>subtitulo1</h3><p>descripcion</p><h3>subtitulo2</h3><p>descripcion</p>
<h2>titulo2</h2><p>descripcion</p><h3>subtitulo1</h3><p>descripcion</p><h3>subtitulo2</h3><p>descripcion</p>
<h4>categoria1</h4><p>descripcion<a>enlace</a></p><h4>categoria2</h4>
<h2>conclusion</h2><p>texto</p>
</body>
</html>
"""
gpt_post = """
Escribe un post lo más detallado posible, en formato HTML, renderizado para SEO con headers, sub-headers, negritas, cursivas, etc.
En formato HTML. En texto plano. Como mínimo, 5 párrafos con 5 títulos en <h2></h2> y varios subtítulos en <h3></h3>.
Título: {}
Plantilla: {}
"""
gpt_image_v1 = """
{}, low poly, isometric art, 3d art, high detail, artstation, concept art,
behance, ray tracing, smooth, sharp focus, ethereal lighting
"""
gpt_image_v2 = """
{}, The Future of Comfort: How Home Automation is Revolutionizing Our Lives, ultra hd,
realistic, vivid colors, highly detailed, UHD drawing, pen and ink, perfect composition,
beautiful detailed intricate insanely detailed octane render trending on artstation,
8k artistic photography, photorealistic concept art,
soft natural volumetric cinematic perfect light
"""
url_block = """
<figure class="wp-block-image size-full"><img src="{}" alt=""/></figure>
<hr class="wp-block-separator has-alpha-channel-opacity"/>
"""


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
        featured=requests.get(image_urls[0]).content,
        img1=requests.get(image_urls[1]).content,
        img2=requests.get(image_urls[2]).content,
        img3=requests.get(image_urls[3]).content,
    )

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
        if select_img >= 4:
            continue
        if select_img == 1:
            img_url = os.path.join(settings.MEDIA_ROOT, post.img1.url)
        if select_img == 2:
            img_url = os.path.join(settings.MEDIA_ROOT, post.img2.url)
        if select_img == 3:
            img_url = os.path.join(settings.MEDIA_ROOT, post.img3.url)

        fpost += url_block.format(img_url)

    return fpost, tokens


def call_gpt(description, tokens):
    result = ""
    retries = 5
    ntries = 0
    error = True

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
