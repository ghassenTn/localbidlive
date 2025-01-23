from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='category_icons/', verbose_name='Icon')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='auctions.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('start_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Start Price')),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Current Price')),
                ('reserve_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Reserve Price')),
                ('start_time', models.DateTimeField(verbose_name='Start Time')),
                ('end_time', models.DateTimeField(verbose_name='End Time')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending Approval'), ('active', 'Active'), ('ended', 'Ended'), ('cancelled', 'Cancelled')], default='draft', max_length=20, verbose_name='Status')),
                ('location', models.CharField(max_length=200, verbose_name='Location')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Longitude')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auctions', to='auctions.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Auction',
                'verbose_name_plural': 'Auctions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bid',
                'verbose_name_plural': 'Bids',
                'ordering': ['-amount'],
            },
        ),
        migrations.CreateModel(
            name='AuctionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='auction_images/', verbose_name='Image')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Is Primary')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='auctions.auction')),
            ],
            options={
                'verbose_name': 'Auction Image',
                'verbose_name_plural': 'Auction Images',
            },
        ),
        migrations.CreateModel(
            name='AuctionAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Views Count')),
                ('unique_viewers', models.PositiveIntegerField(default=0, verbose_name='Unique Viewers')),
                ('max_bid', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Maximum Bid')),
                ('bids_count', models.PositiveIntegerField(default=0, verbose_name='Bids Count')),
                ('watchers_count', models.PositiveIntegerField(default=0, verbose_name='Watchers Count')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('auction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to='auctions.auction')),
            ],
            options={
                'verbose_name': 'Auction Analytics',
                'verbose_name_plural': 'Auction Analytics',
            },
        ),
    ]
