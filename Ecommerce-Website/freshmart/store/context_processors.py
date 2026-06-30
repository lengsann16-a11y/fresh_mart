from .models import Category, CustomerProfile


def cart_context(request):
    """Make cart available in all templates"""
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values())
    cart_total = sum(
        float(item.get('price', 0)) * item.get('quantity', 0)
        for item in cart.values()
    )

    # ✅ FIX: Safe profile access for templates
    user_profile = None
    if request.user.is_authenticated:
        user_profile = CustomerProfile.objects.filter(user=request.user).first()

    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
        'categories': Category.objects.all(),
        'user_profile': user_profile,
    }