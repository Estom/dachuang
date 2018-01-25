from django.conf.urls import url
from dcweb import views
from django.conf import settings
from django.conf.urls.static import static
from dcweb.views import test

urlpatterns = [
    url(r'^test$', test, name='test'),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^rec$', views.IndexRecView.as_view(), name='index_rec'),
    url(r'^star$', views.IndexStarView.as_view(), name='index_star'),

    url(r'^category/(?P<cate_id>\d+)$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),

    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),

    url(r'^pub_list$', views.PublishView.as_view(), name='pub_list'),
    url(r'^pub_detail/(?P<pub_id>\d+)$', views.PubDetailView.as_view(), name='pub_detail'),

    url(r'^data$', views.DataView.as_view(),name='data'),

    url(r'^person$', views.PersonView, name='person'),
    url(r'^person_edit2$',views.PersonEdit, name='person_edit2'),
    url(r'person_edit',views.update_data, name='person_edit'),

    url(r'^logout', views.do_logout, name='logout'),
    url(r'^reg', views.do_reg, name='reg'),
    url(r'^login', views.do_login, name='login'),

    url(r'^article/love',views.love, name='love'),
    url(r'^pub_detail/staring',views.staring, name='staring'),
    url(r'^pub_detail/staroff',views.staroff,name='staroff'),
    # url(r'^pub_detail/(?P<pub_id>\d+)$',views.PublishDetailView.as_View(),name='pub_detail'),
    # url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    # url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)