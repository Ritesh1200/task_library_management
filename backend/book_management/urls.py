from django.urls import path
from book_management import views


urlpatterns = [
    path('book/', views.Book.as_view(), name="book"),
    path('borrow_book/', views.Borrow.as_view(), name="borrow"),
    path('renew/', views.Renew.as_view(), name="renew"),
    path('returned/', views.Returned.as_view(), name="returned"),
]