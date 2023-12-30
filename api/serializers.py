from rest_framework import serializers


try:

    from home.models import Product
    from home.models import Order

except:
    pass 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:

        try:
            model = Product
        except:
            pass    
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:

        try:
            model = Order
        except:
            pass    
        fields = '__all__'

