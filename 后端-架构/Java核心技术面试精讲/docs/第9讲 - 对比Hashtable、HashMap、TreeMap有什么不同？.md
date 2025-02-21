Map是广义Java集合框架中的另外一部分，HashMap作为框架中使用频率最高的类型之一，它本身以及相关类型自然也是面试考察的热点。

今天我要问你的问题是，对比Hashtable、HashMap、TreeMap有什么不同？谈谈你对HashMap的掌握。

## 典型回答

Hashtable、HashMap、TreeMap都是最常见的一些Map实现，是以**键值对**的形式存储和操作数据的容器类型。

Hashtable是早期Java类库提供的一个[哈希表](https://zh.wikipedia.org/wiki/%E5%93%88%E5%B8%8C%E8%A1%A8)实现，本身是同步的，不支持null键和值，由于同步导致的性能开销，所以已经很少被推荐使用。

HashMap是应用更加广泛的哈希表实现，行为上大致上与HashTable一致，主要区别在于HashMap不是同步的，支持null键和值等。通常情况下，HashMap进行put或者get操作，可以达到常数时间的性能，所以**它是绝大部分利用键值对存取场景的首选**，比如，实现一个用户ID和用户信息对应的运行时存储结构。

TreeMap则是基于红黑树的一种提供顺序访问的Map，和HashMap不同，它的get、put、remove之类操作都是O（log(n)）的时间复杂度，具体顺序可以由指定的Comparator来决定，或者根据键的自然顺序来判断。

## 考点分析

上面的回答，只是对一些基本特征的简单总结，针对Map相关可以扩展的问题很多，从各种数据结构、典型应用场景，到程序设计实现的技术考量，尤其是在Java 8里，HashMap本身发生了非常大的变化，这些都是经常考察的方面。

很多朋友向我反馈，面试官似乎钟爱考察HashMap的设计和实现细节，所以今天我会增加相应的源码解读，主要专注于下面几个方面：

- 理解Map相关类似整体结构，尤其是有序数据结构的一些要点。
- 从源码去分析HashMap的设计和实现要点，理解容量、负载因子等，为什么需要这些参数，如何影响Map的性能，实践中如何取舍等。
- 理解树化改造的相关原理和改进原因。

除了典型的代码分析，还有一些有意思的并发相关问题也经常会被提到，如HashMap在并发环境可能出现[无限循环占用CPU](https://bugs.java.com/bugdatabase/view_bug.do?bug_id=6423457)、size不准确等诡异的问题。

我认为这是一种典型的使用错误，因为HashMap明确声明不是线程安全的数据结构，如果忽略这一点，简单用在多线程场景里，难免会出现问题。

理解导致这种错误的原因，也是深入理解并发程序运行的好办法。对于具体发生了什么，你可以参考这篇很久以前的[分析](http://mailinator.blogspot.com/2009/06/beautiful-race-condition.html)，里面甚至提供了示意图，我就不再重复别人写好的内容了。

## 知识扩展

1.Map整体结构

首先，我们先对Map相关类型有个整体了解，Map虽然通常被包括在Java集合框架里，但是其本身并不是狭义上的集合类型（Collection），具体你可以参考下面这个简单类图。

![](https://static001.geekbang.org/resource/image/26/7c/266cfaab2573c9777b1157816784727c.png?wh=768%2A493)

Hashtable比较特别，作为类似Vector、Stack的早期集合相关类型，它是扩展了Dictionary类的，类结构上与HashMap之类明显不同。

HashMap等其他Map实现则是都扩展了AbstractMap，里面包含了通用方法抽象。不同Map的用途，从类图结构就能体现出来，设计目的已经体现在不同接口上。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/49/d71e939d.jpg" width="30px"><span>三口先生</span> 👍（30） 💬（1）<div>最常用的方法就是线性再散列。即插入元素时，没有发生冲突放在原有的规则下的空槽下，发生冲突时，简单遍历hash表，找到表中下一个空槽，进行元素插入。查找元素时，找到相应的位置的元素，如果不匹配则进行遍历hash表。
然后就是我们非线性再散列，就是冲突时，再hash，核心思想是，如果产生冲突，产生一个新的hash值进行寻址，如果还是冲突，则继续。
上述的方法，主要的缺点在于不能从表中删除元素。
还有就是我们hashmap的思想外部拉链。</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/11/5d113d5c.jpg" width="30px"><span>天凉好个秋</span> 👍（246） 💬（1）<div>解决哈希冲突的常用方法有：

开放定址法
基本思想是：当关键字key的哈希地址p=H（key）出现冲突时，以p为基础，产生另一个哈希地址p1，如果p1仍然冲突，再以p为基础，产生另一个哈希地址p2，…，直到找出一个不冲突的哈希地址pi ，将相应元素存入其中。

再哈希法
这种方法是同时构造多个不同的哈希函数：
Hi=RH1（key）  i=1，2，…，k
当哈希地址Hi=RH1（key）发生冲突时，再计算Hi=RH2（key）……，直到冲突不再产生。这种方法不易产生聚集，但增加了计算时间。

链地址法
这种方法的基本思想是将所有哈希地址为i的元素构成一个称为同义词链的单链表，并将单链表的头指针存在哈希表的第i个单元中，因而查找、插入和删除主要在同义词链中进行。链地址法适用于经常进行插入和删除的情况。

建立公共溢出区
这种方法的基本思想是：将哈希表分为基本表和溢出表两部分，凡是和基本表发生冲突的元素，一律填入溢出表。</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（74） 💬（6）<div>为什么HashMap要树化？

文章说『本质是个安全问题』，但是导致安全问题的本质其实是性能问题。哈希碰撞频繁，导致链表过长，查询时间陡升，黑客则会利用这个『漏洞』来攻击服务器，让服务器CPU被大量占用，从而引起了安全问题。 而树化(使用红黑树）能将时间复杂度降到O(logn)，从而避免查询时间过长。所以说，本质还是个性能问题。    

----------
个人理解哈


</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/10/7b4a2ecc.jpg" width="30px"><span>鲤鱼</span> 👍（26） 💬（2）<div>读到最后链表树化刚准备开始飙车，结果突然跳车。树化讲细点更好</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/83/a912bfb4.jpg" width="30px"><span>xinfangke</span> 👍（13） 💬（1）<div>老师 如果hashmap中不存在hash冲突 是不是就相当于一个数组结构呢 就不存在链表了呢</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/df/bc98ecda.jpg" width="30px"><span>kevin</span> 👍（12） 💬（2）<div>看不太懂，讲的还不是不太浅显，既然是面试题，最好不要太浅，但也不要太深，你这个度掌握的不是很好</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/d4/abb7bfe3.jpg" width="30px"><span>代码狂徒</span> 👍（7） 💬（1）<div>针对负载因子，您所指的存太满会影响性能是指什么？毕竟已经开辟了相应内存空间的，没什么不用呢？</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/9e/c88ac921.jpg" width="30px"><span>沈琦斌</span> 👍（5） 💬（1）<div>老师，感觉最后讲为什么要树化的时候结尾有点突然。既然您说了树化本质上是个安全问题，那么树化以后怎么就解决安全问题了呢，这个我没有理解，谢谢。</div>2018-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b1/20/8718252f.jpg" width="30px"><span>鲲鹏飞九万里</span> 👍（4） 💬（1）<div>这个内容延展的好多，这要补多少天的功课，才能搞定😂</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/d4/abb7bfe3.jpg" width="30px"><span>代码狂徒</span> 👍（3） 💬（1）<div>为什么不是一开始就树化，而是要等到一定程度再树化，链表一开始就是消耗查找性能啊？另外其实不太明白为什么是0.75的负载因子，如果是.08或者0.9会有什么影响吗？毕竟已经开辟了相关内存空间</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/84/791fb8f1.jpg" width="30px"><span>Meteor</span> 👍（2） 💬（1）<div>hashCode() 和equals()两个方法之间什么关系</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/bb/eed7b035.jpg" width="30px"><span>Yonei</span> 👍（2） 💬（1）<div>我感觉树化一个目的是防止hash冲突导致的resize时的死循环，还有就是减少查找遍历路径，毕竟树的查找不用遍历全部，特别像是平衡二叉树的遍历。</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/a9/ae10f6cd.jpg" width="30px"><span>影随</span> 👍（2） 💬（1）<div>LinkedHashMapSample 那个示例，为什么

accessOrderedMap
@Override 的 removeEldestEntry()方法报错？  
只有我这儿报错吗？</div>2018-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/20/e93190e2.jpg" width="30px"><span>江昆</span> 👍（2） 💬（1）<div>为什么 HashMap 要树化呢？因为在最坏条件下，链表的查询时间是O(N），数的查询时间是O(LOG N）？能请老师解释一下为什么说本质上是因为安全呢？谢谢老师</div>2018-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/44/c4eadde0.jpg" width="30px"><span>沉默的雪人</span> 👍（2） 💬（1）<div>hashmap的树化，我记得是Jdk1.8的内容吧</div>2018-05-30</li><br/><li><img src="" width="30px"><span>whhbbq</span> 👍（1） 💬（1）<div>LinkedHashMapSample这段代码编译通不过吧？</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8d/a5/5d2acc00.jpg" width="30px"><span>Linus</span> 👍（1） 💬（1）<div>为什么hashcode与equals方法一定都要重写呢？</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（1） 💬（1）<div>杨老师，我使用你提供的LinkedHashMap Simple样例，.get()方法感觉没有效果，新增后，触发删除，删除的还是第一个插入的数据。</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（0） 💬（1）<div>jdk8 下 LinkedHashMapSample 示例的 new LinkedHashMap&lt;String, String&gt;(16, 0.75F, true)，&lt;&gt;的泛型要填上。</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/31/3a/206598a3.jpg" width="30px"><span>李继武</span> 👍（0） 💬（1）<div>哈希碰撞是指key算出来的哈希值相同还是说根据哈希值得到的索引值相同</div>2018-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/c9/f44cb7f3.jpg" width="30px"><span>爪哇夜未眠</span> 👍（0） 💬（1）<div>同问：
请问老师，为什么不是一开始就树化，而是要等到一定程度再树化，链表一开始就是消耗查找性能啊？另外其实不太明白为什么是0.75的负载因子，如果是0.8或者0.9会有什么影响吗？毕竟已经开辟了相关内存空间
</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/1e/a06abc12.jpg" width="30px"><span>鹤鸣</span> 👍（0） 💬（1）<div>写的真好，感谢</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（315） 💬（8）<div>Hashtable、HashMap、TreeMap心得

三者均实现了Map接口，存储的内容是基于key-value的键值对映射，一个映射不能有重复的键，一个键最多只能映射一个值。

（1）	元素特性
HashTable中的key、value都不能为null；HashMap中的key、value可以为null，很显然只能有一个key为null的键值对，但是允许有多个值为null的键值对；TreeMap中当未实现 Comparator 接口时，key 不可以为null；当实现 Comparator 接口时，若未对null情况进行判断，则key不可以为null，反之亦然。

（2）顺序特性
HashTable、HashMap具有无序特性。TreeMap是利用红黑树来实现的（树中的每个节点的值，都会大于或等于它的左子树种的所有节点的值，并且小于或等于它的右子树中的所有节点的值），实现了SortMap接口，能够对保存的记录根据键进行排序。所以一般需要排序的情况下是选择TreeMap来进行，默认为升序排序方式（深度优先搜索），可自定义实现Comparator接口实现排序方式。

（3）初始化与增长方式
初始化时：HashTable在不指定容量的情况下的默认容量为11，且不要求底层数组的容量一定要为2的整数次幂；HashMap默认容量为16，且要求容量一定为2的整数次幂。
扩容时：Hashtable将容量变为原来的2倍加1；HashMap扩容将容量变为原来的2倍。

（4）线程安全性
HashTable其方法函数都是同步的（采用synchronized修饰），不会出现两个线程同时对数据进行操作的情况，因此保证了线程安全性。也正因为如此，在多线程运行环境下效率表现非常低下。因为当一个线程访问HashTable的同步方法时，其他线程也访问同步方法就会进入阻塞状态。比如当一个线程在添加数据时候，另外一个线程即使执行获取其他数据的操作也必须被阻塞，大大降低了程序的运行效率，在新版本中已被废弃，不推荐使用。
HashMap不支持线程的同步，即任一时刻可以有多个线程同时写HashMap;可能会导致数据的不一致。如果需要同步（1）可以用 Collections的synchronizedMap方法；（2）使用ConcurrentHashMap类，相较于HashTable锁住的是对象整体， ConcurrentHashMap基于lock实现锁分段技术。首先将Map存放的数据分成一段一段的存储方式，然后给每一段数据分配一把锁，当一个线程占用锁访问其中一个段的数据时，其他段的数据也能被其他线程访问。ConcurrentHashMap不仅保证了多线程运行环境下的数据访问安全性，而且性能上有长足的提升。

(5)一段话HashMap
HashMap基于哈希思想，实现对数据的读写。当我们将键值对传递给put()方法时，它调用键对象的hashCode()方法来计算hashcode，让后找到bucket位置来储存值对象。当获取对象时，通过键对象的equals()方法找到正确的键值对，然后返回值对象。HashMap使用链表来解决碰撞问题，当发生碰撞了，对象将会储存在链表的下一个节点中。 HashMap在每个链表节点中储存键值对对象。当两个不同的键对象的hashcode相同时，它们会储存在同一个bucket位置的链表中，可通过键对象的equals()方法用来找到键值对。如果链表大小超过阈值（TREEIFY_THRESHOLD, 8），链表就会被改造为树形结构。</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/6d/73cc6c5b.jpg" width="30px"><span>浮幻随尘</span> 👍（306） 💬（8）<div>感觉每个知识点都很重要，但又点到为止，感觉读完不痛不痒，好像学到什么，但细想又没掌握什么，希望能够深入一点！</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/ca/2d8c4733.jpg" width="30px"><span>amourling</span> 👍（215） 💬（0）<div>提个意见，文章中请不要出现太多似乎，怀疑之类的必须，该是什么就是什么，不确定的不要拿出来。</div>2018-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/21/104b9565.jpg" width="30px"><span>小飞哥 ‍超級會員</span> 👍（64） 💬（2）<div>总觉得还是不太深，只是每个map的区别。我觉得每个map的实现都能讲出很多问题来，在面试时也经常碰壁，看完但也没觉得学到什么深入的地方</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/22/06/9549f55d.jpg" width="30px"><span>Darcy</span> 👍（21） 💬（0）<div>equals 的对称、反射、传递等特性。
这里的反射是不是写错了，应该是自反性，对称性，传递性，一致性等等</div>2018-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（17） 💬（0）<div>我一直认为：JAVA集合类是非常好的学习材料。

如果敢说精通JAVA集合类，计算机功底肯定不会太差</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/4c/fd6e6116.jpg" width="30px"><span>睡骨</span> 👍（15） 💬（0）<div>希望作者分享源码的时候，最好备注是基于哪个版本的 毕竟有些地方不同版本差异较大</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/2e/b816a431.jpg" width="30px"><span>陈大麦</span> 👍（14） 💬（1）<div>老师我想问一下，hashmap明明继承了abstractmap，而abstractmap已经实现了map接口，为什么hashmap还要实现map接口呢?</div>2018-07-28</li><br/>
</ul>