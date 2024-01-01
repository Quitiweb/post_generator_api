from django.core.management.base import BaseCommand

from aws.samples.sample_get_items_api import get_items


class Command(BaseCommand):
    help = """Runs AWS PAAPI commands"""

    def add_arguments(self, parser):
        required = parser.add_argument_group("Action flags")

        required.add_argument("--get_items", action="store_true",
                              help="Get items from PAAPI")

        parser.add_argument(
            "--aws_id", type=str, nargs="?", default=[],
            help="A list with AWS products IDs",
            action="append",
        )

    def handle(self, *args, **kwargs):

        if kwargs["get_items"]:
            print(kwargs["aws_id"])
            get_items(kwargs["aws_id"])

        return
