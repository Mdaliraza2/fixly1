from rest_framework import serializers
from .models import Review
from registration.models import User

from rest_framework import serializers
from .models import Review
from registration.models import User  

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'service_provider']
        read_only_fields = ['id']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_service_provider(self, value):
        if value.user_type != 'SERVICE_PROVIDER':
            raise serializers.ValidationError("You can only review service providers.")
        return value

    def validate(self, data):
        user = self.context['user']
        service_provider = data.get('service_provider')

        if service_provider == user:
            raise serializers.ValidationError({"service_provider": "You cannot review yourself."})

        if Review.objects.filter(reviewer=user, service_provider=service_provider).exists():
            raise serializers.ValidationError({"non_field_errors": ["You have already reviewed this service provider."]})

        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['user']
        return super().create(validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    provider_name = serializers.CharField(source='service_provider.get_full_name', read_only=True)
    provider_email = serializers.EmailField(source='service_provider.email', read_only=True)
    service_category = serializers.CharField(source='service_provider.category.category', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer_name', 'provider_name', 'provider_email',
            'service_category', 'rating', 'comment', 'created_at'
        ]
