from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from users.views import register,profile
from products.views import serve_file,serve_image,index,blog,cart,shop,about,checkout,contact,services,thankyou,profile,staff,product_list,calendar,plans,singleproduct

urlpatterns = [

    path('plans/', plans),
    path('calendar/', calendar),
    path('staff/', staff),
    path('profile/', profile),
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
    path('media/product_images/<str:filename>/', serve_image, name='serve_image'),

]
