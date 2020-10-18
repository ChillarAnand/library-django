from django.contrib import admin


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
