from django import forms
from .models import School
from Accounts.models import User


class SchoolForm(forms.ModelForm):
    staff_username = forms.CharField(max_length=150)
    staff_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = School
        fields = ['name', 'logo', 'description', 'address', 'staff_username', 'staff_password']

    def save(self, commit=True):
        school = super().save(commit=commit)

        # Create the staff user
        username = self.cleaned_data['staff_username']
        password = self.cleaned_data['staff_password']

        staff_user = User.objects.create_user(
            username=username,
            password=password,
            school=school,
            is_staff_account=True
        )

        return school
