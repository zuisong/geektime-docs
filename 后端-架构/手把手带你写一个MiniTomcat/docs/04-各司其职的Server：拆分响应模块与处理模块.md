你好，我是郭屹。今天我们继续手写MiniTomcat。

在上一节课，我们基于最早的最小可用HttpServer服务器进行了改造。主要包括对HTTP协议返回内容中的状态行与返回头进行封装，以及引入动态资源和Servlet的概念，对Web端返回内容进行了扩充，已经有点Servlet容器的雏形了。

但我也提到，当前我们自定义的Servlet接口是不满足Java Servlet规范的。因此这节课我们首先会讨论如何符合Servlet规范，在Java的规则下实现MiniTomcat。

其次，在当前的HttpServer中，HttpServer类承担了接收客户端请求、调用Servlet、响应客户端等多种功能，功能太多了，因此我们要将其进行功能拆分，使各个部分各司其职。

![](https://static001.geekbang.org/resource/image/54/a2/54c07fb03981dca6c02f61a9279b4aa2.png?wh=2144x874)

好，就让我们一起来动手实现。

## 项目结构

这节课我们计划采用Maven结构对项目的包依赖进行管理，省去了导入jar包的环节。但有一点我们始终坚持，就是引入最少的依赖包，一切功能尽可能用最原生的JDK来实现，以便于我们从头做起更深地理解原理。在这节课中，项目结构变化如下：

```plain
MiniTomcat
├─ src
│  ├─ main
│  │  ├─ java
│  │  │  ├─ server
│  │  │  │  ├─ HttpConnector.java
│  │  │  │  ├─ HttpProcessor.java
│  │  │  │  ├─ HttpServer.java
│  │  │  │  ├─ Request.java
│  │  │  │  ├─ Response.java
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
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/76/ad/f192d95e.jpg" width="30px"><span>？新！</span> 👍（1） 💬（2）<div>老师我有个关于tomcat连接层的问题求教？
    场景：外部nginx日志记录调用了A服务并且超时，但是A服务本地日志localhost_access_log，没有记录，了解后怀疑是连接层，会等待队列就超时了，所以没有到容器层，没有被localhost_access_log记录？
    问题：
        1  我的怀疑是否可能？
        2 有办法验证吗？比如tomcat等待队列超时或者accept超时，能记录日志
      </div>2024-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（5）<div>请教老师几个问题：
Q1：streamHandler不需要赋值吗？
ServletProcessor.java的process方法中：
URLStreamHandler streamHandler = null;
urls[0] = new URL(null, repository, streamHandler);
代码声明了变量“streamHandler”，
但是没有赋值，然后直接用来创建URL的对象。
请问：为什么没有给“streamHandler”赋值？

Q2：HttpConnector的run方法为什么没有注解？
类定义：HttpConnector implements Runnable，
其run方法上面没有注解，Idea2019提示：
Missing &#39;@Override&#39; annotation on &#39;run()&#39; 。
但程序能运行。请问老师的代码中，run方法为什么没有注解？

Q3：第03课代码，一次请求，socket = serverSocket.accept();为什么运行两次？
HttpServer.java文件中,while(true)代码块,在serverSocket.accept();这里阻塞。浏览器中输入请求，创建Request，成功地走完了整个流程。走完整个流程后按道理应该还在serverSocket.accept();这里阻塞。但竟然再次创建Request，不过在Request类的parse函数中，在i = input.read(buffer);这个地方不再往下面执行。我在input.read前后都加了打印语句，前面的打印语句执行了，后面的没有执行，神奇啊，为什么啊？
简单地说，就是：浏览器发送一个请求，HttpServer收到了两个request,第一个正常处理，第二个不能正常执行。（我用的是Chrome浏览器，也许和浏览器有关？）</div>2023-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（1） 💬（2）<div>😄池子+队列， 学艺不精具体细节答不上来， 请老师指点。</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/7c/25abe455.jpg" width="30px"><span>stars</span> 👍（0） 💬（1）<div>只是在主线程启动了一个子线程，这样就提高吞吐率了吗？请教老师。</div>2023-12-25</li><br/>
</ul>