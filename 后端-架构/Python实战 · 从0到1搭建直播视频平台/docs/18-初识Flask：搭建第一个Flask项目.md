你好，我是Barry。

从这节课开始，我们就进入到后端实战篇。这个章节重点培养的是我们从0到1做项目后端开发的能力。我们将经历从代码设计到具体功能的模块接口开发，深度体验独立平台搭建和后端开发的完整链路，学会灵活应用框架技术来应对多种类型的项目需求。

这节课，我们要拿下的就是后端部分的第一个核心知识点—— Flask 项目搭建。之所以选择基于Python的Flask框架，是因为它更合适用来完成视频直播平台的后端开发。

## 为什么选用Flask

为了让你知道选型的来龙去脉。我们先聊聊为什么要选用Flask框架，而不是选择使用Django这个应用也很广泛的框架呢？

这就要说到Flask和Django的区别了。首先，二者都是企业当中用的很多的Web的后端框架。接下来，我们一起来看一下二者的对比。

Flask主要有两大优点。第一个优点，它是轻量级Python开发框架。意思就是Flask核心就是几个文件，不用大量的配置文件，很快就能搭建起来一个小型的Web应用并快速启动运行，很适合搞微服务。

第二个优点就是灵活，其实这不光是Flask的优点，也是Python的优点，因为Flask是基于Python的Web应用框架。灵活的地方就在于这个框架用的人多，整体生态比较好。Flask有很多别人做好的扩展包，并且整体处在一个持续的维护和更新状态，我们可以灵活使用这些包和库做定制和扩展。它的API部分也不需要大量的配置文件和模板，几行代码就可以完成一个实现简单功能的应用。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：微服务需要很多组件，比如springCloud就包括配置中心、服务发现、网关、负载均衡等。Flask做微服务，功能组件齐全吗？
Q2：get_weather绑定到url上，是个笔误吧。
文中有“把 get_weather 函数绑定到 “&#47;weather&#47;” 的 URL 路径上”，感觉是weather函数绑定到url的，也许是个笔误。
Q3：Flask不能用python语言访问数据库吗？
Q4：用PyCharm，每个项目都需要指定python.exe吗？
Q5：对于文件夹的解释，“libs”和”thirdparty”的解释不太对吧。 Thirdparty:存放用户上传的头像等。”libs”：包含了管理后台的一些函数或工具等。
Q6：平级目录怎么变成包含关系了？
“后面是对应的项目目录图，你可以对照图片来了解文件之间的层级关系”，这句话下面有两个图，上面的图中目录还是平级关系，下面怎么就不是平级了？（紧挨着下面的图同样）
Q7：怎么判断是main模块？
Hello_world.py为什么是main模块？标志是什么？是放在特定目录下面就是main吗？  如果在hello_world.py同样的目录下面创建一个aaa.py，也是main吗？
另外，放在哪个目录下面就不会是main了？</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/df/a64b3146.jpg" width="30px"><span>长林啊</span> 👍（1） 💬（1）<div>老师，每次在新加一个路由后，就需要重新运行程序，否则就访问不到新加的路由，有什么方式可以实现热重载呢？</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/df/a64b3146.jpg" width="30px"><span>长林啊</span> 👍（1） 💬（1）<div>实现——用户输入不同 URL，页面显示不同内容
——————————————————————

from flask import Flask  # 导入Flask模块

app = Flask(__name__)  # 创建Flask实例，并指定模块名


@app.route(&#39;&#47;&#39;)  # 定义路由，即当访问 根目录 时返回下面的函数结果
def hello_world():
    return &#39;Hello, World!&#39;  # 返回字符串Hello, World!


@app.route(&#39;&#47;any&#47;&lt;content&gt;&#39;)
def other(content):
    return &#39;输入的内容是：{}&#39;.format(content)


if __name__ == &#39;__main__&#39;:
    app.run()  # 运行Flask应用程序


————————————————
浏览器或者postman 中访问：http:&#47;&#47;127.0.0.1:5000&#47;any&#47;flask
现实结果为：输入的内容是：flask
</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（1）<div>第18讲打卡~ 入门Flask</div>2024-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/5e/31/a6c2515c.jpg" width="30px"><span>        </span> 👍（0） 💬（1）<div>思考题如下： 通过判断请求url来触发返回消息 </div>2024-02-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELrxUK36wj3AesBNLK4tPibu7URiaI48cMWho2t8bfZOyfYDnQwQu2TTXibIbGVZ8DkPhNXDGr7VTfOJv1R1ccw1KBv5qfbq1bYvDhL1MtAVjISA/132" width="30px"><span>Aegean Sea</span> 👍（0） 💬（1）<div>python是哪个版本</div>2023-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ae/f5/a17bbcc9.jpg" width="30px"><span>蜡笔小新爱看书</span> 👍（0） 💬（1）<div>前端的章节里，怎么没介绍用哪个IDE的？</div>2023-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（2）<div>前端的终于过去了 我亲爱的老师前端完整代码上传了吗 嘻嘻😁</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/5e/31/a6c2515c.jpg" width="30px"><span>        </span> 👍（0） 💬（0）<div># -*- coding:utf-8 -*-

&#39;&#39;&#39;你可以尝试设置两个路由，实现——用户输入不同 URL，页面显示不同内容。&#39;&#39;&#39;

from flask import Flask, jsonify
from flask import request
from datetime import datetime

app = Flask(__name__)

def handle_request():
    # 根据请求的路由判断如何返回消息
    if request.path == &#39;&#47;date&#39;:
        current_date = datetime.now().strftime(&#39;%Y-%m-%d&#39;)
        return f&#39;当前日期为{current_date}&#39;
    elif request.path == &#39;&#47;url&#39;:
        data = {
            &#39;url&#39;: request.url,
            &#39;addr&#39;: request.remote_addr
        }
        return jsonify(data)
    else:
        return &#39;404&#39;


@app.route(&#39;&#47;date&#39;)
@app.route(&#39;&#47;url&#39;)
def view():
    return handle_request()

if __name__ == &#39;__main__&#39;:
    app.run()

</div>2024-02-21</li><br/>
</ul>