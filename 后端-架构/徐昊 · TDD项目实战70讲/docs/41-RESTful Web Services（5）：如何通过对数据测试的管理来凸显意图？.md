你好，我是徐昊。今天我们继续使用TDD的方式实现RESTful Web Services。

## 回顾架构愿景与任务列表

在上节课最后的视频演示中，我们发现了新的扩展点HeaderDelegate，调整后的架构愿景如下图所示：

![](https://static001.geekbang.org/resource/image/ed/2e/ed95e0629105b3fe661590be6ab4af2e.jpg?wh=2284x1285)  
![](https://static001.geekbang.org/resource/image/aa/56/aacdc2230e337d593308c0184b799956.jpg?wh=2284x1285)

调整后的任务列表为：

- ResourceServlet
  
  - 将请求派分给对应的资源（Resource），并根据返回的状态、超媒体类型、内容，响应Http请求
    
    - 使用OutboundResponse的status作为Http Response的状态
    - 使用OutboundResponse的headers作为Http Response的Http Headers
    - 通过MessageBodyWriter将OutboundResponse的GenericEntity写回为Body
    - 如果找不到对应的MessageBodyWriter，则返回500族错误
  - 当资源方法抛出异常时，根据异常影响Http请求
    
    - 如果抛出WebApplicationException，且response不为null，则使用response响应Http
    - 如果抛出WebApplicationException，而response为null，则通过异常的具体类型查找ExceptionMapper，生产response响应Http请求
    - 如果抛出的不是WebApplicationException，则通过异常的具体类型查找ExceptionMapper，生产response响应Http请求
- RuntimeDelegate
  
  - 为MediaType提供HeaderDelegate
  - 为CacheControl提供HeaderDelegate
  - 为Cookie提供HeaderDelegates
  - 为EntityTag提供HeaderDelegate
  - 为Link提供HeaderDelegate
  - 为NewCookie提供HeaderDelegate
  - 为Date提供HeaderDelegate
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（0）<div>学习感言
1、终于见到了 Builder 模式是怎么写出来的，之前都是自动生成的，不会写！
2、OutboundResponseBuilder 让构造测试数据变的超级简单，太神奇了！

对于重构与重写，你的理解是什么？
重构：在已有功能测试的保障下，按自己的喜好修改代码，但需要保证功能不变，老代码也会随之改变
重写：根据现有功能，按自己的喜好模仿出另一套功能一样的代码，不用理会老代码，也不会影响老代码

代码 https:&#47;&#47;github.com&#47;wyyl1&#47;geektime-tdd-framework&#47;tree&#47;5</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/22/7606c6ba.jpg" width="30px"><span>张铁林</span> 👍（0） 💬（0）<div>https:&#47;&#47;github.com&#47;vfbiby&#47;tdd-restful
步骤加代码</div>2022-06-20</li><br/>
</ul>