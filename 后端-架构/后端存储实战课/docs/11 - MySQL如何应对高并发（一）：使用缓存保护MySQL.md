你好，我是李玥。

通过前面几节课的学习，相信你对MySQL这类关系型数据库的能力，已经有了定量的认知。

我们知道，大部分面向公众用户的互联网系统，它的并发请求数量是和在线用户数量正相关的，而MySQL能承担的并发读写的量是有上限的，当系统的在线用户超过几万到几十万这个量级的时候，单台MySQL就很难应付了。

绝大多数互联网系统，都使用MySQL加上Redis这对儿经典的组合来解决这个问题。Redis作为MySQL的前置缓存，可以替MySQL挡住绝大部分查询请求，很大程度上缓解了MySQL并发请求的压力。

Redis之所以能这么流行，非常重要的一个原因是，它的API非常简单，几乎没有太多的学习成本。但是，要想在生产系统中用好Redis和MySQL这对儿经典组合，并不是一件很简单的事儿。我在《[08 | 一个几乎每个系统必踩的坑儿：访问数据库超时](https://time.geekbang.org/column/article/211008)》举的社交电商数据库超时故障的案例，其中一个重要的原因就是，对缓存使用不当引发了缓存穿透，最终导致数据库被大量查询请求打死。

今天这节课，我们就来说一下，在电商的交易类系统中，如何正确地使用Redis这样的缓存系统，以及如何正确应对使用缓存过程中遇到的一些常见的问题。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/76/79c1f23a.jpg" width="30px"><span>李玥</span> 👍（35） 💬（0）<div>Hi，我是李玥。

这里回顾一下上节课的思考题：

课后请你选一种你熟悉的非关系型数据库，最好是支持 SQL 的，当然，不支持 SQL 有自己的查询语言也可以。比如说 HBase、Redis 或者 MongoDB 等等都可以，尝试分析一下查询的执行过程，对比一下它的执行器和存储引擎与 MySQL 有什么不同。

谈一下我的理解：

我们拿一个分布式数据库Hive来看一下它的执行器和存储引擎。严格来说，Hive并不是一个数据库，它只是一个执行器，它的存储引擎就是HDFS加上Map-Reduce。在Hive中，一条SQL的执行过程是和MySQL差不多的，Hive会解析SQL，生成并优化逻辑执行计划，然后它就会把逻辑执行计划交给Map-Reduce去执行了，后续生成并优化物理执行计划，在HDFS上执行查询这些事儿，都是Map-Reduce去干的。顺便说一下，Hive的执行引擎（严格来说是物理执行引擎）是可以替换的，所以就有了Hive on Spark，Hive on Tez这些。</div>2020-03-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKrzZT06vXeP6IfR9iasoiaaDeYiaUmmN6pgwvNUpLhrauiasU9acvNcdSuicrhicMmBhvEufcjPTS7ZXRA/132" width="30px"><span>Geek_3894f9</span> 👍（73） 💬（21）<div>数据加版本号，写库时自动增一。更新缓存时，只允许高版本数据覆盖低版本数据。</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/2d/1eebfc3c.jpg" width="30px"><span>GaGi</span> 👍（41） 💬（16）<div>对于Cache aside和read&#47;write through而带来的数据不一致问题，工作中是这样解决：
a写线程，b读线程：
b线程：读缓存-&gt;未命中-&gt;上写锁&gt;从db读数据到缓存-&gt;释放锁；
a线程：上写锁-&gt;写db-&gt;删除缓存&#47;改缓存-&gt;释放锁；
这样来保证a，b线程并发读写缓存带来的脏数据问题；

</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6d/46/e16291f8.jpg" width="30px"><span>丁小明</span> 👍（4） 💬（1）<div>老师，经常看到说用布隆过滤来解决缓存穿透问题，这个方案有实际的案例吗？
如果是真的可以那么怎么去操作呢？
先初始化所有可能存到缓存里面数据的key到一个足够大的布隆过滤器，然后如果有新增数据就就继续往过滤器中放，删除就从过滤器里面删（又看到说不用bit的话支持累加删除）
如果发现不在过滤器中就表示一定不存在，就无需查询了。如果在过滤器中也有可能不存在，这个时候在配合null值。
这个方案靠谱么，希望老师能解答一下</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/d6/47da34bf.jpg" width="30px"><span>任鹏斌</span> 👍（3） 💬（4）<div>老师Cache Aside应该是先删缓存后更新数据库吧？先更新数据库的话一旦缓存删除失败了，就会产生脏数据</div>2020-05-21</li><br/><li><img src="" width="30px"><span>王杰</span> 👍（3） 💬（5）<div>作者回复: 你可以参考一下“GaGi”同学的留言，用锁来解决并发问题。------------------------------------------------------老师，在读线程上写锁（说独占锁比较合适），是否跟MVCC相违背，MVCC不就是为了用来解决高并发带来的读写阻塞问题吗？我这边有两种解决思路不知可否：第一用版本控制，类似MVCC，第二种用Read&#47;Write Through，写写并发在MVCC模式下依然是阻塞的，不算违背，所以只要把更新数据库与更新缓存放入统一事务中就行。读写并发不阻塞，是因为mysql用了快照读原因，那我们可以继续写线程更新缓存，读线程采用redis的setnx方式解决覆盖</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/dd/1e5e7b0c.jpg" width="30px"><span>image</span> 👍（3） 💬（1）<div>如果缓存时有大量命中为null如何处理？如果命中null 也进行缓存，会导致缓存增长太快，容易被攻击
如果不缓存，又容易引起大量穿透</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ed/e0/c63d6a80.jpg" width="30px"><span>1</span> 👍（0） 💬（1）<div>是不是model的话使用缓存，列表的话是不是不适合用缓存？列表应该怎么去缓存？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（2）<div>Cache Aside解决的只是并发写请求导致的缓存数据不一致问题。对于读写这种场景并没有彻底解决。
A：读，缓存穿透，查库。
B：写，更新数据库。
B：写，删除缓存。
A：读，回写缓存。导致不一致。
目前针对这种问题我们这边才去的方案是写请求后用MQ延迟删除缓存。老师有什么好的方法和实践吗？</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（0） 💬（3）<div>老师有个问题请教你，我这边有个业务，合同编号，存在redis 🀄️和数据库中，每次先查redis 获取合同编号后面虚寒，然好加1⃣️，保存回去，外去更新数据库，做了数据库合同编号重复，检验，但是每次还是有合通编号重复的，请问这个怎么解决？市并发导致？</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（52） 💬（13）<div>Cache Aside 在高并发场景下也会出现数据不一致。
读操作A，没有命中缓存，就会到数据库中取数据v1。
此时来了一个写操作B，将v2写入数据库，让缓存失效；
读操作A在把v1放入缓存，这样就会造成脏数据。因为缓存中是v1，数据库中是v2.
</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/0b/ad56aeb4.jpg" width="30px"><span>AI</span> 👍（19） 💬（2）<div>老师，看了你对缓存模式的解读之后，跟我之前的理解感觉有比较大的冲突。

在文中，你提到的 Read&#47;Write Through 策略，我看到的更多的是把这种方式称为Cache Aside。
而Cache Aside 和 Read&#47;Write Throug的差别，也不是是否去删除缓存。

我看的一些文章，包括买的书籍，大部分都跟ehcache caching-patterns描述的意思差不多，总结如下：

# Cache Aside

应用程序直接与DB、缓存交互，并负责对缓存的维护。

读数据时，先访问缓存，命中则直接返回。
如果不命中，则先查询DB，并将数据写到缓存，最后返回数据。

写数据时，同时更新DB和缓存。


# Read-Through

应用程序只与缓存交互，而对DB的读取由缓存来代理。

读数据时，先访问缓存，命中则直接返回。
如果不命中，则由缓存查询DB，并将数据写到缓存，最后返回数据。


# Write-Through

应用程序只与缓存交互，而对DB的写由缓存来代理。

写数据时，访问缓存，由缓存将数据写到DB，并将数据缓存起来。


例如使用Redis来缓存MySQL的数据，一般都是通过应用程序来直接与Redis、MySQL交互，我的理解是Cache Aside，包&quot;是&#47;否&quot;删除Cache在内。

而Read-Through，像Guava LoadingCache，在load里面定义好访问DB的代码，后续的读操作都是直接与Cache交互了。


https:&#47;&#47;www.ehcache.org&#47;documentation&#47;3.8&#47;caching-patterns.html
https:&#47;&#47;docs.oracle.com&#47;cd&#47;E15357_01&#47;coh.360&#47;e15723&#47;cache_rtwtwbra.htm#COHDG5178
https:&#47;&#47;dzone.com&#47;articles&#47;using-read-through-amp-write-through-in-distribute
https:&#47;&#47;docs.microsoft.com&#47;en-us&#47;azure&#47;architecture&#47;patterns&#47;cache-aside
《亿级流量网站架构核心技术》
</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（8） 💬（0）<div>思考题
Cache Aside 模式如何产生脏数据？
首先 Cache Aside 这种模式和 Read&#47;Write Through    模式的读取操作一样，都是先尝试读缓存，如果命中直接返回;未命中的话读数据库，然后更新缓存。
写操作不是更新缓存，而是把缓存中的数据删掉
那怎么出现脏数据？
假设有下面两个线程对 key 分别进行读写操作
读线程 t1
写线程 t2
按照下面的流程进行操作
1. t1 读缓存未命中，然后从数据库中读到 value1
2. t2 更新 key 为 value2，并尝试删缓存(此时缓存中并没有)
3. t1 把从 db 中读到的 value1写回缓存

这时 db 中 key 的 value 为新数据 value2，缓存中为旧数据 value1，产生了不一致。
这种情况只发生在读线程从 bd 读到旧数据往 cache    中写前，有写线程更新了 db，然后读线程把老数据写回 cache


Read&#47;Write Through 发生脏数据的情况
第一种情况是并发读写
对 key 进行读写的两个线程
读线程 t1
写线程 t2

按照如下时间顺序操作
1.t1 尝试读缓存但未命中，然后去 db 中读取到了数据 value1，但还未更新缓存兄弟的数据
2. t2 更新数据库 value2，更新成功后常识读取缓存，未命中，所以更新缓存为 value2
3.t1 线程继续把之前从 db 中读到的旧数据 value1 写回缓存
这样 db 中是新数据，但缓存中是旧数据

第二种情况是并发写
这种情况是db 中产生了 ABA 问题
比如有两个写线程 t1,t2，分别按下面的先后顺序操作
1.t1 尝试把 key 更新为 value1，但响应丢失
2.t2 尝试把 key 更新为 value2，还未响应结果
3.t1 发生重试操作
4.t2 响应成功
5.t1 响应成功
本来写应该按先后顺序的，t2后到，数据库和缓存中应该是 value2，但因为 t1 发生了重试，导致数据库和缓存中是 value1了，产生了ABA问题，解决办法是在更新时加上 version 版本号判断

所以没啥万能的方法，需要根据业务场景来制定方法</div>2020-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLBllicLBj61g1ibmCeWzLYpQYEteTOtAAAypoIg6CD19ibXQBbM09VsME9Ta1G8ubwk0ibjiacItavibaeg/132" width="30px"><span>seg-上海</span> 👍（5） 💬（1）<div>1）缓存刚好失效
（2）请求A查询数据库，得一个旧值
（3）请求B将新值写入数据库
（4）请求B删除缓存
（5）请求A将查到的旧值写入缓存
</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（5） 💬（2）<div>A,B两个进程
B read cache  x=null
B read DB x=1
A write DB x=2
A delete cache
B write cache x=1
这时数据库里x=2，缓存中x=1，直到缓存过期之前一直是脏数据。这种概率算是比较小的了。

文章中提到用灰度来解决问题，似乎解决不了基于类似redis这种做分布式缓存时的问题。

</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/e4/e6faf686.jpg" width="30px"><span>握了个大蚂蚱</span> 👍（4） 💬（0）<div>总结：
1.为什么先更新mysql再更新（删除）redis比反过来好？

降低了脏数据出现的概率，前者产生脏数据是由于并发，后者几乎是必然，只要先写再读的请求发生，都会造成脏数据：先把redis中的缓存清了，然后读请求读不到去数据库中找到并更新在redis中。
2.为什么aside cache比read&#47;write through好？
也是降低了脏数据出现的概率。前者只有读写先后访问数据库，又调转顺序访问redis时redis中出现脏数据，这个概率很小，而并发写时相当于不操作redis；而后者在并发写的情况下也容易脏。</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（4） 💬（0）<div>老师好。文中写“订单服务收到更新数据请求之后，先更新数据库，如果更新成功了，再尝试去删除缓存中订单，如果缓存中存在这条订单就删除它，如果不存在就什么都不做，然后返回更新成功。这条更新后的订单数据将在下次被访问的时候加载到缓存中。”

请问，前面的读线程没命中，去数据库读到了订单数据，这是写进程进来完成后，读线程将原来读的脏数据生成了缓存，这样还是不能解决问题啊？</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a5/f0/c4eba20f.jpg" width="30px"><span>程堃</span> 👍（2） 💬（0）<div>问题：读线程查到缓存为空后，读db数据并写入缓存，在写入之前另一个更新操作修改了db数据，会导致db与缓存数据不一致。
方案：将Cache Aside的删除操作改成设置缓存几秒后失效，或者加分布式锁</div>2020-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（2） 💬（0）<div>线程1读取缓存未命中，查询当前数据库数据
线程2更新当前数据库数据，删除缓存(不存在)
线程1讲老数据更新至缓存，导致当前数据库数据与缓存不一致</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/24/32/c712d415.jpg" width="30px"><span>陶金</span> 👍（2） 💬（0）<div>package main

import (
	&quot;fmt&quot;
	&quot;sync&quot;
	&quot;time&quot;
)

type BaseModel struct {
	data int
	mu sync.RWMutex
}


var cache *BaseModel
var db *BaseModel
const FIRST_DATA = 1
const SECNOD_DATA = 2
const EMPTY_DATA = 0

func init() {
	cache = new (BaseModel)
	db = new (BaseModel)
	db.setData(FIRST_DATA)
}


func main() {

	go read()
	go write(SECNOD_DATA)

	time.Sleep(3 * time.Second)
	fmt.Println(&quot;db&#39;s data is %d, cache&#39;s data is %d&quot;, db.getData(), cache.getData())
}


func read() {
	data := cache.getData()
	if data == 0 {
		data = db.getData()
		time.Sleep(2* time.Second)
		cache.setData(data)
	}
}


func write(data int) {
	time.Sleep(1*time.Second)
	db.setData(data)
	cache.setData(EMPTY_DATA)
}


func (self *BaseModel) getData() int {
	self.mu.RLock()
	defer self.mu.RUnlock()
	return self.data
}

func (self *BaseModel) setData(data int) {
	self.mu.Lock()
	defer self.mu.Unlock()
	self.data = data
}

大概场景如下：
1. 初始数据库中数据为“1”，缓存无数据
2. 线程A为读线程，读取缓存未果，然后读取数据库中的记录为“1”，这时候缓存阻塞住。
3. 线程B为写线程，先把数据库中的数据更新为“2”，再删除缓存，结束。
4. 此时线程A解除阻塞，然后把记录“1”更新到缓存中。

此时缓存中数据为“1”， 数据库中数据为“2”， 缓存落后于数据库中的数据。
</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/f4/95191165.jpg" width="30px"><span>R20114</span> 👍（2） 💬（2）<div>Cache Aside 模式在下面的场景下：
读写线程之间在执行 Cache Aside Pattern 操作的时候，写线程删除了缓存，读线程从 DB 读到老的数据，把老的数据放到了缓存中，这样就会在缓存中产生脏数据。</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/bd/e14ba493.jpg" width="30px"><span>翠羽香凝</span> 👍（1） 💬（0）<div>有一个问题，一直没搞明白。如果使用redis作为mysql的前置，在写数据的时候，需要同时写Mysql和redis，如果更新mysql成功后，更新redis没成功，造成了两者之间的不一致，这种情况怎么办？</div>2020-10-22</li><br/><li><img src="" width="30px"><span>王杰</span> 👍（1） 💬（0）<div>你好，使用 Cache Aside 模式更新缓存好像也会产生脏数据。就如文章里所说，当一个读线程没有从缓存中读到数据，进而去查数据库获取到数据，这时一个写线程更新了数据库并删除缓存，可能由于读线程放入旧数据到缓存时机比较晚写线程没法删到，导致缓存中可能不是最新的数据，后面再有线程过来查询自然也读不到新数据了</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/f7/91ac44c5.jpg" width="30px"><span>Mq</span> 👍（1） 💬（1）<div>老师好，写数据跟删缓存不是一致的，写完数据到删缓存这段时间内其他并发访问都是脏数据，这种思维方式感觉不解决一致性问题，都会有可能出现脏读，只是时间长短问题</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/6b/434b7396.jpg" width="30px"><span>阳明zozA</span> 👍（0） 💬（0）<div>有点说的不够准确，脏数据的概率不是和系统的并发量正相关，而是和单key(此处指单用户、单订单)的并发度，其实即使业务规模很大，脏数据的概率也未必大。</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（0） 💬（0）<div>思考题：
Cache Aside产生脏数据，个人肤浅理解也是有两种情况：
1、当两个线程同时更新数据时，一个因为网络原因更新失败，一个成功，而后，失败的那个再次重试更新，覆盖了更新成功的那个数据，也就是ABA的情况；
2、两个线程一个更新数据，一个读数据，前者在数据更新完成后，在还未删除缓存的情况下，第二个线程恰好读到了缓存，这时第二个线程就是脏数据。</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/37/29/b3af57a7.jpg" width="30px"><span>凯文小猪</span> 👍（0） 💬（0）<div>首先回答下老师的问题：
理论上总是存在这种情况。比方说 缓存失效发生在写库与失效缓存之间 那么此时读请求读出来的数据就是旧的。但是这种场景通常概率极低，因为读总是快于写 所以工程上不多见。再来说下如何解决，两种方法：
1. 不解决 。通常也是这么做 即接受这种问题
2. 使用容错窗口。原理类似老师上节课提出的 spu改动价格，允许一段时间内旧价格下单成功

下面再来说说为什么write through &#47; read through 不适合这种场景
本质上是由于两个并发写（读请求与写请求）会存在彼此脏写覆盖 因为最终写入其实没有锁或同步机制来做协调。
这个问题在《Why does Facebook use delete to remove the key-value pair in Memcached instead of updating the Memcached during write request to the backend?》有讨论过</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cd/df/c520d418.jpg" width="30px"><span>董俊俊</span> 👍（0） 💬（0）<div>用分布式锁更新缓存啊，大量的请求过年，只允许一个请求请求数据库并更新缓存</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/7e/64730c47.jpg" width="30px"><span>张凯</span> 👍（0） 💬（0）<div>文中一直在说缓存穿透，其实文中举例缓存失效，数据库中数据存在的这种情景，应该为缓存击穿。</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/2c/e2f3cfc0.jpg" width="30px"><span>注意力$</span> 👍（0） 💬（0）<div>老师，传统行业前台业务比较更新频繁的数据，这个能做缓存吗？还是也能实现，业务SQL写的慢，导致很多压力都在数据库上。</div>2021-08-17</li><br/>
</ul>