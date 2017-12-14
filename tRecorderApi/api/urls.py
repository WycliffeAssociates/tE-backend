from django.conf.urls import url
from rest_framework import routers
from . import views
from .views import (
    book, language,
    version, anthology, index,
    resumable_upload, all_projects,
    ProjectViewSet)

router = routers.DefaultRouter()
router.register(r'languages', views.LanguageViewSet)
router.register(r'anthologies', views.AnthologyViewSet)
router.register(r'versions', views.VersionViewSet)
router.register(r'^books', views.BookViewSet)
router.register(r'modes', views.ModeViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'chapters', views.ChapterViewSet)
router.register(r'chunks', views.ChunkViewSet)
router.register(r'takes', views.TakeViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'zip', views.ZipViewSet)
router.register(r'tr', views.TrViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/(?P<filename>[^/]+)$',
        views.file_upload.FileUploadView.as_view()),
    url(r'^resumable_upload/(?P<filename>[^/]+)/$',
        views.resumable_upload.ResumableFileUploadView.as_view()),
    # url(r'^source/(?P<filename>[^/]+)$', views.UploadSourceFileView.as_view()),
    # url(r'^exclude_files/$', views.ExcludeFilesView.as_view()),
]

urlpatterns += router.urls
