from django.shortcuts import render
import requests
from django.shortcuts import redirect
from django.http import HttpResponse

def base_file(request):
    print("Im reached here")
    response = requests.get('http://localhost:5000/getbanners')
    if response.status_code == 200:
        banners = response.json()
        print("Banners",banners)
        obj = [{'id': banner['id'], 'public_id': banner['public_id']} for banner in banners]
    else:
        obj = []
    print(obj)
    return render(request, 'index.html', {'obj': obj})

def adminbannerlist(request):

        if 'search' in request.GET:
            search = request.GET['search']
            response = requests.get('http://localhost:5000/getbanners')
            if response.status_code == 200:
                banners = response.json()
                # Filter banners based on your search criteria
                filtered_banners = [banner for banner in banners if search in banner.get('name', '')] 
            else:
                filtered_banners = []  # Set an empty list if there was an error
        else:
            # If there's no search criteria, just get all banners from the Flask service
            response = requests.get('http://localhost:5000/getbanners')
            if response.status_code == 200:
                filtered_banners = response.json()
            else:
                filtered_banners = []  # Set an empty list if there was an error
        print(filtered_banners)
        return render(request, 'adminbannerlist.html', {'member': filtered_banners})


def deletebanner(request):

        uid = request.GET['uid']
        response = requests.delete(f'http://localhost:5000/deletebanner/{uid}')
        
        if response.status_code == 200:
            return redirect('adminbannerlist')
        else:
            return redirect('adminbannerlist')
        
def adminaddbanner(request):
    if request.method == 'POST':
        image = request.FILES['image']
        endpoint_url = 'http://localhost:5000/uploadbanner'
        data = {'image': image}
        try:
            response = requests.post(endpoint_url, files=data)
            if response.status_code == 201:
                return redirect('adminbannerlist')
            else:
                return HttpResponse(f'Error: {response.status_code}', status=response.status_code)
        except requests.exceptions.RequestException as e:
            return HttpResponse(f'Error: {str(e)}', status=500)
    else:
        return render(request, 'adminaddbanner.html')
    
