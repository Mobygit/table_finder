from django.db import models

# Create your models here.

class Table(models.Model):
    number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} (Seats {self.capacity})"

class MenuItem(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='menu_images/')
    Description = models.TextField()

    def __str__(self):
        return self.name

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem)
    name = models.CharField(max_length=60)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    num_guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
