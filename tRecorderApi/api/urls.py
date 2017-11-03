from django.conf.urls import url
from rest_framework import routers
from api.views import GetChunks, GetTakes, GetComments, CommentViewSet, TakeViewSet, AnthologyViewSet
from .views import book

router = routers.DefaultRouter()
# router.register(r'projects', views.ProjectViewSet)
# router.register(r'chapters', views.ChapterViewSet)
# router.register(r'chunks', views.ChunkViewSet)
# router.register(r'languages', views.LanguageViewSet)
router.register(r'books', book.BookViewSet)
# router.register(r'users', views.UserViewSet)
router.register(r'takes', TakeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'anthologies', AnthologyViewSet)

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
    # url(r'^resumable_upload/(?P<filename>[^/]+)/$', views.ResumableFileUploadView.as_view()),
    # url(r'^source/(?P<filename>[^/]+)$', views.UploadSourceFileView.as_view()),
    # url(r'^get_project_takes/$', views.GetProjectTakesView.as_view()),
    # url(r'^update_project_takes/$', views.UpdateProjectTakesView.as_view()),
    # url(r'^get_source/$', views.SourceFileView.as_view()),
    # url(r'^zip_files/$', views.ProjectZipFilesView.as_view()),
    # url(r'^exclude_files/$', views.ExcludeFilesView.as_view()),
    # url(r'^all_projects/$', views.AllProjectsView.as_view()),
    # url(r'^get_chapters/$', views.ProjectChapterInfoView.as_view()),
    # url(r'^get_langs/$', views.getLangsView.as_view()),
    # url(r'^get_versions/$', views.getVersionsView.as_view()),
    # url(r'^get_books/$', views.getBooksView.as_view()),
    # url(r'^push_takes/$', views.PushTakesView.as_view()),
    # url(r'^stitch_takes/$', views.SourceStitchView.as_view()),
    url(r'^get_chunks/$', GetChunks.as_view()),
    url(r'^get_takes/$', GetTakes.as_view()),
    url(r'^get_comments/$', GetComments.as_view())
    url(r'^get_books/$', book.GetBooksView.as_view())
]

urlpatterns += router.urls
