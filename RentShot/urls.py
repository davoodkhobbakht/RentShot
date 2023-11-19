from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from users.views import register,profile
from products.views import index,blog,cart,shop,about,checkout,contact,services,thankyou,product_detail,profile,staff,product_list

urlpatterns = [
    
    path('staff/', staff),
    path('profile/', profile),
    path('product_detail/', product_detail),
    path('thankyou/', thankyou),
    path('services/', services),
    path('contact/', contact),
    path('checkout/', checkout),
    path('about/', about),
    path('cart/', cart),
    path('product_list/', product_list),
    path('shop/', shop),
    path('', index),
    path('blog/', blog),
    path('admin/', admin.site.urls),
    path('p/', include('products.urls')),
    path('', include('users.urls')), 

]
