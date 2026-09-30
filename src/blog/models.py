from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import User
from django.db import models

from utils.images import resize_image
from utils.rands import slugify_new

if TYPE_CHECKING:
    from django.db.models import ManyToManyField


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=50,
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if not self.slug:
            self.slug = slugify_new(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=50,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if not self.slug:
            self.slug = slugify_new(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True,
        default="",
        null=False,
        blank=True,
        max_length=50,
    )
    excerpt = models.CharField(max_length=200)
    is_published = models.BooleanField(
        default=True,
        help_text="Share your post publicly.",
    )
    content = models.TextField()
    cover = models.ImageField(upload_to="posts/%Y/%m/", blank=True, default=None)
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text="Show cover image in post content.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="post_created_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="post_updated_by",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    tags: ManyToManyField[Tag, Tag] = models.ManyToManyField(Tag, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        if not self.slug:
            self.slug = slugify_new(self.title)

        current_cover_name = str(self.cover.name) if self.cover else ""
        super().save(*args, **kwargs)

        if self.cover and current_cover_name != self.cover.name:
            resize_image(self.cover, 900, 70)
