你好，我是孔令飞。

[上一讲](https://time.geekbang.org/column/article/401190)，我介绍了 iam-apiserver 是如何构建 Web 服务的。这一讲，我们再来看下 iam-apiserver 中的核心功能实现。在对这些核心功能的讲解中，我会向你传达我的程序设计思路。

iam-apiserver 中包含了很多优秀的设计思想和实现，这些点可能比较零碎，但我觉得很值得分享给你。我将这些关键代码设计分为 3 类，分别是应用框架相关的特性、编程规范相关的特性和其他特性。接下来，我们就来详细看看这些设计点，以及它们背后的设计思想。

## 应用框架相关的特性

应用框架相关的特性包括三个，分别是优雅关停、健康检查和插件化加载中间件。

### 优雅关停

在讲优雅关停之前，先来看看不优雅的停止服务方式是什么样的。

当我们需要重启服务时，首先需要停止服务，这时可以通过两种方式来停止我们的服务：

- 在 Linux 终端键入 Ctrl + C（其实是发送 SIGINT 信号）。
- 发送 SIGTERM 信号，例如 `kill` 或者 `systemctl stop` 等。

当我们使用以上两种方式停止服务时，都会产生下面两个问题：

- 有些请求正在处理，如果服务端直接退出，会造成客户端连接中断，请求失败。
- 我们的程序可能需要做一些清理工作，比如等待进程内任务队列的任务执行完成，或者拒绝接受新的消息等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（6） 💬（2）<div>Extend和ExtendShadow设计真的很棒，敢问灵感从哪里来的👍</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（5） 💬（4）<div>这两篇老师的总结很受启发。
练习：
1 在项目中一般还是使用goroutine比较多，或者atomic，或者读写锁；
2 限流可以使用令牌桶和漏桶，或者自适应限流；

问：
一个业务通过A-&gt;B-&gt;C完成，通过requestID可以串起来，假如严格一点，是不是还要搞个parnent-request-id ？</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（3） 💬（1）<div>健康检查这里有两个疑问：
1 配置了健康检查会阻塞，不会运行 eg.Wait() ，这是故意阻塞在ping这里的吗？
2 健康检查ping函数for中，我查看到逻辑是这样的，
  a) 在启动时web服务还未启动，会出错err，每隔1s运行一次，
  b) 当服务正常启动后，这是能请求通畅，然后就return nil，只运行一次就不再运行了。
这个逻辑有些疑惑，健康检查不应该总是运行的么？

代码位置：iam&#47;internal&#47;pkg&#47;server&#47;genericapiserver.go
版本：当前master版本</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（2） 💬（3）<div>项目源码中的var _ UserSrv = (*userService)(nil) 的目的是为了在编译阶段检查 userServer 类型是否实现了 UserSrv 的接口, 如果没有实现则panic, (*userService)(nil)这种语法是出自哪里呢, 在哪里能找到这个语法的详细说明呢, 我找了半天没找到, 只知道(*userService)(nil)用来表示类型*userService的零值.</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/1f/f3/791d0f5e.jpg" width="30px"><span>xgt132</span> 👍（1） 💬（1）<div>老师你好：在 ”并发处理模板“这一模块时，当遇到错误就会返回nil, 此时剩下的协程会不会还在继续运行，这样是不是浪费了系统资源呢</div>2022-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/7e/ebc28e10.jpg" width="30px"><span>NULL</span> 👍（1） 💬（1）<div>&quot;这样，我们下次需要新增参数的话，只需要调用 context 的 WithValue 方法：&quot;
这样不好吧, 传递的sex可能会被修改. 也不清晰, 不知道传递了什么数据

官方文档也说
&quot;Use context Values only for request-scoped data that transits processes and APIs, not for passing optional parameters to functions.&quot;
https:&#47;&#47;pkg.go.dev&#47;context</div>2022-08-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKXjfJWVQGDHmDEI73VQO4dgTzaK5LLz2ax9XUF4FCPy1Oib8aQLibFzpcsiavVVbAQlG4pbrfibdwaYA/132" width="30px"><span>Geek_63505f</span> 👍（1） 💬（2）<div>老师请问下这里 下面那个run方法是启动命令行的命令吗？我看a.cmd.Execute()命令里面是执行os.Args[1:] 。
         apiserver.NewApp(&quot;iam-apiserver&quot;).Run()
                   func (a *App) Run() {
	if err := a.cmd.Execute(); err != nil {
		fmt.Printf(&quot;%v %v\n&quot;, color.RedString(&quot;Error:&quot;), err)
		os.Exit(1)
	}
}   </div>2022-01-27</li><br/><li><img src="" width="30px"><span>Geek_433b2b</span> 👍（1） 💬（1）<div>孔老师，你好。我是 Go 语言初学者，在并发处理模板这块有个疑问：
为什么在协程中不是直接对参数 user 赋值：user.TotalPolicy = policies.TotalCount，最后直接返回 users。而是重新创建一个 User 对象？包括在 ListWithBadPerformance 中也是重新创建了一个对象。
我写了个 demo 是可以正常赋值的。这样做的话不就可以不使用 map 了吗，而且也能保证顺序。</div>2021-12-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（1） 💬（1）<div>请问SQL文件里面时间字段为什么是如下语句？和实际gorm的逻辑不一致
```sql
`createdAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
`updatedAt` timestamp NOT NULL DEFAULT &#39;0000-00-00 00:00:00&#39;,
```
实际表现应该是如下
```sql
`createdAt` timestamp NOT NULL DEFAULT current_timestamp(),
`updatedAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
```
</div>2021-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5f/e2/e6d3d9bf.jpg" width="30px"><span>XI</span> 👍（1） 💬（2）<div> go func() {        &#47;&#47; 将服务在 goroutine 中启动        if err := srv.ListenAndServe(); err != nil &amp;&amp; err != http.ErrServerClosed {            log.Fatalf(&quot;listen: %s\n&quot;, err)        }    }()
优雅关停机这段代码，当前面有nginx的时候是无法拿到客户端ip的，拿到的ip 会是nginx的ip 详请可见gin 的r.run 方法

</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/18/4f/9e4d5591.jpg" width="30px"><span>翡翠虎</span> 👍（1） 💬（1）<div>老师可不可以讲讲那些断线重连的实现，例如消息队列的断线重连、数据库的断线重连等。是 go func 协程定时去检查连接状况（异常时重连），还是有其他方法处理这类问题？先谢谢老师</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（1） 💬（1）<div>有个问题咨询下，initRedisStore这个函数 defer cancel() 通常要先执行，若是这样ConnectToRedis会直接retrun吧，是吗？若是这样当ConnectToRedis协程运行到for 时，会直接在 &lt;-ctx.Done():后return，并关闭defer tick.Stop()，因此感觉&lt;-tick.C貌似总是用不到。
【见iam&#47;internal&#47;apiserver&#47;server.go的函数initRedisStore()】

func (s *apiServer) initRedisStore() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	config := &amp;storage.Config{
		Host:                  s.redisOptions.Host,
		Port:                  s.redisOptions.Port,
		Addrs:                 s.redisOptions.Addrs,
		MasterName:            s.redisOptions.MasterName,
		Username:              s.redisOptions.Username,
		Password:              s.redisOptions.Password,
		Database:              s.redisOptions.Database,
		MaxIdle:               s.redisOptions.MaxIdle,
		MaxActive:             s.redisOptions.MaxActive,
		Timeout:               s.redisOptions.Timeout,
		EnableCluster:         s.redisOptions.EnableCluster,
		UseSSL:                s.redisOptions.UseSSL,
		SSLInsecureSkipVerify: s.redisOptions.SSLInsecureSkipVerify,
	}

	&#47;&#47; try to connect to redis
	go storage.ConnectToRedis(ctx, config)
}</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（1） 💬（1）<div>源码中的storeIns, _ := mysql.GetMySQLFactoryOr(nil),  其中GetMySQLFactoryOr这个函数名的Or是表达的什么意思呢</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/de/5819440a.jpg" width="30px"><span>旋风</span> 👍（1） 💬（1）<div>并发处理模板如何复用，只能复制粘贴吗？</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/6b/af7c7745.jpg" width="30px"><span>tiny🌾</span> 👍（0） 💬（2）<div>Extend和ExtendShadow 存储在db是json格式，这个怎么去SQL查询了？ 还有每次都需要编解码性能怎么样</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4d/90/b34f4a91.jpg" width="30px"><span>GGFGG</span> 👍（0） 💬（1）<div>并发模版那里，errChan := make(chan error, 1)，这是个缓冲 chan，如果并发的 goroutine 都出错，那么对 errChan 的写就会阻塞，难道没有 goroutine 泄露风险么？</div>2022-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/9a/6f/c4490cf2.jpg" width="30px"><span>czy</span> 👍（0） 💬（2）<div>请问老师，在并发处理那里，使用sync.Map存储数据，通过m.Store(user.ID, &amp;v1.User{})把所有的数据存储进去以后会按照user.ID排序吗？会什么说再取出来以后会和数据库中的顺序是一致的呢？</div>2022-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/47/78/c9f22d40.jpg" width="30px"><span>运维开发故事</span> 👍（0） 💬（1）<div>老师你好，extend字段如果扩展多了，数据库中存的json就会越来越大，这样不会影响性能么</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/80/9f/b78478fe.jpg" width="30px"><span>阳明</span> 👍（0） 💬（1）<div>一路看老师的文章学到不少知识，这篇也是，但还是有两个小问题：
1.  Extend 类型直接实现 Value() &amp; Scan() 应该能简单做到 string 和 map 的转换，这样不需要用到 gorm 的 hook 和加一个冗余字段；
2. ctx 作为第一个参数，存储 request id 我能理解，但是把业务参数也放里面总感觉很奇怪，并且这样做同样也需要改动调用函数的代码，原文的理由似乎站不住脚。还有如果其他开发用到这个函数，必须知道函数的显示参数和 context 里的参数，这样是不是不太合适。
希望老师能帮助解答，谢谢。</div>2022-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/18/19/11780879.jpg" width="30px"><span>云边红日</span> 👍（0） 💬（1）<div>https:&#47;&#47;blog.csdn.net&#47;flye422304&#47;article&#47;details&#47;116890946</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/18/19/11780879.jpg" width="30px"><span>云边红日</span> 👍（0） 💬（1）<div>发送 SIGTERM 信号，例如 kill -9 或XXX . 老师这里讲的 kill -9 发送的好像不是SIGTERM信号，SIGKILL  才是kill -9 。</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（1）<div>select {
  case &lt;-finished: 
    &#47;&#47; 这里其实要判断下，errChan 是否为空
  case err := &lt;-errChan: 
  	return nil, err 
}</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（1）<div>总结：
应用框架相关的特性：
1. 接收并处理信号，与 net&#47;http 的 ShutDown 方法，google.golang.org&#47;grpc 的 GracefulStop 方法联动起来。
2. 健康检查。服务启动后，自己开始启动检查 healthz 接口是否能正常工作，如果在10s内仍无法完成启动，则程序退出。相当于 k8s 的 startup probe。
3. 插件的集中管理，以及选择性使用。

编程规范相关的特性：
1. API 版本。你不但需要在URI中添加版本标识，还需要在代码结构中标识版本。如果以资源作为package名称，那么package内部的文件名可以是动词，对应CRUD操作。
2. 统一的资源元数据。资源元数据是要存储到数据中的，有ID、InstanceID、Name、ExtendShadow、CreatedAt、UpdatedAt。建议所有的 REST 资源都使用统一的资源元数据。
3. 通过 Extend 和 ExtendShadow 为资源添加扩展属性，在数据库层面引入了一个string类型的列。

其它特性：
1. build tag 功能，方面你在两个库之间快速切换它们的实现
</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（1）<div>第三步，iam-authz-server 会订阅 iam.cluster.notifications通道，当监听到有 SecretChanged&#47;PolicyChanged 消息时，会请求 iam-apiserver 拉取所有的密钥 &#47; 授权策略。

每次变更，都是全量拉消息？</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/81/0f/f8ced7d9.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div>第二步，当我们通过控制台调用 iam-apiserver 密钥 &#47; 授权策略的写接口（POST、PUT、DELETE）时，会向 Redis 的 iam.cluster.notifications通道发送 SecretChanged&#47;PolicyChanged 消息。

看代码这个通知的操作注册在push middleware里面了，只要用户触发&#47;v1&#47;policies API， 就会发送通知；但是实际情况下，调用API并不会每次都成功，也有401、500的情况，合理的逻辑应该是调用API成功后才去通知吧？</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/83/17/df99b53d.jpg" width="30px"><span>随风而过</span> 👍（3） 💬（0）<div>get到，都是干活，代码很简单，主要是整个思路才是干货。</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/57/2a/cb7e3c20.jpg" width="30px"><span>Nio</span> 👍（2） 💬（0）<div>很不错，有启发，边学边用！</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/02/03/3cc4c2f4.jpg" width="30px"><span>KyLin</span> 👍（1） 💬（0）<div>每一个iam-authz-server实例都直接用远端redis做缓存，不是更好地解决了数据一致性问题么</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（1） 💬（0）<div>iam-apiserver中用到的技术点，每一个都经过对比分析，用得恰到好处。
对技术点也进行了详细的介绍，清晰明了。
iam-apiserver项目可以作为很好的参考（copy）对象。</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（0） 💬（0）<div>这里还有一个问题：当ExtendShadow错误为空时，查询数据会出错吧？应该加个判断是否为空的逻辑吧？</div>2023-08-07</li><br/>
</ul>