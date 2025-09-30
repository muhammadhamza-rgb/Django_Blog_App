from django import forms
from django.contrib import admin
from django.db import models

from .models import Post

# Register your models here.


admin.site.register(Post)
