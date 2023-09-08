#
# All prompts to call AI will lay here
#

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
Escribe un post lo más detallado posible, renderizado para SEO con headers, sub-headers, negritas, cursivas, etc.
En formato HTML. En texto plano. Como mínimo, 5 títulos en <h2></h2> y varios subtítulos en <h3></h3>.
Las descripciones que sean de, al menos, dos párrafos.
Título: {}
Plantilla: {}
"""
gpt_image_v1 = """
{}, low poly, isometric art, 3d art, high detail, artstation, concept art,
behance, ray tracing, smooth, sharp focus, ethereal lighting
"""
gpt_image_v2 = """
{}, ultra hd,
realistic, vivid colors, highly detailed, UHD drawing, pen and ink, perfect composition,
beautiful detailed intricate insanely detailed octane render trending on artstation,
8k artistic photography, photorealistic concept art,
soft natural volumetric cinematic perfect light
"""
# TODO: alt
url_block = """
<figure class="wp-block-image size-full"><img src="{}" alt=""/></figure>
<hr class="wp-block-separator has-alpha-channel-opacity"/>
"""
