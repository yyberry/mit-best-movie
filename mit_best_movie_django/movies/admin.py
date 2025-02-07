from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect

from .models import Category, Movie, WatchedMovie

from update_dynamic_movies import fetch_dynamic_movies

class CategoryAdmin(admin.ModelAdmin):
    # Add a button to the ModelAdmin to trigger the update operation
    change_list_template = "admin/category_change_list.html"  

    # Custom url path to trigger updates
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('trigger-update/', self.admin_site.admin_view(self.trigger_update), name='trigger_update'),
        ]
        return custom_urls + urls

    def trigger_update(self, request):
        fetch_dynamic_movies()  
        self.message_user(request, "Dynamic category updated successfully!")
        return HttpResponseRedirect("..") 

    actions = ['trigger_update']  # Add button to trigger update


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Movie)
admin.site.register(WatchedMovie)