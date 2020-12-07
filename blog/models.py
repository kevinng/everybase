from common.models import Choice
from leads.models import Supply, Demand

from django.db import models

from wagtail.core.models import Page, Orderable, ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.search import index

class BlogIndexPage(Page):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname='full')
    ]

class BlogCategoryPage(Page):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname='full')
    ]

class BlogTag(Choice):
    pass

class BlogCategory(Choice):
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        related_query_name='children',
        null=True,
        blank=True,
        db_index=True
    )

class BlogPage(Page):
    introduction = RichTextField(blank=True)
    body = RichTextField(blank=True)

    tags = models.ManyToManyField(
        'BlogTag',
        related_name='pages',
        related_query_name='pages',
        db_index=True
    )
    categories = models.ManyToManyField(
        'BlogCategory',
        related_name='pages',
        related_query_name='pages',
        db_index=True
    )

    supplies = models.ManyToManyField(
        'leads.Supply',
        related_name='pages',
        related_query_name='pages',
        db_index=True
    )
    demands = models.ManyToManyField(
        'leads.Demand',
        related_name='pages',
        related_query_name='pages',
        db_index=True
    )

class BlogImage(Orderable):
    page = ParentalKey(
        BlogPage,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        related_name='images'
    )
    caption = models.CharField(
        blank=True,
        max_length=300
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]

class BlogDocument(Orderable):
    page = ParentalKey(
        BlogPage,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.SET_NULL,
        null=True,
        related_name='images'
    )
    caption = models.CharField(
        blank=True,
        max_length=300
    )

    panels = [
        DocumentChooserPanel('document'),
        FieldPanel('caption')
    ]
