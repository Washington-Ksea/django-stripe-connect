from django.shortcuts import render
from django.views.generic import TemplateView

from config.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY

import stripe

stripe.api_key = STRIPE_SECRET_KEY

def create_custom_account():
    account = stripe.Account.create(
        type="custom",
        country="JP",
        email="test@test.com"
    )
    return account

class ShopView(TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        
        print("home context!!!")
        account = create_custom_account()
        """
        ...
        "id": "acct_1F6HqzJqJdl62Rgc",        
        ...
        "type": "custom"
        """
        return context
    