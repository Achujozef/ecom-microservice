import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        images = request.FILES.getlist('images')
        if not name or name.isspace():
            messages.error(request, 'Name should not be empty or contain only spaces.')
            return redirect('add_product')

        if not description or description.isspace() or len(description) < 10:
            messages.error(request, 'Description should be at least 10 characters long and should not be empty or contain only spaces.')
            return redirect('add_product')
        data = {
            'name': name,
            'description': description,
            'category': category_id,
        }
        files = {}
        for image in images:
            files['images'] = (image.name, image, image.content_type)
        try:
            response = requests.post('http://localhost:8001/add/', data=data, files=files)
            response.raise_for_status() 
            messages.success(request, 'Product added successfully.')
            return redirect('admin_product_page')
        except requests.exceptions.RequestException as e:
            messages.error(request, 'Failed to add the product.')
    category_api_url = 'http://localhost:8002/categories/'  

    try:
        response = requests.get(category_api_url)
        response.raise_for_status()  
        categories = response.json()
    except requests.exceptions.RequestException as e:
        categories = [] 
    context = {'categories': categories}

    return render(request, 'add_product.html', context)

@csrf_exempt
def edit_product(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        images = request.FILES.getlist('images')
        remove_images = request.POST.getlist('remove_images')
        if not name or name.isspace():
            messages.error(request, 'Name should not be empty or contain only spaces.')
            return redirect('edit_product', id=id)
        if not description or description.isspace() or len(description) < 10:
            messages.error(request, 'Description should be at least 10 characters long and should not be empty or contain only spaces.')
            return redirect('edit_product', id=id)
        data = {
            'id': id,
            'name': name,
            'description': description,
            'category': category_id,
        }
        files = {}
        for image in images:
            files['images'] = (image.name, image, image.content_type)
        try:
            response = requests.post(f'http://localhost:8001/update_product/{id}/', data=data, files=files)
            response.raise_for_status()  
            messages.success(request, 'Product updated successfully.')
            return redirect('admin_product_page')
        except requests.exceptions.RequestException as e:
            messages.error(request, 'Failed to update the product.')
    other_server_url = f'http://localhost:8001/get_product/{id}/'
    try:
        response = requests.get(other_server_url)
        if response.status_code == 200:
            product_data = response.json()
        else:
            return JsonResponse({'error': 'Failed to fetch product from the other server.'}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to connect to the other server.'}, status=500)
    print(product_data)
    category_api_url = 'http://localhost:8002/categories/'  
    try:
        response = requests.get(category_api_url)
        response.raise_for_status()  
        categories = response.json()
    except requests.exceptions.RequestException as e:
        categories = [] 
    print(categories)
    context = {
        'orgi': product_data,
        'categories':categories
    }
    return render(request, 'edit_product.html', context)

def admin_product_page(request): 
    other_server_url = 'http://localhost:8001/get_product/'
    try:
        response = requests.get(other_server_url)
        if response.status_code == 200:
            product_data = response.json()
        else:
            return JsonResponse({'error': 'Failed to fetch product from the other server.'}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to connect to the other server.'}, status=500)

    orgi =product_data
    category_api_url = 'http://localhost:8002/categories/'  
    try:
        response = requests.get(category_api_url)
        response.raise_for_status()  
        categories = response.json()
    except requests.exceptions.RequestException as e:
        categories = [] 
    categories = categories

    context = {
        'orgi': product_data,
             
        'categories': categories}
        
    return render(request,'admin.html',context)

def delete_product(request, product_id):
    delete_url = f'http://localhost:8001/delete/{product_id}/'
    try:
        response = requests.get(delete_url)
        if response.status_code == 204:
            return redirect('admin_product_page')
        else:
            return JsonResponse({'error': 'Failed to delete the product'}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to connect to the other server.'}, status=500)
    



def shop(request):
    products_url = 'http://localhost:8001/filter_products/' 
    cat_id = request.GET.get('cat_id')
    prod = request.GET.get('prod_id')
    products_params = {}
    if cat_id is not None:
        products_params['cat_id'] = cat_id
    if prod is not None:
        products_params['prod_name'] = prod
    response = requests.get(products_url, params=products_params)
    if response.status_code != 200:
        return render(request, 'error.html', {'error_message': 'Failed to fetch products'})
    products = response.json()
    categories_url = 'http://localhost:8002/categories/'  
    response = requests.get(categories_url)
    if response.status_code != 200:
        return render(request, 'error.html', {'error_message': 'Failed to fetch categories'})
    cat = response.json()
    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(cat)
    return render(request, 'index_user.html', {'page_obj': page_obj, 'cat': cat, 'products': products})

# def shopsingle(request):
#     uid = request.GET.get('uid')
#     product = Product.objects.prefetch_related('images').filter(id=uid).first()
#     images = product.images.all() if product else []
#     variants = ProductVariant.objects.filter(product=product).order_by('price')
#     products_in_same_category = Product.objects.filter(category=product.category)
#     category_offer_percentage = None
#     if product.category:
#         category_offer_percentage = product.category.offer_percentage
#     return render(request, 'product_detail.html', {'product': product, 'images': images,'variants': variants, 'products_in_same_category':products_in_same_category,'category_offer_percentage':category_offer_percentage})

def add_variant_prod(request, product_id):
    # Define the URL of the ProductVariant service (localhost:8003)
    product_variant_url = f'http://localhost:8003/create_variant/'

    # Make a request to fetch the product data from another server (localhost:8001)
    try:
        response = requests.get(f'http://localhost:8001/get_product/{product_id}/')
        if response.status_code == 200:
            product_data = response.json()
        else:
            return JsonResponse({'error': 'Failed to fetch product from the other server.'}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Failed to connect to the other server.'}, status=500)

    if request.method == 'POST':
        # Retrieve variant details from the form
        variant_name = request.POST['variant_name'].strip()
        variant_price = request.POST['variant_price'].strip()
        variant_stock = request.POST['variant_stock'].strip()

        # Validate variant data
        if variant_name == '':
            messages.error(request, 'Variant name cannot be empty.')
        elif variant_price == '':
            messages.error(request, 'Variant price cannot be empty.')
        elif not variant_price.isdigit() or int(variant_price) <= 0:
            messages.error(request, 'Variant price should be a positive integer.')
        elif variant_stock == '':
            messages.error(request, 'Variant stock cannot be empty.')
        elif not variant_stock.isdigit() or int(variant_stock) < 0:
            messages.error(request, 'Variant stock should be a non-negative integer.')

        if not messages.get_messages(request):
            # Create a variant data to send to the ProductVariant service
            variant_data = {
                'product': product_id,  # The ID of the product
                'variant': variant_name,
                'price': variant_price,
                'stock': variant_stock
            }

            # Make a POST request to create the product variant
            print(variant_data)
            variant_response = requests.post(product_variant_url, variant_data)

            if variant_response.status_code == 201:
                messages.success(request, 'Variant added successfully.')
                return redirect('admin_product_page')
            else:
                return JsonResponse({'error': 'Failed to create the variant in the other server.'}, status=500)
    return render(request, 'add_variant.html', {'product': product_data})


product_service_url = 'http://localhost:8002/'
product_variant_service_url = 'http://localhost:8003/'

def fetch_product_from_service(product_id):
    product_url = f'{product_service_url}get_product/{product_id}/'
    response = requests.get(f'http://localhost:8001/get_product/{product_id}/')

    if response.status_code == 200:
        return response.json()
    return None 

def fetch_variants_from_service(product_id):
    variants_url = f'{product_variant_service_url}get_variants/?product_id={product_id}'
    response = requests.get(variants_url)

    if response.status_code == 200:
        return response.json()
    return []  
def edit_variants(request, product_id):
    product = fetch_product_from_service(product_id)

    if product is None:
        return JsonResponse({'error': 'Failed to fetch the product.'}, status=500)

    variants = fetch_variants_from_service(product_id)

    if request.method == 'POST':
        for variant in variants:
            variant_name = request.POST.get(f'{variant["id"]}_name', '').strip()
            variant_price = request.POST.get(f'{variant["id"]}_price', '').strip()
            variant_stock = request.POST.get(f'{variant["id"]}_stock', '').strip()

            if variant_name == '':
                messages.error(request, 'Variant name cannot be empty.')
            elif variant_price == '':
                messages.error(request, 'Variant price cannot be empty.')
            elif not variant_price.isdigit() or int(variant_price) < 0:
                messages.error(request, 'Variant price should be a non-negative integer.')
            elif variant_stock == '':
                messages.error(request, 'Variant stock cannot be empty.')
            elif not variant_stock.isdigit() or int(variant_stock) < 0:
                messages.error(request, 'Variant stock should be a non-negative integer.')

            if not messages.get_messages(request):
                variant_update_url = f'{product_variant_service_url}update_variant/{variant["id"]}/'
                variant_data = {
                    'variant': variant_name,
                    'price': variant_price,
                    'stock': variant_stock
                }
                print(variant_data)
                response = requests.put(variant_update_url, json=variant_data)

                if response.status_code == 200:
                    # Variant updated successfully
                    messages.success(request, f'Variant {variant_name} updated successfully.')
                    return redirect('admin_product_page')
                elif response.status_code == 204:
                    # Variant deleted successfully
                    messages.success(request, f'Variant {variant_name} deleted successfully')
                    return redirect('admin_product_page')
                else:
                    messages.error(request, 'Failed to update the variant.')

        if not messages.get_messages(request):
            return redirect('admin_product_page')

    return render(request, 'edit_variants.html', {'product': product, 'variants': variants})


def shopsingle(request):
    uid = request.GET.get('uid')

    # Make a request to the product service to get the product information
    product_response = requests.get('http://localhost:8001/get_product', params={'product_id': uid})
    
    if product_response.status_code == 200:
        product = product_response.json()
        # Get the category ID from the product
        category_id = product[0]['category']
        
        # Make a request to the product service to get products in the same category
        products_in_same_category_response = requests.get(f'http://localhost:8001/get_products_by_category/{category_id}/')
        
        if products_in_same_category_response.status_code == 200:
            products_in_same_category = products_in_same_category_response.json()
        else:
            products_in_same_category = []

        # Make a request to the product variant service to get product variants
        variants_response = requests.get('http://localhost:8003/get_variants', params={'product_id': uid})
        
        if variants_response.status_code == 200:
            variants = variants_response.json()
        else:
            variants = []

        # category_offer_percentage = product.get('category_offer_percentage')
        print("product",product)
        print()
        print("variants",variants)
        print()
        print("products_in_same_category",products_in_same_category)
        print()
        return render(request, 'product_detail.html', {'product': product[0], 'variants': variants, 'products_in_same_category': products_in_same_category})
    else:
        # Handle the case where the product service returns an error
        return render(request, 'error.html', {'error_message': 'Failed to retrieve product information'})