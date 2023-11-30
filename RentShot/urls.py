from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from users.views import register,profile
from products.views import index,blog,cart,shop,about,checkout,contact,services,thankyou,profile,product_list,admin_panel,plans,profile_contact,pro_status,ticket,rules

urlpatterns = [

    path('rules/', rules),
    path('ticket/', ticket),
    path('pro_status/', pro_status),
    path('profile_contact/', profile_contact),
    path('admin_panel/', admin_panel),
    path('plans/', plans),
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

]
