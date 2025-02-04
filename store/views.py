
from django.shortcuts import render, redirect
from .models import Product

def product_list(request):
    """Display products, filtered by category if selected."""
    category_id = request.GET.get('category')  # Get category ID from URL query parameters
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()  # Fetch categories for the dropdown

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'store/product_list.html', {'products': products, 'query': query})

def add_to_cart(request, product_id):
    """Add a product to the cart (stored in session)."""
    product = Product.objects.get(id=product_id)

    # Get the cart from session, or create an empty one
    cart = request.session.get('cart', {})

    # Add or update the product quantity
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart  # Save cart in session
    return redirect('product_list')

def view_cart(request):
    """Display the shopping cart."""
    cart = request.session.get('cart', {})
    return render(request, 'store/cart.html', {'cart': cart})

def remove_from_cart(request, product_id):
    """Remove an item from the cart."""
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart  # Update session
    return redirect('view_cart')

def clear_cart(request):
    """Remove all items from the shopping cart."""
    request.session['cart'] = {}  # Set cart to an empty dictionary
    return redirect('view_cart')
from .models import Category

def categories_context(request):
    """Fetch categories for the navigation menu in all templates."""
    categories = Category.objects.all()
    return {'categories': categories}

