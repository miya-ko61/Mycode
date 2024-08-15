要使用 Django 创建一个简单的示例（Demo），我们可以创建一个基本的博客应用，其中用户可以发布和查看文章。以下是一个简要的步骤指导：

### 步骤 1: 安装 Django

首先，需要确保 Django 已安装。如果尚未安装，可以使用 pip 进行安装：

```bash
pip install django
```

### 步骤 2: 创建 Django 项目

创建一个新的 Django 项目。例如，我们将其命名为 `myblog`：

```bash
django-admin startproject myblog
cd myblog
```

### 步骤 3: 创建 Django 应用

在项目中创建一个应用来处理博客的逻辑：

```bash
python manage.py startapp blog
```

### 步骤 4: 设置 Django 项目

在 `myblog/settings.py` 文件中，将 `blog` 应用添加到 `INSTALLED_APPS` 列表中：

```python
INSTALLED_APPS = [
    ...
    'blog',
]
```

### 步骤 5: 定义模型

在 `blog/models.py` 中定义一个简单的 `Post` 模型，表示博客文章：

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### 步骤 6: 迁移数据库

在创建模型后，需要将其迁移到数据库中：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 步骤 7: 创建视图

在 `blog/views.py` 中，创建视图以显示所有博客文章：

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
```

### 步骤 8: 配置 URL

在 `myblog/urls.py` 中，将 `post_list` 视图连接到 URL：

```python
from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list, name='post_list'),
]
```

### 步骤 9: 创建模板

在 `blog/templates/blog/` 文件夹中创建 `post_list.html` 模板：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog</title>
</head>
<body>
    <h1>Blog Posts</h1>
    <ul>
        {% for post in posts %}
            <li>
                <h2>{{ post.title }}</h2>
                <p>{{ post.content }}</p>
                <small>Published on {{ post.created_at }}</small>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
```

### 步骤 10: 运行开发服务器

完成上述步骤后，可以启动 Django 开发服务器，并查看应用：

```bash
python manage.py runserver
```

打开浏览器，访问 `http://127.0.0.1:8000/`，你将会看到一个简单的博客文章列表。

这个示例展示了如何使用 Django 构建一个简单的博客应用，涵盖了项目创建、应用创建、模型定义、视图、模板及 URL 配置等核心内容。
