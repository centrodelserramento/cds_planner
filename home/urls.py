from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path(''       , views.index,  name='index'),
  path('tables/', views.tables, name='tables'),
  path('calendario/', views.calendario, name='calendario'),
  path("posa/<pk>/", views.PosaUpdateView.as_view(), name="posa-update"),
  path("ordine/<numero_ordine>/", views.ordine, name="ordine"),
  path("crea-posa/<numero_ordine>/", views.crea_posa),
  path("posa/<pk>/cancella", views.cancella_posa, name="cancella-posa"),

]
