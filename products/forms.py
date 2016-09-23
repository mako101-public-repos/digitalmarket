from django import forms

AVILABILITY_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

class ProductAddForm(forms.Form):
    title = forms.CharField(label='Product Title')
    description = forms.CharField(widget=forms.Textarea)  # this may be a problem
    price = forms.DecimalField()
    # available = forms.ChoiceField(choices=AVILABILITY_CHOICES)  # default option is drop-down menu
    is_available = forms.ChoiceField(label='Is available for sale',
        widget=forms.RadioSelect, choices=AVILABILITY_CHOICES, initial=True)  # initial is the default value!

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 1:
            raise forms.ValidationError('Price must be higher than $1')
        elif price >= 100:
            raise forms.ValidationError('Price must be less than $100')
        else:
            return price

    # this function HAS to be called clean_(valid attribute name) or it doesnt apply!
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be 5 characters or longer')
        else:
            return title



