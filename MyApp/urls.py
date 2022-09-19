

from django.urls import include, path
from django.views.generic.base import TemplateView
from . import views
 
urlpatterns = [
     path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
     path('linkedin/', views.linkedin, name='linkedin'),
     path('linkedin/editor/auth/editor/', views.editor, name='editor'),
     path('linkedin/editor/auth/', views.authcode, name= 'authcode'),

]