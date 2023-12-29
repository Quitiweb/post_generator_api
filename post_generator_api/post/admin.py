from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from .forms import CreateTitlesForm
from .gpt import generate_titles_gpt
from .models import Post, Title, Category, Section, GptPrompt


def create_titles_from_gpt(category, ntitles=30):
    retries = 5
    ntries = 0
    text = ""
    # TODO: revisar ese while X < ntitles
    while (ntries < retries) and (len(text.split(";")) < ntitles):
        ntries += 1
        text, tokens = generate_titles_gpt(ntitles=ntitles, category=category)

    if ntries == 5:
        return False

    for title in text.split(";"):
        if title != "":
            Title.objects.create(
                name=title,
                category=category,
                used=False
            )
    return True


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "used",)
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
                categories = form.cleaned_data["categories"]
                ntitles = form.cleaned_data["number_of_titles"]
                if ntitles is None:
                    ntitles = 30

                cat_failed = []
                for category in categories:
                    created = create_titles_from_gpt(category=category, ntitles=ntitles)
                    if not created:
                        cat_failed.append(category.name)

                self.message_user(
                    request,
                    "Títulos generados correctamente",
                )
                if cat_failed:
                    self.message_user(
                        request,
                        "Títulos no generados: {}".format(
                            [c for c in cat_failed]
                        ),
                        level="WARNING",
                    )

                return redirect("..")

        form = CreateTitlesForm()
        payload = {"form": form}

        # return HttpResponseRedirect(request.META["HTTP_REFERER"])
        return render(request, "generate_titles.html", payload)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "section",)


class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


@admin.register(GptPrompt)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Section, SectionAdmin)
