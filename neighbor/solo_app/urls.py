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

    # path('password_reset', views.password_reset),
    # path('password_reset/done/', views.password_reset_done),
    # path('password_change', views.password_change),
    # path('password_change/done/', views.password_change_done),

    # blog portion
    
    path('home/create_post', views.create_post),
    path('home/like_post/<int:post_id>', views.like_post),
    path('home/dislike_post/<int:post_id>', views.dislike_post),
    path('home/delete_post/<int:post_id>', views.delete_post),

    # question portion
    path('help', views.help),
    path('help/done', views.question_sent),
    path('help/post', views.question_confirmation),

    # # account edit portion
    path('my_account/<int:user_id>', views.my_account),
    path('my_account/<int:user_id>/update', views.update_account),

    # # marketplace portion
    path('marketplace', views.marketplace),
    path('marketplace/create_item', views.create_item),
    path('marketplace/mark_sold/<int:item_id>', views.mark_sold),
    path('marketplace/update_item/<int:item_id>', views.update_item),
    path('marketplace/updated/<int:item_id>', views.item_updated),
    path('marketplace/<int:item_id>', views.item_info),
    path('marketplace/delete_item/<int:item_id>', views.delete_item),

    # path('home/user/<int:user_id>', views.show_user_info),
    path('invite', views.invite_user),
    path('invite/done', views.invited),
    path('invite/sent', views.invite_confirmation),
]