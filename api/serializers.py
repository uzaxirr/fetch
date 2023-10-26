from rest_framework import serializers
from api.models import Txn

class TxnSerializer(serializers.Serializer):
    payer = serializers.CharField(max_length=520)
    receiver = serializers.CharField(max_length=520)
    action = serializers.JSONField()
    message = serializers.CharField(max_length=520)
    label = serializers.CharField(max_length=520)
    signature = serializers.CharField(max_length=520)

    def create(self, validated_data):
        return Txn.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.payer = validated_data.get('payer', instance.payer)
        instance.receiver = validated_data.get('receiver', instance.receiver)
        instance.action = validated_data.get('actions', instance.actions)
        instance.message = validated_data.get('message', instance.message)
        instance.label = validated_data.get('label', instance.label)
        instance.signature = validated_data.get('signature', instance.signature)
        instance.save()
        return instance
