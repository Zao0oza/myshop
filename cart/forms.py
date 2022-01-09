from django import forms


class CartAddProductForm(forms.Form): # форма корзины
    quantity = forms.IntegerField(min_value=1, initial=1, label='Кол-во')  # кол-во товара в заказе
    '''в заисимости от True, False update добавляет товар или обновляет его количество'''
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
    amount = forms.IntegerField() # кол-во товара в магазине

    def clean(self):  # проверет наличие достаточного кол-ва товара в магазине
        cleaned_data = super().clean()
        quantity = cleaned_data['quantity']
        amount = cleaned_data['amount']
        if quantity > amount:
            raise forms.ValidationError('недостаточно единиц товара в наличии')
