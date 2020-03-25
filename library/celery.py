from celery import Celery

app = Celery(broker='amqp://guest@localhost//')
app.conf.update(
    result_backend='django-db',
    result_backend_db='db+postgresql://test:test@localhost:5432/test')


@app.task()
def add(x, y):
    return x + y


from django.contrib.admin.actions import delete_selected
from django.contrib.admin.sites import site
import object_tools


class Delete(object_tools.ObjectTool):
    name = 'delete'
    label = 'Delete all'

    def view(self, request, extra_context=None):
        queryset = self.model.objects.all()
        modeladmin = site._registry.get(self.model)
        response = delete_selected(modeladmin, request, queryset)
        if response:
            return response
        else:
            return modeladmin.changelist_view(request)


object_tools.tools.register(Delete)
