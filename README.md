# Django5 又拍云存储

用于又拍云的 Django5 存储后端。

## 安装

```bash
pip install django5-upyun-storage
```

## 配置
在您的 Django settings.py INSTALLED_APPS 中添加以下设置：

```python
INSTALLED_APPS = [
    ...
    'django5_upyun_storage',
    ...
]
```


在您的 Django settings.py 中添加以下设置：

```python
UPYUN_STORAGE = {
    'SERVICE': '服务名称',
    'USERNAME': '授权账户',
    'PASSWORD': '授权密码',
    'DOMAIN': '绑定域名', # 可选，如果为空，则使用又拍云的默认域名 http://yourdomain.com
}

# 设置为默认存储器
STORAGES = {
    'default': {
        'BACKEND': 'django5_upyun_storage.storage.UpYunStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    }
}
```

## 使用

```python
from django.db import models

class YourModel(models.Model):
    file = models.FileField(upload_to='uploads/')
    image = models.ImageField(upload_to='images/')
```

## 特性

- 兼容 Django 5.0+
- 支持所有基本文件操作
- 处理文件删除
- 可配置的上传路径
- 支持静态文件存储

## 许可证

MIT 许可证

## 贡献

欢迎贡献！请随时提交拉取请求。