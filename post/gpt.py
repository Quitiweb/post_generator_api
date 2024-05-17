import time
from urllib.error import HTTPError

import openai
from decouple import config
from dotenv import load_dotenv
from openai._exceptions import RateLimitError

from aws.utils import get_product_title_and_description
from .models import Post, Title
from .tools.prompts import gpt_image_v2, gpt_multiple_titles, gpt_titles_non_related
from .tools.utils import remove_html_tags

load_dotenv()
openai.api_key = config("OPENAI_API_KEY")
#GPT_MODEL = "gpt-3.5-turbo"
# GPT_MODEL = "gpt-3.5-turbo"
GPT_MODEL = "gpt-4o"
# GPT_MODEL = "gpt-4-32k"
# GPT_MODEL = "gpt-4-1106-preview"

client = openai.OpenAI()


def get_openai_models():
    """
    Esta función es solo para ver por consola los modelos de openai existentes
    """
    res = openai.Model.list()
    for r in res.data:
        print(r.id)


def generate_image(title):
    """
    Esta funcionalidad actualmente tiene coste y no es una "maravilla" precisamente.
    La dejo por aquí, pero en principio no voy a utilizarla.
    :param title: Título de la imagen para el prompt de text-to-image
    :return: las urls de las imágenes
    """
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


def generate_post_gpt(title, tokens=0, asin=None, domain=None):
    if asin:
        # Call PAAPI and get amazon product description
        title.name, title.description = get_product_title_and_description(asin)
        gpt_prompt = title.get_gpt_prompt("analisis_producto")
    else:
        gpt_prompt = title.get_gpt_prompt()

    description = f"Título: {title.name}. " + gpt_prompt.prompt
    if title.description:
        description += ". Básate en esta información: " + title.description

    title.used = True
    title.save()

    result, tokens = call_gpt(description, tokens)

    # Generar imagen del título por API e IA
    # image_urls = generate_image(title.name)

    post = Post.objects.create(
        title=title,
        category=title.category,
        description=result,
    )
    # save_images_from_url(post, image_urls)

    # TODO: Featured image
    #   CODIGO AQUI
    #

    # post.description = insert_images_into_text(post, result, domain)
    post.description = result
    post.save()

    return post.description, tokens


def call_gpt(description, tokens=0, model=GPT_MODEL):
    result = ""
    retries = 5
    ntries = 0
    error = True
    response = None

    while (ntries < retries) and error:
        try:
            response = client.chat.completions.create(
                model=model,
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

    if not error:
        for option in response.choices:
            result += option.message.content

        tokens = response.usage.total_tokens

    return remove_html_tags(result), tokens
