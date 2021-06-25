from django.forms import ModelForm, forms

from app.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password']
        labels = {
            'name': '用户名',
            'password': '密码'
        }

    def clean_name(self):
        name = self.cleaned_data.get('username')
        form = User.objects.filter(name=name).first()
        if form:
            raise forms.ValidationError('用户名已存在')
        else:
            return name

    def clean(self):
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')
        if password and repassword and password != repassword:
            raise forms.ValidationError('两次密码输入不一致')
        else:
            return self.cleaned_data
