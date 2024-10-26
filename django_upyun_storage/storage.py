import os
from datetime import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
import upyun

@deconstructible
class UpYunStorage(Storage):
    """
    又拍云存储后端
    """
    
    def __init__(self):
        # 从设置中获取又拍云的配置信息
        self.service = settings.UPYUN_STORAGE.get('SERVICE')
        self.username = settings.UPYUN_STORAGE.get('USERNAME')
        self.password = settings.UPYUN_STORAGE.get('PASSWORD')
        # 初始化又拍云存储桶
        self.bucket = upyun.UpYun(self.service, self.username, self.password)
        
    def _open(self, name, mode='rb'):
        # 打开文件
        return self.bucket.get(self._get_key(name))
        
    def _save(self, name, content):
        # 保存文件
        key = self._get_key(name)
        if hasattr(content, 'chunks'):
            # 将内容转换为字节流
            self.bucket.put(key, b''.join(content.chunks()))
        else:
            self.bucket.put(key, content.read())
        return name
        
    def delete(self, name):
        # 删除文件
        self.bucket.delete(self._get_key(name))
        
    def exists(self, name):
        # 检查文件是否存在
        try:
            self.bucket.getinfo(self._get_key(name))
            return True
        except upyun.UpYunServiceException:
            return False
            
    def url(self, name):
        # 获取文件的URL
        return self.bucket.sign_url('GET', self._get_key(name))
        
    def size(self, name):
        # 获取文件大小
        key = self._get_key(name)
        return self.bucket.getinfo(key).size
        
    def get_modified_time(self, name):
        # 获取文件的最后修改时间
        key = self._get_key(name)
        return datetime.fromtimestamp(self.bucket.getinfo(key).mtime)
        
    def get_valid_name(self, name):
        # 获取有效的文件名
        return name
        
    def get_available_name(self, name, max_length=None):
        # 获取可用的文件名，如果文件已存在则添加数字后缀
        if self.exists(name):
            dir_name, file_name = os.path.split(name)
            file_root, file_ext = os.path.splitext(file_name)
            count = 1
            
            while self.exists(name):
                # 文件名.扩展名 -> 文件名_1.扩展名
                name = os.path.join(dir_name, f"{file_root}_{count}{file_ext}")
                count += 1
                
        return name
        
    def listdir(self, path):
        # 列出目录内容
        path = self._get_key(path)
        if path and not path.endswith('/'):
            path += '/'

        directories = set()
        files = []

        for obj in upyun.FileIterator(self.bucket, prefix=path):
            relative_path = obj.key[len(path):] if path != '/' else obj.key
            if not relative_path:
                continue

            # 如果包含 /，说明是子目录
            if '/' in relative_path:
                directories.add(relative_path.split('/')[0])
            else:
                files.append(relative_path)

        return list(directories), files

    def _get_key(self, name):
        # 获取文件在又拍云存储中的完整路径
        return name.lstrip('/')
