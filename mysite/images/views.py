from django.shortcuts import redirect, render, get_object_or_404
from .forms import ImageCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Image
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from common.decorators import ajax_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from actions.utils import create_action
import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')
            # redirect to new created image detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(request.GET)

    return render(request, 'images/image/create.html', {'section':'images', 'form':form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1
    total_views = r.incr(f'image:{image.id}:views')
    return render(request, 
                  'images/image/detail.html', 
                  {'image':image, 
                   'section':'images',
                   'total_views':total_views})

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
                create_action(request.user, 'likes', image)
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
    '''
    view to handle both HTTP and AJAX request for image list
    '''
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:   
        if images_only:
            # If AJAX request and page out of range return an empty page
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request, 'images/image/list_images.html', {'section':'images', 'images':images})
    return render(request, 'images/image/list.html', {'section':'images', 'images':images})
    