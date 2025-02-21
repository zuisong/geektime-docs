你好，我是Mike。

你真的很棒！已经学完我们这门30讲正文内容了，最后我们还是和前面两章一样处理一下第三章应用篇的思考题。这部分思考题动手操作的内容比较多，我希望你真的可以自己动手敲敲代码，在我给的示例里做出自己想要的效果。

话不多说，我们开始吧！

### [21｜Web开发（上）：如何使用Axum框架进行Web后端开发？](https://time.geekbang.org/column/article/733433)

#### 思考题

请你说一说 Request/Response 模型是什么，Axum 框架和其他 gRPC 框架（比如 Tonic）有什么区别？

#### 答案

Request/Response 模型是一种通用的网络模型架构，用于简化跨越网络的数据传输操作。在这种模型中，客户端发送一个请求（Request），服务器端接收并处理该请求，然后返回一个响应（Response）给客户端。这种模型广泛应用于各种网络应用和协议中，如HTTP、FTP等。Request / Response 模型就是一来一回交互。

Axum 框架和其他 gRPC 框架主要是通信模式不一样。Axum提供了一种基于actor模型的通信模式。gRPC模型在Request / Response 模型基础上构造了更多的交互模型支持。

![图片](https://static001.geekbang.org/resource/image/b4/44/b4e98da3c970f3fe9217c0e506fdc244.png?wh=1556x524)

### [22｜Web开发（下）：如何实现一个Todo List应用？](https://time.geekbang.org/column/article/734130)
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/4d/7df516d5.jpg" width="30px"><span>一带一路</span> 👍（2） 💬（1）<div>结课了嘛？</div>2024-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（0） 💬（0）<div>这篇答疑有点提前了哦</div>2024-04-28</li><br/>
</ul>