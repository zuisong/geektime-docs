你好，我是轩脉刃。

上面两节课把数据库操作接入到hade框架中了，现在我们能使用容器中的ORM服务来操作数据库了。在实际工作中，一旦数据库出现性能瓶颈，除了优化数据库本身之外，另外一个常用的方法是使用缓存来优化业务请求。所以这节课，我们来讨论一下，hade框架如何提供缓存支持。

现在的Web业务，大部分都是使用Redis来做缓存实现。但是，缓存的实现方式远不止Redis一种，比如在Redis出现之前，Memcached一般是缓存首选；在单机上，还可以使用文件来存储数据，又或者直接使用进程的内存也可以进行缓存实现。

缓存服务的底层使用哪个存储方式，和具体的业务架构原型相关。我个人在不同业务场景中用过不少的缓存存储方案，不过业界用的最多的Redis，还是优点比较突出。相比文件存储，它能集中分布式管理；而相比Memcached，优势在于多维度的存储数据结构。所以，顺应潮流，我们hade框架主要也针对使用Redis来实现缓存服务。

我们这节课会创建两个服务，一个是Redis服务，提供对Redis的封装，另外一个是缓存服务，提供一系列对“缓存”的统一操作。而这些统一操作，具体底层是由Redis还是内存进行驱动的，这个可以根据配置决定。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/ed/4e249c6b.jpg" width="30px"><span>Vincent</span> 👍（1） 💬（1）<div>以redis为基础，最大限度扩展cache的抽象，学习了</div>2021-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6b/23/ddad5282.jpg" width="30px"><span>Aaron</span> 👍（0） 💬（1）<div>SetObj方法的说明【GetObj 获取某个key对应的对象, 对象必须实现 https:&#47;&#47;pkg.go.dev&#47;encoding#BinaryUnMarshaler】， 我并没有这样实现， 我直接以json.Marshal，转成字符串的形式进行存储。get的时候，再json.Unmarshal进行转换，转换成结构体。另外，我实现的时候，设置过期时间的时候， 0代表永久存储， 在V8(v8.11.4, GO是1.17) 的源码里也能看到说明。【Zero expiration means the key has no expiration time.】</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/52/56dbb738.jpg" width="30px"><span>牙小木</span> 👍（0） 💬（1）<div>层次描述清晰，感觉缺了点层次图。字不如图哦</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（6）<div>看上去封装的redis服务只会返回go-redis实现的redis client，那么定义redis服务的接口似乎就不是很必要，因为不会再有其他的redis服务的实现了。文中使用redis服务是为了实现缓存服务，那么直接用go-redis实现就好了。</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/da/dcf8f2b1.jpg" width="30px"><span>qiutian</span> 👍（0） 💬（0）<div>这篇感觉有点乱，一会是Redis的代码，一会又插入了Cache的代码，能看懂，但不是很清晰</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/36/fd46331c.jpg" width="30px"><span>Jussi Lee</span> 👍（0） 💬（0）<div>redis 关闭链接的相关逻辑，好像没有看到</div>2022-06-28</li><br/>
</ul>