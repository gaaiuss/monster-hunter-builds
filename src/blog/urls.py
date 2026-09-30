from django.urls import path

from blog.views import index, post_detail

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("post_detail/<int:post_id>/", post_detail, name="post"),
]
