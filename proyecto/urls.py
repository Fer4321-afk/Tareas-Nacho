from django.contrib import admin #adminis 
#CARGAR MEDIA O IMAGENES
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include  #urls
 # vistas de la app
from proyecto import views
# vistas del proyecto 

urlpatterns = [
    
    path("__reload__/", include("django_browser_reload.urls")), #recargar pag
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),       # página principal
    path('blog/', include('blog.urls')),  # URLs de la app blog
    path('users/', include(('users.urls','users'),namespace='users')),  # URLs de la app users
    path('products/',include('products.urls')), #Urls de products
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
