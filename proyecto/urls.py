from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# vistas del proyecto
from proyecto import views
# vistas de users
from users import views as user_views

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('blog/', include('blog.urls')),
    path('users/', include(('users.urls','users'), namespace='users')),  # urls de users
    path('products/', include('products.urls')),
    path('games/', include('games.urls')),
   ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
