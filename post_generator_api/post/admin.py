from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path

from .forms import CreateTitlesForm
from .models import Post, Title, Category, Section


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", )
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
                # Llamamos a ChatGPT?
                category = form.cleaned_data["category"]
                self.message_user(request, "Títulos generadas correctamente")
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
