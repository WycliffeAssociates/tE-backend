from django.conf.urls import url
from rest_framework import routers
import api.views

router = routers.DefaultRouter()
router.register(r'api/projects', api.views.ProjectViewSet)
router.register(r'api/chapters', api.views.ChapterViewSet)
router.register(r'api/chunks', api.views.ChunkViewSet)
router.register(r'api/languages', api.views.LanguageViewSet)
router.register(r'api/books', api.views.BookViewSet)
router.register(r'api/users', api.views.UserViewSet)
router.register(r'api/takes', api.views.TakeViewSet)
router.register(r'api/comments', api.views.CommentViewSet)

urlpatterns = [
    url(r'^(?!api).*$', api.views.frontend.FrontendAppView.as_view()),
    url(r'^api/$', api.views.index, name='index'),
    url(r'^api/upload/(?P<filename>[^/]+)$', api.views.FileUploadView.as_view()),
    url(r'^api/resumable_upload/(?P<filename>[^/]+)/$', api.views.ResumableFileUploadView.as_view()),
    url(r'^api/source/(?P<filename>[^/]+)$', api.views.UploadSourceFileView.as_view()),
    url(r'^api/get_project_takes/$', api.views.GetProjectTakesView.as_view()),
    url(r'^api/update_project_takes/$', api.views.UpdateProjectTakesView.as_view()),
    url(r'^api/get_source/$', api.views.SourceFileView.as_view()),
    url(r'^api/zip_files/$', api.views.ProjectZipFilesView.as_view()),
    url(r'^api/exclude_files/$', api.views.ExcludeFilesView.as_view()),
    url(r'^api/all_projects/$', api.views.AllProjectsView.as_view()),
    url(r'^api/get_chapters/$', api.views.ProjectChapterInfoView.as_view()),
    url(r'^api/get_langs/$', api.views.getLangsView.as_view()),
    url(r'^api/get_versions/$', api.views.getVersionsView.as_view()),
    url(r'^api/get_books/$', api.views.getBooksView.as_view()),
    url(r'^api/push_takes/$', api.views.PushTakesView.as_view()),
    url(r'^api/stitch_takes/$', api.views.SourceStitchView.as_view()),
]

urlpatterns += router.urls
