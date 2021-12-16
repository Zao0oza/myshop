from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label='Кол-во')
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
    amount = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data['quantity']
        amount = cleaned_data['amount']
        if quantity > amount:
            raise forms.ValidationError('недостаточно единиц товара в наличии')


    def __init__(self, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'