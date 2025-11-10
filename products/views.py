
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import UploadProduct

@login_required(login_url="/users/login/")
def product_list_view(request):
    product_list = Product.objects.all()[:20]
    form = UploadProduct()
    return render(request, 'products/list.html', {'product_list': product_list, 'form': form})

def post_new(request):
    if request.method == 'POST':
        form = UploadProduct(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.user = request.user
            newpost.save()
    return redirect('products:product_list')
# Create your views here.
