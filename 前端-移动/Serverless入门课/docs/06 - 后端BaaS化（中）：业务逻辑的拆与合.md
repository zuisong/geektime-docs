你好，我是秦粤。上一课中，我们学习了后端BaaS化的重要模块：微服务。现在我们知道微服务的核心理念就是先拆后合，拆解功能是为了提升我们功能的利用率。同步我们也了解了实现微服务的10要素，这10要素要真讲起来够单独开一门课的。如果你不熟悉，我向你推荐杨波老师的[《微服务架构核心20讲》](https://time.geekbang.org/course/intro/100003901)课程。

BaaS化的核心其实就是把我们的后端应用封装成RESTful API，然后对外提供服务，而为了后端应用更容易维护，我们需要将后端应用拆解成免运维的微服务。这个逻辑你要理解，这也是为什么我要花这么多篇幅给你谈微服务的关键原因。

上节课我们将“待办任务”Web服务的后端，拆解为用户微服务和待办任务微服务。但为什么要这样拆？是凭感觉，还是有具体的方法论？这里你可以停下来想想。

微服务的拆解和合并，都有一个度需要把握，因为我们在一拆一合之间，都是有成本产生的。如果我们拆解得太细，就必然会导致我们的调用链路增长。调用链路变长，首先影响的就是网络延迟，这个好理解，毕竟你路远了，可能“堵车”的地方也会变多；其次是运维成本的增加，调用链路越长，整个链条就越脆弱，因为其中一环出现问题，都会导致整个调用链条访问失败，而且我们排查问题也变得更加困难。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（3） 💬（1）<div>老师，请问下BaaS化就是把后端服务设计成微服务，提供标准的RestFul Api给客户端，且客户端无需关注服务端的ops工作是吧， 感觉像是后端服务直接&quot;云化&quot;了。</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（3） 💬（1）<div>今天在实践的过程中,走了些弯路,在此提醒一下同学.

实际上的架构图是&#39;JWT示意图&#39;.
index-faas和rule-faas两个是分开部署的.
两个函数的触发器都是ANONYMOUS方式!!!

index-faas中的&#47;api&#47;currentUser接口负责生成jwtToken.
rule-faas中接口&#47;api&#47;rule的post、delete、put方法才验证jwtToken.
作为实验,可以在`新建`代办前,将浏览器中的cookie移除,再请求时会收到403的错误码.
</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（3）<div>我昨天实践了云溪社区的一篇文章,是关于Serverless进行CI&#47;CD的.
觉得值得一看,推荐给大家.
[Serverless 实战 —— Funcraft + OSS + ROS 进行 CI&#47;CD](https:&#47;&#47;yq.aliyun.com&#47;articles&#47;741414)
该文章,演示了发布前的验证环节.

后面的回归验证和灰度流量验证,就需要其他技术了.
比如借助k8s方便的部署多套环境,进行回归验证.
使用k8s&#47;istio实现金丝雀&#47;灰度发布.
</div>2020-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIrg3ZKwyfUSoWDdB4mdmEOCeicfWO5WJXvNwDJsy6QV18gwQ5rlUg9MmYGIjCWU6QqQIZnXXGonIw/132" width="30px"><span>miser</span> 👍（1） 💬（1）<div>或许我有基本的后端部署认知，我感觉serverless在架构设计上意义不大，但是在人员安排上意义重大，对于前端来说可以不太关心运维的工作，代码推上线就完了，它帮助前端或者不太懂运维的开发者解决了大量运用工作，降低了上线成本和学习成本。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/e3/2529c7dd.jpg" width="30px"><span>吴科🍀</span> 👍（1） 💬（1）<div>老师的课程实践性很强。实验的例子，如果没有云服务器，可以在本地环境模似吗。</div>2020-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIro8BKyich3jMOTRFibsbYeX9oWfNUa6dAcNDia5EH7VVHbibiaZavnDX1VlZ8NbQGrtJuYz0oKkfgSNA/132" width="30px"><span>Programmer</span> 👍（0） 💬（1）<div>老师想咨询一下，为什么“待办任务”架构图到这一节没有SFF层了呢，这里的faas函数充当什么角色呢</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/48/15/8db238ac.jpg" width="30px"><span>神仙朱</span> 👍（0） 💬（1）<div>老师好，现在我们做的作业就是baas吗，怎么感觉还是在faas中做，这样还是不能连数据库哇</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/10/af49fa20.jpg" width="30px"><span>左耳朵狮子</span> 👍（0） 💬（1）<div>&quot;线上根据灰度策略，将小部分流量导入灰度环境验证灰度版本。&quot; 老师这块能否说的再细一点。
假设在Cloud-native 开发中，小部分流量倒入这个docker container(s) 来验证，如果灰度发布不成功。是否多个containers 全部销毁，还是编排到其他containers。</div>2020-05-19</li><br/>
</ul>