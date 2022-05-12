from django.urls import path
from register.views import views
from register.views import user_operator


app_name = 'register'
urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    # ユーザー登録・修正
    path('signup/', user_operator.TempUserCreateView.as_view(), name='signup'),
    path('signup_done/', user_operator.TempUserDoneView.as_view(), name='temp_user_done'),
    path('user_list/', user_operator.UserListView.as_view(), name='user_list'),
    path('user_update/<int:pk>/', user_operator.UserManagementView.as_view(), name='user_update'),
    # path('pwd_update/<int:pk>/', user_operator.UserPasswordUpdate.as_view(), name='pwd_update'),
    # ユーザー削除
    path('delete_user/<int:pk>', user_operator.DeleteUserView.as_view(), name='delete_user'),
]
