class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'password', 'password2',
            'phone', 'blood_group', 'location_name'
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_phone(self, value):
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone already exists.")
        return value

    def validate(self, data):
        if data.get('password') != data.pop('password2', None):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def _geocode_location(self, location_name):
        if not location_name:
            return None, None

        try:
            geolocator = Nominatim(user_agent="bloodlink_app")
            location = geolocator.geocode(location_name, timeout=5)

            if location:
                return location.latitude, location.longitude

        except Exception as e:
            print("Geocoding error:", str(e))  # 👈 DEBUG

        return None, None

    def create(self, validated_data):
        location_name = validated_data.get('location_name')

        latitude, longitude = self._geocode_location(location_name)

        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                phone=validated_data.get('phone'),
                blood_group=validated_data.get('blood_group'),
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
            )

            return user

        except IntegrityError as e:
            print("Integrity error:", str(e))  # 👈 DEBUG
            raise serializers.ValidationError({"error": str(e)})

        except Exception as e:
            print("User creation error:", str(e))  # 👈 MOST IMPORTANT
            raise serializers.ValidationError({"error": str(e)})