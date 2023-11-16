from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from users.views import register,profile
from products.views import index,blog,cart,shop

urlpatterns = [
    path('cart/', cart),
    path('shop/', shop),
    path('', index),
    path('blog/', blog),
    path('admin/', admin.site.urls),
    path('p/', include('products.urls')),
    path('', include('users.urls')),

]
