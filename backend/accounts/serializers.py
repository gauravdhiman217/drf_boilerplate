from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import User, Roles
from .constants import GENDER


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ["id", "name", "description"]


class UserSerializer(ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Roles.objects.all(), source="role", write_only=True, required=False
    )
    role = serializers.StringRelatedField(read_only=True)
    gender = serializers.ChoiceField(choices=GENDER)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile_code",
            "mobile_no",
            "age",
            "gender",
            "profile_pic",
            "role",
            "role_id",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
            "password",
            "last_login",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {
                "default": True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_role(self, value):
        current_user = self.context["request"].user

        if value.name.lower() == "admin" and not (
            current_user.is_superuser or current_user.role.name == "admin"
        ):
            raise serializers.ValidationError(
                "Only admins or superusers can assign the admin role."
            )

        return value
