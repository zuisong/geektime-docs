你好，我是郑建勋。

上节课，我讲解了开发一个Go项目需要遵守的编程规范。接下来我们就要开始正式书写爬虫实战项目了。

这个项目的核心是通过HTTP协议与目标网站通信，然后发送请求并获取目标网站的对应资源。在下面两节课，我会带着你从一个最简单的HTTP请求入手，一步步理解请求背后发生的故事。

在课程正式开始之前，我想先和你分享一段话：“经验用来对待特殊场景，方法论用来处理通用场景，没有经验可能会慢一些，没有方法论可能寸步难行。”

而为了更好地理解爬虫项目可能遇到的难题，并且在解决网络问题时有方法论的支撑，我们需要掌握网络分层协议与层层封装的流转过程、网络数据包的路由过程，操作系统收发包的处理过程。另外，还要熟悉HTTP协议以及Go标准库对HTTP协议的巧妙封装。

## 最简单的HTTP服务器与请求

为了方便开发者使用，Go语言对网络库和HTTP库的封装可以说是费尽心力。在平时，三行核心代码就能够写出一个HTTP的服务器或是HTTP请求，但其实Go标准库内部进行了大量处理。

下面这个例子是借助Go HTTP标准库书写的一个最简单的HTTP服务器。

```plain
package main

import (
	"fmt"
	"net/http"
)

func hello(w http.ResponseWriter, _ *http.Request) {
	fmt.Fprintf(w, "Hello")
}

func main() {
    // 访问路由到hello函数
	http.HandleFunc("/", hello)
    // 监听本地8080端口
	http.ListenAndServe("0.0.0.0:8080", nil)
}
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（32） 💬（10）<div>课程快到1&#47;3了，就那篇爬虫整体设计，感受到是本专栏的重点。

不是说其他内容不重要，但铺垫太多，是不是会喧宾夺主、稀释专栏的含金量？

还是希望看到Go网络编程的一些技巧、软件设计的一些哲学、接口抽象、功能编排、组合、扩展、分布式、反爬...

希望专栏组能关注下！🤩🤩🤩</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/d2/e2/4d84ac9f.jpg" width="30px"><span>.</span> 👍（18） 💬（0）<div>铺垫太多 底层原理虽然很重要但是应该不是大家非常关心的吧  实战内容才是重点</div>2022-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJv3HPde36ll9u5EpEIJyR9jMXE0K7pcuxOlf4HUcbs0po9nkicR0mbXlF1Vdoytj1vxSRCZJGOH7Q/132" width="30px"><span>愤怒的小猥琐</span> 👍（8） 💬（0）<div>能不能搞点硬货，js逆向，用golang如何补环境，还有一些爬虫常用的加解密算法都没有，感觉跟专栏的初衷相悖</div>2022-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/22/ae/8a2945c8.jpg" width="30px"><span>_MISSYOURLOVE</span> 👍（1） 💬（0）<div>使用ping命令来测试与目标网络的连通性，nslookup查看域名被解析到了那个IP，还可以使用 traceroute命令来对路由进行跟踪</div>2022-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/41/132295f2.jpg" width="30px"><span>默雲端</span> 👍（0） 💬（0）<div>作者的课程还是很有深度的，他呈现给我们的不仅仅是 一个爬虫项目该如何实现，而是具备通用性的软件开发实现。适合反复阅读，直到掌握为止~

如果喜欢上来直接上代码的课程，慕课网的比较合适，坦白来讲，慕课网有的课程讲的反而十分浅显，也就只有代码了。

软件开发的能力本身就是靠关键性知识构建而来，在这样的框架下面作 内容填充（即编写代码），可能有些朋友的需求就是 填充，而不是构建。

的确，talk is cheap, show me the code. 作者的 code 也将在接下来的章节中逐一展现。</div>2023-05-03</li><br/>
</ul>