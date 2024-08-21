from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.view_documents, name='view_documents'),
    path('recommend-subject/', views.recommend_subject, name='recommend_subject'),
    path('my-documents/', views.document_list, name='document_list')
]

