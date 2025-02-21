你好，我是大明。今天我们来聊一聊微服务架构下的服务注册与发现。

服务注册与发现在微服务架构中处于一个非常核心的地位，也是面试中的常见问题。不过因为微服务架构大行其道，现在我们多少都能回答出来一些服务注册与发现的内容，也因此不容易在面试中刷出亮点，拉开和其他面试者的差距。

所以这一节课我就要带着你深入剖析服务注册与发现，学习服务注册与发现的基本模型，然后在服务端崩溃检测、客户端容错和注册中心选型三个角度找到高可用微服务架构的亮点。

那么我们先来看看服务注册与发现的基本模型。

## 前置知识

为什么我们会需要服务注册与发现呢？你设想这样一个场景，你的服务部署在不同的机房、不同的机器上，监听不同的端口。现在你的客户端收到了一个请求，要发送给服务端，那么你的客户端怎么知道哪些服务端能够处理这个请求呢？

![](https://static001.geekbang.org/resource/image/be/90/be4c280fcdb6d64cfd5fd2649cfd0990.png?wh=2262x1352)

举一个例子，你去一个陌生的城市出差，下班了想去吃个火锅，还得是重庆火锅。那么你怎么知道这个城市哪里有重庆火锅？

你可能会说，我在 App 里面搜一下。那么 App 又怎么知道这里有一家重庆火锅店呢？你继续说，这肯定是商家去这个 App 注册过了呀！对，服务注册与发现模型就是这样。你扮演了客户端的角色，火锅店扮演了服务端的角色，而 App 则是扮演了我们常说的注册中心的角色。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（0） 💬（0）<div>添加小助手微信geektime012，回复「后端面试」，即可进入专栏学习群，领取面试资料包~</div>2023-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/06/b9/f9bf6696.jpg" width="30px"><span>牧童倒拔垂杨柳</span> 👍（32） 💬（1）<div>如果出现注册中崩溃，站在客户端的角度，会有两种情况
1. 只有注册中心崩溃了
2. 注册中心和所有服务端节点一起崩溃了

客户端需要确认是哪种情况，客户端需要继续向注册中心发送心跳，同时使用本地缓存的服务端节点列表，向服务端发送请求，确认是否出现无法访问的服务端节点，可以分为以下几种情况
1. 向注册中心发送心跳失败，但是服务端仍可调用，此时因根据客户端容错策略使用本地缓存的服务端节点进行调用
2. 向注册中心发送心跳失败，同时服务端不可调用，此时客户端需要使用本地缓存的服务端节点，确认是否所有服务端节点都不可用，如果都不可用，客户端停止向服务端发送请求，并保持向注册中心发送心跳，等待注册中心重新上线

还有一种情况是客户端还没缓存服务端节点列表，这时注册中心挂了，此时客户端无法获取到服务端节点的位置信息，只能保持向注册中心发送心跳 等待注册中心上线</div>2023-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d8/5d/07dfb3b5.jpg" width="30px"><span>杯莫停</span> 👍（18） 💬（1）<div>老师要是能距举例说明一下选C(数据一致性)和选A(服务可用性)的优缺点就更好了,谢谢。我觉的应该不是体量大小的问题，而是对数据的一致性要求是否严格的问题。不知道我理解的对不对。</div>2023-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/81/1c614f4a.jpg" width="30px"><span>stg609</span> 👍（9） 💬（5）<div>好像并没有解释为什么高可用是标准答案</div>2023-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/0a/59639f1f.jpg" width="30px"><span>penbox</span> 👍（8） 💬（1）<div>1. 如果注册中心崩溃了，你的系统会怎么样？
注册中心崩溃之后，相当于三角形里面客户端与注册中心、服务端与注册中心这两条线断掉了。
对服务端的影响就是，服务端上线和下线没法通知到客户端。
对客户端的影响是，客户端没法更新可用服务端列表，只能使用本地现有的可用服务端列表，勉强维持服务。
2. 再列举一个心跳频率、心跳重试机制对系统可用性影响的例子？
心跳频率过长，会增加系统判断故障的延迟；如果心跳频率过短，又会增加系统负载和网络流量，造成系统资源的过度消耗。需要在系统负载和实时性要求之间做权衡，选择合适的心跳频率。
心跳重试机制，避免了偶发性的网络抖动造成的故障误判，但同时也变相增加了判断故障的延迟。重试次数、间隔设计不合理，同样会造成系统资源的过度消耗。</div>2023-06-29</li><br/><li><img src="" width="30px"><span>Geek_933088</span> 👍（7） 💬（1）<div>感觉老师提到的这个应该是指后端服务部署在传统虚拟机上的场景吧，这么来看确实得这么去实现保证高可用问题，虽然复杂度较高，且貌似也引入了额外的耦合，例如无论客户端或服务端都直接要求有一个注册中心，要是部署在没有注册中心的环境里面应该是跑不起来了，可见这套玩法也有着其的权衡取舍；

随着K8S的普及，现在大部分都用K8S来部署服务了，其自带服务发现与注册（对集群内部）机制，如果客户端和服务端都在集群内部则直接通过service来访问；如果客户端在集群外部，一般是通过提供ingress对应域名（通常会前挂一套负载均衡到K8S）给到客户端，这样一来上面提到这些就不需要了，而且服务端和客户端都无需加入与注册中心交互逻辑，感觉老师可以在文章里提一下这类场景，个人愚见，如果问题欢迎纠正指出，谢谢</div>2024-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d0/7f/1ad28cd3.jpg" width="30px"><span>王博</span> 👍（7） 💬（3）<div>刚好经历过我司注册中心炸掉的outage，当时使用etcd作为注册中心，etcd维护团队离职了，我们做了以下事情：
1、禁止所有部署（我们使用aws，部署可能会换新机器）
2、保护住所有的现有机器，禁止scale in和scale out（多花了很多钱qaq）
3、在经历多轮抢修依然无法启动etcd的情况下，我们切换到了consul
4、注册中心团队对consul添加了fallback的方案，当consul挂掉的时候进行fallback
5、我们有个服务是通过注册中心获取有序的节点列表从而分配定时任务执行，注册中心故障时可能有时成功有时失败，所以我们添加了基于配置的固定列表，当注册中心down掉时，我们可以配置自己的机器列表，在内存中做排序，以分配定时任务</div>2023-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/08/bb/a9d2a39d.jpg" width="30px"><span>周新建</span> 👍（3） 💬（3）<div>”客户端也要朝着那个疑似崩溃的服务端节点继续发送心跳。如果心跳成功了，就将节点放回可用列表。“
客户端能向服务端发送心跳么？对这个点比较疑惑</div>2023-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fc/f5/6b65f63a.jpg" width="30px"><span>大将军Leo。。</span> 👍（2） 💬（1）<div>老师 如果是注册中心的节点信息被误删除了，而且这个信息注册中心已经同步给客户端了，这种情况客户端客户端是不是要做一个缓存历史节点的功能？不然被全删了没办法保持心跳了</div>2023-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/a9/83684d4a.jpg" width="30px"><span>喆里</span> 👍（1） 💬（1）<div>有个疑问，客户端和注册中心失联时，为了维护缓存中节点信息的有效性，需要客户端和服务端发送心跳？？？
客户端怎么给服务端发心跳？？  服务端还需要开放一个心跳接口给客户端？？
还有注册中心和客户端之间的数据同步，并不总是推模式的，还有拉模式的，所以注册中心和客户端之间的心跳其实并不是必须的</div>2023-12-19</li><br/><li><img src="" width="30px"><span>Geek_281b2d</span> 👍（1） 💬（1）<div>讀完這堂課有以下疑問,想請問一下課堂老師
1. 這邊的客戶端是包含瀏覽器&amp; Mobile等等嗎
2. 每個服務前面都會一台loadbalance 主機去做附載平衡,請問是附載平衡主機的網址去服務註冊中心註冊還是服務去註冊
3. 如果目前系統是採用k8s+istio,但是目前是將k8s中每個服務對應的endpoint domain寫到istio中,讓istio的網關可以在api請求過來時,經由網址找到服務端,請問這樣的架構算是有服務註冊嗎?</div>2023-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ee/46/7d65ae37.jpg" width="30px"><span>木几丶</span> 👍（1） 💬（1）<div>回答问题：你可以再举出一个心跳频率、心跳重试机制对系统可用性影响的例子吗？
据我所知，所有根据心跳来判断是否存活的系统都会有因延迟带来的可用性问题，例如Redis主从切换、Nginx反向代理upstream探测，不同系统应对这种可用性问题也有各自的办法，如Redis直接就是服务短暂不可用、Nginx则是选择下一个服务</div>2023-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（1） 💬（1）<div>学些了</div>2023-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（1） 💬（2）<div>老师太牛了，offer收割机名不虚传👍🏻</div>2023-06-19</li><br/><li><img src="" width="30px"><span>Geek_9027db</span> 👍（0） 💬（3）<div>老师能说下为什么必须要选择p吗？</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cb/a2/5e7c557e.jpg" width="30px"><span>傲娇的小宝</span> 👍（0） 💬（1）<div>关于问题一：首先要判断我这个客户端节点是否成功接入过注册中心，如果没有，应该异常退出。如果成功接入过，只是当前注册中心不可用，我本地应该有缓存的服务器信息，如果需要服务调用，我先在本地缓存找可用节点，加上容错机制，保障一下服务器调用。同时我需要尝试连接注册中心，尝试着发心跳包。这期间，注册中心如果恢复了，可用拉取得到最新，一切如常。
关于问题二：如果心跳间隙过长，无法及时发现服务端已下线，但如果太频繁了，客户端和服务器的导致吞吐量下降。</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/e7/e2cf9d6d.jpg" width="30px"><span>二师兄</span> 👍（0） 💬（1）<div>老师和政法大学的罗翔老师是老乡吗？口音好像</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/86/07a10be2.jpg" width="30px"><span>Lee</span> 👍（0） 💬（1）<div>老师  前面不是说注册中心发现心跳中断就会通知客户端，然后注册中心与服务端直接进行重试 ，为什么后面又说服务端崩溃到客户端最终知道是有一段延时的，在这段延时内，客户端还是会把请求发送到已经崩溃的服务端节点上。</div>2023-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/1f/21/791d0f5e.jpg" width="30px"><span>Byte Learner</span> 👍（0） 💬（1）<div>&quot;万一你公司并没有使用 AP 模型的注册中心，比如说用了 CP 模型的 ZooKeeper，那么你就可以进一步解释，关键词是体量小&quot;

老师你好，看到上面这段话，结合自己公司情况感觉没法回答面试官，字节的服务发现用的 consul，基于 CP 架构，了解到 consul 有多数据中心支持、基于 Gossip 协议等优点，但是字节集群的规模很大，是有其他方式保证了可用性吗</div>2023-10-16</li><br/><li><img src="" width="30px"><span>Geek_680632</span> 👍（0） 💬（1）<div>1.如果注册中心崩溃，客户端使用之前缓存的服务端地址列表，还可以维持可用状态；客户端和服务端需要一直重试心跳检测；2.例如Redis或者ElasticsSearch集群中，多个节点之间的心跳检测机制。</div>2023-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/c5/7a/c03cb56e.jpg" width="30px"><span>一弦一柱思华年</span> 👍（0） 💬（1）<div>服务注册发现 都是公司基础架构部门搞的，有成熟的内部平台，无需业务部门关心，这种咋搞。。看了下这块，感觉有点懵圈，平时开发完全没关注过服务注册发现</div>2023-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（0） 💬（1）<div>1我们注册中心是用的nacos，nacos挂了，整个服务无法进行通信了
2在一些监控当，进行探活，经常隔一段时间ping几秒
3作者是如何理解nacos是ap还是cp？</div>2023-07-23</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLm8skz4F7FGGBTXWUMia6qVEc00BddeXapicv5FkAx62GmOnUNEcE4scSR60AmappQoNdIQhccKsBA/132" width="30px"><span>末日，成欢</span> 👍（0） 💬（1）<div>老师， 不是核心员工，我们如何才能知道注册中心集群的QPS呢？ 注册中心什么情况下会出现故障？
1. 当注册中心故障时， 客户端只能用曾经在注册中心上拉取的提供方服务地址列表，无法感知到更新。</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（0） 💬（2）<div>注册中心选择cp有什么问题呢？客户端是有本地可用节点缓存的，就算注册中心不可用了，是不是影响也不大</div>2023-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a9/66/2df6b3fe.jpg" width="30px"><span>滴滴答答</span> 👍（0） 💬（1）<div>请教下老师，公司用的k8s+istio这套。微服务里的注册中心，负载均衡等可能被开发者弱化了。这种要怎么去引导面试官呢？</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/c1/f6/8a38a179.jpg" width="30px"><span>jinhaoqicode</span> 👍（0） 💬（1）<div>受益匪浅，喜欢你的总结，我想做一个实际的项目，有推荐吗？</div>2023-06-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJBVPzcO55PyLPeicoZ6zuaZNryYK7OnAkgz0jV6Tl9vOLIrkEGDgen8E9NwamAsTckS1D2Wl2prCQ/132" width="30px"><span>夏文兵</span> 👍（0） 💬（3）<div>老师问一下，为什么是注册中心向服务器发送心跳，而不是服务器向注册中心发送心跳，注册中心用服务端最后心跳时间判断失效状态呢</div>2023-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（0） 💬（1）<div>如果注册中心崩溃：
1. 新服务无法将自身信息注册到注册中心
2. 老服务无法将自己的状态信息同步给注册中心，同时客户端也无法从注册中心获取到最新的服务节点列表以做更新。客户端只能继续使用本地的服务节点列表。
3. 客户端无法收到注册中心的通知，那么服务端崩溃信息就无法同步到客户端，这样客户端发起的请求就都会失败，影响系统的使用</div>2023-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c1/ad/62d3df46.jpg" width="30px"><span>剑存</span> 👍（4） 💬（2）<div>如果注册中心崩溃：

已知服务-服务端无法将自己的状态信息更新到注册中心，同时客户端本地缓存的已知服务的节点列表就无法得到更新，客户端只能继续使用这个本地服务列表发送请求，如客户端发现有服务节点不可达，通过客户端的容错策略来路由到可用节点上。

未知服务-如果在注册中心崩溃的时候，第一次访问某个服务，这个时候是拿不到服务节点列表的，由于本地还没有缓存这个服务的列表 ，只能重复尝试，等standby的注册中心failover上线后，拿到服务列表继续后续处理。如果注册中心不是高可用的部署，这个时候客户端对此服务的访问就只能返回不可用。</div>2023-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/36/25938cd1.jpg" width="30px"><span>Emmcd</span> 👍（0） 💬（0）<div>k8s部署的集群 是不是就不用自己实现服务注册与发现了呢</div>2024-09-19</li><br/>
</ul>