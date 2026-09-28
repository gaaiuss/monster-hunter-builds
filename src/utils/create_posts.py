import os
import sys
from pathlib import Path
from random import choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
settings.USE_TZ = False

django.setup()

if __name__ == "__main__":
    import faker

    from blog.models import Category, Post

    Post.objects.all().delete()
    Category.objects.all().delete()

    fake = faker.Faker("en")
    categories = [
        "Dual Blades",
        "Long Sword",
        "Hammer",
        "Insect Glaive",
        "Lance",
        "Sword and Shield",
        "Bow",
        "Light Bowgun",
        "Heavy Bowgun",
        "Gunlance",
        "Hunting Horn",
        "Switch Axe",
        "Charge Blade",
        "Great Sword",
    ]

    django_categories = [Category(name=name) for name in categories]

    for category in django_categories:
        category.save()

    django_posts: list[Post] = []

    for _ in range(NUMBER_OF_OBJECTS):
        title = fake.catch_phrase()
        short_description = fake.text(max_nb_chars=50)
        description = fake.text(max_nb_chars=100)
        created_date = fake.date_this_year()
        category = choice(django_categories)  # noqa: S311

        django_posts.append(
            Post(
                title=title,
                short_description=short_description,
                description=description,
                created_date=created_date,
                category=category,
            ),
        )

    if len(django_posts) > 0:
        Post.objects.bulk_create(django_posts)
