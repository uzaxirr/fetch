from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Txn

@shared_task
def save_transactions_to_db(transactions):
    txn_instances = []
    for txn in transactions:
        txn_instance = Txn(
            payer=txn['payer'],
            receiver=txn['receiver'],
            action=txn["action"],
            message=txn['message'],
            label=txn['label'],
            signature=txn['signature']
        )
        txn_instances.append(txn_instance)
    try:
        Txn.objects.bulk_create(txn_instances)
        print("Transactions poplulated into DB")
        return True
    except:
        print("Failed to populate transactions into DB")
        return False
