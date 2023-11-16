from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from users.views import register,profile
from products.views import index,blog,cart,shop,about,checkout,contact,services,thankyou

urlpatterns = [
    
    path('thankyou/', thankyou),
    path('services/', services),
    path('contact/', contact),
    path('checkout/', checkout),
    path('about/', about),
    path('cart/', cart),
    path('cart/', cart),
    path('shop/', shop),
    path('', index),
    path('blog/', blog),
    path('admin/', admin.site.urls),
    path('p/', include('products.urls')),
    path('', include('users.urls')), 

]
