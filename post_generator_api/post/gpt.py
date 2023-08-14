import os
import time
from urllib.error import HTTPError

import openai
from dotenv import load_dotenv
from openai.error import RateLimitError

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_openai_models():
    res = openai.Model.list()
    for r in res.data:
        print(r.id)


def generate_title_gpt(category="ciencia", tokens=0):
    description = f"""
    Necesito un título, solo un título, relacionado con {category} para escribir un post en un blog.
    """

    retries = 5
    print()
    print("Longitud actual: ", tokens)
    print()

    ntries = 0
    error = True
    while (ntries < retries) and error:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": description},
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

    result = ""
    for option in response.choices:
        result += option.message.content

    # Eliminar las dobles comillas y la barra inclinada al principio y al final
    cleaned_string = result.strip("\"")

    # Reemplazar las barras inclinadas restantes
    cleaned_string = cleaned_string.replace("\\", "")

    tokens = response["usage"]["total_tokens"]

    return cleaned_string, tokens


def generate_post_gpt(title, tokens):
    description = f"""
    Escribe un post lo más detallado posible, en formato HTML, renderizado para SEO con headers, sub-headers, negritas, cursivas, etc.
    En formato HTML. En texto plano.
    Título: "{title}"
    """

    # conversation = ""

    retries = 5
    print()
    print("Longitud actual: ", tokens)
    print()
    # conversation += title + "\nPersona: "

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

    result = ""
    for option in response.choices:
        result += option.message.content

    # conversation += result + "\nPersona: "

    tokens = response["usage"]["total_tokens"]

    return result, tokens
