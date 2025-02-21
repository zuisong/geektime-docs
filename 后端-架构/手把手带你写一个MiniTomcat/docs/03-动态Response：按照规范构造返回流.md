你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课我们初步构造了一个最原始的可运行的 HTTP Server，做到了将文件内容输出到浏览器。但我们也发现，这个原始版本的HTTP Server局限性很大，只能使用静态资源，不能组装Response返回结果，竟然还要求静态资源本身的文本格式符合HTTP协议中Response的规范，而且也不满足不同异常场景下的Response返回。这个服务需要业务程序员自行准备完整的满足HTTP Response规范格式的静态资源，非常不友好。

其次，一个正常的 HTTP 服务响应请求不应只有静态资源，也应存在动态资源。这就是这节课我们要引入的一个重要概念——**Servlet，它是实现动态资源返回的好工具**。总体结构图如下，现在就让我们一起来动手实现。

![图片](https://static001.geekbang.org/resource/image/yy/39/yy5870c90fbb711ae8667cabf5c5c839.png?wh=1920x852)

## 项目结构

这节课我们计划采用Maven结构对项目的包依赖进行管理，省去了手工导入jar包的环节。但有一点我们始终坚持，就是**引入最少的依赖包，一切功能尽可能用最原生的JDK来实现**。

这节课项目结构变化如下：

```plain
MiniTomcat
├─ src
│  ├─ main
│  │  ├─ java
│  │  │  ├─ server
│  │  │  │  ├─ HttpServer.java
│  │  │  │  ├─ Request.java
│  │  │  │  ├─ Response.java
│  │  │  │  ├─ Servlet.java
│  │  │  │  ├─ ServletProcessor.java
│  │  │  │  ├─ StatisResourceProcessor.java
│  │  ├─ resources
│  ├─ test
│  │  ├─ java
│  │  │  ├─ test
│  │  │  │  ├─ HelloServlet.java
│  │  ├─ resources
├─ webroot
│  ├─ test
│  │  ├─ HelloServlet.class
│  ├─ hello.txt
├─ pom.xml
```
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（2） 💬（1）<div>老师请教一个问题，ServletProcessor没有设置响应头Content-Length，浏览器不会有拆包或者粘包的问题吗？</div>2023-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（1） 💬（1）<div>🤪匹配 web.xml 或注解定义的 servlet 名称， 找到就可以当做动态 servlet。 不知道对不对， 想法比较单调， 希望老师和朋友给出点评和意见</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/bd/27/e653a220.jpg" width="30px"><span>Xiaosong</span> 👍（0） 💬（1）<div>欸 从来没 单独编译过单独的 java文件，我看target里面不编译test dir底下的文件，请教一下怎么操作</div>2024-01-27</li><br/><li><img src="" width="30px"><span>Geek_50a5cc</span> 👍（0） 💬（1）<div>所以 Servlet 动态资源的 classloader 都是去 编译后的classes定位需要的Servlet，对吗</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/89/4c/791d0f5e.jpg" width="30px"><span>彩笔采购</span> 👍（0） 💬（1）<div>啊我悟了</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师几个问题：
Q1：老师开发用的IDE是Idea吗？
我用Idea2019，打开老师的第三课代码，打开HttpServer.java,运行main函数，提示编译错误：“Error:java: 错误: 不支持发行版本 5”。
我的电脑上java版本是java8。老师的代码只有三部分：src目录、webroot目录、pom.xml，都没有包含Java版本信息啊。
Note1:其中一部分代码是： if (index2 &gt; index1) return requestString.substring(index1 + 1, index2);  对于这个代码，idea2019的提示是：&#39;if&#39;没有加大括号。）
Note2:
import java.time.ZonedDateTime;
对于此导包，有红色下划线，Idea2019提示“Usage of API documented as @since 1.8+ ”。这个有影响吗？

Q2：Response类只有这些内容吗？
本课中，Response只当做实体类处理，实体类的话，应该包含响应的多个字段，比如状态行、响应头等字段，但本文只有Request和OutputStream，是没有全部列出来吗？

Q3：对于图片，Response是怎么处理的？
把图片也当做文件，读取文件，读出的结果应该是二进制数据，然后把二进制数据放到response的响应体中，是这样吗？</div>2023-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/d7/9d/73390cc0.jpg" width="30px"><span>wild wings.Luv</span> 👍（0） 💬（0）<div>请问老师，在02处理静态资源的时候，contenttype设置为12，hello.txt是整个http报文的内容，此时会解析前面的内容作为响应头。但是在03处理静态资源，是拼接响应头，所以hello.txt整个文件都被当成了响应体。此时hello.txt就不需要是整个报文了。</div>2024-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/64/62/8b20c551.jpg" width="30px"><span>Martito</span> 👍（0） 💬（1）<div>为什么我编译这个HelloServlet.java报错呢 idea中也没有提示错误呀</div>2023-12-19</li><br/>
</ul>