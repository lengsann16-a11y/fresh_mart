from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CustomerProfile, Product, Category, Order, OrderItem
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm # Add ProductForm to your imports at the top
from .forms import (
    UserRegisterForm, UserLoginForm, CheckoutForm,
    CustomerProfileForm, ContactForm, ProductForm # <-- Add ProductForm here!
)
# Add these to the bottom of store/views.py



from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm # Add ProductForm to your imports at the top

# Helper to check if user is staff
def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if not product.slug:
                from django.utils.text import slugify
                product.slug = slugify(product.name)
            product.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('store:product_detail', pk=product.pk, slug=product.slug)
    else:
        form = ProductForm()
    
    return render(request, 'product_form.html', {'form': form, 'title': 'Add New Product'})

@user_passes_test(is_staff)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('store:product_detail', pk=product.pk, slug=product.slug)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product_form.html', {'form': form, 'title': f'Edit: {product.name}'})

@user_passes_test(is_staff)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('store:product_list')
    
    return render(request, 'product_confirm_delete.html', {'product': product})




# ─── PROFILE ───────────────────────────────────────────────────
@login_required
def profile(request):
    # ✅ FIX: Get or create profile to avoid RelatedObjectDoesNotExist
    profile_obj, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'address': '',
            'city': '',
        }
    )

    if request.method == 'POST':
        form = CustomerProfileForm(
            request.POST, request.FILES,
            instance=profile_obj  # ✅ Use the safe profile_obj
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('store:profile')
    else:
        form = CustomerProfileForm(instance=profile_obj)  # ✅ Use the safe profile_obj

    orders = Order.objects.filter(user=request.user).order_by('-created')[:5]
    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'profile.html', context)



# Helper to check if user is staff
def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if not product.slug:
                from django.utils.text import slugify
                product.slug = slugify(product.name)
            product.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('store:product_detail', pk=product.pk, slug=product.slug)
    else:
        form = ProductForm()
    
    return render(request, 'product_form.html', {'form': form, 'title': 'Add New Product'})

@user_passes_test(is_staff)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('store:product_detail', pk=product.pk, slug=product.slug)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product_form.html', {'form': form, 'title': f'Edit: {product.name}'})

@user_passes_test(is_staff)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('store:product_list')
    
    return render(request, 'product_confirm_delete.html', {'product': product})


# ─── HOME ──────────────────────────────────────────────────────
def home(request):
    featured_products = Product.objects.filter(is_featured=True, available=True)[:8]
    new_products = Product.objects.filter(available=True).order_by('-created')[:8]
    categories = Category.objects.all()
    organic_products = Product.objects.filter(is_organic=True, available=True)[:4]

    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories,
        'organic_products': organic_products,
    }
    return render(request, 'home.html', context)


# ─── PRODUCTS ──────────────────────────────────────────────────
def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-created')
    is_organic = request.GET.get('organic')

    if category_slug:
        products = products.filter(category_fk__slug=category_slug)

    if search_query:
        products = products.filter(name__icontains=search_query)

    if is_organic:
        products = products.filter(is_organic=True)

    valid_sorts = ['-created', 'price', '-price', 'name']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)

    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


# ─── CART ──────────────────────────────────────────────────────
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = float(item_data['price']) * item_data['quantity']
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': item_data['price'],
                'total': item_total,
            })
        except Product.DoesNotExist:
            del cart[product_id]
            request.session['cart'] = cart

    context = {
        'cart_items': cart_items,
        'cart_total': total,
    }
    return render(request, 'cart.html', context)


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    product_key = str(product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product_key in cart:
        cart[product_key]['quantity'] += quantity
    else:
        cart[product_key] = {
            'quantity': quantity,
            'price': str(product.price),
        }

    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to cart!')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = sum(item['quantity'] for item in cart.values())
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'message': f'{product.name} added to cart!',
        })

    return redirect('store:cart')


@require_POST
def cart_update(request, product_id):
    cart = request.session.get('cart', {})
    product_key = str(product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product_key in cart:
        if quantity > 0:
            cart[product_key]['quantity'] = quantity
        else:
            del cart[product_key]

    request.session['cart'] = cart
    messages.info(request, 'Cart updated!')
    return redirect('store:cart')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_key = str(product_id)

    if product_key in cart:
        product_name = Product.objects.filter(id=product_id).first()
        del cart[product_key]
        request.session['cart'] = cart
        if product_name:
            messages.info(request, f'{product_name.name} removed from cart.')

    return redirect('store:cart')


def cart_clear(request):
    request.session['cart'] = {}
    messages.info(request, 'Cart cleared!')
    return redirect('store:cart')


# ─── CHECKOUT ──────────────────────────────────────────────────
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('store:cart')

    cart_items = []
    total = 0
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = float(item_data['price']) * item_data['quantity']
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': item_data['price'],
                'total': item_total,
            })
        except Product.DoesNotExist:
            pass

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total
            order.paid = False
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            request.session['cart'] = {}
            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('store:order_detail', order_id=order.id)
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        # ✅ FIX: Safe profile access
        profile_obj = CustomerProfile.objects.filter(user=request.user).first()
        if profile_obj:
            initial_data.update({
                'phone': profile_obj.phone,
                'address': profile_obj.address,
                'city': profile_obj.city,
            })
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': cart_items,
        'cart_total': total,
    }
    return render(request, 'checkout.html', context)


# ─── ORDERS ────────────────────────────────────────────────────
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'order_detail.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    context = {'orders': orders}
    return render(request, 'order_list.html', context)


# ─── AUTH ──────────────────────────────────────────────────────
def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:home')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}! Welcome to Fresh Mart!')
            return redirect('store:home')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


# ─── PROFILE ───────────────────────────────────────────────────
@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomerProfileForm(
            request.POST, request.FILES,
            instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('store:profile')
    else:
        form = CustomerProfileForm(instance=request.user.profile)

    orders = Order.objects.filter(user=request.user).order_by('-created')[:5]
    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'profile.html', context)


# ─── CONTACT ───────────────────────────────────────────────────
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('store:contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# ─── SEARCH ────────────────────────────────────────────────────
def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    if query:
        products = products.filter(name__icontains=query)

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'product_list.html', context)
