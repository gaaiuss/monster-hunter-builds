from typing import TYPE_CHECKING

from django.http import Http404
from django.shortcuts import render

from blog.models import Post

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

app_name = "blog"


def index(request: HttpRequest) -> HttpResponse:
    template = "blog/pages/index.html"
    posts = Post.objects.all()
    context = {
        "posts": posts,
    }
    return render(request, template, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    template = "blog/pages/post.html"
    posts = Post.objects.all()
    post_found: Post | None = None

    for post in posts:
        if post.id == post_id:
            post_found = post
            break

    if post_found is None:
        msg = "Post does not exists!"
        raise Http404(msg)

    context = {
        "post": post_found,
    }
    return render(request, template, context)
