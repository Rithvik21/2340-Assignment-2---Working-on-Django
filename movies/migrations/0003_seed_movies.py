from django.db import migrations

def reset_and_seed_movies(apps, schema_editor):
    Movie = apps.get_model("movies", "Movie")

    # Clear out existing movies
    Movie.objects.all().delete()

    # Insert the new set
    movies = [
        {
            "name": "The Batman",
            "price": 12,
            "description": "A gritty detective take on Gotham’s Dark Knight.",
            "image": "movie_images/batman.jpeg",
        },
        {
            "name": "Fantastic Four",
            "price": 11,
            "description": "Marvel’s first family prepares for launch.",
            "image": "movie_images/fantastic_four.jpeg",
        },
        {
            "name": "Joker",
            "price": 10,
            "description": "Arthur Fleck descends into madness in Gotham City.",
            "image": "movie_images/joker.jpeg",
        },
        {
            "name": "Mission: Impossible",
            "price": 9,
            "description": "Ethan Hunt undertakes an impossible covert mission.",
            "image": "movie_images/Mission_Impossible.jpeg",
        },
        {
            "name": "Oppenheimer",
            "price": 14,
            "description": "The story of J. Robert Oppenheimer and the atomic age.",
            "image": "movie_images/Oppenheimer.jpeg",
        },
        {
            "name": "Superman",
            "price": 13,
            "description": "The Man of Steel returns to protect Metropolis.",
            "image": "movie_images/superman.jpeg",
        },
    ]
    for m in movies:
        Movie.objects.create(**m)

def unseed_movies(apps, schema_editor):
    Movie = apps.get_model("movies", "Movie")
    Movie.objects.filter(
        name__in=[
            "The Batman",
            "Fantastic Four",
            "Joker",
            "Mission: Impossible",
            "Oppenheimer",
            "Superman",
        ]
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_review'),  # adjust if your last migration has a different name
    ]

    operations = [
        migrations.RunPython(reset_and_seed_movies, unseed_movies),
    ]
