from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from book_management import models, serializers


# Create your views here.

class Book(generics.ListCreateAPIView):
    queryset = models.Book.objects.all().order_by('-created_at')
    serializer_class = serializers.BookSerializer

    def create(self, request, *args, **kwargs):
        print(request.user)
        if not request.user.is_superuser:
            return Response({"error":"only librarian can add book"}, status=403)
        title = request.data.get("title", None)
        available_copy = request.data.get("available_copy", None)
        if not title or not available_copy:
            return Response({"error":"title and available_copy is maindatory"}, status=400)
        book = models.Book.objects.filter(title = title).first()
        if book:
            return Response({"error":"title is already taken"}, status=400)
        return super().create(request, *args, **kwargs)

class Borrow(generics.ListCreateAPIView):
    queryset = models.Borrow.objects.all()
    serializer_class = serializers.BorrowSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            borrow_data = models.Borrow.objects.all()
        else:
            borrow_data = models.Borrow.objects.filter(user= request.user.id)
        borrow_serial = serializers.BorrowSerializer(borrow_data, many = True)
        return Response(borrow_serial.data, status=200)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser:
            return Response({"data":"","error":"User is not Librarian"}, status=400)
        data = request.data
        book = data.get("book", None)
        user = data.get("user", None)
        if not book or not user:
            return Response({"data":"","error":"book and user are required"}, status=400)

        push_data = {
            "book":book,
            "user":user
        }
        book_data = models.Book.objects.filter(pk= book).first()
        if book_data:
            if not book_data.available_copy > 0:
                return Response({"data":"","error":"Book is out of stock."}, status=401)
        else:
            return Response({"data":"","error":"Book not found."}, status=402)
        user_borrows_count = models.Borrow.objects.filter(user = request.user.id, returned= False).count()
        if user_borrows_count >= 10:
            return Response({"data":"","error":"User can borrow up to 10 books only."}, status=403)
        borrowserial = serializers.BorrowSerializer(data= push_data)
        borrowserial.is_valid(raise_exception=True)
        borrowserial.save()
        models.Book.objects.filter(pk= book).update(available_copy= book_data.available_copy -1)
        return Response({"data":borrowserial.data,"error":""}, status=201)

class Renew(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        data = request.data
        borrow_id = data.get("borrow_id", None)
        renew = data.get("renew", None)
        if not borrow_id or not renew:
            return Response({"data":"","error":"Please provide renew and borrow id"}, status=400)

        borrow = models.Borrow.objects.filter(pk = borrow_id).first()
        if not borrow:
            return Response({"data":"","error":"Borrow data not present"}, status=400)
        if renew == "true":
            return Response({"data":"","error":"Borrow is already renew once"}, status=400)
        borrow_serial = serializers.BorrowSerializer(borrow, data = {"renew": True},  partial=True)
        borrow_serial.is_valid(raise_exception=True)
        borrow_serial.save()
        return Response({"data":borrow_serial.data,"error":""}, status=201)

class Returned(APIView):
    def patch(self, request):
        user = request.user
        if not user or not user.is_superuser:
            return Response({"data":"","error":"Please login as librarian"}, status=400)
        data = request.data
        borrow_id = data.get("borrow_id", None)
        if not borrow_id:
            return Response({"data":"","error":"Please provide borrow id"}, status=400)

        borrow = models.Borrow.objects.filter(pk = borrow_id).first()
        if not borrow:
            return Response({"data":"","error":"Borrow data not present"}, status=400)
        if borrow.returned == True:
            return Response({"data":"","error":"Book is already returned"}, status=400)
        borrow_serial = serializers.BorrowSerializer(borrow, data = {"returned": True},  partial=True)
        borrow_serial.is_valid(raise_exception=True)
        borrow_serial.save()
        models.Book.objects.filter(pk = borrow.book.pk).update(available_copy = borrow.book.available_copy +1)
        return Response({"data":borrow_serial.data,"error":""}, status=201)