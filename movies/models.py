from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return self.name


class Review(models.Model):
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} on {self.movie.name}"


class MoviePetition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def vote_count(self):
        return self.votes.count()
    
    def has_user_voted(self, user):
        if not user.is_authenticated:
            return False
        return self.votes.filter(user=user).exists()


class PetitionVote(models.Model):
    petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['petition', 'user']
    
    def __str__(self):
        return f"{self.user.username} voted for {self.petition.title}"
