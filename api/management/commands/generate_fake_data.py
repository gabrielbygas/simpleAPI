from django.core.management.base import BaseCommand
from faker import Faker
import random
from api.models import Persons  # Remplacez par le nom de votre modèle

class Command(BaseCommand):
    help = 'Générer 100 données fictives'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(100):
            # Remplacez les champs par ceux de votre modèle
            Persons.objects.create(
                firstname = fake.first_name(),
                lastname = fake.last_name(),
                sex = random.choice(["M", "F"]),
                email = fake.email(),
                phone = fake.phone_number(),
                city = fake.city(),
                country = fake.country(),
                age = random.randint(18, 65),
            )
        self.stdout.write(self.style.SUCCESS('100 données fictives générées avec succès !'))
