from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormMixin

from products.mixins import LoginRequiredMixin
from sellers.forms import NewSellerForm
from sellers.models import SellerAccount


# Create your views here.
class SellerDashboard(LoginRequiredMixin, FormMixin, View):
    form_class = NewSellerForm
    success_url = '/seller/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        apply_form = self.get_form()  # NewSellerForm()
        account = SellerAccount.objects.filter(user=self.request.user)
        context = {}

        # 3 possible options whe arriving to the sellers URL
        # if account does not exist, show form
        # if exists but not active, show pending
        # if exists and active, show dashboard

        if account.exists():
            account = account.first()
            active = account.active

            if active:
                context['title'] = 'Seller Dashboard'
            # i.e. if not approved
            else:
                context['title'] = 'Account Pending Approval'

        # if account does not exist
        else:
            context['title'] = 'Register a New Seller Account'
            context['apply_form'] = apply_form

        return render(request, 'sellers/dashboard.html', context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        print('Working')
        print(valid_data)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data

