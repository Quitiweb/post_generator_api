# post_generator_api

Esta API se utiliza para generar POST automáticos utilizando Chat-GPT

La idea es, utilizando el plugin de WordPress, generar posts de forma automática según la categoría que elijas.
Estas categorías tienen unos títulos vinculados y generados también por la IA. A partir de ellos, crea un artículo.

Para que funcione correctamente, hay que crear un fichero `.env` en local y utilizar las siguientes variables:
### La API Key de Open AI (Chat GPT)
```commandline
OPENAI_API_KEY
```

### Los datos de acceso de la PAAPI (la API de AWS de afiliados)
```commandline
ACCESS_KEY
SECRET_KEY
PARTNER_TAG
```
