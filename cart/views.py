from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item

def index(request):
    cart = request.session.get('cart', {})
    movie_ids = [int(k) for k in cart.keys()]
    movies = []
    cart_total = 0
    if movie_ids:
        movies = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies)
    template_data = {
        "title": "Cart",
        "movies": movies,
        "cart_total": cart_total,
    }
    return render(request, "cart/index.html", {"template_data": template_data})

def add(request, id):
    if request.method != "POST":
        return redirect("movies_show", id=id)
    get_object_or_404(Movie, id=id)
    try:
        qty = int(request.POST.get("quantity", "1"))
    except ValueError:
        qty = 1
    if qty < 1:
        qty = 1
    cart = request.session.get("cart", {})
    key = str(id)
    cart[key] = cart.get(key, 0) + qty
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart_index")

def clear(request):
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("cart_index")

@login_required
def purchase(request):
    cart = request.session.get("cart", {})
    movie_ids = [int(k) for k in cart.keys()]
    if not movie_ids:
        return redirect("cart_index")
    movies = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies)
    order = Order.objects.create(user=request.user, total=cart_total)
    for movie in movies:
        Item.objects.create(
            movie=movie,
            price=movie.price,
            order=order,
            quantity=int(cart[str(movie.id)]),
        )
    request.session["cart"] = {}
    request.session.modified = True
    template_data = {
        "title": "Purchase confirmation",
        "order_id": order.id,
    }
    return render(request, "cart/purchase.html", {"template_data": template_data})
