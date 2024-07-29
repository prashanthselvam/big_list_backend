from rest_framework import viewsets, generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company, CompanyList
from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    CompanyListSimpleSerializer,
    CreateCompanyListSerializer,
    AddCompaniesToListSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from .tasks import add_companies_to_list_async


class CompanyPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 1000


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = CompanyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "industry"]


class CompanyListViewSet(viewsets.ModelViewSet):
    queryset = CompanyList.objects.all()
    serializer_class = CompanyListSimpleSerializer

    @action(detail=True, methods=["post"])
    def add_companies(self, request, pk=None):
        company_list = self.get_object()
        serializer = AddCompaniesToListSerializer(data=request.data)
        if serializer.is_valid():
            company_ids = serializer.validated_data.get("company_ids", [])
            search_query = serializer.validated_data.get("search", "")

            if search_query:
                companies = Company.objects.filter(
                    name__icontains=search_query
                ) | Company.objects.filter(industry__icontains=search_query)
                company_ids = list(companies.values_list("id", flat=True))

            if len(company_ids) > 1000:
                first_batch = company_ids[:1000]
                remaining_batch = company_ids[1000:]
                company_list.companies.add(*first_batch)

                add_companies_to_list_async.delay(company_list.id, remaining_batch)

                return Response(
                    {
                        "message": f"First 1000 companies added to list {company_list.name}. The remaining companies are being processed.",
                        "list_id": company_list.id,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                companies = Company.objects.filter(id__in=company_ids)
                company_list.companies.add(*companies)
                return Response(
                    {
                        "message": f"All companies added to list {company_list.name}.",
                        "list_id": company_list.id,
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="create-with-companies")
    def create_with_companies(self, request):
        serializer = CreateCompanyListSerializer(data=request.data)
        if serializer.is_valid():
            company_list = serializer.save()

            search_query = request.data.get("search", "")
            if search_query:
                companies = Company.objects.filter(
                    name__icontains=search_query
                ) | Company.objects.filter(industry__icontains=search_query)
                company_ids = list(companies.values_list("id", flat=True))

            if len(company_ids) > 1000:
                first_batch = company_ids[:1000]
                remaining_batch = company_ids[1000:]
                company_list.companies.add(*first_batch)

                add_companies_to_list_async.delay(company_list.id, remaining_batch)

                return Response(
                    {
                        "message": f"First 1000 companies added to list {company_list.name}. The remaining companies are being processed.",
                        "list_id": company_list.id,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                companies = Company.objects.filter(id__in=company_ids)
                company_list.companies.add(*companies)
                return Response(
                    {
                        "message": f"All companies added to list {company_list.name}.",
                        "list_id": company_list.id,
                    },
                    status=status.HTTP_200_OK,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyListCompaniesView(generics.ListAPIView):
    serializer_class = CompanySerializer
    pagination_class = CompanyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "industry"]

    def get_queryset(self):
        list_id = self.kwargs["pk"]
        return Company.objects.filter(company_lists__id=list_id)
