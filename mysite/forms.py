from django import forms

from .models import *


class Login(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=12,
        widget=forms.TextInput(attrs={"class": "form-control required", "placeholder": "Username"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=15,
        widget=forms.PasswordInput(attrs={"class": "form-control required", "placeholder": "Password"}),
    )

class Edit(forms.ModelForm):
    class Meta:
        model = User
        fields = ["password", "name", "email", "phone"]
        labels = {
            "password": "密码",
            "name": "昵称",
            "email": "邮箱",
            "phone": "手机号码",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "YourName"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone": forms.NumberInput(attrs={"class": "form-control", "placeholder": "YourPhone"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
        }

        # def clean_name(self):
        #     name = self.cleaned_data.get("name")
        #     result = User.objects.filter(name=name)
        #     if result:
        #         raise form.ValidationError("Name already exists")
        #     return name


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    email = forms.EmailField(
        label="邮箱", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password1 = forms.CharField(
        label="密码",
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )
    name = forms.CharField(
        label="姓名",
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "YourName"}),
    )
    phone = forms.CharField(
        label="手机",
        max_length=128,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "YourPhone"}),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 1:
            raise forms.ValidationError(
                "Your username must be at least 6 characters long."
            )
        elif len(username) > 50:
            raise forms.ValidationError("用户名太长啦")
        else:
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("用户名已存在")
        return username

    def clean_name(self):
        name = self.cleaned_data.get("name")
        filter_result = User.objects.filter(name=name)
        if len(filter_result) > 0:
            raise forms.ValidationError("名字已存在")
        return name

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("密码太短啦")
        elif len(password1) > 20:
            raise forms.ValidationError("密码太长啦.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码输入不匹配，请再输入一次")
        return password2
