你好，我是轩脉刃。欢迎加入我的课程，和我一起从0开始构建Web框架。

之前我简单介绍了整个课程的设计思路，也是搭建Web框架的学习路径，我们会先基于标准库搭建起Server，然后一步一步增加控制器、路由、中间件，最后完善封装和重启，在整章学完后，你就能建立起一套自己的Web框架了。

其实你熟悉Golang的话就会知道，用官方提供的 net/http 标准库搭建一个Web Server，是一件非常简单的事。我在面试的时候也发现，不少同学，在怎么搭怎么用的问题上，回答的非常溜，但是再追问一句为什么这个 Server 这么设计，涉及的 net/http 实现原理是什么? 一概不知。

这其实是非常危险的。**实际工作中，我们会因为不了解底层原理，想当然的认为它的使用方式**，直接导致在代码编写、应用调优的时候出现各种问题。

所以今天，我想带着你从最底层的 HTTP 协议开始，搞清楚Web Server本质，通过 net/http 代码库梳理 HTTP 服务的主流程脉络，先知其所以然，再搭建框架的Server结构。

之后，我们会基于今天分析的整个 HTTP 服务主流程原理继续开发。所以这节课你掌握的程度，对于后续内容的理解至关重要。

## Web Server 的本质
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/2d/48/bc2648c4.jpg" width="30px"><span>程旭</span> 👍（23） 💬（3）<div>1. http.FileServer 创建 FileHandler 数据结构
2. FileHandler 结构体中包含 FileSystem 接口，FileSystem 接口包含Open 方法
3. http.Dir 的 Open 方法 实现  FileSystem 接口 的 Open 方法
4. http.Dir 的 Open 方法对表示字符串的文件路径进行判断：
    （1）先判断 分隔符是否为 &quot;&#47;&quot;且该字符串中是否包含分隔符，若不满足 返回 nil 和 error信息 &quot;http: invalid character in file path&quot;
    （2）将 http.Dir 从 Dir 类型转换为 string 类型，判断该是否为空，若为空，将 dir 赋值为 &quot;.&quot;
    （3）使用 path.Clean ，filepath.FromSlash 和 filepath.Join 方法获得路径全名
    （4）使用 os.Open 方法打开文件，如果打开失败，返回错误信息，如果成功以读模式打开文件</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（17） 💬（1）<div>很赞， 读源码的 思路和 思维导图 很值得学习</div>2021-09-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJyibojtJCnzAE7E8sMqgiaiaAHl3FuzcXcicQnjnT5huUFMxGUMzV5NGuqzzHHr8dBzCs3xfuhwcOnPw/132" width="30px"><span>好家庭</span> 👍（9） 💬（1）<div>老师，请问 go c.serve(connCtx) 里面为什么还有一个循环？c值得是一个connection，我理解不是每个连接处理一次就好了吗，为啥还有一个for循环呢？
···
&#47; Serve a new connection.
func (c *conn) serve(ctx context.Context) {
	c.remoteAddr = c.rwc.RemoteAddr().String()
	ctx = context.WithValue(ctx, LocalAddrContextKey, c.rwc.LocalAddr())
	defer func() {
		if err := recover(); err != nil &amp;&amp; err != ErrAbortHandler {
			const size = 64 &lt;&lt; 10
			buf := make([]byte, size)
			buf = buf[:runtime.Stack(buf, false)]
			c.server.logf(&quot;http: panic serving %v: %v\n%s&quot;, c.remoteAddr, err, buf)
		}
		if !c.hijacked() {
			c.close()
			c.setState(c.rwc, StateClosed)
		}
	}()

	...

	for {
		w, err := c.readRequest(ctx)
		if c.r.remain != c.server.initialReadLimitSize() {
			&#47;&#47; If we read any bytes off the wire, we&#39;re active.
			c.setState(c.rwc, StateActive)
		}
		if err != nil {
			const errorHeaders = &quot;\r\nContent-Type: text&#47;plain; charset=utf-8\r\nConnection: close\r\n\r\n&quot;

...
		}
...
```</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/8f/4b0ab5db.jpg" width="30px"><span>Middleware</span> 👍（9） 💬（3）<div>目录有点不清晰，从零开始，那么是不是应该给出建立合适的文件目录结构，命名。我们也能跟着上手敲一遍。比如这个 framework .目录是如何命名。希望老师真的能手把手</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/29/425a2030.jpg" width="30px"><span>Groot</span> 👍（4） 💬（3）<div>一篇文章值回票价，感觉后续的文章都是在做慈善 😂

受益匪浅，感谢分享 👍</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/24/547439f1.jpg" width="30px"><span>ghostwritten</span> 👍（3） 💬（1）<div>打卡第二天：
https:&#47;&#47;github.com&#47;gohade&#47;coredemo&#47;blob&#47;geekbang&#47;01&#47;go.mod
https:&#47;&#47;datatracker.ietf.org&#47;doc&#47;html&#47;rfc2616
https:&#47;&#47;github.com&#47;valyala&#47;fasthttp
https:&#47;&#47;pkg.go.dev&#47;net&#47;http@go1.15.5

Web Server 第一个go架构：net&#47;http
熟悉库技巧：库函数 &gt; 结构定义 &gt; 结构函数
查看库命令：
go doc net&#47;http | grep &quot;^func
go doc net&#47;http | grep &quot;^type&quot;|grep struct

结构函数如下：
&#47;&#47; 创建一个Foo路由和处理函数
http.Handle(&quot;&#47;foo&quot;, fooHandler)

&#47;&#47; 创建一个bar路由和处理函数
http.HandleFunc(&quot;&#47;bar&quot;, func(w http.ResponseWriter, r *http.Request) {
  fmt.Fprintf(w, &quot;Hello, %q&quot;, html.EscapeString(r.URL.Path))
})

&#47;&#47; 监听8080端口
log.Fatal(http.ListenAndServe(&quot;:8080&quot;, nil))

画源代码分析图，学会脑图构思是关键（略）
流程：
 - 第一层，标准库创建 HTTP 服务是通过创建一个 Server 数据结构完成的；
 - 第二层，Server 数据结构在 for 循环中不断监听每一个连接；
 - 第三层，每个连接默认开启一个 Goroutine 为其服务；
 - 第四、五层，serverHandler 结构代表请求对应的处理逻辑，并且通过这个结构进行具体业务逻辑处理；
 - 第六层，Server 数据结构如果没有设置处理函数 Handler，默认使用 `DefaultServerMux` 处理请求；
 - 第七层，`DefaultServerMux` 是使用 map 结构来存储和查找路由规则。


创建框架的 Server 结构
1.创建一个 coredemo&#47;framework&#47;core.go,实现具体业务逻辑
&#47;&#47; 框架核心结构
type Core struct {
}

&#47;&#47; 初始化框架核心结构
func NewCore() *Core {
  return &amp;Core{}
}

&#47;&#47; 框架核心结构实现Handler接口
func (c *Core) ServeHTTP(response http.ResponseWriter, request *http.Request) {
  &#47;&#47; TODO
}

2.创建一个 coredemo&#47;main.go,创建服务的方法 `ListenAndServe` 先定义了监听信息 `net.Listen`，然后调用 `Serve` 函数,实现对外提供服务

</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cc/de/59a530dc.jpg" width="30px"><span>布丁老厮</span> 👍（3） 💬（1）<div>老师，HTTP 库 Server 的代码流程是不是应该为：创建服务 -&gt; 监听请求 -&gt; 创建连接 -&gt; 处理请求 要更准确一点？因为net.Listen是在srv.newConn之前进行的。</div>2021-09-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJfTnE46bP9zFU0MJicYZmKYTPhm97YjgSEmNVKr3ic1BY3CL8ibPUFCBVTqyoHQPpBcbe9GRKEN1CyA/132" width="30px"><span>逗逼章鱼</span> 👍（2） 💬（1）<div>FileServer 的主要流程前面五层应该都一样，第六层开始不一样，FileServer --&gt; fileHandler --&gt; fileHandler里实现的 ServeHTTP --&gt; serveFile 。</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/45/b2/24dee83c.jpg" width="30px"><span>Ppppppp</span> 👍（1） 💬（1）<div>前两天再看这一块儿，画了好几个”蜘蛛图“，人都看蒙了。感谢感谢！！</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5f/57/791d0f5e.jpg" width="30px"><span>Geek_8ed998</span> 👍（0） 💬（1）<div>老师为啥你代码里mani.go里面import 是&quot;coredemo&#47;framework&quot; ，而我这里按你一样的目录结构要写成&quot;.&#47;framework&quot;才能找到包</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（1）<div>1. dir 是一个自定义类型 本质是字符串 实现了 FileSystem 接口
2. 通过http.StripPrefix(&quot;&#47;static&quot;, fs) 返回一个处理请求，里面的逻辑大概看了下 应该是把前缀static 删除之后重新构建一下path
3. 最终还是通过 ServeHttp处理请求，代码中还处理了 “&#47;” 如果前缀没有&#47; 还贴心的帮忙补充一个
4. 调用 serveFile （还包含重定向代码到 index.HTML 这个不是重点），调用Open函数打开文件
最后关闭文件

如果是读取文件夹，则遍历文件夹内所有文件，将文件名直接输出返回值。 关于这段话我其实具体细节代码没看太明白  = =难受</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/3c/0668d6ae.jpg" width="30px"><span>盘胧</span> 👍（0） 💬（2）<div>老师  为什么这个实现的实例方法 一定要叫  func (c *Core) ServeHTTP    我不小心写错了， 系统会报错提示呢</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/48/00/dd8c0dc1.jpg" width="30px"><span>.</span> 👍（0） 💬（1）<div>- http.FileServer

  1. 通过http.Dir返回FileSystem

  2. 创建fileHandler结构体

  3. 通过http.StripPrefix返回HandlerFunc

  4. 在HandlerFunc中通过请求的url来判断该请求是否存在

    4.1. 请求存在，则使用ServeHTTP

    4.2. 请求不存在，则返回404</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（0） 💬（1）<div>FileServer调用如下过程：
1 handler = DefaultServeMux 
2 调用handler.ServeHTTP
 2.1  调用h := mux.Handler(r) ，其中 h是http.HandlerFunc类型，是http.StripPrefix的返回函数。
 2.2 调用h.ServeHTTP(w, r)，执行http.HandlerFunc的ServeHTTP。
   2.2.1 调用f(w, r)，是http.HandlerFunc.ServeHTTP的内部，此时的f==http.StripPrefix的返回函数。
   2.2.1.1 调用FileServer.ServeHTTP。
</div>2021-10-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/mWicFKgbjL299CQPEhoFdSAphVb4UpibkhF8loRxryBRt3H7ZGkibibhaKANTxvSiatic4PLCy2MsbEMH1hc76YefPUw/132" width="30px"><span>eviltion</span> 👍（0） 💬（1）<div>.\main.go:10:3: cannot use framework.NewCore() (type *framework.Core) as type http.Handler in field value:
        *framework.Core does not implement http.Handler (missing ServeHTTP method)
老师帮忙看下，demo 启动报这个错，什么原因那</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/67/4e381da5.jpg" width="30px"><span>Derek</span> 👍（0） 💬（1）<div>老师，关于“如果入口服务 server 结构已经设置了 Handler，就调用这个 Handler 来处理此次请求，反之则使用库自带的 DefaultServerMux“这句话：
DefaultServeMux 是怎么寻找 Handler 这一层代码的啊？，第七层我没看到DefaultServeMux直接调用Handle方法啊? 
```go
func (mux *ServeMux) ServeHTTP(w ResponseWriter, r *Request) {
	if r.RequestURI == &quot;*&quot; {
		if r.ProtoAtLeast(1, 1) {
			w.Header().Set(&quot;Connection&quot;, &quot;close&quot;)
		}
		w.WriteHeader(StatusBadRequest)
		return
	}
	h, _ := mux.Handler(r)
	h.ServeHTTP(w, r)
}
```
这里调用的是Handler，后面跟下去也没有用到Handle方法啊? 
</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/84/171b2221.jpg" width="30px"><span>jeffery</span> 👍（0） 💬（1）<div>net&#47;http 原理分析的透彻

第一层，标准库创建 HTTP 服务是通过创建一个 Server 数据结构完成的；
第二层，Server 数据结构在 for 循环中不断监听每一个连接；
第三层，每个连接默认开启一个 Goroutine 为其服务；
第四、五层，serverHandler 结构代表请求对应的处理逻辑，并且通过这个结构进行具体业务逻辑处理；
第六层，Server 数据结构如果没有设置处理函数 Handler，默认使用 DefaultServerMux 处理请求；
第七层，DefaultServerMux 是使用 map 结构来存储和查找路由规则。</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（0） 💬（1）<div>思维导图是个好东西，平时用 ide 点着一个个封装的函数、结构，跳着跳着脑子就乱了、懵了~</div>2021-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/db/858337e3.jpg" width="30px"><span>Ethan Liu</span> 👍（0） 💬（2）<div>老师，思维导图用什么工具？</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（0） 💬（1）<div>老师，这个课程源码分析的源码，基于哪个版本的golang？</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/f1/e4fc57a3.jpg" width="30px"><span>无隅</span> 👍（3） 💬（0）<div>算法有时要写服务端程序，搜go看到这门课，意外的惊喜～</div>2022-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/54/86056001.jpg" width="30px"><span>小马🐎</span> 👍（1） 💬（0）<div>代码中NewCore返回是一个自定义的core结构体 如何和封装好的server里面的handler成为了同一个类型？不报错的嘛？还请指教下！</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/8f/1a/7a7e0225.jpg" width="30px"><span>子非鱼</span> 👍（0） 💬（0）<div>老师：有一个实例化的问题
既然已经为 Core 增加了 Constructor：func NewCore() *Core 函数，那为什么要把 Core 做成 Public 呢？</div>2023-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/8f/1a/7a7e0225.jpg" width="30px"><span>子非鱼</span> 👍（0） 💬（0）<div>老师，请问：结构函数 是不是就是 方法？</div>2023-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/0a/23/c26f4e50.jpg" width="30px"><span>Sunrise</span> 👍（0） 💬（1）<div>授人以鱼不如授人以渔，首先感谢老师教授的学习技巧，有几点不太明白，望抽空解答：
go doc net&#47;http | grep &quot;^func&quot; 这个命令不是能查询出 net&#47;http 库所有的对外库函数吗，那 http.FileServer 不也是对外的库函数吗，为啥没有列出来</div>2022-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/72/85/c337e9a1.jpg" width="30px"><span>老兵</span> 👍（0） 💬（0）<div>1. 使用go doc net&#47;http.FileServer | grep &#39;^func&#39; 得到结果 func FileServer(root FileSystem) Handler
2. 使用fs作为handler传递给http.Handle 作为参数，这样可以更加route的map，得到fs作为静态文件的handler方法。
3. FileServer方法中创建一个fileHandler的结构，文件路径作为root被传入fileHandler的结构中。与此同时handler都需要实现ServeHTTP的方法。
4. fileHanlder.ServeHTTP 方法中在使用&quot;upath := r.URL.Path&quot;得到upath后，将这个路径作为文件路径调用serveFile方法，这个方法根据请求文件进行Open操作。
5. 最后将文件读取的内容作为参数调用serveContent方法，方法中对io操作进行处理，最后io.CopyN将content赋值到w（ResponseWriter）中，也就是response</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（0）<div>找到了 dirList 打印文件目录 </div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（0）<div>打卡第一题，跟着老师学习完然后有机会可以和老师交流。</div>2021-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ba/0d/5b7c8ff9.jpg" width="30px"><span>winkyi</span> 👍（0） 💬（0）<div>&#47;&#47; 具体处理逻辑的处理函数
func (sh serverHandler) ServeHTTP(rw ResponseWriter, req *Request) {
  handler := sh.srv.Handler
  if handler == nil {
    handler = DefaultServeMux
  }
  ...
  handler.ServeHTTP(rw, req)
}

老师好，到第六层的这个方法有点不明白,同样是命名为ServeHTTP的接口,怎么和main函数中定义的Handle和HandleFunc方法进行关联。</div>2021-10-20</li><br/>
</ul>