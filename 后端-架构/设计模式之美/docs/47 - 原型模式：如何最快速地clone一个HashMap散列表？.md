对于创建型模式，前面我们已经讲了单例模式、工厂模式、建造者模式，今天我们来讲最后一个：原型模式。

对于熟悉JavaScript语言的前端程序员来说，原型模式是一种比较常用的开发模式。这是因为，有别于Java、C++等基于类的面向对象编程语言，JavaScript是一种基于原型的面向对象编程语言。即便JavaScript现在也引入了类的概念，但它也只是基于原型的语法糖而已。不过，如果你熟悉的是Java、C++等这些编程语言，那在实际的开发中，就很少用到原型模式了。

今天的讲解跟具体某一语言的语法机制无关，而是通过一个clone散列表的例子带你搞清楚：原型模式的应用场景，以及它的两种实现方式：深拷贝和浅拷贝。虽然原型模式的原理和代码实现非常简单，但今天举的例子还是稍微有点复杂的，你要跟上我的思路，多动脑思考一下。

话不多说，让我们正式开始今天的学习吧！

## 原型模式的原理与应用

如果对象的创建成本比较大，而同一个类的不同对象之间差别不大（大部分字段都相同），在这种情况下，我们可以利用对已有对象（原型）进行复制（或者叫拷贝）的方式来创建新对象，以达到节省创建时间的目的。这种基于原型来创建对象的方式就叫作**原型设计模式**（Prototype Design Pattern），简称**原型模式**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/e9/2f02a383.jpg" width="30px"><span>冬瓜蔡</span> 👍（5） 💬（3）<div>日常开发中常用的是spring提供的对象之间拷贝的方法： BeanUtils.copyProperties
1、如果是基础类型，则没有问题。
2、如果要拷贝对象里面有小对象，且小对象的全限定名不一样，则拷贝结束后，该对象为null；
public class Person {
    private Photo photo;
}
3、如果要拷贝对象里面有集合，集合里面存放的是小对象，则会由于泛型的存在，可以拷贝成功，但是这个拷贝的对象是错误的，会在后续使用过程中产生问题
public class Person {
    private List&lt;Photo&gt; photo;
}

本质上BeanUtils.copyProperties是浅拷贝，在使用过程中需要对嵌套对象或者集合进行额外处理</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/4e/b81969fa.jpg" width="30px"><span>南北少卿</span> 👍（1） 💬（1）<div>如果对象的创建成本比较大，而同一个类的不同对象之间差别不大（大部分字段都相同） ...
这句话没有想明白</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/4e/ef406442.jpg" width="30px"><span>唯她命</span> 👍（0） 💬（2）<div>
public class Demo {
  private ConcurrentHashMap&lt;String, SearchWord&gt; currentKeywords = new ConcurrentHashMap&lt;&gt;();
  private long lastUpdateTime = -1;

  public void refresh() {
    &#47;&#47; 从数据库中取出更新时间&gt;lastUpdateTime的数据，放入到currentKeywords中
    List&lt;SearchWord&gt; toBeUpdatedSearchWords = getSearchWords(lastUpdateTime);
    long maxNewUpdatedTime = lastUpdateTime;
    for (SearchWord searchWord : toBeUpdatedSearchWords) {
      if (searchWord.getLastUpdateTime() &gt; maxNewUpdatedTime) {
        maxNewUpdatedTime = searchWord.getLastUpdateTime();
      }
}

代码有问题啊，   List&lt;SearchWord&gt; toBeUpdatedSearchWords = getSearchWords(lastUpdateTime);
toBeUpdatedSearchWords里的数据是改过的数据，时间都大于lastUpdateTime
那为啥下面还要searchWord.getLastUpdateTime() &gt; maxNewUpdatedTime？？？？
</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/13/80/2c9da1b1.jpg" width="30px"><span>L🚲🐱</span> 👍（94） 💬（2）<div>问题 1: 逻辑删除即可
问题 2:  返回深拷贝对象</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/3c/5d54c510.jpg" width="30px"><span>skull</span> 👍（60） 💬（0）<div>原型模式，最为常用经典就是BeanUtils</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（18） 💬（2）<div>问题1:
方法一：新旧的数据取交集，可以删除旧map中的删除关键字，之后的逻辑就和文章中一样了。
方法二：逻辑删除，当map的size中已删除占比过高时，resize map。

争哥说：这里我们利用了 Java 中的 clone() 语法来复制一个对象。如果你熟悉的语言没有这个语法，那把数据从 currentKeywords 中一个个取出来，然后再重新计算哈希值，放入到 newKeywords 中也是可以接受的。

Java HashMap的clone方法就把数据取出来，计算hash值，在放回去的。clone方法中，调用了putMapEntries方法，其中有一关键的一行，克隆重新计算了hash值：
putVal(hash(key), key, value, false, evict); 

文章中的深复制：为什么SearchWord不重写clone方法呢？
@Override
protected Object clone() throws CloneNotSupportedException {
  SearchWord newWord = new SearchWord(this.keyWord, this.times, this.tmstamp);
  return newWord;
}
</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/fe/1353168d.jpg" width="30px"><span>岁月</span> 👍（17） 💬（3）<div>课堂讨论题
关键字如果支持删除, 最简单高效的方法就是在数据表里加一个delete bool类型的字段, 占用空间不多, 但是很方便程序识别最近更新的数据里面, 有哪条是需要删除的. 不过这样会带来一个问题, 就是插入新关键字的时候, 要先检查一下是否存在同名的关键字, 有的话要把delete字段修改为false, 所以还需要对关键字建立索引, 这样可以高效查找出是否存在同名关键字</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/f4/5df17eff.jpg" width="30px"><span>新的起点，新的开始^_^</span> 👍（15） 💬（8）<div>我有个问题，最后一种方式使用copy()的浅拷贝+对象替换可以提高效率。但是copy()之后，数据库中更没有发生变化的数据其实newKeywords中指向的还是之前的对象引用啊，不是一个新的对象，那这个结果不久和需求冲突了吗？需求是：任何时刻，系统 A 中的所有数据都必须是同一个版本的。举个例子，比如说我修改了一个newKeywords中value对应的SearchWord对象的某个属性，那么响应的，currentKeywords中肯定也会发生变化，因为SearchWord地址值时一样的，这个就不是刚开始讲的深拷贝得到的是一份完完全全独立的对象，它不是独立的，只有数据库中被更新过的数据是独立的，因为执行了map.remove()和map.put()</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/80/da/9c0c458c.jpg" width="30px"><span>安静</span> 👍（14） 💬（1）<div>老师，就是java分层架构中各层的对象，比如VO，BO，PO之间的互相转换，使用的就是原型模式，而做业务开发每天都要与这些打交道。</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/37/98991aeb.jpg" width="30px"><span>不似旧日</span> 👍（13） 💬（2）<div>既然说在Java中不常用那我就不看了，以后有时间再学。</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（10） 💬（13）<div>让我想到了linux下面fork，其实内核也是拷贝了一份数据。Java里面的copyonwrite是不是也是这种深拷贝原理呢？</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（6） 💬（4）<div>1. 考虑到删除关键词，那么最好数据库使用软删除，这样可以知道哪些关键词是被删除的，那么拿到这些被删除的关键词就可以在clone出来的newKeywords基础上，直接remove掉已经删除的哪些关键词就可以了。反之如果不是使用的软删除，那么就不好使用原型模式，需要获取新版本全量数据，然后和旧版本数据一一比对，看哪些数据是被删除的了。
2. 代码如下，将原来的items deep clone一份，这样就切断了与原来items的联系。
  public class ShoppingCart { 
    &#47;&#47; ...省略其他代码... 
    public List&lt;ShoppingCartItem&gt; getItems() {
      List&lt;ShoppingCartItem&gt; tmpShoppingCartItems = new ArrayList&lt;&gt;();
      tmpShoppingCartItems.addAll(this.items);
      return Collections.unmodifiableList(tmpShoppingCartItems); 
    }
  }</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/97/3762ca10.jpg" width="30px"><span>小情绪</span> 👍（5） 💬（0）<div>copy-on-write</div>2020-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（5） 💬（2）<div>看了几遍才明白第一次的浅拷贝问题在哪，在遍历的时候就已经替换了其中一些旧对象；而最后浅拷贝和深拷贝结合的方式，是先把浅拷贝得到的索引（引用）删除，然后再添加新的对象到浅拷贝中，最后在遍历结束后一并替换原型。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（4） 💬（3）<div>我在实际工作中就用到了类似的代码，这就是一个关键词识别模块，第一次在学习专栏中看到如此契合生产的代码，很赞👍

问题1: 数据库中新增一个字段标识逻辑删除
问题2:深拷贝出去，不过为啥我外部需要一个深拷贝的对象呢，还没理解</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4a/34/1faac99b.jpg" width="30px"><span>夕林语</span> 👍（3） 💬（3）<div>数据库中加载 10 万条数据并构建散列表索引，操作非常耗时，比较推荐使用浅拷贝，否则，没有充分的理由，不要为了一点点的性能提升而使用浅拷贝。这里表述有问题吧，最后应该是深拷贝吧。两个浅拷贝比较怎么都别扭</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/74/a9/5eb3ebc6.jpg" width="30px"><span>唐龙</span> 👍（3） 💬（0）<div>之前听说，可能你在不经意间已经用过一些设计模式了，今天终于有这种感觉了，确实对原型模式有过一些简单应用。</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4c/98/2e916c7e.jpg" width="30px"><span>Senble</span> 👍（2） 💬（0）<div>问题1：逻辑删除。系统B在更新数据库时不是真实删除数据，而是修改状态，标记被删除。等到A读取数据库的时候，将此部分数据过滤出来，然后更新内存内容即可。</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/bb/ea/160e4c38.jpg" width="30px"><span>it to learn</span> 👍（2） 💬（0）<div>1个快速克隆散列表的例子，既讲明白原型模式的基本要点，又体会到了需求变化和或实现发现问题后的代码迭代，老师真是用心了，点个赞！</div>2022-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/57/31/6772744d.jpg" width="30px"><span>ちよくん</span> 👍（2） 💬（1）<div>if (searchWord.getLastUpdateTime() &gt; maxNewUpdatedTime) {
        maxNewUpdatedTime = searchWord.getLastUpdateTime();
      }
这段逻辑没看懂起什么作用？和下面的额代码没什么链接</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/ae/66ae403d.jpg" width="30px"><span>熊猫</span> 👍（1） 💬（0）<div>浅拷贝和深拷贝的案例，王老师善于从工作中提取，太棒啦</div>2023-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/4d/b0228a1a.jpg" width="30px"><span>平风造雨</span> 👍（1） 💬（1）<div>1. 两个Map比较下key找到差集
2. 可以返回深复制的购物车结构，或者干脆分成两个方法，一个返回深复制的结构，一个返回当前结构，区分使用场景。</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（1） 💬（0）<div>1.逻辑删除的话，代码都不用改。物理删除的话，我觉得在删除时联动清除map的缓存可行（单进程，分布式就得引入一个外部存储，告知所有节点删除某个缓存）。


2.根据业务场景，采用cow写时复制。提供只读的列表返回和写时的复制列表的返回两个方法。</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/3a/0dd9ea02.jpg" width="30px"><span>Summer  空城</span> 👍（1） 💬（3）<div>1，删除key对于clone的对象而言，不会影响之前的对象，所以实现应该不需要变化吧
2，return new ArrayList&lt;&gt;(this.items);</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4b/92/03338a22.jpg" width="30px"><span>王圣军</span> 👍（0） 💬（0）<div>老师你好，currentKeywords = newKeywords;将新版本在赋值给老的引用时，如果多线程高并发的情况下会不会有问题呢？</div>2024-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/8c/b261e15a.jpg" width="30px"><span>张滔</span> 👍（0） 💬（0）<div>后面浅拷贝深拷贝的例子中，既然已经从数据库里面查出了更新的对象，为什么不直接覆盖Map中的对象，而要拷贝呢？感觉不合理，像是为了举例子而强行虚构的。请老师解释一下。</div>2023-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d6/01/2448b4a9.jpg" width="30px"><span>py</span> 👍（0） 💬（0）<div>还有一种情况是不想有些操作改变当前类的状态</div>2023-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/b8/e1/a52f5c54.jpg" width="30px"><span>BILL</span> 👍（0） 💬（0）<div>1.可以用对比新旧版本散列表，得出删除对象，然后新版本散列表中删除即可。
2.getItems()方法返回clone对象</div>2023-10-12</li><br/><li><img src="" width="30px"><span>Geek_f73a3e</span> 👍（0） 💬（0）<div>ShoppingCartItem item = items.get(0）.clone();新的修改对原来的数据不产生影响
</div>2023-07-27</li><br/><li><img src="" width="30px"><span>Geek_281c7b</span> 👍（0） 💬（0）<div>请问在示意图中, &quot;算法&quot;和&quot;小争哥&quot;这两个节点为什么会放在同一个bucket中呢? 二者的 hash 值应该不一样.</div>2023-07-11</li><br/>
</ul>