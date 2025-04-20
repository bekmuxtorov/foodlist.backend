from django.core.management.base import BaseCommand
from bot.bot import run_bot


class Command(BaseCommand):
    help = "Telegram botni ishga tushiradi"

    def handle(self, *args, **kwargs):
        run_bot()
