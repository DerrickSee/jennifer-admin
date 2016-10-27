from django.dispatch import receiver
from django.db.models.signals import post_save

from shopify_webhook.signals import products_create
from .utils import shopify
from .models import *


@receiver(products_create)
def update_product(sender, data, **kwargs):
    from core.celery import add
    add.delay(1,2)


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    if created and not instance.shopify_id:
        sp = shopify.Product({
            'title': instance.title,
            'body_html': instance.body_html,
            'handle': instance.handle,
            'product_type': instance.product_type.title,
            'published_at': None,
            'vendor': instance.vendor.name,
        })
        p = sp.save()
        Product.objects.filter(id=instance.id).update(shopify_id=sp.id)
