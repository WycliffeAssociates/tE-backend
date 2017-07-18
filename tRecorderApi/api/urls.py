from django.conf.urls import url
from rest_framework import routers

from .views_sets import version_list, index, language, book, file_upload,comment, user, file_stream, take, source_file, source_file_upload, exclude_files,index,helpers,project,project_chapter_info,project_zip_file,all_projects

#sys.path.append("./views_sets")

router = routers.DefaultRouter()
router.register(r'languages', language.LanguageViewSet)
router.register(r'books', book.BookViewSet)
router.register(r'users', user.UserViewSet)
router.register(r'takes', take.TakeViewSet)
router.register(r'comments', comment.CommentViewSet)

urlpatterns = [
    url(r'^get_versions/$', version_list.getVersionsView.as_view()),
    #url(r'^$', index.index, name='index'),
    url(r'^upload/(?P<filename>[^/]+)$', file_upload.FileUploadView.as_view()),
    url(r'^stream/(?P<filepath>.*)$', file_stream.FileStreamView.as_view()),
    url(r'^get_project/$', project.ProjectView.as_view()),
    url(r'^get_source/$', source_file.SourceFileView.as_view()),
    url(r'^zipFiles/$', project_zip_file.ProjectZipFilesView.as_view()),
    url(r'^exclude_files/$', exclude_files.ExcludeFilesView.as_view()),
    url(r'^all_project/$', all_projects.AllProjectsView.as_view()),
    url(r'^get_chapters/$', project_chapter_info.ProjectChapterInfoView.as_view()),
    url(r'^source/(?P<filename>[^/]+)$', source_file_upload.UploadSourceFileView.as_view()),
]

urlpatterns += router.urls
