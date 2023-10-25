from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ProductVariant
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_POST
def create_variant(request):
    try:
        data = request.POST 
        print(data.get('variant'))
        variant = ProductVariant(
            product=data.get('product'),
            variant=data.get('variant'),
            price=data.get('price'),
            stock=data.get('stock')
        )
        variant.save()
        print(variant)
        return JsonResponse({'message': 'Product variant created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': 'Failed to create product variant'}, status=500)

@require_http_methods(["PUT", "DELETE"])
def update_or_delete_variant(request, variant_id):
    variant = get_object_or_404(ProductVariant, pk=variant_id)

    if request.method == 'PUT':
        try:
            variant_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request body'}, status=400)
        print("Firt Time variant_data",variant_data)
        variant.variant = variant_data.get('variant', variant.variant)
        variant.price = variant_data.get('price', variant.price)
        variant.stock = variant_data.get('stock', variant.stock)
        variant.save()
        return JsonResponse({'message': 'Variant updated successfully'})

    elif request.method == 'DELETE':
        variant.delete()
        return JsonResponse({'message': 'Variant deleted successfully'}, status=204)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

def get_variants_by_product(request):
    product_id = request.GET.get('product_id')
    if product_id is None:
        return JsonResponse({'error': 'Product ID is required'}, status=400)
    variants = ProductVariant.objects.filter(product=product_id).order_by('price')
    serialized_variants = []
    for variant in variants:
        serialized_variants.append({
            'id': variant.id,
            'variant': variant.variant,
            'price': variant.price,
            'stock': variant.stock,
        })

    return JsonResponse(serialized_variants, safe=False)