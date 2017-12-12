from django.conf.urls import url
from rest_framework import routers
import api.views as views


router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
# router.register(r'chapters', views.ChapterViewSet)
# router.register(r'chunks', views.ChunkViewSet)
# router.register(r'languages', views.LanguageViewSet)
# router.register(r'books', views.BookViewSet)
# router.register(r'languages', language.LanguageViewSet)
router.register(r'^books', views.BookViewSet)
# router.register(r'users', views.UserViewSet)
router.register(r'takes', views.TakeViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'anthologies', views.AnthologyViewSet)


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/(?P<filename>[^/]+)$',
        views.file_upload.FileUploadView.as_view()),
    url(r'^resumable_upload/(?P<filename>[^/]+)/$',
        views.resumable_upload.ResumableFileUploadView.as_view()),
    # url(r'^source/(?P<filename>[^/]+)$', views.UploadSourceFileView.as_view()),
    #url(r'^get_project_takes/$', views.GetProjectTakesView.as_view()),
    # url(r'^update_project_takes/$', views.UpdateProjectTakesView.as_view()),
    url(r'^get_source/$', views.TrProjectFiles.as_view()),
    url(r'^zip_project_files/$', views.ZipProjectFiles.as_view()),
    # url(r'^exclude_files/$', views.ExcludeFilesView.as_view()),
    #url(r'^all_projects/$', all_projects.AllProjectsView.as_view()),
    # url(r'^book/$', views.GetBooksView.as_view()),
]

urlpatterns += router.urls
