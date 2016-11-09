import datetime as d
from django.db.models import (Count, Min, Max, Sum, Avg)

from digitalmarket.mixins import LoginRequiredMixin

from billing.models import Transaction
from products.models import Product
from sellers.models import SellerAccount


# Defines methods to get common seller-related information
class SellerAccountMixin(LoginRequiredMixin, object):
    account = None
    products = []
    transactions = []

    def get_account(self):
        user = self.request.user
        accounts = SellerAccount.objects.filter(user=user)
        if accounts.exists() and accounts.count() == 1:
            self.account = accounts.first()
            return accounts.first()
        return None

    def get_products(self):
        account = self.get_account()
        products = Product.objects.filter(seller=account)
        return products

    # get ALL transactions
    def get_transactions(self):
        products = self.get_products()
        transactions = Transaction.objects.filter(product__in=products)
        return transactions

    def get_sales(self, transaction_set):
        sales = transaction_set.aggregate(Sum('price'))
        return sales['price__sum']

    def get_transactions_today(self):
        today = d.date.today()
        today_min = d.datetime.combine(today, d.time.min)
        today_max = d.datetime.combine(today, d.time.max)
        print(today, today_min, today_max)
        transactions_today = self.get_transactions().filter(timestamp__range=(today_min, today_max))
        return transactions_today

    def get_recent_transactions(self, limit=10):
        recent_transactions = self.get_transactions().order_by('-timestamp').exclude(
            pk__in=self.get_transactions_today())[:limit]
        return recent_transactions

    def get_all_sales(self):
        return self.get_sales(self.get_transactions())

    def get_sales_today(self):
        return self.get_sales(self.get_transactions_today())

    def get_sales_by_product(self):
        sales_by_product = []
        for product in self.get_products():
            product_transactions = Transaction.objects.filter(product=product)
            sales_count = product_transactions.count()
            total_sales = product_transactions.aggregate(Sum('price'))
            total_sales = total_sales['price__sum']
            if sales_count > 0:
                product_stats = (product.title, sales_count, total_sales)
                sales_by_product.append(product_stats)
        return sales_by_product
