from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Customer, Item, Restaurant, Cart


def index(request):
    return render(request, 'index.html')


def SignIn(request):
    return render(request, 'SignIn.html')


def SignUp(request):
    return render(request, 'SignUp.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if Customer.objects.filter(name=name).exists():
            return HttpResponse("Duplicate username not allowed ✖️")

        Customer.objects.create(
            name=name,
            password=password,
            email=email,
            phone=phone,
            address=address
        )

        return render(request, 'SignIn.html')

    return render(request, 'SignUp.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(name=username, password=password)
            request.session['username'] = username
            request.session['customer_id'] = customer.id

            if username == "admin":
                return render(request, "admin_home.html")
            return redirect('customer_home')

        except Customer.DoesNotExist:
            return render(request, "fail.html")

    return render(request, "SignIn.html")


def customer_home(request):
    if 'customer_id' not in request.session:
        return redirect('SignIn')

    restaurants = Restaurant.objects.all()
    return render(request, 'customer_home.html', {
        'restaurants': restaurants,
        'username': request.session.get('username', '')
    })


def open_restaurant_page(request):
    return render(request, "add_restaurant_page.html")


def add_restaurant(request):
    if request.method == "POST":
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        Restaurant.objects.create(
            name=name,
            picture=picture,
            cuisine=cuisine,
            rating=rating
        )

        restaurants = Restaurant.objects.all()

        return render(request, 'show_restaurants.html', {
            'restaurants': restaurants
        })

    return HttpResponse("Invalid request")

# Show Restaurants
def open_show_restaurant(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'display_restaurants.html', {"restaurants": restaurants})

# Opens Update Restaurant Page
def open_update_restaurant(request, restaurant_id):
    #return HttpResponse("Working")
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant": restaurant})

# Update Restaurant
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'show_restaurants.html', {"restaurants": restaurants})
    
# Delete Restaurant
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        restaurant.delete()
        return redirect("open_show_restaurant")  # make sure this view exists!
    return render(request, "confirm_delete.html", {"restaurant": restaurant})
    
def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get( id=restaurant_id)
    # itemList = Item.objects.all()
    itemList = restaurant.items.all()
    return render(request, 'update_menu.html', 
{"itemList": itemList, "restaurant": restaurant})


def update_menu(request,restaurant_id ):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')

        
        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )
        return render(request, 'admin_home.html')
    
#To view Menu
def view_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get( id=restaurant_id)
    # itemList = Item.objects.all()
    itemList = restaurant.items.all()
    return render(request, 'customer_menu.html', 
                  {"itemList": itemList,
                    "restaurant": restaurant,
                    "username": request.session.get('username', '')})


# Cart Functions
def add_to_cart(request, item_id):
    if 'customer_id' not in request.session:
        return redirect('SignIn')
    
    customer = Customer.objects.get(id=request.session['customer_id'])
    item = get_object_or_404(Item, id=item_id)
    
    # Check if item already in cart
    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        item=item,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')


def view_cart(request):
    if 'customer_id' not in request.session:
        return redirect('SignIn')
    
    customer = Customer.objects.get(id=request.session['customer_id'])
    cart_items = Cart.objects.filter(customer=customer).select_related('item')
    
    total = sum(cart_item.item.price * cart_item.quantity for cart_item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'username': request.session.get('username', '')
    })


def remove_from_cart(request, cart_item_id):
    if 'customer_id' not in request.session:
        return redirect('SignIn')
    
    cart_item = get_object_or_404(Cart, id=cart_item_id, customer_id=request.session['customer_id'])
    cart_item.delete()
    
    return redirect('view_cart')


def update_cart_quantity(request, cart_item_id):
    if 'customer_id' not in request.session:
        return redirect('SignIn')
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item = get_object_or_404(Cart, id=cart_item_id, customer_id=request.session['customer_id'])
            cart_item.quantity = quantity
            cart_item.save()
    
    return redirect('view_cart') 

