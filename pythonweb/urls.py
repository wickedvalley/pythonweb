"""pythonweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from hotels import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^index.action', views.index),
    url(r'^index_main.action', views.index_main),
    url(r'^registry_ui.action', views.registry_ui),
    url(r'^login_ui.action', views.login_ui),
    url(r'^home.action', views.home),
    url(r'^hotel_order.action', views.hotel_order),
    url(r'^my_order.action', views.my_order),
    url(r'^index_search.action', views.index_search),
    url(r'^registry.action', views.registry),
    url(r'^login.action', views.login),
    url(r'^logout.action', views.logout),
    url(r'^home_main.action$', views.home_main),
    url(r'^home_search.action$', views.home_search),
    url(r'^password_ui.action$', views.password_ui),
    url(r'^edit_password.action$', views.edit_password),
    url(r'^add_comment.action$', views.add_comment),
    url(r'^book_hotel.action$', views.book_hotel),
    url(r'^all_orders.action$', views.all_orders),

]
