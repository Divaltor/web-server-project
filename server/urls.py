from django.conf import settings
from django.conf.urls import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from server.views import (
    ItemViewSet,
    LoginView,
    items_page,
    item_view,
    ItemUpdateView,
    CategoryViewSet,
    main_page,
    register_view,
)

router = DefaultRouter(trailing_slash=False)
router.register('items', ItemViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', main_page),
    path('api/', include(router.urls)),
    path('items/', items_page, name='items'),
    path('items/<uuid:pk>', ItemUpdateView.as_view()),
    path('items/add', item_view),
    path('auth/login', LoginView.as_view()),
    path('auth/register', register_view),
    *static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]