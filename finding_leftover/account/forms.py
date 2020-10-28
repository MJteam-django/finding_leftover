
from django.contrib.auth.models import User
from post.models import Store
from django.forms import ModelForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('store_name', 'store_adress', 'store_memo')