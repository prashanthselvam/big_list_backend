from rest_framework import serializers
from .models import Company, CompanyList


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CompanyListSerializer(serializers.ModelSerializer):
    companies = CompanySerializer(many=True, read_only=True)

    class Meta:
        model = CompanyList
        fields = ["id", "name", "description", "companies"]


class CompanyListSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyList
        fields = ["id", "name", "description"]


class CreateCompanyListSerializer(serializers.ModelSerializer):
    companies = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), many=True
    )

    class Meta:
        model = CompanyList
        fields = ["name", "description", "companies"]


class AddCompaniesToListSerializer(serializers.Serializer):
    company_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    search = serializers.CharField(required=False, allow_blank=True)
