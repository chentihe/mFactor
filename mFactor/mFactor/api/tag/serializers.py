from rest_framework import serializers

from mFactor.api.tag.models import Tag

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag

        def to_representation(self, instance):
            return instance.name