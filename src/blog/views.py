from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

app_name = "blog"


def index(request: HttpRequest) -> HttpResponse:
    template = "blog/pages/index.html"
    return render(request=request, template_name=template)
