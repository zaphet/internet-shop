## Установка:
### - python manage.py migrate
для удобства - в проекте лежит пустая база со сгенерированными настройками. Если хотите создать базу с нуля - то для первой миграции потребуется в the_shop/app_shop/admin.py закомментить __init__ в SiteSettingsAdmin.

### - python manage.py loaddata demo_base.json
заполнит базу демонстрационными данными.

	login: superuser 	password: super12345678
	login: admin 		password: admin12345678
	login: test1		password: test12345678
	login: test2		password: test12345678


###  - python manage.py runserver


также базу товаров можно заполнить случайными данными при помощи комманды:

###  - python manage.py fill_base