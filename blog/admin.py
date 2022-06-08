from django.contrib import admin
from blog.models import Post,Comment,Profile
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
