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
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/93/0f1cbf44.jpg" width="30px"><span>枫中的刀剑</span> 👍（0） 💬（1）<div>exceptionMapper_toResponse的异常抛出这样写会不会好一些。
when(providers.getExceptionMapper(eq(RuntimeException.class))).thenReturn(ex -&gt; {
            throw exception;
        });
强调是在toResponse 里抛出的。
不然感觉和providers_getExceptionMapper没区别。</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a8/66/e2781d4a.jpg" width="30px"><span>忘川</span> 👍（3） 💬（0）<div>伦敦学派 
	适用场景: 自己不太熟悉的框架或者大型结构
	使用方法: 使用约定和api的配合,来验证组件的功能,同时增加自己对于框架的理解.用来吸收和消化框架
	大的方向: 自上而下 从抽象到具体
经典学派:
	适用场景: 大的思路和方向已有把握
	使用方法: 不需要去生硬的模仿,就可以从0-1不断整理,不断演进的方式
	大的方向: 自下而上 从具体到抽象 使用抽象 让经验升华
给我带来的思考:
	学习或者制造一个自己不熟悉的东西的时候 模仿是最快的 可以避免走弯路
	当我们已经有大的把握的时候 自下而上 会更快捷 可以避免模拟的成本  </div>2023-01-06</li><br/>
</ul>