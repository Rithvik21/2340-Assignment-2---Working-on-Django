from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Movie, Review, MoviePetition, PetitionVote

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


# Petition Views
def petition_list(request):
    """Display all movie petitions."""
    petitions = MoviePetition.objects.all()
    template_data = {"title": "Movie Petitions", "petitions": petitions}
    return render(request, "movies/petition_list.html", {"template_data": template_data})


@login_required
def petition_create(request):
    """Create a new movie petition."""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        
        if title and description:
            petition = MoviePetition.objects.create(
                title=title,
                description=description,
                created_by=request.user
            )
            messages.success(request, "Petition created successfully!")
            return redirect("petition_detail", id=petition.id)
        else:
            messages.error(request, "Please fill in all fields.")
    
    template_data = {"title": "Create Movie Petition"}
    return render(request, "movies/petition_create.html", {"template_data": template_data})


def petition_detail(request, id):
    """Display a specific petition and allow voting."""
    petition = get_object_or_404(MoviePetition, id=id)
    has_voted = petition.has_user_voted(request.user) if request.user.is_authenticated else False
    
    template_data = {
        "title": petition.title,
        "petition": petition,
        "has_voted": has_voted
    }
    return render(request, "movies/petition_detail.html", {"template_data": template_data})


@login_required
def petition_vote(request, id):
    """Vote on a petition."""
    petition = get_object_or_404(MoviePetition, id=id)
    
    if request.method == "POST":
        # Check if user already voted
        if petition.has_user_voted(request.user):
            messages.warning(request, "You have already voted on this petition.")
        else:
            PetitionVote.objects.create(petition=petition, user=request.user)
            messages.success(request, "Your vote has been recorded!")
        
        return redirect("petition_detail", id=id)
    
    return redirect("petition_detail", id=id)


@login_required
def petition_vote_ajax(request, id):
    """AJAX endpoint for voting on petitions."""
    if request.method == "POST":
        petition = get_object_or_404(MoviePetition, id=id)
        
        if petition.has_user_voted(request.user):
            return JsonResponse({"success": False, "message": "You have already voted on this petition."})
        
        PetitionVote.objects.create(petition=petition, user=request.user)
        return JsonResponse({
            "success": True, 
            "message": "Your vote has been recorded!",
            "vote_count": petition.vote_count
        })
    
    return JsonResponse({"success": False, "message": "Invalid request method."})
