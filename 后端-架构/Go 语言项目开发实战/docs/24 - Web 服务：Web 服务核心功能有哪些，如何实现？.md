你好，我是孔令飞。从今天开始，我们进入实战第三站：服务开发。在这个部分，我会讲解 IAM项目各个服务的构建方式，帮助你掌握Go 开发阶段的各个技能点。

在Go项目开发中，绝大部分情况下，我们是在写能提供某种功能的后端服务，这些功能以RPC API 接口或者RESTful API接口的形式对外提供，能提供这两种API接口的服务也统称为Web服务。今天这一讲，我就通过介绍RESTful API风格的Web服务，来给你介绍下如何实现Web服务的核心功能。

那今天我们就来看下，Web服务的核心功能有哪些，以及如何开发这些功能。

## Web服务的核心功能

Web服务有很多功能，为了便于你理解，我将这些功能分成了基础功能和高级功能两大类，并总结在了下面这张图中：

![](https://static001.geekbang.org/resource/image/1a/2e/1a6d38450cdd0e115e505ab30113602e.jpg?wh=2248x1835)

下面，我就按图中的顺序，来串讲下这些功能。

要实现一个Web服务，首先我们要选择通信协议和通信格式。在Go项目开发中，有HTTP+JSON 和 gRPC+Protobuf两种组合可选。因为iam-apiserver主要提供的是REST风格的API接口，所以选择的是HTTP+JSON组合。

**Web服务最核心的功能是路由匹配。**路由匹配其实就是根据`(HTTP方法, 请求路径)`匹配到处理这个请求的函数，最终由该函数处理这次请求，并返回结果，过程如下图所示：
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM5suA7q5mM40ULTY5OlQpoerPRMQD8NcMbKxDHhNmjQNUCngkSJEzRvMVDibAHw2whGZxAFlibzribOA/132" width="30px"><span>jxlwqq</span> 👍（5） 💬（1）<div>signal.Notify 需要使用 buffered channel 哦

```go
c := make(chan os.Signal, 1)
```

参考：https:&#47;&#47;blog.wu-boy.com&#47;2021&#47;03&#47;why-use-buffered-channel-in-signal-notify&#47;</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（4） 💬（2）<div>老师，没有理解编码实现优雅关闭服务的程序。这段程序和我们期望的：【期望 HTTP 服务可以在处理完所有请求后，正常地关闭这些连接，也就是优雅地关闭服务】有什么关系？</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/df/367f2c75.jpg" width="30px"><span>🌀🐑hfy🐣</span> 👍（3） 💬（1）<div>请问老师觉得go-zero怎样？值得学习吗？</div>2022-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/f5/ed/d23daf19.jpg" width="30px"><span>Neroldy</span> 👍（3） 💬（1）<div>Get handler函数用Rlock会不会更合适？因为好像只有对product的读操作而没有写操作。</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/5d/db3c1401.jpg" width="30px"><span>tajizhijia</span> 👍（1） 💬（2）<div>在goroute里log.Fatal()之后程序不就推出了么？</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/f1/ce10759d.jpg" width="30px"><span>wei 丶</span> 👍（1） 💬（2）<div>老师想问下server.key这个用cfssl怎么生成呀？ 我往回翻了下只看到了cfssl生成的 .pem 证书文件 🙈</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bb/e0/29dc8a06.jpg" width="30px"><span>LosinGrip</span> 👍（1） 💬（1）<div>curl -XGET http:&#47;&#47;127.0.0.1:8080&#47;v1&#47;products&#47;iphone12
获取如下 
Client sent an HTTP request to an HTTPS server.
什么原因</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bb/e0/c7cd5170.jpg" width="30px"><span>Bynow</span> 👍（0） 💬（1）<div> c.JSON(http.StatusNotFound, gin.H{&quot;error&quot;: fmt.Errorf(&quot;can not found product %s&quot;, c.Param(&quot;name&quot;))}) 这行代码是错误的，应该是Sprintf</div>2022-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/58/a5/6b5e1525.jpg" width="30px"><span>平常心</span> 👍（0） 💬（1）<div>如何用 curl 来访问 https的 服务呢？ ca.pem 放到本机的证书库里，运行了一下，还是跑不通 https的服务呢。</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（0） 💬（1）<div>「表单参数 form」是否可以和「请求消息体参数 body」合并在一起，因为后者是包含前者的。其请求内容都是在请求体部分，而且格式有多种，比如 application&#47;json、application&#47;xml、text&#47;plain，再比如就是 application&#47;form。</div>2021-10-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erRavHNiaicxIIrTK5JjKyCNaSKN2MhnM2X0IuNpcoDoyn0OUOqYgdEb0brT9QgibAKyjBP3R3x0W3Jw/132" width="30px"><span>huntersudo</span> 👍（12） 💬（0）<div>Gin的示例和代码看了很多，知道这样写，有时候就不知道为啥这样写，老师的文章不少地方给了解释，给力给力！！</div>2021-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（2） 💬（0）<div>写web服务，就用Gin框架。
从需求出发，介绍Gin框架的核心功能，即成体系又便于理解。</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/07/7711d239.jpg" width="30px"><span>ling.zeng</span> 👍（1） 💬（0）<div>老师您可太赞了。</div>2021-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（0） 💬（0）<div>package main

import (
    &quot;net&#47;http&quot;
    &quot;time&quot;

    &quot;github.com&#47;gin-gonic&#47;gin&quot;
    &quot;golang.org&#47;x&#47;time&#47;rate&quot;
)

&#47;&#47; 创建限流器，限制每秒最多5个请求
var healthzLimiter = rate.NewLimiter(5, 10)

func rateLimiterMiddleware(limiter *rate.Limiter) gin.HandlerFunc {
    return func(c *gin.Context) {
        if !limiter.Allow() {
            c.JSON(http.StatusTooManyRequests, gin.H{&quot;error&quot;: &quot;请求过于频繁，请稍后再试&quot;})
            c.Abort()
            return
        }
        c.Next()
    }
}

func main() {
    router := gin.Default()

    &#47;&#47; 健康检查路由，应用限流中间件
    router.GET(&quot;&#47;healthz&quot;, rateLimiterMiddleware(healthzLimiter), func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{&quot;status&quot;: &quot;ok&quot;})
    })

    &#47;&#47; 其他路由
    router.GET(&quot;&#47;process&quot;, func(c *gin.Context) {
        &#47;&#47; 处理逻辑
    })

    router.Run(&quot;:8080&quot;)
}</div>2024-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/47/b7/276be208.jpg" width="30px"><span>P=NP?</span> 👍（0） 💬（0）<div>这个项目的github地址是多少</div>2024-06-13</li><br/><li><img src="" width="30px"><span>Geek_d167a6</span> 👍（0） 💬（0）<div>HTTP 头参数（header）。例如curl -X POST -H &#39;Content-Type: application&#47;json&#39; -d &#39;{&quot;username&quot;:&quot;colin&quot;,&quot;password&quot;:&quot;colin1234&quot;}&#39; http:&#47;&#47;mydomain.com&#47;login，Content-Type 就是 HTTP 头参数。消息体参数（body）。例如curl -X POST -H &#39;Content-Type: application&#47;json&#39; -d &#39;{&quot;username&quot;:&quot;colin&quot;,&quot;password&quot;:&quot;colin1234&quot;}&#39; http:&#47;&#47;mydomain.com&#47;login，username 和 password 就是消息体参数。
[这里的curl有区别吗？]</div>2023-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（0） 💬（1）<div>真像老母亲忙前忙后，把饭喂到嘴边吃。专栏很赞~</div>2022-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（0）<div>总结：
1. web服务的常见功能：路由匹配（精确匹配和模糊匹配）、路由分组、参数解析；参数校验；逻辑处理；返回结果。
2. 高级功能有：中间件、优雅关停。通过中间件技术，可以实现认证、RequestID、跨域等常见功能。
3. 除了路由匹配和路由分组等基础功能外，Gin的功能还包括：针对不同位置的HTTP参数进行解析；有很多开源的中间件，可以复用。
4. 需要注意Web服务的优雅启动和停止。</div>2021-11-27</li><br/>
</ul>