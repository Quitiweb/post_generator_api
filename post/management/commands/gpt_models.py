from django.core.management.base import BaseCommand

from post.gpt import get_openai_models


class Command(BaseCommand):
    help = """Show GPT models"""

    def add_arguments(self, parser):
        required = parser.add_argument_group("Action flags")

        required.add_argument("--show", action="store_true",
                              help="Show GPT models in the console")

    def handle(self, *args, **kwargs):

        if kwargs["show"]:
            get_openai_models()

        return
