from django.conf.urls import url
from dcweb import views
from dcweb import android_views
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
    url(r'^person_edit$',views.update_data, name='person_edit'),

    url(r'^logout', views.do_logout, name='logout'),
    url(r'^reg', views.do_reg, name='reg'),
    url(r'^login', views.do_login, name='login'),

    url(r'^article/love',android_views.love, name='love'),
    url(r'^pub_detail/staring',android_views.staring, name='staring'),
    url(r'^pub_detail/staroff',android_views.staroff,name='staroff'),


    url(r'^app$', android_views.IndexView.as_view(), name='app_index'),
    url(r'^app_rec$', android_views.IndexRecView.as_view(), name='app_index_rec'),
    url(r'^app_star$', android_views.IndexStarView.as_view(), name='app_index_star'),

    url(r'^app_category/(?P<cate_id>\d+)$', android_views.CategoryView.as_view(), name='app_category'),
    url(r'^app_tag/(?P<tag_id>\d+)$', android_views.TagView.as_view(), name='app_tag'),

    url(r'^app_article/(?P<article_id>\d+)$', android_views.ArticleDetailView.as_view(), name='app_detail'),

    url(r'^app_pub_list$', android_views.PublishView.as_view(), name='app_pub_list'),
    url(r'^app_pub_detail/(?P<pub_id>\d+)$', android_views.PubDetailView.as_view(), name='app_pub_detail'),

    url(r'^app_data$', android_views.DataView.as_view(),name='app_data'),

    url(r'^app_person$', android_views.PersonView, name='app_person'),
    url(r'^app_person_edit$', android_views.update_data, name='app_person_edit'),

    url(r'^app_logout', android_views.do_logout, name='app_logout'),
    url(r'^app_reg', android_views.do_reg, name='app_reg'),
    url(r'^app_login', android_views.do_login, name='app_login'),

    url(r'^app_article/love', android_views.love, name='app_love'),
    url(r'^app_pub_detail/staring', android_views.staring, name='app_staring'),
    url(r'^app_pub_detail/staroff', android_views.staroff,name='app_staroff'),
    # url(r'^pub_detail/(?P<pub_id>\d+)$',views.PublishDetailView.as_View(),name='pub_detail'),
    # url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    # url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)