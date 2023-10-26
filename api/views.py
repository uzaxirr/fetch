from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.decorators import throttle_classes
from .serializers import TxnSerializer
from .models import Txn
from django.utils.decorators import method_decorator

from rest_framework.pagination import PageNumberPagination
from .tasks import save_transactions_to_db

class TransactionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@throttle_classes([ScopedRateThrottle])
class TxnView(APIView):
    throttle_scope = 'custom'

    def post(self, request):
        serializer = TxnSerializer(data=request.data, many=True)
        if serializer.is_valid():
            save_transactions_to_db.delay(serializer.validated_data)
            return Response({"message": "Task started successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@throttle_classes([ScopedRateThrottle])
class TxnList(APIView):
    throttle_scope = 'custom'

    @method_decorator(cache_page(300, key_prefix="txn-"))
    def get(self, request, *args, **kwargs):
        transactions = Txn.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        serializer = TxnSerializer(paginated_transactions, many=True)
        return paginator.get_paginated_response(serializer.data)
