from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    year_founded = models.PositiveIntegerField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    headquarters = models.CharField(max_length=255, blank=True, null=True)
    num_employees = models.PositiveIntegerField(blank=True, null=True)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name


class CompanyList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    companies = models.ManyToManyField(Company, related_name="company_lists")

    def __str__(self):
        return self.name
