"""apitest URL Configuration

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
from interface_platform.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index),
    url(r'^variable_detail/(.+)/$',variable_detail),
    url(r'^variable_new$',variable_new),
    url(r'^base_addstep/(.+)/$',base_addstep),
    url(r'^api_new$', api_new),
    url(r'^variable$', ctrl),
    url(r'^deal_result$', deal_result),
    url(r'^api_ctrl$', api_ctrl),
    url(r'^api_detail/(.+)/$', api_detail),
    url(r'^login$', login_),
    url(r'^signup$', signup),
    url(r'^new_project$', new_project),
    url(r'^variable_update$', variable_update),
    url(r'^apitest_post$', apitest_post),
    url(r'^apitest_get$', apitest_get),
    url(r'^api_update$', api_update),
    url(r'^getparentlevel$', getparentlevel),
    url(r'^newylj$', newylj),
    url(r'^getdirtree$', getdirtree),
    url(r'^responsible_list$', responsible_list),
    url(r'^newtestcase$', newtestcase),
    url(r'^addtestcasestep$', addtestcasestep),
    url(r'^logout_view$', logout_view),

    url(r'^new_its_req_header$', new_its_req_header),
    url(r'^new_its_req_body$', new_its_req_body),
    url(r'^new_its_res_header$', new_its_res_header),
    url(r'^new_its_res_body$', new_its_res_body),
    url(r'^getLevel3$', getLevel3),
    url(r'^runtestsuit$', run_testsuit),
    url(r'^showtestsuit/(.+)/$', showtestsuit),
    url(r'^updateStatus$', updateStatus),
]
