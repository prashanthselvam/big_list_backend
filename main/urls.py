from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, CompanyListViewSet, CompanyListCompaniesView

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"company-lists", CompanyListViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "company-lists/<int:pk>/companies/",
        CompanyListCompaniesView.as_view(),
        name="company-list-companies",
    ),
    path(
        "company-lists/<int:pk>/add-companies/",
        CompanyListViewSet.as_view({"post": "add_companies"}),
        name="add-companies",
    ),
]
