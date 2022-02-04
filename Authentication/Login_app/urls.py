import imp
from xml.dom.minidom import Document
from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import views
app_name = 'Login_app'
urlpatterns = [
    path('', views.Index, name='index'),
    path('registration/', views.Registration, name='registration'),
    path('login/', views.Login_page, name='login'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),


]
#for image
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
