from modeltranslation.translator import translator, TranslationOptions
from .models import Drug

class DrugTranslationOptions(TranslationOptions):
    fields = ('description',)

translator.register(Drug, DrugTranslationOptions)
