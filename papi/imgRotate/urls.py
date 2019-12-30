from django.contrib import admin
from django.urls import include,path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import api_test
from . import api_imgOcr
from . import api_gif

app_name = 'imgRotate'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', api_test.test),  # 添加api中 test 路由
    path('imgRotate/', api_imgOcr.img_rotate),               #添加api中 img_rotate 路由
    path('imgOcr/', api_imgOcr.img_ocr),                     #添加api中 img_ocr 路由
    path('gifRemoveLogo/', api_gif.gif_logo_remove),  # 添加api中 gif_logo_remove 路由
    path('logoLocate/', api_gif.pic_logo_location),  # 添加api中 pic_logo_location 路由
]