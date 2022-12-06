# Harmony

For at sætte projektet op:
1. Installér Python 3.9 eller nyere: https://www.python.org/downloads/
2. Installér Python biblioteker med denne kommando: pip install django django-crispy-forms django-mobile-detect mysqlclient pillow pymemcache django-emoji-picker agora_token_builder
3. Gå ind i harmony/settings.py og instil database-indstillinger til hvad du bruger
4. Lav en fil i root mappen der hedder keys.py og put de sensitite database-informationer i den. Kald variablerne det som er angivet i settings.py
5. Kør denne kommando for at oprette databasen:  python manage.py migrate
6. Start severen med: runserver.sh for Linux, eller runserver.bat for Windows

For at oprette den første administrator-bruger:
1. Åben er terminal i projektmappen
2. Skriv python manage.py createsuperuser
3. Udfyld de angivne fælter
4. Du kan nu logge ind med den nye bruger
