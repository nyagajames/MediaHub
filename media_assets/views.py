from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import login_required
from django.core.paginator import Paginator
from .models import MediaAssets
from .forms import MediaAssetsForm
from django.db.models import Q  # for complex queries
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required
def dashboard_view(request):
    # main dashboard view - shows all media assets uploaded by the user
    media_list = MediaAssets.objects.filter(is_public=True) # show only public media assets
    query = request.GET.get('q') # search query from the dashboard search form
    if query:
        media_list = media_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) 
        )
    # content pagination(showcase data in chunks)
    paginator = Paginator(media_list, 12) # show 12 media assets per page
    page_number = request.GET.get('page')
    media_asssets = paginator.get_page(page_number)
    return render(request, 'media_assets/dashboard.html', {'media_assets': media_asssets, 'query': query})

# view to show only the media files that belong to the user
@login_required
def my_media_view(request):
    media_list = MediaAssets.objects.filter(uploaded_by=request.user) # show only media assets uploaded by the user
    # content pagination(showcase data in chunks)
    paginator = Paginator(media_list, 12) # show 12 media assets per page
    page_number = request.GET.get('page')
    media_asssets = paginator.get_page(page_number)
    return render(request, 'media_assets/my_media.html', {'media_assets': media_asssets})
# view to handle media asset upload(allow the user to upload media files)
@login_required
def upload_view(request):
    if request.method == 'POST':
        form = MediaAssetsForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False) # create a media asset object but don't save to the database yet
            media.uploaded_by = request.user # set the uploaded_by field to the current user
            media.save() # save the media asset to the database
            messages.success(request, "Media asset uploaded successfully!")
            return redirect('media_assets::my_media') # redirect to the user's media page after successful upload
    else:
        form = MediaAssetsForm()
    return render(request, 'media_assets/upload.html', {'form': form})  

## view to show the details of a media asset
# to be used in updating the view count
@login_required
def media_detail_view(request, pk):
    # pk is the primary key of the media asset to be displayed unique identifier for the media asset used to identify the role of current user (uploader or viewer)
    # get_object_or_404 is a shortcut function that retrieves an object from the database based on the primary key (pk) and raises a 404 error if the object does not exist
    media = get_object_or_404(MediaAssets,pk=pk)
    # app specifications #tag whether media is private or public
    if media.is_public and media.uploaded_by != request.user and not request.user.is_teacher() and not request.is_superuser:
        messages.error(request, "You do not have permission to view this media asset.")
        return redirect('media_assets::dashboard')
    # update view count only if the viewer is not the uploader and the media asset is public
    # increment the view count by 1 and save the media asset to the database
    media.views_count += 1
    media.save(update_fields=['views_count']) # update only the views_count field in the database
    # compute edit and delete permissions based on the role of the user
    # the user can only edit or delete if they uploaded the media or they are a superuser/ teacher
    can_edit = media.can_edit(request.user) # check if the user has permission to edit the media asset
    can_delete = media.can_delete(request.user) # check if the user has permission to delete the media asset
    return render(request, 'media_assets/media_detail.html', {'media': media, 'can_edit': can_edit, 'can_delete': can_delete})

# edit view to handle media asset updates (allow the user to edit media files they have uploaded)
def edit_media_view(request, pk):
    # only allow editing if user is the uploader or is a superuser/teacher
    media = get_object_or_404(MediaAssets, pk=pk)
    if not media.can_edit(request.user):
        messages.error(request, "You do not have permission to edit this media asset.")
        return redirect('media_assets::media_detail', pk=pk)
    if request.method == 'POST':
        form = MediaAssetsForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save() # save the updated media asset to the database
            messages.success(request, "Media asset updated successfully!")
            return redirect('media_assets::media_detail', pk=pk) # redirect to the media detail page after successful update
    else:
        form = MediaAssetsForm(instance=media)
    return render(request, 'media_assets/edit_media.html', {'form': form, 'media': media})

@login_required
def delete_media_view(request, pk):
    # only allow deletion if user is the uploader or is a superuser/teacher
    media = get_object_or_404(MediaAssets,pk=pk)
    if not media.can_delete(request.user):
        messages.error(request, "You do not have permission to delete this media asset.")
        return redirect('media_assets:dashboard', pk=pk)
    if request.method == 'POST':
        media.delete() # delete the media asset from the database
        messages.success(request, "Media asset deleted successfully!")
        return redirect('media_assets:my_media') # redirect to the user's media page after successful deletion
    return render(request, 'media_assets/delete_media.html', {'media': media})