from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Order(models.Model):
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - ${self.total}"


class Item(models.Model):
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.name} (x{self.quantity})"


class CheckoutFeedback(models.Model):
    """
    NEW class for J–R User Story:
    After purchase, let user leave a short statement about checkout.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=80, blank=True)  # optional display name
    message = models.TextField()                        # short statement about checkout
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        who = self.name or (self.user.username if self.user else "Anonymous")
        return f"{who}: {self.message[:40]}"
