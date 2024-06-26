from modeltranslation.translator import translator, TranslationOptions
from .models import Drug, BlogPost

class DrugTranslationOptions(TranslationOptions):
    fields = ('description','price',)

class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'content','description',)

translator.register(Drug, DrugTranslationOptions)
translator.register(BlogPost, BlogPostTranslationOptions)
