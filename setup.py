# setup.py
from setuptools import setup, find_packages

# 读取README文件，用于在PyPI上显示项目说明
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django5-upyun-storage",  # 项目名称
    version="1.0.4",  # 版本号
    author="Mircool",  # 作者名称
    description="又拍云 Django5 存储后端",  # 简短描述
    long_description=long_description,  # 长描述，通常来自README文件
    long_description_content_type="text/markdown",  # 长描述的格式，这里是Markdown
    url="https://github.com/mircool/django-upyun-storage.git",  # 项目网址
    project_urls={  # 项目相关URL
        "Bug Tracker": "https://github.com/mircool/django-upyun-storage/issues",
    },
    classifiers=[  # 分类器，用于描述项目的一些元数据
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
    ],
    package_dir={"": "."},  # 包目录
    packages=find_packages(where="."),  # 发现并包含所有子包
    python_requires=">=3.8",  # 指定Python版本要求
    install_requires=[  # 安装依赖
        "Django>=5.0",
        "upyun>=2.5.5",  # 添加 Upyun SDK 依赖
    ],
    keywords="django, upyun, storage, file upload",  # 关键词
)
