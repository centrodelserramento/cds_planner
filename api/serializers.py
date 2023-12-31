from rest_framework import serializers


try:
    from home.models import Order

except:
    pass


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        try:
            model = Order
        except:
            pass
        fields = "__all__"
