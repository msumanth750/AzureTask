from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import TaskView,TaskCommentView,NoteView,ImageView,TaskStatusListView

router = DefaultRouter()
router.register('details',TaskView)
router.register('comment',TaskCommentView)
router.register('note',NoteView)
router.register('images',ImageView)
router.register('statuslist',TaskStatusListView)

urlpatterns = [
    path('',include(router.urls))
]
