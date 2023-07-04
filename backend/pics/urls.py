"""
URL configuration for pics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pics import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #old urls
    #path('admin/', admin.site.urls),
    #path('pics/', views.pic_list),
    #path('pics/<int:id>', views.pic_detail),
    #path('pets/get_all', views.pets_get_all),
    #path('pics/get_all', views.pics_get_all),
    #path('pics/get_all_until_id', views.pics_get_all_until_id)

    #working urls
    path('pets/post', views.pet_camera_post),
    path('pets/get_images', views.pet_get_images),
    path('pets/check_for_new_images', views.pet_check_for_new_images),

    #experimental urls
    path('mongo/test', views.mongo_test),
    path('mongo/new_db', views.mongo_new_db),
]

urlpatterns = format_suffix_patterns(urlpatterns)