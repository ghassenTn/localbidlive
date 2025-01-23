from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, BusinessDocument


@login_required
def profile_view(request):
    """Display user profile."""
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit user profile."""
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        # Handle form submission
        profile.business_name = request.POST.get('business_name', '')
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        profile.save()
        
        messages.success(request, _('Profile updated successfully.'))
        return redirect('accounts:profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile_edit.html', context)


@login_required
def business_documents_view(request):
    """Handle business document upload and display."""
    documents = BusinessDocument.objects.filter(user=request.user)
    
    if request.method == 'POST' and request.FILES.get('document'):
        document = BusinessDocument(
            user=request.user,
            document_type=request.POST.get('document_type', ''),
            document_file=request.FILES['document']
        )
        document.save()
        messages.success(request, _('Document uploaded successfully.'))
        return redirect('accounts:business_documents')
    
    context = {
        'documents': documents,
    }
    return render(request, 'accounts/business_documents.html', context)
