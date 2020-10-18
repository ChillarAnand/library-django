from django import forms
from django.contrib import admin

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

class DynamicLookupMixin(object):
    '''
    a mixin to add dynamic callable attributes like 'book__author' which
    return a function that return the instance.books.author value
    '''

    def __getattr__(self, attr):
        if ('__' in attr
            and not attr.startswith('_')
            and not attr.endswith('_boolean')
            and not attr.endswith('_short_description')):

            def dyn_lookup(instance):
                # traverse all __ lookups
                return reduce(lambda parent, child: getattr(parent, child),
                              attr.split('__'),
                              instance)

            # get admin_order_field, boolean and short_description
            dyn_lookup.admin_order_field = attr
            dyn_lookup.boolean = getattr(self, '{}_boolean'.format(attr), False)
            dyn_lookup.short_description = getattr(
                self, '{}_short_description'.format(attr),
                attr.replace('_', ' ').capitalize())

            return dyn_lookup

        # not dynamic lookup, default behaviour
        return self.__getattribute__(attr)


# admin.site.register(Basket, BasketAdmin)
# admin.site.register(Fruit)
