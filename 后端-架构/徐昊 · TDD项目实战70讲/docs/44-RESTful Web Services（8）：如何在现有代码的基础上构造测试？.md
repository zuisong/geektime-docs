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
    - 如果找不到对应的MessageBodyWriter，则返回500族错误
    - 如果找不到对应的HeaderDelegate，则返回500族错误
    - 如果找不到对应的ExceptionMapper，则返回500族错误
    - 如果entity为空，则忽略body
  - 当资源方法抛出异常时，根据异常响应Http请求
    
    - 如果抛出WebApplicationException，且response不为null，则使用response响应Http
    - 如果抛出的不是WebApplicationException，则通过异常的具体类型查找ExceptionMapper，生产response响应Http请求
  - 当其他组件抛出异常时，根据异常响应Http请求
    
    - 调用ExceptionMapper时
    - 调用HeaderDelegate时
    - 调用MessageBodyWriter时
    - 通过Providers查找ExceptionMapper时
    - 通过Providers查找MessageBodyWriter时
    - 通过RuntimeDelegate查找HeaderDelegate时
- RuntimeDelegate
  
  - 为MediaType提供HeaderDelegate
  - 为CacheControl提供HeaderDelegate
  - 为Cookie提供HeaderDelegates
  - 为EntityTag提供HeaderDelegate
  - 为Link提供HeaderDelegate
  - 为NewCookie提供HeaderDelegate
  - 为Date提供HeaderDelegate
  - 提供OutboundResponseBuilder
- OutboundResponseBuilder
- OutboundResponse
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（2） 💬（1）<div>@TestFactory + 标签 + 反射刷新了我对自动化测试认知！</div>2022-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/ae/a08024b2.jpg" width="30px"><span>Luke</span> 👍（0） 💬（1）<div>踩了个坑。如果测试时遇到 StackOverflowError 的，看看 stub 的 OutboundResponse 是否都是默认值。</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/93/0f1cbf44.jpg" width="30px"><span>枫中的刀剑</span> 👍（0） 💬（0）<div>看老师重构代码是真的舒服，信手拈来，一气呵成。
动态测试配合函数式还能这么用，学到了。</div>2022-06-29</li><br/>
</ul>