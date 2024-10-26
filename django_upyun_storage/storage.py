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
        self.domain = settings.UPYUN_STORAGE.get('DOMAIN',None)
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
        if self.domain:
            return f'{self.domain}/{self._get_key(name)}'
        else:
            return f'http://{self.service}.test.upcdn.net/{self._get_key(name)}'
        
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
        """
        获取可用的文件名，如果文件已存在则添加数字后缀
        确保使用正确的路径分隔符
        """
        if self.exists(name):
            dir_name, file_name = os.path.split(name)
            file_root, file_ext = os.path.splitext(file_name)
            count = 1
            
            # 确保目录名使用正确的路径分隔符
            dir_name = dir_name.replace('\\', '/')
            
            while self.exists(name):
                # 使用 / 作为路径分隔符
                if dir_name:
                    name = f"{dir_name}/{file_root}_{count}{file_ext}"
                else:
                    name = f"{file_root}_{count}{file_ext}"
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
        """
        获取文件在又拍云存储中的完整路径
        将 Windows 路径分隔符替换为 URL 路径分隔符
        """
        # 将 Windows 路径分隔符替换为 URL 路径分隔符
        name = name.replace('\\', '/')
        
        # 获取配置中的上传目录前缀，如果没有则使用空字符串
        upload_prefix = settings.UPYUN_STORAGE.get('UPLOAD_PREFIX', '').strip('/')
        
        # 组合路径
        if upload_prefix:
            name = f"{upload_prefix}/{name.lstrip('/')}"
        else:
            name = name.lstrip('/')
        
        return name
