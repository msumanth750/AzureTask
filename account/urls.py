from django.urls import path,include
from account.views import (SendPasswordResetEmailView, UserChangePasswordView,
                            UserLoginView, UserProfileView,
                            UserRegistrationView, UserPasswordResetView,
                            ProfileView,OrganisationView,
                            ProjectView,ReportsView,UsersView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile',ProfileView)
router.register('org',OrganisationView)
router.register('project',ProjectView)
router.register('reports',ReportsView)
router.register('all',UsersView)

urlpatterns = [
    path('',include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profileview/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),

]
