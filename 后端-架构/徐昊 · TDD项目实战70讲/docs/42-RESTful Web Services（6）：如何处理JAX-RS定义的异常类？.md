你好，我是徐昊。今天我们继续使用TDD的方式实现RESTful Web Services。

## 回顾架构愿景与任务列表

目前我们的架构愿景如下：

![](https://static001.geekbang.org/resource/image/ed/2e/ed95e0629105b3fe661590be6ab4af2e.jpg?wh=2284x1285)  
![](https://static001.geekbang.org/resource/image/aa/56/aacdc2230e337d593308c0184b799956.jpg?wh=2284x1285)

任务列表为：

- ResourceServlet
  
  - 将请求派分给对应的资源（Resource），并根据返回的状态、超媒体类型、内容，响应Http请求
    
    - 使用OutboundResponse的status作为Http Response的状态
    - 使用OutboundResponse的headers作为Http Response的Http Headers
    - 通过MessageBodyWriter将OutboundResponse的GenericEntity写回为Body
    - 如果找不到对应的MessageBody，则返回500族错误
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
<li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/22/7606c6ba.jpg" width="30px"><span>张铁林</span> 👍（1） 💬（1）<div>https:&#47;&#47;github.com&#47;vfbiby&#47;tdd-restful&#47;blob&#47;main&#47;doc&#47;Geektime%20TDD%2042.md
这是操作步骤，我是先看视频纪录，再自己跟着步骤做，相当于检查了一遍。
这章做了3次提交，</div>2022-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>代码 https:&#47;&#47;github.com&#47;wyyl1&#47;geektime-tdd-framework&#47;tree&#47;6</div>2022-06-20</li><br/>
</ul>