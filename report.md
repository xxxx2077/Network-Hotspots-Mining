# Development report



## 运行须知

子项目的readme文件中有的东西可以不写，说明一下该子项目负责的模块功能就行

### 爬虫



### 数据库



### 后端

安装依赖

```
pip install -r requirements.txt
```

启动项目

```
python3 manage.py runserver
```



### 前端

在`hotpoints`目录下：

- 安装依赖

  ```bash
  npm install
  ```

- 启动

  ```bash
  npm run serve
  ```

## 代码结构

主要保留二次开发的可能，说明开发需要用到的某某文件用处用途，写完后我会统一放在子文件的readme里

### 爬虫



### 数据库



### 后端

```
├── Network_Hotspots_Mining         # 项目根目录，项目名为Network Hotspots Mining
│   ├── app                         # Django应用目录
│   │   ├── admin.py                	# Django admin后台配置
│   │   ├── apps.py                 	# Django应用定义文件
│   │   ├── controller              	# 控制器模块，存放处理业务逻辑的脚本
│   │   │   ├── LLM.py              		# 处理语言模型相关功能的脚本
│   │   │   ├── __pycache__          		# Python编译后的字节码缓存目录
│   │   │   │   ├── LLM.cpython-310.pyc  		# LLM.py对应的字节码文件
│   │   │   │   └── single_pass.cpython-310.pyc 	# single_pass.py对应的字节码文件
│   │   │   └── single_pass.py      		# single-pass聚类算法文件
│   │   ├── data                    	# 存放数据文件的目录
│   │   │   ├── data1.txt           		# 示例数据文件1
│   │   │   └── stop_words.txt      		# 停用词文件，常用于文本预处理
│   │   ├── __init__.py             	# 初始化文件，用于定义模块属性
│   │   ├── migrations              	# 数据库迁移文件目录，记录模型变更历史
│   │   │   ├── 0001_initial.py     		# 初始数据库迁移脚本
│   │   │   ├── __init__.py         		# 迁移模块初始化文件
│   │   │   └── __pycache__         		# 迁移脚本的字节码缓存
│   │   ├── misc                    	# 杂项或辅助脚本目录
│   │   │   ├── clear_db.py         		# 清空数据库脚本
│   │   │   ├── data_processing.py  		# 数据处理脚本
│   │   │   ├── __pycache__         		# 杂项脚本的字节码缓存
│   │   │   └── test.py             		# 测试脚本或示例脚本
│   │   ├── models.py               	# 定义Django模型（数据库表结构）的文件
│   │   ├── __pycache__             	# app模块中各py文件的字节码缓存
│   │   ├── result                  	# 存放处理结果或报告的目录
│   │   │   ├── ...                 		# 各种结果文件
│   │   ├── tasks.py                	# Celery异步任务定义文件
│   │   ├── tests.py                	# 单元测试文件
│   │   ├── util                    	# 工具函数或模块目录
│   │   │   ├── data_analysis.py    		# 数据分析工具脚本
│   │   │   ├── __pycache__         		# 工具模块的字节码缓存
│   │   │   └── util.py             		# 工具函数主文件
│   │   └── views.py                	# 视图函数定义，处理HTTP请求和响应
│   ├── manage.py                   # Django项目管理命令入口
│   └── Network_Hotspots_Mining     # 与项目同名的目录，可能包含了项目级别的配置
│       ├── asgi.py                 	# ASGI服务器配置文件，用于部署Web应用
│       ├── celery.py               	# Celery配置文件，用于任务队列设置
│       ├── __init__.py             	# 项目级别初始化文件
│       ├── __pycache__             	# 项目级别配置文件的字节码缓存
│       ├── settings.py             	# Django项目设置文件
│       ├── urls.py                 	# URL路由配置文件
│       └── wsgi.py                 	# WSGI服务器入口文件，用于生产环境部署
├── README.md                      # 项目说明文档，包含安装、使用等指导信息
└── requirements.txt               # 项目依赖列表文件，用于pip安装所需第三方库
```



### 前端

```
src/
│
├── api/					// 网络请求
│   ├── xxx.js
│   └── xxx.js
│
├── assets/					// 资源文件
│   └── xxx
│
├── components/				// 组件
│   ├── xxx.vue/
│   ...
│   └── xxx.vue2/
│
├── router/					// 路由
│   └── index.js
│
├── utils/					// 自定义功能函数
│   └── xxx
│
├── views/					// 页面文件
│   ├── HomeView/
│   └── Topic/
│
└── App.vue					// 入口文件
```

## 技术报告

展示技术工作以及个人贡献，顺序按ppt的来，简单讲讲用的什么怎么用的就行，留点开发建议。涉及个人工作的东西不会提交到最终的github上。

### 整体架构（不用写

### zjt

### sdp

### ywx

#### 调研阶段

调研事件总结、事件抽取方法，产出调研知识文档，提出尝试deepKE进行事件抽取的建议。

针对网络热点文本聚类方法和对Python语言下的后端框架进行调研，对实现难度和性能进行评估。

#### 开发阶段

个人从零搭建项目后端部分，完成后端部分开发。

- 实现后端与数据库对接，使后端能从数据库读取数据
- 基于SIngle-Pass算法实现新闻热点聚类
  - 设置停用词列表，形式为文件，通过读取文件可获取停用词列表。 
  - 切割句子cut_sentences： 接受文本或文本文件路径作为输入，使用jieba进行分词处理，并将分词后的文本转换为“空格+词”的字符串形式，同时构建文本ID到文本内容的映射。
  - 获取TF-IDF方法 get_tfidf： 将分词后的文本转换为TF-IDF矩阵表示，并将其转换为稠密列表形式返回。
  - 余弦相似度计算方法 cosion_simi： 计算给定向量与所有簇中心向量之间的余弦相似度，并返回最大相似度值及其对应的簇索引。 
  - 单遍聚类方法 single_pass： 对输入文本执行single_pass聚类算法。首先调用cut_sentences和get_tfidf方法预处理文本，然后遍历每个文本的TF-IDF向量，根据与已有簇中心的相似度决定是否加入现有簇或创建新簇。最后，将聚类结果保存到指定的JSON文件中。
- 与大模型API对接
  - 使用线程池并行技术对调用大模型API函数进行性能优化
  - 调用LLM API对事件聚类进行总结的同时计算每个聚类的热度和热度上升率
- 接口开发
  - 获取热度上升榜get_speedlist
  - 获取热度总值榜get_hotlist。
- 编写测试脚本（misc目录）
  - 数据预处理脚本data_processing.py
  - 清空数据库指定库表脚本clear_db.py
  - 测试部分后端接口功能脚本test.py

### hwy

### yzr

#### 调研阶段

针对事件抽取任务，对不同的事件抽取模型（如DeepKE、ERNIE-UIE等）进行调研，并在本地服务器部署。对不同的模型评估其效率、效果等。

#### 开发阶段

从零搭建项目前端部分，完成前端开发。

主要前端组件：

- Echarts：用于图表绘制
- DataV：用于非图表数据展示
- relation-graph：用于绘制事件关系图

为提高代码复用性、规范性、可读性等，将图表等可复用元素封装成组件。组件之间相互独立，提高前端程序的稳定性。