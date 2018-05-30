import qiniu
from ball import settings
from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data
import uuid
from PIL import Image  #pip install pillow
import io
import os

url = settings.MEDIA_URL
bucket_name = settings.QINIU_BUCKET_NAME
q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)

def qiniu_upload(key, localfile):
    _img = localfile.read()
    size = len(_img) / (1024 * 1024)  # 上传图片的大小 M单位
    print(size)
    image = Image.open(io.BytesIO(_img))
    key = str(uuid.uuid1()).replace('-', '') + '.' + image.format
    token = q.upload_token(bucket_name, key, 3600)
    print(token)
    name = 'upfile.{0}'.format(image.format)  # 获取图片后缀（图片格式）
    if size > 1:
        x, y = image.size
        im = image.resize((int(x / 1.73), int(y / 1.73)), Image.ANTIALIAS)  # 等比例压缩 1.73 倍
        print('压缩')
    else:
        print('不压缩')
        im = image
    # im = image
    print(name)
    im.save('./media/' + name)  # 在根目录有个media文件
    path = './media/' + name
    ret, info = qiniu.put_file(token, key, path)
    if ret:
        return '{0}{1}'.format(url, ret['key'])
    else:
        return 'error'