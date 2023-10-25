from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm
from django.contrib import messages
from django.http import JsonResponse

def category_list(request):
    categories = Category.objects.all()
    category_list = list(categories.values())  # Convert queryset to a list of dictionaries
    
    return JsonResponse({'categories': category_list}, safe=False)

def get_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    data = {'id': category.id, 'category': category.name}
    return JsonResponse(data)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name',]
            if Category.objects.filter(name=name).exists():
                messages.error(request, 'Category with this name already exists.')
            else:
                Category.objects.create(name=name)
                messages.success(request, 'Category added successfully.')
            return redirect('category_list')
        else:
            messages.error(request, 'Name Already Taken.')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'add_category.html', context)

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    context = {'form': form, 'category': category}
    return render(request, 'edit_category.html', context)

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    context = {'category': category}
    return render(request, 'delete_category.html', context)
