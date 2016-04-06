from django.conf.urls import url, include
from rest_framework import routers
from manager import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^create_models/$', views.create_models),
    url(r'^update_models/$', views.update_models),
    url(r'^remove_models/$', views.remove_models)
]