from django.urls import path
from .import views

urlpatterns = [
    # main page (landing page)
    path('', views.index),
    path('home', views.index_authorized),
    # login portion
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('login_page', views.login_page),
    path('register_page', views.register_page),
    path('password_page', views.password_page),
    path('password_restore', views.password_restore),
    # blog portion
    # path('blog', views.blog),
    # path('create_post', views.create_post),
    # path('like_post/<int:post_id>', views.like_post),
    # path('dislike_post/<int:post_id>', views.dislike_post),
    # path('delete_post/<int:post_id>', views.delete_post),
    # path('user/<int:user_id>', views.show_posts),
    # # comments

    # # account edit portion
    # path('myaccount/<int:user_id>', views.show_account),
    # path('myaccount/<int:user_id>/update', views.update_account),

    # # marketplace portion
    # path('marketplace', views.marketplace),
    # path('create_item', views.create_item),
    # path('mark_sold/<int:item_id>', views.mark_sold),
    # path('update_item/<int:item_id>', views.update_item),
    # path('delete_item/<int:item_id>', views.delete_item),
    # path('user/<int:user_id>', views.show_user_info),
]