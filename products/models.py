from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

class Availability(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    authority = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date",
                check=models.Q(start_date__lt=models.F("end_date")),
                # Optional: Add an error message for the constraint
                deferrable=models.DEFERRED,
            )
        ]






    def save(self, *args, **kwargs):
        # Update product availability when a reservation is made
        availability_objects = Availability.objects.filter(
            product=self.product,
            date__range=[self.start_date, self.end_date]
        )
        for availability in availability_objects:
            availability.is_available = False
            availability.save()
        super().save(*args, **kwargs)




