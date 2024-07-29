from django.contrib import admin
from .models import Company


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_founded', 'industry', 'num_employees', 'revenue')
    search_fields = ('name', 'industry', 'headquarters')
