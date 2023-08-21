from django.db import models


class Brend(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Product(models.Model):
    SEASON_CHOICES = (
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
    )

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='товар активен')
    quantity = models.PositiveIntegerField(default=0)
    vendor = models.IntegerField(unique=True)
    dimensions = models.ManyToManyField(Size)
    colors = models.ManyToManyField(Color)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brend, on_delete=models.CASCADE)
    season = models.CharField(choices=SEASON_CHOICES, max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукции'


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name
