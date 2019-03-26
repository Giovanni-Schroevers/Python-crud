from django.contrib import admin
from django.urls import path, include

handler404 = 'crud.views.handler404'
handler500 = 'crud.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crud.urls'))
]
