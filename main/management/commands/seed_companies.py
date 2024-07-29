import random
import logging
import time
from django.core.management.base import BaseCommand
from main.models import Company
from faker import Faker


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed the database with 25 million company records"

    def handle(self, *args, **kwargs):
        fake = Faker()
        batch_size = 10000  # Number of records to create in each batch
        total_records = 10000000

        industries = [
            "Technology",
            "Finance",
            "Healthcare",
            "Retail",
            "Manufacturing",
            "Education",
            "Real Estate",
            "Transportation",
            "Entertainment",
        ]
        headquarters = [
            "New York, NY",
            "San Francisco, CA",
            "Los Angeles, CA",
            "Chicago, IL",
            "Houston, TX",
            "Phoenix, AZ",
            "Philadelphia, PA",
        ]

        start_time = time.time()
        logger.info(f"Starting to seed {total_records} company records...")

        for i in range(total_records // batch_size):
            batch_start_time = time.time()

            companies = [
                Company(
                    name=fake.company(),
                    description=fake.catch_phrase(),
                    year_founded=random.randint(1800, 2023),
                    industry=random.choice(industries),
                    website=fake.url(),
                    headquarters=random.choice(headquarters),
                    num_employees=random.randint(1, 10000),
                    revenue=round(random.uniform(10000, 1000000000), 2),
                )
                for _ in range(batch_size)
            ]
            Company.objects.bulk_create(companies)

            batch_end_time = time.time()
            batch_duration = batch_end_time - batch_start_time
            logger.info(
                f"Batch {i + 1} created successfully in {batch_duration:.2f} seconds"
            )

        end_time = time.time()
        total_duration = end_time - start_time
        logger.info(
            f"Successfully seeded {total_records} company records in {total_duration:.2f} seconds"
        )
