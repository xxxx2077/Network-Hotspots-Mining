# Network-Hotspots-Mining
网络热点挖掘（后端）



## 环境配置 Quick Start

### Step 1：安装Django

```
pip install Django
```

安装完成后，你可以通过运行以下命令验证 Django 是否成功安装：

```
python3 -m django --version
```

如果一切顺利，你将看到安装的 Django 版本号，如：**4.2.7**。



如果遇到红色warning

```
You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
```

输入

```
python manage.py migrate
```

### Step 2：项目启动

```python
python manage.py runserver 0.0.0.0:8000
```



## 项目说明 Directory Description

- **Network-Hotspots-Mining:** 项目的容器。
- **manage.py:** 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。【不用动】
- **HelloWorld/wsgi.py:** 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。【不用动】
- **HelloWorld/asgi.py:** 一个 ASGI 兼容的 Web 服务器的入口，以便运行你的项目。【不用动】
- **HelloWorld/__init__.py:** 一个空文件，告诉 Python 该目录是一个 Python 包。
- **HelloWorld/settings.py:** 该 Django 项目的设置/配置。【经常修改】
- **HelloWorld/urls.py:** 该 Django 项目的 URL 声明，记录URL与对应执行函数的对应关系 【经常修改】
