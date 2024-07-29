from celery import shared_task
from .models import CompanyList, Company


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


@shared_task
def add_companies_to_list_async(list_id, company_ids):
    try:
        company_list = CompanyList.objects.get(id=list_id)
        for chunk in chunker(company_ids, 100):
            companies = Company.objects.filter(id__in=chunk)
            company_list.companies.add(*companies)
        return {"status": "success", "list_id": list_id}
    except CompanyList.DoesNotExist:
        return {"status": "error", "message": "Company list not found"}
