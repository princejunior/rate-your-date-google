from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.shortcuts import render, redirect

######################################################################################################################

@receiver(user_signed_up)
def redirect_to_edit_profile(sender, **kwargs):
    request = kwargs.get('request')
    # Assuming your edit profile page URL is '/edit_profile/'
    return redirect('/edit_profile/')
######################################################################################################################