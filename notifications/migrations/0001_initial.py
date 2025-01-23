from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_notifications', models.BooleanField(default=True, verbose_name='Email Notifications')),
                ('push_notifications', models.BooleanField(default=True, verbose_name='Push Notifications')),
                ('auction_start_reminder', models.BooleanField(default=True, verbose_name='Auction Start Reminder')),
                ('new_bid_alert', models.BooleanField(default=True, verbose_name='New Bid Alert')),
                ('outbid_alert', models.BooleanField(default=True, verbose_name='Outbid Alert')),
                ('auction_end_reminder', models.BooleanField(default=True, verbose_name='Auction End Reminder')),
                ('auction_won_notification', models.BooleanField(default=True, verbose_name='Auction Won Notification')),
                ('payment_notification', models.BooleanField(default=True, verbose_name='Payment Notification')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification_preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification Preference',
                'verbose_name_plural': 'Notification Preferences',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('auction_start', 'Auction Start'), ('new_bid', 'New Bid'), ('outbid', 'Outbid'), ('auction_end', 'Auction End'), ('auction_won', 'Auction Won'), ('payment_received', 'Payment Received'), ('auction_canceled', 'Auction Canceled')], max_length=20, verbose_name='Type')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('message', models.TextField(verbose_name='Message')),
                ('is_read', models.BooleanField(default=False, verbose_name='Is Read')),
                ('object_id', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-created_at'],
            },
        ),
    ]
