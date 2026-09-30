import os
import sys
from pathlib import Path
from random import choice, choices, randint

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 100

sys.path.append(str(DJANGO_BASE_DIR))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
settings.USE_TZ = False

django.setup()

if __name__ == "__main__":
    from faker import Faker
    from faker_file.providers.png_file import PngFileProvider

    from blog.models import Category, Post, Tag

    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()

    fake = Faker()
    fake.add_provider(PngFileProvider)

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
    tags = [
        "Fun",
        "DPS",
        "DoT",
        "Endgame",
        "Early Game",
        "Mid Game",
    ]

    django_categories = [Category(name=name) for name in categories]
    django_tags = [Tag(name=name) for name in tags]

    for category in django_categories:
        category.save()

    for tag in django_tags:
        tag.save()

    django_posts: list[Post] = []

    for _ in range(NUMBER_OF_OBJECTS):
        title = fake.catch_phrase()
        # slug auto
        excerpt = fake.text(max_nb_chars=50)
        # is_published auto
        content = fake.text(max_nb_chars=10000)
        # cover = fake.png_file()
        category = choice(django_categories)  # noqa: S311
        tags = choices(django_tags, k=randint(1, 6))  # noqa: S311

        post = Post(
            title=title,
            excerpt=excerpt,
            content=content,
            category=category,
        )
        post.save()
        post.tags.set(tags)
