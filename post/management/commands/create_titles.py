from django.core.management.base import BaseCommand

from post.admin import create_titles_from_gpt
from post.models import Category


class Command(BaseCommand):
    help = """Create new titles for a category"""

    def add_arguments(self, parser):
        required = parser.add_argument_group("Action flags")

        required.add_argument(
            "--category", type=str, default="software",
            help="A string with existing category name",
        )
        required.add_argument(
            "--ntitles", type=int, default="3",
            help="The number of titles you want to be created",
        )

    def handle(self, *args, **kwargs):

        if kwargs["category"] and kwargs["ntitles"]:
            try:
                category = Category.objects.get(name=kwargs["category"])
                create_titles_from_gpt(category, kwargs["ntitles"])
                print("Titles created successfully")
            except Category.DoesNotExist:
                print("The category does not exist. Please, use one of these")
                for cat in Category.objects.all():
                    print(f" - {cat.name}")

        return
