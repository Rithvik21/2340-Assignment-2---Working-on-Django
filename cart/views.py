from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from movies.models import Movie
from .models import Order, Item, CheckoutFeedback
from .forms import CheckoutFeedbackForm

# --- your existing helpers (example) ---
def _get_cart(request):
    return request.session.get("cart", {})

def _set_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True

def calculate_cart_total(cart):
    # cart: {"<movie_id>": "qty"}
    total = 0
    ids = [int(mid) for mid in cart.keys()]
    for m in Movie.objects.filter(id__in=ids):
        qty = int(cart[str(m.id)])
        total += m.price * qty
    return total

# --- your existing views (index/add/clear/etc.) stay the same ---

def index(request):
    """Display the shopping cart."""
    cart = _get_cart(request)
    ids = [int(mid) for mid in cart.keys()]
    movies = Movie.objects.filter(id__in=ids)
    
    # Add quantity to each movie
    for movie in movies:
        movie.quantity = int(cart[str(movie.id)])
        movie.subtotal = movie.price * movie.quantity
    
    total = calculate_cart_total(cart)
    
    template_data = {
        "title": "Shopping Cart",
        "movies": movies,
        "total": total
    }
    return render(request, "cart/index.html", {"template_data": template_data})

def add(request, id):
    """Add a movie to the cart."""
    movie = get_object_or_404(Movie, id=id)
    cart = _get_cart(request)
    
    movie_id = str(movie.id)
    if movie_id in cart:
        cart[movie_id] = str(int(cart[movie_id]) + 1)
    else:
        cart[movie_id] = "1"
    
    _set_cart(request, cart)
    messages.success(request, f"{movie.name} added to cart!")
    return redirect("movies_index")

def clear(request):
    """Clear the shopping cart."""
    _set_cart(request, {})
    messages.info(request, "Cart cleared!")
    return redirect("cart_index")

@login_required
def purchase_success(request, order_id):
    """Display purchase success page with survey modal."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    form = CheckoutFeedbackForm()
    
    template_data = {
        "title": "Purchase Successful",
        "order": order,
        "form": form
    }
    return render(request, "cart/purchase_success", {"template_data": template_data})

@login_required
@transaction.atomic
def purchase(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart_index")

    # Create order
    total = calculate_cart_total(cart)
    order = Order.objects.create(user=request.user, total=total)

    # Create items
    ids = [int(mid) for mid in cart.keys()]
    movies = {m.id: m for m in Movie.objects.filter(id__in=ids)}
    for mid, qty_str in cart.items():
        mid_int = int(mid)
        Item.objects.create(
            order=order,
            movie=movies[mid_int],
            quantity=int(qty_str),
            price=movies[mid_int].price
        )

    # clear cart
    _set_cart(request, {})

    messages.success(request, f"Purchase complete. Order #{order.id}")
    # ⬇️ NEW: go to survey page for this order
    return redirect("cart_survey", order_id=order.id)


# =========================
# NEW FEEDBACK VIEWS
# =========================

@login_required
def survey(request, order_id):
    """Display/submit the short statement form after purchase."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        form = CheckoutFeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.order = order
            fb.user = request.user
            if form.cleaned_data.get("anonymous"):
                fb.name = ""  # hide name if anonymous chosen
            fb.save()
            messages.success(request, "Thanks for your feedback!")
            return redirect("cart_survey_thanks")
    else:
        initial = {"name": request.user.get_full_name() or request.user.username}
        form = CheckoutFeedbackForm(initial=initial)

    return render(request, "cart/survey.html", {
        "template_data": {"title": "Checkout Survey", "order": order, "form": form}
    })


def survey_thanks(request):
    return render(request, "cart/survey_thanks.html", {
        "template_data": {"title": "Thanks!"}
    })


def survey_list(request):
    """Public page to view all short statements."""
    feedbacks = CheckoutFeedback.objects.select_related("order", "user").all()
    return render(request, "cart/surveys.html", {
        "template_data": {"title": "Checkout Statements", "feedbacks": feedbacks}
    })
