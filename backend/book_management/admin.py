from django.contrib import admin

# Register your models here.


from book_management import models

admin.site.register(models.Book)
admin.site.register(models.Borrow)