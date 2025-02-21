你好，我是郭屹。今天我们继续手写MiniTomcat。

上一节课我们完成了对Request、Response的Header信息解析，并且采用Facade模式封装了我们希望暴露给外界的方法体，避免被业务程序员直接调用实现类的内部方法。

在实际的请求结构中，除了消息头部的参数之外，请求的URI后缀往往会带上请求参数，例如 `/app1/servlet1?username=Tommy&docid=TS0001`，路径和参数之间用“?”分隔，参数与参数之间使用“&amp;”隔开，这是我们这节课需要解析的部分。

除此之外，Header中可能还会包含用户信息，使用Cookie存储，但用户信息使用明文传递也不大好，而且Cookie是存储在客户端的，为了优化这个问题，Servlet规范规定了Session的用途，这节课我们也会解析并设置Cookie和Session。

下面我们一起动手来实现。

## 项目结构

这节课我们新增Session类，并对其进行封装而定义SessionFacade类。同时会增加TestServlet类，以便更好地测试。pom.xml依赖并未发生任何变化。项目结构如下：

```plain
MiniTomcat
├─ src
│  ├─ main
│  │  ├─ java
│  │  │  ├─ server
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
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/31/05/9028e9ac.jpg" width="30px"><span>ctt</span> 👍（1） 💬（1）<div>GET &#47;path&#47;to&#47;resource HTTP&#47;1.1
Host: www.example.com
User-Agent: Mozilla&#47;5.0 (Windows NT 10.0; Win64; x64) AppleWebKit&#47;537.36
             (KHTML, like Gecko) Chrome&#47;58.0.3029.110 Safari&#47;537.36
Accept: text&#47;html,application&#47;xhtml+xml,application&#47;xml;q=0.9,image&#47;webp,*&#47;*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Cookie: sessionid=abc123; username=ctt
Connection: keep-alive
</div>2023-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：Cookie和Session是成对出现的吗？
有Cookie就一定有Session，对吗？反过来，有Session也一定有Cookie，对吗？
Q2：Session的Set-Cookie字段可以出现多次吗？
我让chatGPT3.5给出一个包含Cookie的Http响应，给出的例子是：
HTTP&#47;1.1 200 OK
Date: Tue, 15 Nov 2022 08:12:31 GMT
Server: Apache&#47;2.4.38 (Unix)
Set-Cookie: sessionid=abc123; Expires=Wed, 16 Nov 2022 08:12:31 GMT; Path=&#47;
Set-Cookie: username=johndoe; Expires=Wed, 16 Nov 2022 08:12:31 GMT; Path=&#47;
Content-Type: text&#47;html; charset=utf-8
Content-Length: 1234

其中，Set-Cookie出现了两次。
我问gpt为什么出现两次，gpt回答“常抱歉，我犯了一个错误。在HTTP响应中，Set-Cookie首部字段只能出现一次”，但给出的修正后的例子还是包含两个。
请问：Http Response的Set-Cookie字段可以出现多次吗？


Q3:本课代码，messaging包不存在
HttpRequest.java文件中有如下导包语句：
import com.sun.xml.internal.messaging.saaj.packaging.mime.internet.InternetHeaders;
编译报错：
Error:(3, 67) java: 程序包com.sun.xml.internal.messaging.saaj.packaging.mime.internet不存在
前面几课的代码，Idea中修改java版本后都能正常运行，第8课的代码却有这个编译错误，为什么？</div>2023-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（2）<div>1、手工写一个请求串
POST &#47;servlet&#47;test.TestServlet HTTP&#47;1.1
Host: localhost:8080
Content-Type: application&#47;x-www-form-urlencoded
Cookie: jsessionid=43C65BC81B4B4DE4623CD48A13E7FF84; userId=123
Content-Length: 9

name=haha

2、回传 jsessionid 到客户端其实文中也有提到了， 通过 cookie  或 URL 重写进行进行回传。</div>2023-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/2a/0e/4e187484.jpg" width="30px"><span>夙夜SEngineer</span> 👍（0） 💬（0）<div>我来完善一段代码逻辑，getParameter(String name)方法中，应只调用一次parseParameters，添加if (parameters.isEmpty())判断：
    @Override
    public String getParameter(String name) {
        if (parameters.isEmpty()) {
            parseParameters();
        }
        String values[] = parameters.get(name);
        if (values != null)
            return (values[0]);
        else
            return (null);
    }
否则遇到POST请求体多个参数解析的时候，由于SocketInputStream提前关闭导致fill函数中is引用空指针异常
    protected void fill() throws IOException {
        pos = 0;
        count = 0;
        int nRead = is.read(buf, 0, buf.length);
        if (nRead &gt; 0) {
            count = nRead;
        }
    }</div>2025-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/fb/b6/728e2d02.jpg" width="30px"><span>偶来人间，风度翩翩</span> 👍（0） 💬（1）<div>代码示例中，对于SocketInputStream类，
第53行代码【requestLine.uriEnd =  readCount - 1; 】是不正确的，
应该是【requestLine.methodEnd = readCount - 1;】。   </div>2024-05-25</li><br/>
</ul>