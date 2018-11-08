from django.contrib import admin
from .models import Post
from import_export import resources
from .models import Articleupload
from import_export.admin import ImportExportModelAdmin

admin.site.register(Post)

class ArticleuploadResource(resources.ModelResource):
    class Meta:
        model = Articleupload

@admin.register(Articleupload)
class ArticleuploadAdmin(ImportExportModelAdmin):
    pass