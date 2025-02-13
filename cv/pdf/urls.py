from django.urls import path
from .views import contact_view, create_cv, success_view, cv_list, share_cv_email

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('success/', success_view, name='success_page'),
    path('create/', create_cv, name='create_cv'),
    path('cv_list/', cv_list, name='cv_list'),
    path('share/email/<int:cv_id>/', share_cv_email, name='share_cv_email'),
]