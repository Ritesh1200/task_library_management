from book_management import models
from account.models import User
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'

class BorrowSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = models.Borrow
        fields = '__all__'

    def get_name(self, obj):
        book = models.Book.objects.filter(pk = obj.book.id).first()
        return book.title
    def get_email(self, obj):
        user = User.objects.filter(email = obj.user.email).first()
        return user.email