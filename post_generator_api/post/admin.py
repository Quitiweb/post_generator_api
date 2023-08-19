from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from .forms import CreateTitlesForm
from .gpt import generate_titles_gpt
from .models import Post, Title, Category, Section


def create_titles_from_gpt(category):
    retries = 5
    ntries = 0
    text = ""
    while (ntries < retries) and (len(text.split(";")) < 2):
        ntries += 1
        text, tokens = generate_titles_gpt(category)

    for title in text.split(";"):
        Title.objects.create(
            name=title,
            category=category,
            used=False
        )


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "used", )
    change_list_template = "title_admin.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("generate_titles/", self.generate_titles),
        ]

        return my_urls + urls

    def generate_titles(self, request):
        if request.method == "POST":
            form = CreateTitlesForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data["category"]
                create_titles_from_gpt(category)
                self.message_user(request, "Títulos generados correctamente")
                return redirect("..")

        form = CreateTitlesForm()
        payload = {"form": form}

        # return HttpResponseRedirect(request.META["HTTP_REFERER"])
        return render(request, "generate_titles.html", payload)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "section", )


class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Section, SectionAdmin)
