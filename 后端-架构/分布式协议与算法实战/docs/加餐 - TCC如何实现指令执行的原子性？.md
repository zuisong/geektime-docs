你好，我是韩健。

在上一讲我提到，虽然MySQL XA能实现数据层的分布式事务，解决多个MySQL操作的事务问题，但我现在负责的这套业务系统还面临别的问题：在接收到外部的指令后，我需要访问多个内部系统，执行指令约定的操作，而且，还必须保证指令执行的原子性（也就是事务要么全部成功，要么全部失败）。

那么我是如何实现指令执行的原子性呢？答案是TCC。

在我看来，上一讲中，基于二阶段提交协议的XA规范，实现的是数据层面操作的事务，而TCC能实现业务层面操作的事务。

对你来说，理解了二阶段提交协议和TCC后，你可以从数据层面到业务层面，更加全面理解如何实现分布式事务了，这样一来，当你在日常工作中，需要实现操作的原子性或者系统状态的一致性时，就知道该如何处理了。

那么为了帮助你更好地理解TCC，咱们还是先来看一道思考题。

我以如何实现订票系统为例，假设现在要实现一个企鹅订票系统，给内部员工提供机票订购服务，但在实现订票系统时，我们需要考虑这样的情况：

我想从深圳飞北京，但这时没有直达的机票，要先定深圳航空的航班，从深圳去上海，然后再定上海航空的航班，从上海去北京。

因为我的目的地是北京，所以如果只有一张机票订购成功，肯定是不行的，这个系统必须保障2个订票操作的事务要么全部成功，要么全部不成功。那么该如何实现2个订票操作的事务呢？
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（15） 💬（6）<div>老师好，想问下，如果有3个服务调用，都会涉及到update数据库等操作，那预留资源具体是怎么预留的呢？开启事务，修改，不commit？然后等着commit请求过来后在commit数据库事务吗？</div>2020-06-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（14） 💬（4）<div>老师，再请教您一个问题，TCC有什么好的开源实现可供借鉴没？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/ac/9cc5e692.jpg" width="30px"><span>Corner</span> 👍（7） 💬（1）<div>首先感谢老师长久以来坚持持续加餐和优化。然后有一个问题需要请教一下，在预留阶段有哪些常用的数据处理手段呢？是否数据上都要为预留操作增加相应的字段标记。</div>2020-06-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（6） 💬（3）<div>老师，请教您一个问题，您文中举例操作1，操作2，操作3这三个操作都各自实现TCC（预留操作、确认操作、撤销操作），那TCC都是针对单个操作（如针对操作1、操作2、操作3）实现，那要实现操作1+操作2+操作3这三个操作要么全成功，要么全失败如如何达到的？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（0） 💬（1）<div>韩老师辛苦了。想问题下，在项目中使用TCC，是否需要额外的点存放着数据变更前的快照呢？因为好让在cancel的时候恢复？</div>2020-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/77/fa/e242ea21.jpg" width="30px"><span>dra</span> 👍（9） 💬（1）<div>良心课程，老师用心了。专栏虽完结，还在不停加餐，为学员提供知识服务</div>2020-06-28</li><br/><li><img src="" width="30px"><span>Geek_7a6fde</span> 👍（1） 💬（0）<div>原文问题：我提到了自己通过 TCC 解决了指令执行的原子性问题。那么你不妨想想，为什么 TCC 能解决指令执行的原子性问题呢？

个人理解回答：TCC的try阶段可以预留或者锁定资源，就当于对该资源加锁，加锁了肯定就可以保证原子性了，confirm或cancel就是相当于释放锁</div>2021-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（1） 💬（0）<div>在执行的过程中,TCC利用了二阶段提交的思想,既能够锁定成功,就相当于收到了锁定的确认操作,只有在所有的锁定确认收到了,才可以继续执行Confrim操作,在执行Confrim操作的时候,就不允许失败的存在,即使挂了,也会有后来人再上线的时候重新顶替上去</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/76/7c/e1d9a256.jpg" width="30px"><span>Psyduck</span> 👍（1） 💬（0）<div>非常感谢老师，之前在看 TCC 时还是很模糊的感觉，通过这篇文章的讲解感觉清晰多了。</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/b7/058276dc.jpg" width="30px"><span>i_chase</span> 👍（0） 💬（0）<div>也就是说，tcc做了如下假设：预留资源成功了，那么confirm&#47;cancel就一定是成功的？
</div>2022-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d0/ad/584a4aa1.jpg" width="30px"><span>NieXY</span> 👍（0） 💬（1）<div>为什么说tcc是最终一致性？感觉它也是应用了二阶段提交的思想，应该是强一致性啊</div>2022-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/65/3da02c30.jpg" width="30px"><span>once</span> 👍（0） 💬（0）<div>这篇说的很好, 让我了解了TCC的实现理论思想, 其实有点像库存中的
预占 后扣减or释放
</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ba/c0/58e3e557.jpg" width="30px"><span>上帝打草稿</span> 👍（0） 💬（1）<div>如果操作2在确认操作时，突然宕机了怎么办</div>2021-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（0） 💬（0）<div>再一次完结撒花~</div>2021-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e0/d9/ad644055.jpg" width="30px"><span>Simple</span> 👍（0） 💬（2）<div>老师你好，对下面这句话没理解：
另外，因为 TCC 的每一个操作对于数据库来讲，都是一个本地数据库事务，那么当操作结束时，本地数据库事务的执行也就完成了，所以相关的数据库资源也就被释放了，这就能避免数据库层面的二阶段提交协议长时间锁定资源，导致系统性能低下的问题。

问题：
tcc不也需要try吗？只有所有服务都try成功了，才能提交，在等待所有业务都try成功的过程中还是会锁定资源，感觉和二阶段一样存在资源锁定问题
</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/e4/e7f7ca92.jpg" width="30px"><span>林绍灏</span> 👍（0） 💬（0）<div>老师讲得真的很好，终于弄通了TCC</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/56/62c38c36.jpg" width="30px"><span>欧阳</span> 👍（0） 💬（0）<div>受益匪浅！感谢老师！</div>2020-07-01</li><br/>
</ul>