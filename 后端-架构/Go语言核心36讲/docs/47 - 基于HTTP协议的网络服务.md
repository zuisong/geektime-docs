我们在上一篇文章中简单地讨论了网络编程和socket，并由此提及了Go语言标准库中的`syscall`代码包和`net`代码包。

我还重点讲述了`net.Dial`函数和`syscall.Socket`函数的参数含义。前者间接地调用了后者，所以正确理解后者，会对用好前者有很大裨益。

之后，我们把视线转移到了`net.DialTimeout`函数以及它对操作超时的处理上，这又涉及了`net.Dialer`类型。实际上，这个类型正是`net`包中这两个“拨号”函数的底层实现。

我们像上一篇文章的示例代码那样用`net.Dial`或`net.DialTimeout`函数来访问基于HTTP协议的网络服务是完全没有问题的。HTTP协议是基于TCP/IP协议栈的，并且它也是一个面向普通文本的协议。

原则上，我们使用任何一个文本编辑器，都可以轻易地写出一个完整的HTTP请求报文。只要你搞清楚了请求报文的头部（header）和主体（body）应该包含的内容，这样做就会很容易。所以，在这种情况下，即便直接使用`net.Dial`函数，你应该也不会感觉到困难。

不过，不困难并不意味着很方便。如果我们只是访问基于HTTP协议的网络服务的话，那么使用`net/http`代码包中的程序实体来做，显然会更加便捷。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/b1/0f/e81a93ed.jpg" width="30px"><span>嘎嘎</span> 👍（9） 💬（1）<div>看测试用例中是用 srv.Shutdown(context.Background()) 的方式停止服务，通过RegisterOnShutdown可添加服务停止时的调用</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5c/67/4e776ee6.jpg" width="30px"><span>袁树立</span> 👍（1） 💬（1）<div>如此一来，每当一个 HTTP 请求被递交时，就都会产生一个新的网络连接。这样做会明显地加重网络服务以及客户端的负载，并会让每个 HTTP 事务都耗费更多的时间。所以，在一般情况下，我们都不要去设置这个DisableKeepAlives字段。

老师，针对这句话，有个问题。
因为我们的服务调用其他内网接口，会通过公司的负载均衡。七层负载均衡是关闭了keep-alive的。所以我们的http就每次都是短链接。   那每次http事务耗费的时间大概是什么量级？  我这里看到，设置了500ms超时的情况下。在频繁请求的场景，每过几分钟就会有一批超时。报net&#47;http  timeout 。
用http trace看，是在getConn前就耗费了500ms

请问，这种情况正常吗？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>郝林老师，在demo94.go中这个字段的值：

DualStack: true,

其中“DualStack”会被编辑器用横线从中穿过，并提示：&#39;DualStack&#39; is deprecated 。</div>2021-09-02</li><br/><li><img src="" width="30px"><span>qiushye</span> 👍（0） 💬（3）<div>http.Transport里没有MaxConnsPerHost字段了，article36&#47;q1的程序运行报错</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/74/7f/114062a3.jpg" width="30px"><span>晨曦</span> 👍（27） 💬（0）<div>“人生的道路都是由心来描绘的，所以，无论自己处于多么严酷的境遇之中，心头都不应为悲观的思想所萦绕。”
被老师的精神打动，真心祝愿早日康复！</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/00/a4a2065f.jpg" width="30px"><span>Michael</span> 👍（10） 💬（0）<div>看了下源码之后感觉应该这样做：

quit := make(chan os.Signal, 1)
signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

server := http.Server{..}

go func(){
     server. ListenAndServe()
}()

&lt;-quit

server.Shutdown()

Shutdown 并不会立即退出，他会首先停止监听，并且启动一个定时器，避免新的请求进来，然后关闭空闲链接，等待处理中的请求完成或者如果定时器到了，再退出，和 NGINX 的 平滑退出很像。</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（5） 💬（0）<div>老师可以讲一下这个不：gomonkey，我看半天都没明白这个打桩是什么意思</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/26/fd4eda95.jpg" width="30px"><span>aebn</span> 👍（2） 💬（0）<div>谢谢老师分享，努力学习中^_^</div>2018-11-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ywV5EjGPovkbcj9zRmibTKBQjAvCFrKVYMmGfDwGfcz6dmq6Sia1AlHvSX8ydibu2xueLuSen1YVDZSKNib1UTJBsQ/132" width="30px"><span>路人</span> 👍（1） 💬（0）<div>这节老师讲得特别好，特别是问题的衍生能思考到很多go的其他重要模块，比如net、io等。</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/c7/083a3a0b.jpg" width="30px"><span>新世界</span> 👍（0） 💬（0）<div>讲的很不错，把http常用的参数注意事项都讲了一遍，这一块是通用技能，无论哪种语言，发送http请求都会有这些参数，很不错</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/ba/3b30dcde.jpg" width="30px"><span>窝窝头</span> 👍（0） 💬（0）<div>我一般通过context的cancel函数，同时通过系统信号量来触发cancel事件</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/e5/3dca2495.jpg" width="30px"><span>上山的o牛</span> 👍（0） 💬（0）<div>学习中，衍生的内容可以看一周</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ac/95/9b3e3859.jpg" width="30px"><span>Timo</span> 👍（0） 💬（1）<div>demo91.go  例子中
reqStrTpl := `HEAD &#47; HTTP&#47;1.1
Accept: *&#47;*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: %s
User-Agent: Dialer&#47;%s
`
协议和头信息之间要空两行，才能正常发出信息</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（0）<div>打卡</div>2019-03-15</li><br/>
</ul>