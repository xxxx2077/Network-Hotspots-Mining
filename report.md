# Development report



## 运行须知

子项目的readme文件中有的东西可以不写，说明一下该子项目负责的模块功能就行

### 爬虫

#### 注意事项

- 开发和测试使用python3.11，版本不要太低应该都可以

  **不推荐python3.12，后续安装paddleocr时会报错缺少lmdb，需要自己配置**

- 日志记录功能目前在Linux环境可用，Windows下会报错（可以禁用日志功能）

#### 运行前准备

- 安装百度飞桨paddlepaddle（用于运行ocr）

  参考[官方安装文档](https://www.paddlepaddle.org.cn/install/quick)

  （以2.6版本，Linux系统，cpu驱动，conda安装为例）

  ```
  conda install paddlepaddle==2.6.1 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/
  ```

- 安装依赖

  终端进入项目路径`SchoolMarket`后，输入以下命令
  ```
  pip install -r requirements.txt
  ```

*requirements_conda.txt是conda list -e生成*

*requirements_env.txt是pip list --format=freeze生成*

*爬虫运行环境可以参考以上两个txt文件*

#### 运行和结束

- ssh退出后，Linux服务器上依然运行：`nohup <command> &`
  (例如`nohup python main.py &`)
  - 错误重定向输出至error.log：`nohup python main.py > logs/error.log 2>&1 &`
  - 不记录终端输出（日志中已记录）：`nohup python main.py > /dev/null 2>&1 &`
  
- 查看进程：`ps -ef | grep main.py`*注意父子进程*
  - 父进程是运行main.py
  - 子进程运行爬虫，每次运行结束关闭该进程
- 结束：`kill -9 <process_id>`

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

```
SchoolMarket/
├── config                // 自定义的配置文件
│   ├── db_config.py             // 数据库连接配置
│   └── spider_config.py         // 爬虫配置
├── __init__.py
├── items.py              // scrapy的item（暂存爬取数据）
├── logs                  // 日志以及日志备份（7天）
│   ├── scrapy_log.log
|   ...
│   └── scrapy_log.log.2024-07-13
├── main.py               // 运行文件
├── middlewares.py        // scrapy中间件
├── pipelines.py          // scrapy流水线（处理爬取的数据）
├── settings.py           // scrapy设置
├── spiders               // scrapy爬虫
│   ├── __init__.py
│   ├── home.py                 // 首页爬虫
│   ├── hot.py                  // 热榜爬虫
│   └── trace.py                // 追踪爬虫
└── utils                 // 自定义组件
    ├── __init__.py
    ├── calculate_hot.py            // 计算热度值和热度增长
    ├── connect_pool.py             // 数据库连接池
    ├── correlation_cal_bert.py     // 计算帖子相关度（用bert模型）
    ├── correlation_cal_w2c.py      // 计算帖子相关度（用w2c）
    ├── database.py                 // 数据库操作
    ├── ocr.py                      // 光学字符识别
    ├── sentiment_Rateing.py        // 情感分析
    └── stopwords        // 各种停用词表（情感分析分词用）
        ├── stopwords_all.txt
        ├── .....
        └── stopwords_scu.txt
```

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

#### 技术工作
- 爬虫

  基于Scrapy框架开发，定时对“赞噢校园集市·中大站”的帖子内容及其评论进行爬取。根据热度值以及热度值的增长率，追踪可能的热点帖子。每天的爬虫信息会存储到相应日期的.log文件中，会定时清理过旧的日志。

- OCR

  采用百度飞桨(paddle)的开源轻量化模型ppocr_v4，对校园集市帖子中的图片进行OCR，实现图转文，为帖子补充信息

- 数据库连接和操作

  维护数据库连接池，避免频繁连接数据库导致性能下降。参数化执行SQL语句，防止注入攻击和提高性能。

- 设计爬虫项目框架逻辑
  
  将OCR、情感分析、热度计算、相关度计算、数据库连接等功能封装，在爬虫的相应位置调用，实现爬虫数据预处理以及存入Mysql数据库。

#### 遇到的问题以及解决办法
- 赞噢校园集市页面只能在微信浏览器打开

  - 问题：

    微信浏览器不允许打开开发者工具进行页面调试，也导致难以分析页面元素进行过滤。若用一些个人开发的插件魔改微信浏览器，有封号的风险。

  - 解决方法：

    用抓包工具Charles，分析打开集市不同页面的数据流。发现传输集市内容数据的json文件以及相关图片，可以通过一般的网络请求获取。只需要使用合法的用户token，改写url和相应的请求参数，即可获取想要的页面信息。


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