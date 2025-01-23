from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(blank=True, max_length=100, verbose_name='Business Name')),
                ('is_business', models.BooleanField(default=False, verbose_name='Is Business')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name='Phone Number')),
                ('address', models.TextField(blank=True, verbose_name='Address')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='BusinessDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=50, verbose_name='Document Type')),
                ('document_file', models.FileField(upload_to='business_documents/', verbose_name='Document File')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Is Verified')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Uploaded At')),
                ('verified_at', models.DateTimeField(blank=True, null=True, verbose_name='Verified At')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_documents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Business Document',
                'verbose_name_plural': 'Business Documents',
            },
        ),
    ]
