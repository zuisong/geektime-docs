你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课我们已经实现对URI里路径的解析，用于适配GET请求时，将参数代入请求地址的情况，而且在请求参数中引入了Cookie与Session，为HTTP引入状态，存储用户的相关信息。但我也提到了，我们暂未在Response返回参数中回写Session信息，所以客户端程序没办法接受这个信息，自然也无法再回传给Server，这是我们接下来要改造的方向。

此外，现在我们对一个Socket的管理是这样的：建立一个Socket，交给Processor处理，当Processor处理完毕后随即把这个Socket关闭。这样也引出一个问题：一个网页的页面上可能有很多模块，每次都需要访问服务器拿到相应资源，导致本可以使用同一个Socket解决的问题，却需要创建多个Socket，这是对资源的浪费，所以这节课我们也来探讨一下用什么技术来解决这个问题。

接下来我们一起来动手实现。

## 项目结构

这节课我们先只引入了一个工具类CookieTools，用来处理Cookie，其余项目结构并没有发生改变，你可以参考我给出的目录。

```plain
MiniTomcat
├─ src
│  ├─ main
│  │  ├─ java
│  │  │  ├─ server
│  │  │  │  ├─ CookieTools.java
│  │  │  │  ├─ DefaultHeaders.java
│  │  │  │  ├─ HttpConnector.java
│  │  │  │  ├─ HttpHeader.java
│  │  │  │  ├─ HttpProcessor.java
│  │  │  │  ├─ HttpRequest.java
│  │  │  │  ├─ HttpRequestFacade.java
│  │  │  │  ├─ HttpRequestLine.java
│  │  │  │  ├─ HttpResponse.java
│  │  │  │  ├─ HttpResponseFacade.java
│  │  │  │  ├─ HttpServer.java
│  │  │  │  ├─ Request.java
│  │  │  │  ├─ Response.java
│  │  │  │  ├─ ServletProcessor.java
│  │  │  │  ├─ Session.java
│  │  │  │  ├─ SessionFacade.java
│  │  │  │  ├─ SocketInputStream.java
│  │  │  │  ├─ StatisResourceProcessor.java
│  │  ├─ resources
│  ├─ test
│  │  ├─ java
│  │  │  ├─ test
│  │  │  │  ├─ HelloServlet.java
│  │  │  │  ├─ TestServlet.java
│  │  ├─ resources
├─ webroot
│  ├─ test
│  │  ├─ HelloServlet.class
│  │  ├─ TestServlet.class
│  ├─ hello.txt
├─ pom.xml
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（2）<div>在补充一点
3、while (keepAlive) 为了保持 socket 存活， 会影响非 keep-alive 的请求， 导致死循环。 这块内容老师是否有好的书籍推荐或者以后有加餐， 这样我们可以进行深一层次的探索。</div>2023-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（2）<div>老师， 我有几个问题
1、服务器端和客户端双方是否都可以控制 close Connection 和使用 chunked 传输？
2、chunked 应用场景有哪些？  目前想到大文件传输， 在现有代码基础上， 自己动手尝试了客户端传输小量文本数据， 客户端多次使用socket 请求服务端， 但服务端并非收到一次请求就返回一次结果， finishResponse 之后也是无法收到服务端返回的结果， 必须 close Connection 才能收到服务端的请求，并且是多次请求合并返回的结果； 这跟我想的有点不一样， 我想的是这个复用的 socket 然后请求一次就返回一次结果， 然后客户端进行处理， 比如客户端请求一个js、一个 css、一个 html， 是需要  close Connection 之后才能返回吗？ 不知道是哪方面想的不对， 还得老师指点。 </div>2023-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：Http请求头中的“connection: keep-alive”是谁控制的？
该部分是浏览器填的，浏览器是自动填的吗？在填的时候是否受到了服务器的控制？
Q2：静态访问不能返回内容
本课程代码，运行后在浏览器中输入：http:&#47;&#47;localhost:8080&#47;hello.txt
浏览器上没有任何输出，空白，为什么？

Q3：错误的servlet网址也能返回
访问地址：http:&#47;&#47;localhost:8080&#47;servlet&#47;test.HelloServlet，此网址是不小心敲错了，在ServletProcessor.java中打印出来的servletName就是test.HelloServlet，接下来的代码“servletClass = HttpConnector.loader.loadClass(servletName);”竟然没有报错，代码中只有HelloServlet和TestServlet，并没有test.HelloServlet，为什么loadClass还能成功？

浏览器上显示的内容是“Hello World 你好”，根据此内容推测，应该是用了HelloServlet。但我在HelloServlet的输出中，随便增加字符：&quot;Hello World 111你好123&quot; ，重新编译运行，
但浏览器上显示的还是“Hello World 你好”，为什么？

Q4：小问题：HelloServlet.java中也多了一个导包语句。
“import jdk.internal.util.xml.impl.Pair;”
估计和上节课的一样，也是IDE自动导入的，我已注释掉该代码。</div>2023-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/32/28/078ec46c.jpg" width="30px"><span>top啦它</span> 👍（0） 💬（3）<div>后面要手写什么？</div>2023-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/d7/9d/73390cc0.jpg" width="30px"><span>wild wings.Luv</span> 👍（0） 💬（0）<div>socket没有关闭。但是同一个用户的下一个http请求，需要找到对应的socket吗，还是不需要？</div>2024-09-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XWv3mvIFORNgRk9wF8QLb9aXfh1Uz1hADtUmlFwQJVxIzhBf8HWc4QqU7iaTzj8wB5p5QJLRAvlQNrOqXtrg1Og/132" width="30px"><span>Geek_320730</span> 👍（0） 💬（0）<div>按照 chunked 模式返回响应内容: https:&#47;&#47;github.com&#47;kuifir&#47;MiniTomcat&#47;tree&#47;test-chunk</div>2024-04-17</li><br/>
</ul>