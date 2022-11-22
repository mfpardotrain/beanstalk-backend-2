from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create(self, email, username, first_name, last_name, farm, is_farmer, is_customer, primary_phone,
               address, is_staff, is_superuser, is_notifiable, created_by, updated_by, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            farm=farm,
            is_farmer=is_farmer,
            is_customer=is_customer,
            primary_phone=primary_phone,
            address=address,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_notifiable=is_notifiable,
            created_by=created_by,
            updated_by=updated_by
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Farm(models.Model):
    name = models.CharField(max_length=200, default="Default Farm Name")
    address = models.CharField(max_length=100, blank=True)
    stripe_account_id = models.CharField(max_length=1000, blank=True)
    is_registered = models.BooleanField(default=False)
    min_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)
    def __str(self):
        return str(self.name)


# This model represents the user. A FarmBoy can be a farmer, a user, or both
# which is based on the is_farmer/is_customer flags
class FarmBoy(AbstractBaseUser):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=30, unique=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_farmer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_notifiable = models.BooleanField(default=False)
    primary_phone = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)

    def __str(self):
        return str(self.email)


# This model associates vegetables to farms
class FarmVegetable(models.Model):
    farmer = models.ForeignKey(FarmBoy, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit_weight = models.CharField(default="lb", max_length=5)
    max_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=99999)
    available_amount = models.DecimalField(max_digits=8, decimal_places=2, default=99999)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)

    def __str(self):
        return str(self.name) + " from the farm: " + str(self.farm)


class Market(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    cron_string = models.CharField(max_length=100)
    end_cron_string = models.CharField(max_length=100)
    market_duration_minutes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    farms = models.ManyToManyField(Farm, blank=True)
    description = models.CharField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)

    def __str(self):
        return str(self.name) + str(self.address)


class MarketInfo(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=False)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=False)
    farmer = models.ForeignKey(FarmBoy, on_delete=models.CASCADE)
    farm_vegetables = models.ManyToManyField(FarmVegetable, blank=True)
    cron_string = models.CharField(max_length=100)
    end_cron_string = models.CharField(max_length=100)
    market_duration_minutes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)

    def __str(self):
        return str(self.market.name) + str(self.farm.name) + str(self.cron_string)


class CustomOrderManager(models.Manager):
    def custom_query(self, query, farmer=False, customer=False):
        from django.db import connection

        query_end = "farmer_id=" + str(farmer) if farmer else "customer_id=" + str(customer)

        if query is False:
            query_string = ""
        else:
            query_string = [k + '=' + '\'' + v + '\'' + ' and ' for k, v in query.items()]
            query_string = ''.join(query_string)

        with connection.cursor() as cursor:
            cursor.execute(f""" SELECT * FROM api_Order WHERE {query_string}{query_end}""")
            output = cursor.fetchall()
        return output

    def get_all_paid_complete_orders(self, farmer=False, customer=False):
        from django.db import connection
        query_end = "farmer_id=" + str(farmer) if farmer else "customer_id=" + str(customer)

        with connection.cursor() as cursor:
            cursor.execute(f""" SELECT * FROM api_Order WHERE 
                                status in ('paid', 'complete') and 
                                order_type = 'order' and
                                {query_end}
                            """)
            output = cursor.fetchall()
        return output

    def get_upcoming_paid_complete_orders(self, farmer=False, customer=False):
        from django.db import connection
        query_end = "farmer_id=" + str(farmer) if farmer else "customer_id=" + str(customer)

        with connection.cursor() as cursor:
            cursor.execute(f""" SELECT * FROM api_Order WHERE 
                                status in ('paid', 'complete') and 
                                order_type = 'order' and
                                market_pickup_date = ( 
                                    select market_pickup_date 
                                    from api_order
                                    where market_pickup_date >= CURRENT_DATE
                                    order by CAST(market_pickup_date as date) - 
                                    CAST(CURRENT_DATE as date) limit 1) 
                                and {query_end}
                            """)
            output = cursor.fetchall()
        return output


# This model associates vegetables to farms
class FarmVegetableOrder(models.Model):
    farm_vegetable = models.ForeignKey(FarmVegetable, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True)
    farmer = models.ForeignKey(FarmBoy, on_delete=models.CASCADE)
    price = models.IntegerField()
    order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=99999)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)

    def __str(self):
        return str(self.farm_vegetable) + ": " + str(self.order_amount) + " for $" + str(self.price)


class Order(models.Model):
    market_info = models.ForeignKey(MarketInfo, on_delete=models.CASCADE, null=True)
    farmer = models.ForeignKey(FarmBoy, related_name='farmer', on_delete=models.CASCADE)
    customer = models.ForeignKey(FarmBoy, related_name='customer', on_delete=models.CASCADE)
    farm_vegetables = models.ManyToManyField(FarmVegetableOrder)
    status = models.CharField(max_length=20)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True)
    market_pickup_date = models.DateTimeField(auto_now=False, null=True)
    amount = models.PositiveIntegerField()
    fee = models.PositiveIntegerField()
    stripe_checkout_session_id = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)

    custom_query = CustomOrderManager()
    objects = models.Manager()

    def __str(self):
        return str(self.id)

