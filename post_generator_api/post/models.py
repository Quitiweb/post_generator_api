from django.db import models


def upload_to_fotos(instance, filename):
    return "img/%s" % instance.id + "/" + filename


class Post(models.Model):
    title = models.ForeignKey(to="Title", on_delete=models.CASCADE, related_name="post_titles")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="post_cats")
    description = models.TextField()
    featured = models.ImageField(upload_to=upload_to_fotos, null=True, blank=True)
    img1 = models.ImageField(upload_to=upload_to_fotos, null=True, blank=True)
    img2 = models.ImageField(upload_to=upload_to_fotos, null=True, blank=True)
    img3 = models.ImageField(upload_to=upload_to_fotos, null=True, blank=True)

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.title.name}"

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Title(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="title_cats")
    gpt_prompt = models.ForeignKey(
        "GptPrompt", on_delete=models.CASCADE, related_name="title_prompts",
        null=True, blank=True
    )

    name = models.CharField(max_length=500, default="")
    description = models.TextField(null=True, blank=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.name}"

    @staticmethod
    def get_random_title_from_cat(category):
        return Title.objects.filter(used=False, category__name__contains=category).first()

    def get_gpt_prompt(self, prompt=""):
        if self.gpt_prompt:
            return self.gpt_prompt
        if prompt:
            try:
                return GptPrompt.objects.get(name=prompt)
            except GptPrompt.DoesNotExist:
                print("Error de garrafa")

        return GptPrompt.objects.all().first()

    class Meta:
        verbose_name = "Title"
        verbose_name_plural = "Titles"


class Category(models.Model):
    name = models.CharField(max_length=50)
    section = models.ForeignKey("Section", on_delete=models.CASCADE, related_name="cat_sections")

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Section(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.name}"

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"


class GptPrompt(models.Model):
    name = models.CharField(max_length=250)
    prompt = models.TextField()

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.name}"

    class Meta:
        verbose_name = "GPT Prompt"
        verbose_name_plural = "GPT Prompts"
