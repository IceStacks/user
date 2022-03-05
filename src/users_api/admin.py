from django import forms
from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name',
            'gender', 'country', 'town', 'address',
            'phone_number', 'identity_number','birth_date',
            'is_active', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        
        fields = ('email', 'first_name', 'last_name',
                    'gender', 'country', 'town', 'address',
                    'phone_number', 'identity_number','birth_date',
                    'password', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    # I couldn't make it. Returns None type.
    # def __init__(self, *args, **kwargs):
    #     is_staff = kwargs.pop('is_staff', None)
    #     print(is_staff)
    #     super(UserChangeForm, self).__init__(*args, **kwargs)
    #     if is_staff:
    #         self.fields = ('email', 'password', 'is_active', 'is_staff', 'is_superuser')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    #staff users can't see superuser and other staff users
    #consider another solution.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False, is_staff=False)

    #staff users can't give permission to other staff users
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ()

        return [(None, {'fields': ('email', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'country',
                 'town', 'address', 'phone_number', 'identity_number','birth_date')}),
                (('Permissions'), {'fields': perm_fields}),
                ]
            
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'country',
    #      'town', 'address', 'phone_number', 'identity_number','birth_date')}),
    #     ('Permissions', {'fields': ('groups', 'user_permissions', 'is_staff', 'is_superuser', 'is_active')}),
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Permission)
admin.site.register(Session)
admin.site.register(LogEntry)

