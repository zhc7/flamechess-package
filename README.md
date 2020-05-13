# Flamechess Tools
这个包包含鹿棋（捉鳖）棋谱播放器、棋谱记录器，以及后续大部分的flamechess中的python部分
## 1 简介
### 1.1 安装方法
* 命令行输入`pip install flamechess`

*这个文档正在完善中......
## 2 具体模块介绍
### 2.1 棋谱记录器
#### 2.1.1 使用方法
* 直接运行：按照指示输入`code1`和`code2`
* 作为引用或在命令行：调用main函数，参数为`code1`, `code2`
#### 2.1.2 程序结构
* `ChessBoard`类用于获取和设置棋盘
* `tpe`函数用于判断棋盘码类型并选择API
* `Recorder`类用于作为记录器，记录棋谱
* `main`函数作为入口函数调用Recorder类执行相关操作
### 2.2 鹿棋（捉鳖）棋谱播放器
#### 2.2.1 使用方法
##### 2.2.1.1 棋谱写法
##### 2.2.1.2 config.ini写法
* section名称为棋类的名称，推荐使用英文或拼音，提高兼容性
* 具体需要的参数： 

| 参数名称 | 可设置的值 | 意义 |
| ------ | -------- | ---- |
| `chess_type` | `luqi`/`zhuobie`/... | 同section名 |
| `policy_file` | `*.txt` | 棋谱策略文件名 |
| `board_size` | `[int, int]` | 棋盘大小 |
| `reading_size` | `[int, int]` | 要读取的区域的大小 |
| `mirror` | `True`/`False` | 是否镜像 |
| `rotation` | `True`/`False` | 是否旋转 |
| `read_continuously` | `True`/`False` | 是否采用连续读取方式 |


##### 2.2.1.3 启动方法
* 直接运行：按照指示输入棋的类型和棋盘码
* 作为引用或在命令行：调用main函数，参数为棋的类型（`chess_type`）和棋盘码（`code`）
#### 2.2.2 程序结构
* `State`类是棋盘状态的基类
* `Board`类负责执行主要操作  
*详情请见注释
#### 2.2.3 引用
* 引用了play.py中的`ChessBoard`和`tpe`，用于获取和设置棋盘
### 2.3 久棋规则
* 未完成的部分
## 3 更新日志
* 0.1.0 最初版本
* 0.1.1 解决了README.md不能渲染的bug
* 0.1.2 彻底解决了README.md不能渲染的bug
* 0.1.3 更新了README.md和url
* 0.1.4 修复了一些已知问题，删除了不该出现的文件
* 0.2.0 将luqi.py的棋盘接口改为了chessTerm的websocket接口，对README.md进行了一些修改完善，修复了若干已知问题
* 0.2.1 删除luqi.py的log记录