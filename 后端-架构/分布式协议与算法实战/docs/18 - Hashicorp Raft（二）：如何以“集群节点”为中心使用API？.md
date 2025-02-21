你好，我是韩健。

上一讲结束后，相信有的同学已经跃跃欲试，想把Hashicorp Raft使用起来了。不过，也有一些同学跟我反馈，说自己看到Hashicorp Raft的[Godoc](https://godoc.org/github.com/hashicorp/raft)，阅读完接口文档后，感觉有些不知所措，无从下手，Hashicorp Raft支持了那么多的函数，自己却不知道如何将这些函数使用起来。

这似乎是一个共性的问题，在我看来，之所以出现这个问题，是因为文档里虽然提到了API的功能，但并没有提如何在实际场景中使用这些API，每个API都是孤立的点，缺乏一些场景化的线将它们串联起来。

所以，为了帮你更好地理解Hashicorp Raft的API接口，在实践中将它们用起来，我以“集群节点”为核心，通过创建、增加、移除集群节点，查看集群节点状态这4个典型的场景，具体聊一聊在Hashicorp Raft中，通过哪些API接口能创建、增加、移除集群节点，查看集群节点状态。这样一来，我们会一步一步，循序渐进地彻底吃透Hashicorp Raft的API接口用法。

我们知道，开发实现一个Raft集群的时候，首先要做的第一个事情就是创建Raft节点，那么在Hashicorp Raft中如何创建节点呢？

## 如何创建Raft节点
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/53/db/858337e3.jpg" width="30px"><span>Ethan Liu</span> 👍（9） 💬（2）<div>老师 状态机的作用是什么，为什么一定要有这个呢</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/9d/daad92d2.jpg" width="30px"><span>Stony.修行僧</span> 👍（8） 💬（2）<div>讲讲增删改查背后的真相</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/3c/0668d6ae.jpg" width="30px"><span>盘胧</span> 👍（2） 💬（1）<div>这就很爽了，搭配一下文档看还是很吃力。加油</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8d/3b/42d9c669.jpg" width="30px"><span>艾瑞克小霸王</span> 👍（1） 💬（1）<div>服务器ID是在什么地方设置的呢？node的config吗？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/21/8c13a2b4.jpg" width="30px"><span>周龙亭</span> 👍（0） 💬（1）<div>非leader节点怎么启动呢？</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/9e/12a23f16.jpg" width="30px"><span>东尘西土</span> 👍（0） 💬（1）<div>ip+端口号代表一个节点，构造单机集群</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/ea/ce9854a5.jpg" width="30px"><span>坤</span> 👍（0） 💬（1）<div>请问加入集群的请求时Raft的哪个API或者RPC？</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/18/8cee35f9.jpg" width="30px"><span>HuaMax</span> 👍（0） 💬（2）<div>集群最开始的时候，只有一个节点，我们让第一个节点通过 bootstrap 的方式启动，它启动后成为领导者
——————————————
请问老师，节点不是通过投票成为领导者吗？是不是所有节点都是bootstrap方式启动，然后再竞争成为领导者？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>1.在启动节点的函数中,使用pid作为唯一区分,在内存中,进行内存地址的交流
2.利用端口号加localhost作为本地的不同标识,进行相关的启动</div>2020-08-25</li><br/>
</ul>