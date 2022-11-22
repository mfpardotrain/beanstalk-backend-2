from ..models import FarmVegetable, FarmVegetableOrder
from ..serializers import FarmVegetableOrderSerializer
from django.forms.models import model_to_dict


class FarmVegetableOrderValidator:
    def prepare_order(self, order):
        vegetable_orders = self.create_vegetable_orders(order)
        if not order.data_errors:
            self.validate_vegetable_orders(vegetable_orders, order)

    @staticmethod
    def validate_vegetable_orders(vegetable_orders, order):
        for vegetable_order in vegetable_orders:
            serializer = FarmVegetableOrderSerializer(data=model_to_dict(vegetable_order))
            if serializer.is_valid():
                order.vegetable_serializers.append(serializer)
            else:
                order.serializer_errors.append(serializer.errors)

    def create_vegetable_orders(self, order):
        vegetables = order.vegetables
        vegetable_orders = []
        for vegetable in vegetables:
            vegetable_obj = FarmVegetable.objects.get(id=vegetable['id'])
            vegetable_order = self.create_vegetable_order(vegetable, vegetable_obj, order.user_email)
            self.validate_vegetable_order_data(vegetable_order, vegetable_obj, order)
            if order.data_errors:
                return
            else:
                vegetable_orders.append(vegetable_order)
        return vegetable_orders

    @staticmethod
    def create_vegetable_order(vegetable, vegetable_obj, user_email):
        vegetable_order = FarmVegetableOrder(
            farm_vegetable=vegetable_obj,
            farm=vegetable_obj.farm,
            farmer=vegetable_obj.farmer,
            price=vegetable_obj.price,
            order_amount=vegetable['order_amount'],
            created_by=user_email,
            updated_by=user_email,
        )
        return vegetable_order

    def validate_vegetable_order_data(self, vegetable, vegetable_obj, order):
        if self.not_enough_available(vegetable, vegetable_obj):
            order.data_errors.append({"message": f"There is not enough available for your order of {vegetable_obj.name}"})
        if self.more_than_max_order_amount(vegetable, vegetable_obj):
            order.data_errors.append({"message": f"You ordered more than the maximum allowed {vegetable_obj.name}"})

    @staticmethod
    def not_enough_available(vegetable, vegetable_obj):
        return float(vegetable.order_amount) >= vegetable_obj.available_amount

    @staticmethod
    def more_than_max_order_amount(vegetable, vegetable_obj):
        return float(vegetable.order_amount) >= vegetable_obj.max_order_amount

    @staticmethod
    def update_available_amount(vegetable_order, vegetable_obj):
        new_amount = vegetable_obj.available_amount - vegetable_order.order_amount
        try:
            vegetable_obj.available_amount = new_amount
            vegetable_obj.save()
        except:
            f"Error when updating available amount for {vegetable_obj.name}"
