from django.shortcuts import redirect, render, get_object_or_404
from .forms import ImageCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Image
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from common.decorators import ajax_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)

    return render(request, 'images/image/create.html', {'section':'images', 'form':form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'image':image, 'section':'images', })

# @ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_liked.add(request.user)
            else:
                image.users_liked.remove(request.user)
            return JsonResponse({'status':'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if is_ajax(request=request):
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if is_ajax(request=request):
        return render(request, 'images/image/list_ajax.html', {'section':'images', 'images':images})
    return render(request, 'images/image/list.html', {'section':'images', 'images':images})
    