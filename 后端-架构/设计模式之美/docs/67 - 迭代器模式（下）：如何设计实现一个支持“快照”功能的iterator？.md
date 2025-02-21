上两节课，我们学习了迭代器模式的原理、实现，并且分析了在遍历集合的同时增删集合元素，产生不可预期结果的原因以及应对策略。

今天，我们再来看这样一个问题：如何实现一个支持“快照”功能的迭代器？这个问题算是对上一节课内容的延伸思考，为的是帮你加深对迭代器模式的理解，也是对你分析、解决问题的一种锻炼。你可以把它当作一个面试题或者练习题，在看我的讲解之前，先试一试自己能否顺利回答上来。

话不多说，让我们正式开始今天的学习吧！

## 问题描述

我们先来介绍一下问题的背景：如何实现一个支持“快照”功能的迭代器模式？

理解这个问题最关键的是理解“快照”两个字。所谓“快照”，指我们为容器创建迭代器的时候，相当于给容器拍了一张快照（Snapshot）。之后即便我们增删容器中的元素，快照中的元素并不会做相应的改动。而迭代器遍历的对象是快照而非容器，这样就避免了在使用迭代器遍历的过程中，增删容器中的元素，导致的不可预期的结果或者报错。

接下来，我举一个例子来解释一下上面这段话。具体的代码如下所示。容器list中初始存储了3、8、2三个元素。尽管在创建迭代器iter1之后，容器list删除了元素3，只剩下8、2两个元素，但是，通过iter1遍历的对象是快照，而非容器list本身。所以，遍历的结果仍然是3、8、2。同理，iter2、iter3也是在各自的快照上遍历，输出的结果如代码中注释所示。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/66/59e0647a.jpg" width="30px"><span>万历十五年</span> 👍（42） 💬（3）<div>思考题：为迭代器创建虚引用，当迭代器被回收时，清空容器中相应元素。</div>2020-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/57/77/5bcefe24.jpg" width="30px"><span>太阳app苹果版</span> 👍（4） 💬（3）<div>1.代码貌似跑得不对，只有justNext方法自增了cursorInAll，假设第一个元素没有被删除，那么总是cursorInAll总是0；
2.时间戳获取有点问题，连续操作获取时间戳很有可能都是一样的，应该将时间戳进行递增操作，防止相等</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/d9/75dd7cf9.jpg" width="30px"><span>Mew151</span> 👍（0） 💬（1）<div>方案二中：
  public E get(int i) {
    if (i &gt;= totalSize) {
      throw new IndexOutOfBoundsException();
    }
    return (E)elements[i];
  }
这个方法不需要判断第i个元素是不是已删除的吗？</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/40/e7ef18de.jpg" width="30px"><span>嘉一</span> 👍（0） 💬（1）<div>发现一个问题，如果在SnapshotArrayIterator创建前添加了几个数据，那么会不会出现这几个数据的添加时间戳和SnapshotArrayIterator创建的时间戳是一样（因为计算机的时间戳最小是毫秒，而添加数据毕竟是非常快的操作，可能在不到一毫秒的时间就完成了）的导致这几个数据遍历不了？</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（93） 💬（11）<div>思考题感觉像是数据库的MVCC？
- 容器中维护一个每个迭代器创建时间的列表
- 每次有迭代器创建时就在这个列表中加入自己的创建时间
- 迭代器迭代完成后将列表中对应时间点删除
- 清理容器时，对于容器中每个元素，如果addTime小于这个列表中的最小时间点就可以进行删除</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（19） 💬（9）<div>在阅读本节代码实现就想到了第二种方案存在类似思考题的问题
解决方案可以在合适的时候清理带删除标记的元素。本想使用数据库的多版本控制（MVCC)的方案，把所有的迭代器对象存起来，并添加创建时间。但是冒出一个新问题，数据库事务有commit来表示事务已完成，而迭代器的使用完成无法知晓，还在思考方案中……</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/4d/58c2ffa1.jpg" width="30px"><span>smartjia</span> 👍（15） 💬（9）<div>感觉代码有两个小问题，若理解有误，请帮指正：

问题1. 重复删除同一个元素时，actualSize 应该保持不变。
以下是修改后的代码：
@Override 
public void remove(E obj) 
{
 for (int i = 0; i &lt; totalSize; ++i) {
 if (elements[i].equals(obj) &amp;&amp; delTimestamps[i] == Long.MAX_VALUE) { &#47;&#47; 防止重复删除
 delTimestamps[i] = System.currentTimeMillis(); 
 actualSize--; }
 } 
}

问题2： 遍历完一个元素后需要让 cursorInAll 自增，否则 cursorInAll 一直指向第一个待遍历的元素。同时hasNext() 恒为true， 也需要修改。
以下是修改后的代码：

@Override 
public E next() { 
 E currentItem = arrayList.get(cursorInAll); 
 cursorInAll++； &#47;&#47;自增，否则 cursorInAll 一直不变
 justNext(); 
 return currentItem; 
}

@Override 
public boolean hasNext() { 
      return this.leftCount &gt;= 0; &#47;&#47; 注意是&gt;=, 而非&gt; （ 修改后 leftCount &gt;= 0 恒成立， 总是返回 true）
      改为：
      return cursorInAll &lt; arrayList.totalSize()；
} </div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（15） 💬（3）<div>课后思考题：类似数组动态扩容和缩容，删除元素时可以比较被删除元素的总数，在被删除元素总数 &lt; 总数的 1&#47;2 时， 进行resize数组，清空被删除的元素，回收空间。</div>2020-04-06</li><br/><li><img src="" width="30px"><span>辉哥</span> 👍（7） 💬（5）<div>课堂讨论：可以创建一个object类型的常量，删除数组元素时，可以将被删除数组元素的引用指向该常量。Android中的SparseArray就是采用此方式实现的</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（7） 💬（2）<div>记录一个迭代变量，每迭代一次，计数加一，迭代完一次减一，当为0的时候就可以删除标记为delete的元素了</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/5f/2cc4060c.jpg" width="30px"><span>子豪sirius</span> 👍（5） 💬（0）<div>第二个问题，我想可不可用个数组记录当前有多少个迭代器。每调用一次iterrator方法，迭代器加一；有元素删除时，记录这个时间点的迭代器的数量；当迭代器访问到该元素时，减一，减到0，说明不再有删除该元素时间点之前生成的迭代器来访问了，就可以实际删除该元素。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/41/dbb7d785.jpg" width="30px"><span>xk_</span> 👍（3） 💬（2）<div>课后题：
我们可以在集合类中记录每一个迭代器创建时间列表iteratorCreateTimeList。

在迭代器创建的时候，删除iteratorCreateTimeList[0]之前的被标记删除的元素。

在迭代器中需要写一个销毁的方法，删掉iteratorCreateTimeList中对应的创建时间，删除iteratorCreateTimeList[0]之前的被标记删除的元素。</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（3） 💬（2）<div>可以参考GC的算法，弄一个减化版的优化方法：
1. 被删除的元素是否还有可能被已经创建的iterator所访问，即被删除的元素还被引用着；（iterator使用完需要有调用关闭动作）
2. 被删除的元素达到一定量时，按照删除时间清理掉效早删除的元素，清理掉的最晚的被删除元素的删除时间放置在清理标识字段，iterator迭代时检查清理标识字段，如果iterator创建时间早于清理标识字段中的时间丢出异常；</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/0e/c77ad9b1.jpg" width="30px"><span>eason2017</span> 👍（3） 💬（0）<div>定时清理里面的数据，做一次同步。期间可能会加锁来保证数据的有效性。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（2） 💬（0）<div>想起来MySQL中的多版本控制，用于实现事物间不同的隔离级别</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（2） 💬（2）<div>1.给元素打时间截实现快照，空间成本会比较大。这里其实采用复制状态机一样能起到效果，只是空间成本就变成了时间成本。

2.至于栏主的课后题，这已经是从实现快照，变成快照操作在多线程可见了。那么当前的实现是不严谨的，并发会有数据不符合预期的情况。

3.不考虑并发问题，仅看如何释放内存这个问题。复制状态机可以将一段时间的log整合，实现快照往前移动（比如redis）。放在这里也一样，定时对元素做整合，将被删除的元素移除即可。（遗憾的时，基于时间截这种，无法在某个快照（状态），结合log，做往后倒退的操作）</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/20/e4f1b17c.jpg" width="30px"><span>zj</span> 👍（2） 💬（3）<div>我有个想法，当迭代器创建后，容器元素如果被删除了，则在迭代器创建强引用指向这个容器元素，容器中元素将之前元素的强引用变为弱引用。
 当迭代器不再使用后，会被gc掉，从而删除的元素只剩下弱引用了，那下一次gc，这个删除的元素就会被gc掉。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ba/9a/73de36cb.jpg" width="30px"><span>九五二七</span> 👍（1） 💬（0）<div>CopyOnWrite的方式可行？</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/69/be/8f7c77e5.jpg" width="30px"><span>vecheer</span> 👍（1） 💬（0）<div>如果是链表的话，个人觉得还是在迭代器创建的时候，直接维护一份迭代器到真实list元素对象的引用列表比较划算。迭代器存在，就会有指针指向这些元素，即便list删除元素而且发生gc，这些元素也不会丢失。当本迭代器消亡时，对于list中已经死亡的引用也随之消亡，大伙都会被gc掉。这么做可能会增加一定的时空成本，但是个人觉得比时间戳方式要简洁一些。</div>2023-02-02</li><br/><li><img src="" width="30px"><span>Geek_7e0e83</span> 👍（1） 💬（0）<div>这个思考题 没有想出来思路。先参考了一下 精选的留言 然后再加上自己的理解 提供给大家参考

1.维护一个迭代器的创建时间戳列表，记录了每一个迭代器创建的时间。迭代器使用完毕后。将时间信息移除。当元素执行删除动作的时候，如果元素的删除时间满足，小于最小的迭代器时间戳列表时间。则当前元素可以删除。意味着没有迭代器使用了这个元素。整个核心的关键在于 元素删除的时间节点是否有迭代器引用此元素。

2.弱引用

实际上是在上一步的基础上自动化的解决了迭代器使用完毕之后的主动删除操作。可以将迭代器存储在弱引用对象中，然后建立一个集合存储这些弱引用的迭代器对象。那么当迭代器不再使用的时候，弱引用对象会自动被GC回收。容器执行元素的删除动作(size() 扩容等等会和元素数据有交互的操作的时候)时，只需要遍历弱引用迭代器集合，看当前迭代器对象还存在的迭代器的创建时间 是否大于 删除元素的删除时间 如果大于 就可以删除此元素。因为这代表着这个元素被删除的之后才创建的迭代器。</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/83/a5/9312bc8c.jpg" width="30px"><span>ZQY</span> 👍（1） 💬（0）<div>异曲同工：Leetcode1146-Snapshot Array</div>2022-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ac/ff/791d0f5e.jpg" width="30px"><span>Geek_b71d2c</span> 👍（1） 💬（0）<div>在方案一中老师说了Java属于浅拷贝，只拷贝容器的引用，那原有容器中的数据发生增删时会同步影响到迭代器中的容器，那这样又如何能实现快照功能呢？</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（1） 💬（1）<div>课堂讨论: 
在调用List#iterator()之前, 删除deltimestamp &lt; 当前时间的元素.</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（1） 💬（1）<div>是的，这个是和数据库的事务隔离差不多，老师这里用的是时间戳，我们还可以利用一个自增的序列号来控制，都是一样的；</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/d0/d8a5f720.jpg" width="30px"><span>Ken张云忠</span> 👍（1） 💬（0）<div>在集合增加一个数组field，专门用来记录引用该元素的迭代器个数，当迭代器个数为0且该元素已经标记为删除元素时才真正的删除元素，当需要迭代器使用者在使用完迭代器后需要显示得调用迭代器注销该元素的函数，对于使用者不太友好了。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f3/db/5b7a8fd8.jpg" width="30px"><span>筱乐乐哦</span> 👍（1） 💬（2）<div>老师，有个问题：你在文章中说到：让容器既支持快照遍历，又支持随机访问？我们可以在 ArrayList 中存储两个数组。一个支持标记删除的，用来实现快照遍历功能；一个不支持标记删除的（也就是将要删除的数据直接从数组中移除），用来支持随机访问
如果是这样操作，那和浅拷贝的那个比较，没发现有优势呀，老师可以说下这块吗</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/3f/bbb8a88c.jpg" width="30px"><span>徐凯</span> 👍（1） 💬（0）<div>容器可以放指向元素的指针，当不用时直接将指针释放并置为空</div>2020-04-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/zwnyvuRu3Wx67uZd3YpVSGRLOaicVicccsbFHQGd5G2PfYlxGZv1TxlgbrkGppIUekfHwtsjjotLMcmohmguNmyQ/132" width="30px"><span>Geek_ce027a</span> 👍（0） 💬（0）<div>作者应该把设计模式的思想抽象成图来表达，而不是特定去利用特定的语言表达，这就导致了思维会被动的跟随作者的代码来走。</div>2024-05-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLCrJQ4AZe8VrDkR6IO03V4Tda9WexVT4zZiahBjLSYOnZb1Y49JvD2f70uQwYSMibUMQvib9NmGxEiag/132" width="30px"><span>Dowen Liu</span> 👍（0） 💬（0）<div>和 PG 的堆表 MVVC 有点像</div>2024-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/bd/0046f85a.jpg" width="30px"><span>管管</span> 👍（0） 💬（0）<div>加时间戳的方法 似乎有点问题，在m1中是跑代码，创建第一个iter1的snapshotTimestamp 与可以与第一个删除的时间相同。。是不是在多核情况下，cpu对代码做了优化哈</div>2024-03-29</li><br/>
</ul>