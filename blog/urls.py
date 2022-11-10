from django.urls import re_path,path
from . import views

urlpatterns =[
    path("register/",views.Register, name="register"),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),

    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("user_profile/<int:myid>/", views.user_profile, name="user_profile"),
    
    path('',views.index,name='main'),
    path('post/',views.PostListView.as_view(),name='post_list'),
    # path('',views.PostListView.as_view(),name='post_list'),
    path('about/',views.AboutView.as_view(),name='about'),
    # path("add_blogs/", views.add_blogs, name="add_blogs"),
    path('drafts/',views.DraftListView.as_view(),name='post_draft_list'),

    path('post/new/',views.CreatePostView.as_view(),name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/$',views.PostDetailView.as_view(),name='post_detail'),
    re_path(r'^post/(?P<pk>\d+)/edit/$',views.PostUpdateView.as_view(),name='post_edit'),
    re_path(r'^post/(?P<pk>\d+)/remove/$',views.PostDeleteView.as_view(),name='post_remove'),
    re_path(r'^post/(?P<pk>\d+)/comment/$',views.add_comment_to_post,name='add_comment_to_post'), #function urls
    re_path(r'^comment/(?P<pk>\d+)/approve/$',views.comment_approve,name='comment_approve'),
    re_path(r'^comment/(?P<pk>\d+)/remove/$',views.comment_remove,name='comment_remove'),
    re_path(r'^post/(?P<pk>\d+)/publish/$',views.post_publish,name='post_publish'),
]
