from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Review

def index(request):
    search_term = request.GET.get("search")
    movies = Movie.objects.filter(name__icontains=search_term) if search_term else Movie.objects.all()
    template_data = {"title": "Movies", "movies": movies}
    return render(request, "movies/index.html", {"template_data": template_data})

def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie).select_related("user")
    template_data = {"title": movie.name, "movie": movie, "reviews": reviews}
    return render(request, "movies/show.html", {"template_data": template_data})

@login_required
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == "POST":
        comment = (request.POST.get("comment") or "").strip()
        if comment:
            Review.objects.create(movie=movie, user=request.user, comment=comment)
    return redirect("movies_show", id=id)

@login_required
def edit_review(request, id, review_id):
    movie = get_object_or_404(Movie, id=id)
    review = get_object_or_404(Review, id=review_id, movie=movie, user=request.user)
    if request.method == "GET":
        template_data = {"title": "Edit Review", "review": review, "movie": movie}
        return render(request, "movies/edit_review.html", {"template_data": template_data})
    comment = (request.POST.get("comment") or "").strip()
    if comment:
        review.comment = comment
        review.save()
    return redirect("movies_show", id=id)

@login_required
def delete_review(request, id, review_id):
    movie = get_object_or_404(Movie, id=id)
    review = get_object_or_404(Review, id=review_id, movie=movie, user=request.user)
    review.delete()
    return redirect("movies_show", id=id)
