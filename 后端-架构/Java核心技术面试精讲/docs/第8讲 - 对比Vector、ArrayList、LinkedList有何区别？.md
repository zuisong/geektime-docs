我们在日常的工作中，能够高效地管理和操作数据是非常重要的。由于每个编程语言支持的数据结构不尽相同，比如我最早学习的C语言，需要自己实现很多基础数据结构，管理和操作会比较麻烦。相比之下，Java则要方便的多，针对通用场景的需求，Java提供了强大的集合框架，大大提高了开发者的生产力。

今天我要问你的是有关集合框架方面的问题，对比Vector、ArrayList、LinkedList有何区别？

## 典型回答

这三者都是实现集合框架中的List，也就是所谓的有序集合，因此具体功能也比较近似，比如都提供按照位置进行定位、添加或者删除的操作，都提供迭代器以遍历其内容等。但因为具体的设计区别，在行为、性能、线程安全等方面，表现又有很大不同。

Vector是Java早期提供的**线程安全的动态数组**，如果不需要线程安全，并不建议选择，毕竟同步是有额外开销的。Vector内部是使用对象数组来保存数据，可以根据需要自动的增加容量，当数组已满时，会创建新的数组，并拷贝原有数组数据。

ArrayList是应用更加广泛的**动态数组**实现，它本身不是线程安全的，所以性能要好很多。与Vector近似，ArrayList也是可以根据需要调整容量，不过两者的调整逻辑有所区别，Vector在扩容时会提高1倍，而ArrayList则是增加50%。

LinkedList顾名思义是Java提供的**双向链表**，所以它不需要像上面两种那样调整容量，它也不是线程安全的。

## 考点分析

似乎从我接触Java开始，这个问题就一直是经典的面试题，前面我的回答覆盖了三者的一些基本的设计和实现。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/51/0d/14d9364a.jpg" width="30px"><span>L.B.Q.Y</span> 👍（16） 💬（1）<div>请教老师个问题，Collection接口的声明是带范型的，其中定义的Object[ ] toArray()方法为什么不是范型方式的？有什么原因吗？</div>2018-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/84/62b4afaf.jpg" width="30px"><span>孙晓刚</span> 👍（43） 💬（5）<div>精选第一个对于读写效率问题，我觉得表述有问欠缺，或者说不能那么绝对。 
1、并不是所有的增删都会开辟新内存，没有开辟新内存的尾部增，效率也是杠杠的。
2、尾部删除也不需要开辟新内存，只是移出最后一个对象。
之前我也是接收了ArrayList的特性随机访问快，增删效率差。直到看到源码才知道，没那么绝对。
直接导致结果就是本身适合使用ArrayList的场景会因为这个笼统的说法而选LinkedList</div>2018-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（109） 💬（2）<div>在这个题目下，自然就会想到优先级队列了，但还需要额外考虑vip再分级，即同等级vip的平权的问题，所以应该考虑除了直接的和vip等级相关的优先级队列优先级规则问题，还得考虑同等级多个客户互相不被单一客户大量任务阻塞的问题，数据结构确实是基础，即便这个思考题考虑的这个场景，待调度数据估计会放在redis里面吧</div>2018-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（89） 💬（3）<div>既然是Java的主题，那就用PriorityBlockingQueue吧。
如果是真实场景肯定会考虑高可用能持久化的方案。
其实我觉得应该参考银行窗口，同时三个窗口，就是三个队列，银台就是消费者线程，某一个窗口vip优先，没有vip时也为普通客户服务。要实现，要么有个dispatcher，要么保持vip通道不许普通进入，vip柜台闲时从其他队列偷</div>2018-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/53/e8/137a75f5.jpg" width="30px"><span>linco_001</span> 👍（53） 💬（1）<div>由于要处理的任务有前后顺序关系，所以首先想到使用优先队列。使用 PriorityQueue，将VIP用户的优先级设置为最高，优先处理。借鉴操作系统中的调度算法，对于其他用户，我们还可以设计各种公平的优先级选择算法（基于排队先后顺序，基于调度任务所需的时间长短（操作系统中的短作业优先算法）排序、高响应比（（所用时间+等待时间）&#47;等待时间）优先进行排序），与 PriorityQueue 结合使用。
类似场景大多就是基于队列的数据结构了。实际工具的话，消息队列（MQ）就是很直接的例子了。可以使用消息队列对用户请求进行削锋操作，前台快速响应，后台私下进行处理操作。
除此之外可以想到优化：利用分布式系统的优点，将VIP用户的请求分发到运算力更高的服务器上进行处理。达到高可用的特点！</div>2019-01-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK8hCUT5pssp9t18pzQVSvXUefMreLvRV7xgVpuWR1oBwLnncouQOWiaBCMZQobW5d1ibfZicflARYxQ/132" width="30px"><span>马建超</span> 👍（6） 💬（1）<div>每天看一集，不断提高自己，加油</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/7b/eed9d6d6.jpg" width="30px"><span>小笨蛋</span> 👍（4） 💬（2）<div>招聘时我更倾向于考察面试者自身最擅长的东西，免得招到纯面试高手?这个你一般会怎么面试？纯面试感受是一个什么样的表现？</div>2018-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（4） 💬（1）<div>杨老师，问个问题，Collection接口下面已细化了List,Set和Queue子接口，未什么又定义了AbstractCollection这个抽象类？具体是什么考虑？以为我发现3个接口的子类都是集成这个抽象类。</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/fd/1e3d14ee.jpg" width="30px"><span>王宁</span> 👍（4） 💬（1）<div>面试的重点HashMap,实现原理，扩展什么的，1.7和1.8的区别。还有和hashtable的异同。还有juc下面集合的熟悉程度。
</div>2018-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/68/9491468e.jpg" width="30px"><span>且以深情共白头</span> 👍（2） 💬（1）<div>之前一直以为Verctor不属于集合，只是数组。学习了。针对VIP客户任务优先处理场景，认为采用SortSet进行，按照默认排序即可，数值越小优先级越高，和线程的优先级级别一致</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/4b/4fb10188.jpg" width="30px"><span>我奋斗去了</span> 👍（2） 💬（1）<div>可以使用priority queue ，维护两个队列 一个VIP队列 一个普通用户队列 。当VIP队列有人的情况优先处理</div>2018-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/7c/f0e808b9.jpg" width="30px"><span>webwombat</span> 👍（2） 💬（1）<div>那个问题，应该是priority queue吧？操作系统的进程调度一般都是基于优先级队列来实现的。</div>2018-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/75/7057e997.jpg" width="30px"><span>听风</span> 👍（0） 💬（1）<div>讲这种东西其实我很想知道它的内部结构以及在内存中的结构</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/0d/14d9364a.jpg" width="30px"><span>L.B.Q.Y</span> 👍（0） 💬（1）<div>集合框架的那张图，SortedSet应该是接口，图里面画成类了，TreeSet看起来有两个父类了。</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/0f/470c6487.jpg" width="30px"><span>悬崖丶</span> 👍（0） 💬（1）<div>想问一个小白问题，List接口继承了Collection接口，为什么List接口还要重写一遍Collection接口中的一些方法</div>2018-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（0） 💬（1）<div>最近学习过程中，感觉看原代码比较吃力。一个Hash Map没有看明白，这么对Key的Set赋值，这么对value的Collection赋值。</div>2018-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（268） 💬（9）<div>Vector、ArrayList、LinkedList均为线型的数据结构，但是从实现方式与应用场景中又存在差别。

1 底层实现方式
ArrayList内部用数组来实现；LinkedList内部采用双向链表实现；Vector内部用数组实现。

2 读写机制
ArrayList在执行插入元素是超过当前数组预定义的最大值时，数组需要扩容，扩容过程需要调用底层System.arraycopy()方法进行大量的数组复制操作；在删除元素时并不会减少数组的容量（如果需要缩小数组容量，可以调用trimToSize()方法）；在查找元素时要遍历数组，对于非null的元素采取equals的方式寻找。

LinkedList在插入元素时，须创建一个新的Entry对象，并更新相应元素的前后元素的引用；在查找元素时，需遍历链表；在删除元素时，要遍历链表，找到要删除的元素，然后从链表上将此元素删除即可。
Vector与ArrayList仅在插入元素时容量扩充机制不一致。对于Vector，默认创建一个大小为10的Object数组，并将capacityIncrement设置为0；当插入元素数组大小不够时，如果capacityIncrement大于0，则将Object数组的大小扩大为现有size+capacityIncrement；如果capacityIncrement&lt;=0,则将Object数组的大小扩大为现有大小的2倍。

3 读写效率

ArrayList对元素的增加和删除都会引起数组的内存分配空间动态发生变化。因此，对其进行插入和删除速度较慢，但检索速度很快。

LinkedList由于基于链表方式存放数据，增加和删除元素的速度较快，但是检索速度较慢。

4 线程安全性

ArrayList、LinkedList为非线程安全；Vector是基于synchronized实现的线程安全的ArrayList。

需要注意的是：单线程应尽量使用ArrayList，Vector因为同步会有性能损耗；即使在多线程环境下，我们可以利用Collections这个类中为我们提供的synchronizedList(List list)方法返回一个线程安全的同步列表对象。

问题回答

利用PriorityBlockingQueue或Disruptor可实现基于任务优先级为调度策略的执行调度系统。</div>2018-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/d8/44023f1f.jpg" width="30px"><span>jackyz</span> 👍（41） 💬（0）<div>集合：就像是一种容器。用于存储、获取、操作对象的容器。

1. 数组的弊端
①数组的长度不可变     ②数组没有提供可以查看有效元素个数的方法

2. 集合的特点
①集合的长度是可变的
②集合可以存储任意类型的对象
③集合只能存储对象

3. 集合框架
java.util.Collection : 集合层次的根接口
    |--- java.util.List: 有序的，可以重复的。
        |--- ArrayList: 采用数组结构存储元素。 查询操作多时选择
        |--- LinkedList: 采用链表结构存储元素。 增删操作多时选择
        |--- Vector:
    |--- java.util.Set: 无序的，不允许重复。
        |--- HashSet : 是 Set 接口的典型实现类。
            判断元素是否存在的依据是：先比较 hashCode 值，若 hashCode 存在，再通过 equals() 比较内容
                                     若 hashCode 值不存在，则直接存储

            注意：重写 hashCode 和 equals 二者需要保持一致！
            |--- LinkedHashSet: 相较于 HashSet 多了链表维护元素的顺序。遍历效率高于 HashSet ， 增删效率低于 HashSet
        |--- TreeSet : 拥有自己排序方式
            |-- 自然排序（Comparable）：
                ①需要添加 TreeSet 集合中对象的类实现  Comparable 接口
                ②实现 compareTo(Object o) 方法
            |-- 定制排序（Comparator）
                ①创建一个类实现 Comparator 接口
                ②实现 compare(Object o1, Object o2) 方法
                ③将该实现类的实例作为参数传递给 TreeSet 的构造器       </div>2018-11-20</li><br/><li><img src="" width="30px"><span>zjh</span> 👍（24） 💬（0）<div>比较片面的说，java集合类底层基本上就是基于数组或者链表来实现的，数组的地址连续性决定了其随机存取速度较快，但是涉及到扩容则比较耗时，而链表则不存在扩容的性能消耗，但随机访问需要遍历地址因此相对数组要慢，所以判断一个集合的特点可以先判断是基于数组还是链表。</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（15） 💬（0）<div>今天看了一下PriorityQueue的源码，发现其是使用最小堆结构(二叉堆)，存放在数组中(数组索引对应树的从上到下，从左到右)。采用上面最小，每插入一个数据，就先与根节点比较，如果小于根节，依次换位置；大于根节点，就放在最后一个位置。</div>2018-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（10） 💬（0）<div>深入到底层数据的存储基本绕不出数组和链表，要么依赖数组，要么依赖链表，要么数组和链表的结合。
其他语言估计类似，所以，看集合的底层实现基本就确定了它的特点，这是数据结构的本质决定的。另外，就是多线程的加持与否啦！
支持，则需加锁，加锁则影响性能，当然，不同的锁，还有不同的特点，比如：是否阻塞、是否可重入、锁是轻量级还是重量级。
这篇也需要反复读，加看源码！</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/08/855abb02.jpg" width="30px"><span>Seven.Lin澤耿</span> 👍（9） 💬（0）<div>实现一个云计算任务调度系统，希望可以保证 VIP 客户的任务被优先处理，你可以利用哪些数据结构或者标准的集合类型呢？
优先级，第一个想到的就是PriorityQueue来实现，自定义权重比较， 优先处理VIP请求。
但是，会有一个问题，就是VIP请求如果过多，那么普通客户的请求就没法处理，一致等待。
改造：
利用不同的队列来保存不同的客户等级请求，然后用两个不同的线程池来处理请求：
第一个线程池只处理普通用户的请求
第二个线程池来处理VIP请求，如果没有VIP请求，则参与处理普通用户请求
也就是客户等级之间是平等的，也达到VIP优先处理，这个时候的队列不一定用PriorityQueue来实现，普通的队列也可以，或者普通的队列都可以。</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/16/48/01567df1.jpg" width="30px"><span>郑泽洲</span> 👍（6） 💬（0）<div>杨老师，请教2个一直困扰我的问题：
1.ArrayList是继承了AbstractArrayList，其中AbstractArrayList已经实现了List接口，ArrayList自然隐含实现了List接口。可是为什么ArrayList还显式声明实现了List接口？
2. Arrays.asList返回的是List类型，其内部是Arrays.ArrayList为什么不直接用java.util.ArrayList
</div>2019-04-17</li><br/><li><img src="" width="30px"><span>呵呵</span> 👍（4） 💬（0）<div>阅读速度太快了</div>2018-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c5/6e/82ef354b.jpg" width="30px"><span>码上Java</span> 👍（3） 💬（1）<div>对比 Vector、ArrayList、LinkedList有何区别？
Vector是Java早期提供的线程安全的动态数组，如果不需要线程安全，并不建议选择，毕竟同步是有额外开销的。Vector内部是使用对象数组来保存数据，可以根据需要自动的增加容量，当数据已满时，会创建新的数组，并拷贝原有数组数据。
ArrayList是应用更加广泛的动态数组实现，它本身不是线程安全的，所以性能要好很多，与Vector近似，ArrayList也是可以根据需要调整容量，不过两者的调整逻辑有所区别，Vector在扩容时会提高1倍，而ArrayList则是增加50%。
LinkedList顾名思义是Java提供的双向链表，所以它不需要像上面那样调整容量，它也不是线程安全的。
-Vector和ArrrayList作为动态数组，其内部元素以数组形式顺序存储的，所以非常适合随机访问的场合。除了尾部插入和删除元素，往往性能会相对较差，比如我们在中间位置插入一个元素，需要移动后续所有元素。
-而ArrayList进行结点插入、删除却要高效很多，但是随机访问性能则要比动态数组慢。
</div>2019-05-03</li><br/><li><img src="" width="30px"><span>Geek</span> 👍（1） 💬（0）<div>&quot;LinkedList 进行节点插入、删除却要高效得多&quot; 这个还真不一定，和数据多少有很大关系。主要是数据组扩容复制和list new一个对象索引插入这两者之间哪个效率高的一个判断。例如，容量大的时候一次数组扩容，就可以插入很多次，此时只需复制移动元素，而list每次都要new，前者效率高</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/d4/f4a2888a.jpg" width="30px"><span>请叫我华仔</span> 👍（1） 💬（0）<div># 集合
Vector 线程安全的动态数组。
ArrayList 动态数组。扩容时复制原数组。随机访问效率高。
LinkedList 双向链表，插入删除效率高。

内部排序：归并，冒泡，快排，选择，插入
外部排序：借助外部存储排序

java集合框架：list set queue
java提供的默认排序算法：双轴快排，TimSort

思考题：优先级队列，操作系统就用了优先级队列。

</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/b4/a12edf06.jpg" width="30px"><span>要离刺荆轲</span> 👍（1） 💬（0）<div>ArrayList和LinkedList在数据量比较大时，指定位置插入，不一定ArrayList慢，LinkedList插入时需要遍历位置。我实际实验过，你不能直说因为链表，插入就快</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（1） 💬（0）<div>杨老师，有个问题，TreeSet为什么不支持正序，只支持倒序(DescendingIteractor)？Tree本身支持正序列.</div>2018-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/41/ffe48d0c.jpg" width="30px"><span>Lawt</span> 👍（1） 💬（0）<div>写得还挺不错的，担心36期能讲那么多没容吗？持续关注，相信您，期待</div>2018-05-24</li><br/>
</ul>