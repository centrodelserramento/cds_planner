from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from api import views


urlpatterns = [
    path("order/", views.OrderList.as_view()),
    path("order/<int:pk>/", views.OrderDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
