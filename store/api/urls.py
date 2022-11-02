from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.api.views import OrderModelViewset, ItemModelViewset, OrderItemModelViewset
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView, TokenObtainPairView
import rest_framework

app_name = 'store'

router = DefaultRouter()

router.register('item', ItemModelViewset, basename='item')
router.register('orderitem', OrderItemModelViewset, basename='orderitem')
router.register('order', OrderModelViewset, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('gettoken/', TokenObtainPairView.as_view(), name='get-token'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh-token'),
    path('verifytoken/', TokenVerifyView.as_view(), name='verify-token'),

]
