你好，我是秦粤。上一讲我们通过一个Node.js纯FaaS的Serverless应用，给你介绍了Serverless引擎盖下的运作机制，总结来说，FaaS依赖分层调度和极速冷启动的特性，在无事件时它居然可以缩容到0，就像我们的声控灯一样，有人的时候它可以亮起来，没人的时候，又可以自动关了。

听完了原理，我估计你肯定会问，FaaS这么好，但是它的应用场景是什么呢？今天我们就来一起看下。不过，想要理解FaaS的应用场景，我们就需要先理解FaaS的进程模型，这也是除了冷启动之后的另外一个重要概念。

## FaaS进程模型

咱先回想一下上节课的FaaS的冷启动过程，我们知道容器和Runtime准备阶段都是由云服务商负责的，我们只需要关注具体的函数执行就可以了。而函数执行在FaaS里是由“函数服务”负责的，当函数触发器通知“事件”到来时，函数服务就会根据情况创建函数实例，然后执行函数。当函数执行完之后，函数实例也随之结束自己的使命，FaaS应用缩容到0，然后开始进入节能模式。

上面这套逻辑是我们上节课讲的，课后有同学就问，函数执行完之后实例能否不结束，让它继续等待下一次函数被调用呢？这样省去了每次都要冷启动的时间，响应时间不就可以更快了吗？
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（17） 💬（4）<div># 最近几天实战了下阿里云的函数计算服务.
使用golang按着官方文档,实现了几个常驻进程模型的服务.
也照着老师的操作,建了node.js和python的函数.

相比之下,python和node.js的冷启动时长确实比较短,我这边看冷启动时接口的响应耗时在600-800ms.
但是之后热启动时的耗时就只有30-50ms.
而golang的冷启动时长不知道为什么要2.5s.而热启动后的接口耗时也才60ms.

我还发现,阿里云上,5分钟以后,常驻进程模型的函数就被干掉了.症状就是初次接口耗时又要2s+.
可以肯定的是,不到10分钟,无响应的函数就被系统回收了.肯定是没到15分钟.

我还发现,介于冷启动和热启动之间,还有一个状态,接口的响应耗时也是介于两者之间.

# 对服务编排的个人感悟
感觉函数服务配合服务编排,就像是在linux上使用shell组合各种命令,实现复杂的功能.
虽然每个命令都很简单,但是组合后的功能就很强大了.
现在的云服务都会有很多现成的sdk,确实如老师所说,需要用到某个云服务时临时把官方的文档拿出来,几乎只需要做很少的变动,就可以马上投入使用.

我目前使用函数服务,配合nas和日志服务,就可以很容易的把东西存在nas上,在阿里云的日志服务中搜索相关日志.
不足之处就是调试没有之前方便了.
</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（9） 💬（1）<div>阿里云 有个 serverless 工作流 是不是就是 一个阿里云提供的云服务的编排工具？</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（3） 💬（8）<div>常驻型应用的冷启动时间会增加, 这里为什么会增加呢？ 不应该是减少吗？ 只需要第一次启动后，长驻内存不就行了吗？</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/10/af49fa20.jpg" width="30px"><span>左耳朵狮子</span> 👍（2） 💬（1）<div>老师 有没有什么好的Serverless 论文推荐推荐 CMU 啥的都可以哈。
</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（1） 💬（1）<div>Serverless要想发展的好，一定要有一套标准的应用迁移方案，这样才能保证现有的大量应用可以平滑的过渡。
目前来看，我个人的理解，对于现有应用，可能常驻进程方式合适一些，对于新应用，用后即销毁的方式更合适。这里搞了一刀切，可能不太对哈。</div>2020-05-10</li><br/><li><img src="" width="30px"><span>suke</span> 👍（1） 💬（1）<div>用完即毁型的服务里如果有mysql的连接查询，建立连接岂不是很慢？而且如果查询不频繁，那岂不是每次都查询要等好久？老师有这方面的实践么</div>2020-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKGeekKkZzialiaB8zNQ4gVp2fNfaAfic8iaiaHBibqZDAMjaROR6sPQIjsSyGmFzLZVFibETh9ZoUhWwHfQ/132" width="30px"><span>InfoQ_f14f3f64ad3e</span> 👍（1） 💬（1）<div>老师你好！函数服务一般是用在无状态场景下，但是看到发邮件的那个例子，存储验证码的常驻服务看起来是个有状态的，是常驻进程类型的可以处理有状态服务吗</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/34/c1/4e4917f5.jpg" width="30px"><span>有一种踏实</span> 👍（0） 💬（1）<div>课程微信群是哪个</div>2023-08-22</li><br/><li><img src="" width="30px"><span>Geek_d972f2</span> 👍（0） 💬（1）<div>&quot;我们的 Web 服务主进程跟之前一样，创建一个子进程来处理这个请求事件&quot;这里没明白，Web服务主进程是指Node进程吗？如果是，Node不是采用事件循环机制来处理请求吗？</div>2023-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/10/79/390568f3.jpg" width="30px"><span>kkkkkkkk</span> 👍（0） 💬（1）<div>老师你好，我node基础薄弱的前端开发，这一节看得有点吃力，需要补充哪些知识可以更能理解老师的优质内容</div>2020-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/b0/78/b4a8d4d1.jpg" width="30px"><span>贫困山区杨先生</span> 👍（0） 💬（6）<div>请问一下老师：按照上面的做，也设置了SDK的access key和secret key
Response
Module &#39;&#47;code&#47;index.php&#39; is missing.</div>2020-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>php 最初的模型就是一个请求创建一个进程。</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/05/09aaa06c.jpg" width="30px"><span>yiwu</span> 👍（0） 💬（1）<div>老师，我在想问FaaS适合做VPN吗？好像也没有人操作过这个，应该是有什么难题需要解决。</div>2020-05-14</li><br/><li><img src="" width="30px"><span>Geek_f7f72f</span> 👍（0） 💬（1）<div>似乎传统的OOP和设计模式在FaaS领域应用不大?  感觉缺少class，适用场景确实有限制</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/81/d5/00efc5b7.jpg" width="30px"><span>Charlie</span> 👍（0） 💬（2）<div>你好老师，我的没收到邮件，显示如下，请问是什么问题？？怎么解决？
Response

email send!

Function Logs

FC Invoke Start RequestId: 2607ad8c-02c9-41b0-b062-16f2ac5507c5

InvalidAccessKeyId.NotFoundSpecified access key is not found.FC Invoke End RequestId: 2607ad8c-02c9-41b0-b062-16f2ac5507c5


Duration: 116.70 ms, Billed Duration: 200 ms, Memory Size: 512 MB, Max Memory Used: 9.97 MB

Request ID
2607ad8c-02c9-41b0-b062-16f2ac5507c5</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6c/69/d5a28079.jpg" width="30px"><span>Bora.Don</span> 👍（0） 💬（1）<div>对老师关于数据编排的看法，存在一点疑问：数据不在本地，会不会存在稳定性和速度的问题？
FaaS感觉看上去很美，实际操作空间还有待考验，个人观点。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/41/820e14af.jpg" width="30px"><span>Marooned。</span> 👍（1） 💬（3）<div>因为用完即毁型对传统 MVC 改造的成本太大 为什么会大呢？</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/71/ed/45ab9f03.jpg" width="30px"><span>八哥</span> 👍（0） 💬（0）<div>服务编排应该后面会讲到serverless framework。</div>2020-04-24</li><br/>
</ul>