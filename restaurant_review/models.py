from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField("review date")

    def __str__(self):
        return f"{self.restaurant.name} ({self.review_date:%x})"


from django.db import models
from django.utils import timezone


class SMS(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    twilio_number = models.CharField(max_length=20, blank=True, null=True)
    sms_body = (models.TextField(),)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"


class Message(models.Model):
    sms = models.ForeignKey(
        SMS, on_delete=models.CASCADE, related_name="messages_received"
    )
    content = models.TextField()
    direction = models.CharField(
        max_length=10,
        choices=[("incoming", "Incoming"), ("outgoing", "Outgoing")],
    )
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["timestamp"]


class Post(models.Model):
    sms = models.ForeignKey(SMS, on_delete=models.CASCADE, related_name="posts")
    url = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)  # New title field
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.sms} - {self.timestamp}"


class WelcomeGreeting(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:50]
