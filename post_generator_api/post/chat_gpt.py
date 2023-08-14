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


def chat_con_gpt(mensaje, conversation, description, tokens):
    retries = 5
    print()
    print("Longitud actual: ", tokens)
    print()
    conversation += mensaje + "\nPersona: "

    ntries = 0
    error = True
    while (ntries < retries) and error:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": description},
                    {"role": "user", "content": conversation},
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

    conversation += result + "\nPersona: "

    tokens = response["usage"]["total_tokens"]

    return result, conversation, tokens
