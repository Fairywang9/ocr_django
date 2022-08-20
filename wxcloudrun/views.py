import json
import logging
import os
# !pip install paddleocr
# from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render
# from paddleocr import PaddleOCR
# import paddleocr
# from paddleocr.tools.infer.utility import draw_ocr

from wxcloudrun.models import Counters
# 导入url模块
from django.conf.urls import url

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     url(r'^hello/$', views.hello)
# ]

logger = logging.getLogger('log')


def result(request):
    return HttpResponse("Hello world!")

    
def ocr_detect(filePath:str):
    '''
     orc识别
    '''
    # print(<span data-raw-text="" "="" data-textnode-index-1652755033716="165" data-index-1652755033716="2672" class="character">"filePath is <span data-raw-text="" "="" data-textnode-index-1652755033716="165" data-index-1652755033716="2685" class="character">",filePath)
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # need to run only once to download and load model into memory
    result = ocr.ocr(filePath, cls=True)
    result_list = result
    (path,fileName) = os.path.split(filePath)
    image = Image.open(filePath).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./template/fonts/Deng.ttf')
    im_show = Image.fromarray(im_show)
    return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    # im_show.save(os.path.join(path,<span data-raw-text="" "="" data-textnode-index-1652755033716="211" data-index-1652755033716="3254" class="character">"draw-<span data-raw-text="" "="" data-textnode-index-1652755033716="211" data-index-1652755033716="3260" class="character">"+fileName))







def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})
