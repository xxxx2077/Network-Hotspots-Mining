
## 简介
 
这是一个基于scrapy框架的爬虫项目，用于爬取“赞噢校园集市”上的内容。

除了爬取帖子内容以外，还会
- 对图片进行OCR处理
- 对评论进行情感倾向分析
- 根据热度信息跟踪记录帖子变化
- 计算帖子和中大的相关程度
- 日志记录以及管理（Windows会报错，Linux可行）


----
## 使用说明

### 安装miniconda
[官方文档](https://docs.anaconda.com/miniconda/)

1. 查看架构

    Linux终端输入`uname -n`

2. 根据不同系统不同架构，选择相应文件安装
（以Linux x86-64为例）

  - 创建目录
  `mkdir -p ~/miniconda3`
  - 获取脚本文件（可以自己选择相应版本，替换.sh文件）
    - 官方源
  `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh`
    - 清华源（推荐，速度快）
  `wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_24.4.0-0-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh`
  - 执行安装脚本
  `bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3`
  - 删除sh脚本
  `rm -rf ~/miniconda3/miniconda.sh`

3. 初始化bash和zsh（重启终端后生效）

  - `~/miniconda3/bin/conda init bash`
  - `~/miniconda3/bin/conda init zsh`

#### conda虚拟环境
**不推荐python3.12，后续安装paddleocr时会报错缺少lmdb，需要自己配置**
1. 创建环境 (python3.11为例)
`conda create -n <env-name> python=3.11`

2. 切换/开启环境
`conda activate <env-name>`

*ps: 使用vscode时可能会出现两个虚拟环境。
第一个是vscode自动启动的，第二个是conda自动启动的。*

*Settings中设置`"terminal.integrated.shellIntegration.enabled": false`可以关闭vscode自动启动*

*终端输入命令`conda config --set auto_activate_base False`可以关闭conda自动启动*

### 安装百度飞桨paddlepaddle 
[官方安装文档](https://www.paddlepaddle.org.cn/install/quick)

（以2.6版本，Linux系统，cpu驱动，conda安装为例）

 `conda install paddlepaddle==2.6.1 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/`

### 从huggingface下载模型
1.安装官方的命令行工具
 `pip install -U "huggingface_hub[cli]"`

2.配置环境变量（镜像网站）
 `export HF_ENDPOINT=https://hf-mirror.com`（终端输入或者添加到.bashrc文件）

 *终端输入是临时的，需要`source ~/.bashrc`使之在该终端生效*

 *也可以在.bashrc中配置环境变量（长期有效）*

3.下载模型 
`huggingface-cli download --resume-download（模型名称） --local-dir (保存位置)`
--resume-download参数，支持断点续传，上一次下载没完成可以接着下载

*根据说明，默认支持断点续传，可以不加这个参数*
 

### 安装依赖
终端开启虚拟环境，进入项目路径后，输入命令
`pip install -r requirements.txt`
  - requirements_conda.txt是通过conda list -e > requirements_conda.txt创建
  - requirements_env.txt是通过pip list --format=freeze> requirements_env.txt创建
  - requirements.txt是通过pigar generate创建
----

### 运行
选择好相应的环境，运行main.py即可

- ssh退出，linux服务器依然运行：`nohup <command> &`
  (例如`nohup python main.py &`)
  - 错误重定向输出：`nohup python main.py > logs/error.log 2>&1 &`
  - 不记录输出：`nohup python main.py > /dev/null 2>&1 &`
  
- 查看进程：`ps -ef | grep main.py`*注意父子进程*
  - 父进程是运行main.py
  - 子进程运行爬虫，每次运行结束关闭该进程
- 结束：`kill -9 <process_id>`

*vscode可能需要在launch.json或者setting.json中配置模块导入路径*

----

## 其它
- 配置
  config文件夹中有相关配置参数，可以按需修改数据库设置以及爬虫设置
- 数据库
  - 共有4个表
  - 数据库结构参考mysql_struct.sql，应该可以直接导入mysql8.0

