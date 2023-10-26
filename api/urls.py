from django.urls import path
from .views import TxnList, TxnView

urlpatterns = [
    path('txn/', TxnView.as_view(), name='txn-create'),
    path('txn/list/', TxnList.as_view(), name='txn-create'),
]
