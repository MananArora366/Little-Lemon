"""Make the deployed site presentable, on every deploy.

Render's free tier has no persistent disk and no shell: the SQLite file is
rebuilt from scratch on each deploy, and `createsuperuser` cannot be run
interactively because there is nowhere to run it. So anything the live site
needs in its database has to be created by the build itself.

This command is idempotent by design -- it is safe to run on every single
deploy. It never overwrites an existing row and never resets a password.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from restaurant.models import Menu

# Mediterranean, to match the Little Lemon brief. Prices in whole dollars and
# cents; `inventory` is what the API exposes as stock.
MENU_ITEMS = [
    ("Greek Salad",            12.50, 25),
    ("Bruschetta",             8.00,  40),
    ("Grilled Fish",           22.00, 15),
    ("Lemon Dessert",          6.50,  30),
    ("Hummus & Pita",          9.00,  35),
    ("Falafel Plate",          14.00, 20),
    ("Lamb Souvlaki",          19.50, 18),
    ("Spanakopita",            10.50, 22),
    ("Moussaka",               17.00, 16),
    ("Baklava",                7.00,  28),
]


class Command(BaseCommand):
    help = "Idempotently seed menu items and an admin user. Safe to run on every deploy."

    def handle(self, *args, **options):
        self._seed_menu()
        self._seed_superuser()

    @transaction.atomic
    def _seed_menu(self):
        created = 0
        for title, price, inventory in MENU_ITEMS:
            # get_or_create keyed on title: a second run finds the existing row
            # and leaves any price edited through the admin untouched.
            _, was_created = Menu.objects.get_or_create(
                title=title,
                defaults={"price": price, "inventory": inventory},
            )
            created += was_created

        total = Menu.objects.count()
        if created:
            self.stdout.write(self.style.SUCCESS(
                f"Menu: created {created} item(s), {total} total."
            ))
        else:
            self.stdout.write(f"Menu: nothing to create, {total} already present.")

    def _seed_superuser(self):
        """Create the admin account from environment variables.

        The password is read from the environment and never appears in this
        repository. If the variables are not set the command says so and moves
        on -- a missing admin account must not fail the build.
        """
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "Admin: DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD not set, skipping."
            ))
            return

        if User.objects.filter(username=username).exists():
            # Deliberately does NOT reset the password. If the account is ever
            # locked out, change the env var and delete the user -- silently
            # rewriting a password on every deploy would be worse.
            self.stdout.write(f"Admin: user '{username}' already exists, leaving it alone.")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Admin: created superuser '{username}'."))
