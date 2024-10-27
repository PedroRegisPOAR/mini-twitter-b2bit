from rest_framework import serializers


def create_paginated_serializer(serializer_class):
    return type(
        f"{serializer_class.__name__}Paginated",
        (serializers.Serializer,),
        dict(count=serializers.IntegerField(read_only=True),
             previous=serializers.CharField(read_only=True),
             next=serializers.CharField(read_only=True),
             results=serializer_class(many=True, read_only=True),
             )
    )
