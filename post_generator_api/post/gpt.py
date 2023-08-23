import os
import time
from urllib.error import HTTPError

import openai
from dotenv import load_dotenv
from openai.error import RateLimitError

from .models import Title

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


def get_openai_models():
    """
    Esta función es solo para ver por consola los modelos de openai existentes
    """
    res = openai.Model.list()
    for r in res.data:
        print(r.id)


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
    return call_gpt(description, tokens)


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
