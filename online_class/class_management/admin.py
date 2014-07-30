from django.contrib import admin
from class_management.models import *
from home.models import *

class ClassAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('class_name',)}

class TinyMCEAdmin(admin.ModelAdmin):
        class Media:
                js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/tiny_mce/textareas.js',)

admin.site.register(Class, TinyMCEAdmin)
admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(Question)
