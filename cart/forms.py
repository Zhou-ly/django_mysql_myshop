from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    '''
    quantity：限制用户选择的数量为1-20个。使用TypedChoiceField字段，并且设置coerce=int，将输入转换为整型字段。
    update：用于指定当前数量是增加到原有数量（False）上还是替代原有数量（True），把这个字段设置为HiddenInput，因为我们不需要用户看到这个字段
    '''
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
