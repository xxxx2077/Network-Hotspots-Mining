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