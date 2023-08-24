from django.db import models


class Post(models.Model):
    title = models.ForeignKey(to="Title", on_delete=models.CASCADE, related_name="post_titles")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="post_cats")
    description = models.TextField()
    featured = models.FileField(null=True, blank=True)
    img1 = models.FileField(null=True, blank=True)
    img2 = models.FileField(null=True, blank=True)
    img3 = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.title.name}"

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Title(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="title_cats")
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.__class__.__name__} - {self.pk}: {self.name}"

    @staticmethod
    def get_random_title_from_cat(category):
        return Title.objects.filter(used=False, category__name__contains=category).first()

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
