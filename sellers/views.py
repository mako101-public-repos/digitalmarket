import datetime as d
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormMixin

from sellers.mixins import SellerAccountMixin

from products.models import Product
from sellers.forms import NewSellerForm
from sellers.models import SellerAccount
from billing.models import Transaction


# Example of RedirectVIew in views
# https://docs.djangoproject.com/en/1.10/ref/class-based-views/base/#redirectview
class SellerProductDetailRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, pk=kwargs['pk'])
        return obj.get_absolute_url()


class SellerTransactionList(SellerAccountMixin, ListView):
    model = Transaction
    template_name = 'sellers/transaction_list_view.html'

    def get_queryset(self):
        transactions = self.get_transactions()
        return transactions


class SellerDashboard(SellerAccountMixin, FormMixin, View):
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
        account = self.get_account()
        context = {}

        # 3 possible options whe arriving to the sellers URL
        # if account does not exist, show form
        # if exists but not active, show pending
        # if exists and active, show dashboard

        # SellerAccountMixin will return account=None if no account found
        if account:

            if account.active:
                # get all seller's products and all transactions involving these products
                today = d.date.today()
                today_min = d.datetime.combine(today, d.time.min)
                today_max = d.datetime.combine(today, d.time.max)
                print(today, today_min, today_max)
                products = self.get_products()[:5]
                transactions_today = self.get_transactions().filter(timestamp__range=(today_min, today_max))
                recent_transactions = self.get_transactions().order_by('-timestamp').exclude(pk__in=transactions_today)[:5]
                context['title'] = 'Seller Dashboard'
                context['products'] = products
                context['transactions_today'] = transactions_today
                context['recent_transactions'] = recent_transactions
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

