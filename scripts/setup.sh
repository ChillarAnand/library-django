#! /bin/bash

export DJANGO_SETTINGS_MODULE=library.settings.dev

./manage.py makemigrations
./manage.py migrate

# ./manage.py createsuperuser --username f --email 'f@f.com' --noinput
# echo "from django.contrib.auth.models import User; u = User.objects.get(username='f'); u.set_password('f')" | python manage.py shell

# echo "from django.contrib.auth.models import User; User.objects.filter(username='f').delete(); User.objects.create_superuser('f', 'f@f.com', 'f')" | python manage.py shell


USER="f"
PASS="f"
MAIL="f@f.com"
script="
from django.contrib.auth.models import User;

username = '$USER';
password = '$PASS';
email = '$MAIL';

u, _ = User.objects.get_or_create(username=username);
u.set_password(password);
u.is_staff = True;
u.is_superuser = True;
u.save();
print('Superuser created.');
"
printf "$script" | python manage.py shell
