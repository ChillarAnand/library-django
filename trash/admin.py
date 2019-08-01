from django.contrib import admin
from django import forms

from .models import *


class BasketAdminForm(forms.ModelForm):

    choices = Fruit.objects.filter(id__gte=2)
    choices = Fruit.objects.all()

    # basket_fruit = forms.ModelMultipleChoiceField(choices, required=False)

    class Meta:
        model = Basket
        fields = '__all__'
        # fields = ['name', 'basket_fruit']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        # self.fields['basket_fruit'].queryset = self.choices


class M2MInlineAdmin(admin.TabularInline):
    model = Basket.fruits.through
    extra = 1

    def get_queryset(self, request):
        qs = super(M2MInlineAdmin, self).get_queryset(request)
        # qs = qs.filter(id__gte=4)
        qs = qs.filter(fruit__name='apple')
        return qs


class BasketAdmin(admin.ModelAdmin):
    inlines = [M2MInlineAdmin,]
    form = BasketAdminForm

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        print('called formfield_for_manytomany')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_field_queryset(self, db, db_field, request):
        print('called get_field_queryset')
        return super().get_field_queryset(db, db_field, request)

    fieldsets = (
        ('Standard info', {
            'fields': ('name',)
        }),
    )


admin.site.register(Basket, BasketAdmin)
admin.site.register(Fruit)
