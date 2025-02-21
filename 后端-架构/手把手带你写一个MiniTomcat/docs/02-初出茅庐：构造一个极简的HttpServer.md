你好，我是郭屹，今天我们继续学习手写 MiniTomcat，从这里开始要同步写代码了。

与MiniSpring相同，我们也会从一个最简单的程序开始，一步步地演化迭代，最终实现Tomcat的核心功能。这节课，我们就来构造第一个简单的Web服务器应用程序。结构如图所示：

![](https://static001.geekbang.org/resource/image/91/80/919b493e16b8853a763d1f7997404880.png?wh=2190x972)

可以看出，当用户从浏览器这端发起一个静态的请求时，这个极简HTTP Server仅仅是简单地将本地的静态文件返回给客户端。这也正是我们手写MiniTomcat的第一步。

## Web请求流程

一个Web服务器，简单来讲，就是要按照HTTP协议的规范处理前端发过来的Request并返回Response。在这节课中，我们计划请求 `http://localhost:8080/test.txt` 这个地址，实现一个最简单的Web应用服务器。

我们简单回顾一下，在浏览器中输入一个网页地址，键入回车的那一刻，从请求开始到请求结束这个过程会经历几步。

1. DNS解析，将域名解析为IP地址。
2. 与目标端建立TCP连接。
3. 发送HTTP请求。
4. 服务器解析HTTP请求并返回处理后的报文。
5. 浏览器解析返回的报文并渲染页面。
6. TCP连接断开。

在这个过程中，还有很多诸如三次握手，DNS解析顺序等具体技术细节，因为不是这节课的主要论题，所以这里不再详细说明。在上述Web请求流程中，我们重点关注“发送HTTP请求”“服务器解析HTTP请求并返回处理后的报文”以及“浏览器解析返回的报文并渲染页面”这三步。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/a3/7c685adf.jpg" width="30px"><span>猛禽不是鸟</span> 👍（1） 💬（1）<div>在应用服务器中维护一个请求地址和对应处理类【方法】的映射关系，然后在parse解析出来uri之后，通过映射关系找到对应的处理方法。</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/f2/26/a8ac6b42.jpg" width="30px"><span>听风有信</span> 👍（1） 💬（2）<div>应用服务器的话，要根据客户端的请求，然后执行相应的业务处理程序，最后将业务程序的输出返回给客户端，这种输出的内容是动态生成的。</div>2023-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/ae/1520ad92.jpg" width="30px"><span>阿加西</span> 👍（1） 💬（1）<div>参考了《How Tomcat Works》</div>2023-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/bd/27/e653a220.jpg" width="30px"><span>Xiaosong</span> 👍（0） 💬（1）<div>好奇为什么parseUri要写的这么麻烦，直接requestString.split(&#39; &#39;)，检查一下length，然后 取第二个不就行了吗</div>2024-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8a/ca/1afcc75b.jpg" width="30px"><span>健康的小牛犊</span> 👍（0） 💬（3）<div>Spring和tomcat是如何结合在一起的呢，按理说tomcat本身就可以作为一个web服务器了，那spring的作用是啥呢</div>2024-01-02</li><br/><li><img src="" width="30px"><span>Geek_50a5cc</span> 👍（0） 💬（1）<div>如果将读取的文件内容，放在message里面返回过去；
String Message = &quot;HTTP&#47;1.1 404 FIle Not Found\r\n&quot; +
                        &quot;Content-Type: text&#47;html\r\n&quot; +
                        &quot;Content-Length: 23\r\n&quot; +
                        &quot;\r\n&quot; +
                        &quot;&lt;h1&gt;&quot;+
                        result.toString() +
                        &quot;&lt;&#47;h1&gt;&quot;;
                output.write(Message.getBytes());
如果文件里 字符 很多的时候，这个是否都会完全输出显示出来呢；
（result就是文件字节流转换的字符串）</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/93/61/791d0f5e.jpg" width="30px"><span>Koyi</span> 👍（0） 💬（1）<div>Request类 第13行 读取数据时，使用一个while循环判断返回值是否大于0以保证成功读取完数据是不是好些</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/8b/74d2ab6b.jpg" width="30px"><span>斜杠青年</span> 👍（0） 💬（0）<div>我自己在学习 http 协议的时候，就想到了，可以直接基于字节码来进行开始到 socket 进而到 http 协议，到多路复用，异步IO，到 tomcat 的知识点串起来，但是一直没有决心进行梳理，看到这个课程如获珍宝，学会此课程可以明白理解为什么压测的时候，无论如何提升服务器规格，数据库规格，吞吐还是上不去，以及各种状态码代表什么，瓶颈在TCP层还是Tomcat层，都会得到答案。</div>2024-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/c4/1f/791d0f5e.jpg" width="30px"><span>旷野之希</span> 👍（0） 💬（2）<div>我遇到一个问题，当时随便使用了一个端口号7000，会报403 forbidden的异常，但是换一个端口，比如8888就可以正常访问hello.txt了，这可能是什么原因呢？</div>2024-03-07</li><br/>
</ul>