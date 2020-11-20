from rest_framework import serializers
from .models import market_time

class TimeSerializer(serializers .ModelSerializer):
    class Meta:
        model = market_time
        fields = ('id', 'country_name', 'open_time', 'status')
