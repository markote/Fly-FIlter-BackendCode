from rest_framework import serializers



class SerializerForm(serializers.Serializer):
    """
        Save a form
    """
    form_response = serializers.DictField(required=False)

    def create(self, validated_data):
        return validated_data

class SerializerFormSelector(serializers.Serializer):
    """
        Selector of a type
    """
    user_id = serializers.CharField(required=True)

    def create(self, validated_data):
        return validated_data