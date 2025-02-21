为了支持水平扩展和高可用，Tomcat提供了集群部署的能力，但与此同时也带来了分布式系统的一个通用问题，那就是如何在集群中的多个节点之间保持数据的一致性，比如会话（Session）信息。

要实现这一点，基本上有两种方式，一种是把所有Session数据放到一台服务器或者一个数据库中，集群中的所有节点通过访问这台Session服务器来获取数据。另一种方式就是在集群中的节点间进行Session数据的同步拷贝，这里又分为两种策略：第一种是将一个节点的Session拷贝到集群中其他所有节点；第二种是只将一个节点上的Session数据拷贝到另一个备份节点。

对于Tomcat的Session管理来说，这两种方式都支持。今天我们就来看看第二种方式的实现原理，也就是Tomcat集群通信的原理和配置方法，最后通过官网上的一个例子来了解下Tomcat集群到底是如何工作的。

## 集群通信原理

要实现集群通信，首先要知道集群中都有哪些成员。Tomcat是通过**组播**（Multicast）来实现的。那什么是组播呢？为了理解组播，我先来说说什么是“单播”。网络节点之间的通信就好像是人们之间的对话一样，一个人对另外一个人说话，此时信息的接收和传递只在两个节点之间进行，比如你在收发电子邮件、浏览网页时，使用的就是单播，也就是我们熟悉的“点对点通信”。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（12） 💬（1）<div>感觉这种方式应该在生产环境用的很少吧，大多数都是用redis集群来保存session</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（6） 💬（2）<div>老师您好，有两个问题想咨询一下：

1、采用DeltaManager模式后，如果主节点挂掉，存在新的主节点选举的这个过程吗？如果有的话，Tomcat是如何防止产生集群分裂（脑裂）的呢？

2、本节说的Tomcat集群部署，入口是Tomcat还是Apache啊？
之前只用过Apache做负载，后面放了Tomcat集群。但说实话，Tomcat session复制的效率还是太低了。
后面就直接Nginx+多个Tomcat，Session干脆放到了Redis里，效率高了很多。</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7d/dd852b04.jpg" width="30px"><span>chon</span> 👍（5） 💬（1）<div>生产中，如果机器多的话，很少用session复制吧</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（2） 💬（1）<div>Tomcat的Session同步机制有两种：
第一是所有集群机器中都保存一份其他机器的数据
第二是备份模式，Session数据保存在任意两台机器中。
我的问题是游戏服务器之间的数据同步是否也可以采用类似的机制呢？其中有两个挑战：一是玩家数据比较大，二是事务如何处理</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（1） 💬（1）<div>好老师哈。那些操作一般不会涉及session变化。BackupManager实现高可用，和好多中间件的原理差不多。以前都是接入层一致性hash，没有启用session集群。这个session集群同步开销高么?一次只同步一个seesion还是批量打包的?Tomcat支持把session放在redis么?我项目是token+redis。</div>2019-07-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIvUlicgrWtibbDzwhLw5cQrDSy2JuE1mVvmXq11KQIwpLicgDuWfpp9asE0VCN6HhibPDWn7wBc2lfmA/132" width="30px"><span>a、</span> 👍（1） 💬（1）<div>今天的问题:我觉得因为一般静态资源不会涉及到session更新，所以就不需要拦截。还有个问题我想问下老师，如果我有四台机器A,B,C,D,设置了BackupManager，那A的备份机器会不会是B，B的备份机器是C，C的备份机器是D，D的备份机器是A？还是说如果A的备份机器是B，那C只能选择D做备份机器？</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（3） 💬（1）<div>这个集群感觉只是教学版，不工程版。应该很少用于生产</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（3） 💬（3）<div>这些方法感觉有些过时了。比如我们可以自己实现一致性哈希算法，也就是说，针对不同的会话，我们给他算一个hash，让它分配到同一个tomcat上。</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5f/67/aedbc96d.jpg" width="30px"><span>你的头发还好吗</span> 👍（1） 💬（0）<div>针对 ReplicationValve 设置 filter值，这些静态文件不会改变 session 状态，不需要进行session同步操作。
翻阅源码：
if (!isRequestWithoutSessionChange(uri)) {
   sendMessage(session,manager);
}</div>2022-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（1） 💬（0）<div>小集群或者一开始没集群但是很久后流量较大或者保证可用性&#47;防止部署时单点故障时可以使用，不过大部分或者一开始就是集群都是redis session集群</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（1） 💬（0）<div>这些静态资源不涉及session，直接过滤就好</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/5a/b67a82e3.jpg" width="30px"><span>shen</span> 👍（0） 💬（0）<div>可以利用ngnix ip hash负载均衡，让请求定位到对应的tomcat上做本地的session，集中存储的session放到redis上</div>2021-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（0） 💬（0）<div>避免复制的时候提及文件这类大数据吧？</div>2019-07-26</li><br/><li><img src="" width="30px"><span>Geek_xbye50</span> 👍（0） 💬（0）<div>思考题应该是静态资源不会更新session值吧！请问老师我也有跟neohope一样的一问，集群分裂的情况tomcat的处理方式</div>2019-07-25</li><br/>
</ul>