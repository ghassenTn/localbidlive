from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    business_name = models.CharField(_('Business Name'), max_length=100, blank=True)
    is_business = models.BooleanField(_('Is Business'), default=False)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True)
    address = models.TextField(_('Address'), blank=True)
    latitude = models.DecimalField(_('Latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return self.user.username


class BusinessDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_documents')
    document_type = models.CharField(_('Document Type'), max_length=50)
    document_file = models.FileField(_('Document File'), upload_to='business_documents/')
    is_verified = models.BooleanField(_('Is Verified'), default=False)
    uploaded_at = models.DateTimeField(_('Uploaded At'), auto_now_add=True)
    verified_at = models.DateTimeField(_('Verified At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Business Document')
        verbose_name_plural = _('Business Documents')

    def __str__(self):
        return f"{self.user.username} - {self.document_type}"
