# Generated migration for adding keywords field to CrawlLog

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_price_desc_product_price_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawllog',
            name='keywords',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='搜索关键词'),
        ),
    ]
