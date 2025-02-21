你好！我是Barry。

通过前面课程的数据库实战，相信你已经能熟练应用数据库了。接下来,我们就来学习功能接口模块化开发。

为什么需要模块化开发呢？随着Flask项目的程序越来越复杂，我们在项目开发和迭代管理上都会成倍消耗精力。为了提升效率，就需要对项目里的请求方法进行封装管理，并且把项目划分成多个单独的功能模块，让每个模块负责不同的处理功能，再通过路由分配把各模块连接成一个完整的Flask项目。

那么在Flask框架中，我们如何实现模块化呢？这就要用到今天要学的内容——蓝图和红图了。

## 什么是蓝图？

我们先通过一个案例，来了解一下蓝图能为我们解决什么问题。

### 案例解析

在我们的视频项目中，包含了首页、分区列表、视频详情等模块，我们先看看代码实现。

```plain
源程序app.py文件:
from flask import Flask

app=Flask(__name__)

@app.route('/')
def VideoIndex():
    return 'VideoIndex'

@app.route('/VideoList')
def VideoList():
    return 'VideoList'

@app.route('/VideoDetail')
def VideoDetail():
    return 'VideoDetail'

if __name__=='__main__':
    app.run()
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ec/58/7948ea79.jpg" width="30px"><span>胡歌衡阳分歌</span> 👍（1） 💬（2）<div>整个的项目目录结构不给我们，有的时候看着看着就懵了，我觉得需要补充一下
</div>2023-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a3/45/8e9c6a69.jpg" width="30px"><span>因为有你心存感激</span> 👍（1） 💬（0）<div>彻底被蓝图、宏图整蒙了
</div>2024-11-28</li><br/>
</ul>