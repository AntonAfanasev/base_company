from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    
    list_display = ('name', 'lastname', 'middlename', 'birthdate', 'email', 'phone','start_work_date', 'end_work_date', 'position', 'sector' )
    list_display_links = ('name', 'lastname', 'middlename')
    list_per_page=50
    ordering = ['lastname', 'position', 'sector']
    search_field = ['lastname', 'position', 'sector']
    exclude = ()

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Sector)
