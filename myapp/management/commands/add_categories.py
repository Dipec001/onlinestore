# yourapp/management/commands/add_categories.py
from django.core.management.base import BaseCommand
from myapp.models import Category

class Command(BaseCommand):
    help = 'Add initial categories to the database'

    def handle(self, *args, **kwargs):
        categories = [
            ('OTC', 'Over The Counter'),
            ('Prescription', 'Prescription'),
            ('Herbal', 'Herbal'),
            ('Vitamins', 'Vitamins'),
            ('Supplements', 'Supplements'),
            ('Homeopathic', 'Homeopathic'),
            ('Ayurvedic', 'Ayurvedic'),
            ('TCM', 'Traditional Chinese Medicine'),
            ('Nutraceuticals', 'Nutraceuticals'),
            ('Antibiotics', 'Antibiotics'),
            ('Analgesics', 'Analgesics'),
            ('Antidepressants', 'Antidepressants'),
            ('Antihistamines', 'Antihistamines'),
            ('Cardiovascular', 'Cardiovascular'),
            ('Diabetes', 'Diabetes'),
            ('Gastrointestinal', 'Gastrointestinal'),
            ('Dermatological', 'Dermatological'),
            ('Respiratory', 'Respiratory'),
            ('Neurological', 'Neurological'),
            ('Oncology', 'Oncology'),
            ('Endocrine', 'Endocrine'),
            ('Pediatric', 'Pediatric'),
            ('Geriatric', 'Geriatric'),
            ('WomensHealth', "Women's Health"),
            ('MensHealth', "Men's Health"),
            ('Ophthalmic', 'Ophthalmic'),
            ('Dental', 'Dental'),
            ('Veterinary', 'Veterinary'),
        ]

        for code, name in categories:
            Category.objects.get_or_create(code=code, name=name)
        self.stdout.write(self.style.SUCCESS('Successfully added categories'))
