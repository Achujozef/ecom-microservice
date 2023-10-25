from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib import messages
import requests
from .models import *

@csrf_exempt
def ADD(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        stock = request.POST.get('stock', 1)
        category = request.POST.get('category', 0)
        normalprice = request.POST.get('normalprice', 0)
        listed = request.POST.get('listed', 'true').lower() == 'true'
        offer_percentage = request.POST.get('offer_percentage', None)
        product = Product(
            name=name,
            description=description,
            stock=stock,
            category=category,
            normalprice=normalprice,
            listed=listed,
            offer_percentage=offer_percentage
        )
        product.save()
        images = request.FILES.getlist('images')
        for image in images:
            img = Image(image=image, product=product)
            img.save()
        return JsonResponse({'message': 'Product created successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


#==========================================Edit==============================================

csrf_exempt
def update_product(request, id):

        # Get the data and files from the request
    name = request.POST.get('name')
    description = request.POST.get('description')
    category = request.POST.get('category')
    images = request.FILES.getlist('images')

        # Find the product to update (assuming you have a Product model)
    try:
         product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

        # Update the product fields
    product.name = name
    product.description = description
    product.category = category
        # Update other fields as needed

        # Save the product
    product.save()

        # Handle images (add or remove as needed)
    for image in images:
        product_image = Image(product=product, image=image)
        product_image.save()

        # Return a success response
    return JsonResponse({'message': 'Product updated successfully'}, status=200)



#========================================== Delete=====================================================

def get_product_with_images(request, product_id=None):
    if product_id == None:
        products = Product.objects.all()
    
        product_data = []
        for product in products:
            images = Image.objects.filter(product=product)
            product_details = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'stock': product.stock,
                'category': product.category,
                'normalprice': product.normalprice,
                'listed': product.listed,
                'offer_percentage': product.offer_percentage,
                'images': [image.image.url for image in images]
            }
            product_data.append(product_details)
    else:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        images = Image.objects.filter(product=product)

        # Serialize the product and its images data into a JSON response
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'stock': product.stock,
            'category': product.category,
            'normalprice': product.normalprice,
            'listed': product.listed,
            'offer_percentage': product.offer_percentage,
            'images': [image.image.url for image in images]
        }

    return JsonResponse(product_data, safe=False)
@csrf_exempt
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return HttpResponse(status=204)

def filter_products(request):
    # Get parameters for filtering (cat_id and prod_name)
    cat_id = request.GET.get('cat_id')
    prod_name = request.GET.get('prod_name')

    # Start with all products
    products = Product.objects.all()

    # Filter by category if cat_id is provided
    if cat_id:
        products = products.filter(category=cat_id)  # Update this line

    # Filter by name if prod_name is provided
    if prod_name:
        products = products.filter(name__icontains=prod_name)

    # Collect images for each product
    product_data = []
    for product in products:
        images = Image.objects.filter(product=product)
        image_urls = [image.image.url for image in images]

        product_data.append({
            'id': product.id,
            'name': product.name,
            'category_id': product.category,  # Update this line
            'images': image_urls,
            # Add other product fields as needed
        })

    return JsonResponse(product_data, safe=False)




def get_products_by_category(request, category):
    products = Product.objects.filter(category=category)
    product_data = []
    for product in products:
        images = Image.objects.filter(product=product)
        image_data = [str(image.image.url) for image in images]
        product_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'stock': product.stock,
            'normalprice': product.normalprice,
            'listed': product.listed,
            'offer_percentage': product.offer_percentage,
            'images': image_data,
        })
    response_data = {'products': product_data}
    return JsonResponse(response_data)
