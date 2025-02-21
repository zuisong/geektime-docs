上一节课，我们通过Google Guava这样一个优秀的开源类库，讲解了如何在业务开发中，发现跟业务无关、可以复用的通用功能模块，并将它们从业务代码中抽离出来，设计开发成独立的类库、框架或功能组件。

今天，我们再来学习一下，Google Guava中用到的几种经典设计模式：Builder模式、Wrapper模式，以及之前没讲过的Immutable模式。

话不多说，让我们正式开始今天的学习吧！

## Builder模式在Guava中的应用

在项目开发中，我们经常用到缓存。它可以非常有效地提高访问速度。

常用的缓存系统有Redis、Memcache等。但是，如果要缓存的数据比较少，我们完全没必要在项目中独立部署一套缓存系统。毕竟系统都有一定出错的概率，项目中包含的系统越多，那组合起来，项目整体出错的概率就会升高，可用性就会降低。同时，多引入一个系统就要多维护一个系统，项目维护的成本就会变高。

取而代之，我们可以在系统内部构建一个内存缓存，跟系统集成在一起开发、部署。那如何构建内存缓存呢？我们可以基于JDK提供的类，比如HashMap，从零开始开发内存缓存。不过，从零开发一个内存缓存，涉及的工作就会比较多，比如缓存淘汰策略等。为了简化开发，我们就可以使用Google Guava提供的现成的缓存工具类com.google.common.cache.\*。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（63） 💬（5）<div>JDK是浅拷贝，Guava使用的是深拷贝。一个复制引用，一个复制值。</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/a5/625c0a2e.jpg" width="30px"><span>hhhh</span> 👍（22） 💬（2）<div>猜测jdk中的不变集合保存了原始集合的引用，而guava应该是复制了原始集合的值。</div>2020-05-11</li><br/><li><img src="" width="30px"><span>不能忍的地精</span> 👍（11） 💬（0）<div>Guava里面的引用已经是一个新的集合,Jdk里面的引用还是原来的集合</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/71/0b949a4c.jpg" width="30px"><span>何用</span> 👍（11） 💬（2）<div>我是个特别能关注到细节的人。Memcached 是个开源库，不知道为何好多人都喜欢把它叫做 Memcache，本文也不例外。</div>2020-05-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/TEzJ59GslVXQeZqwFgGhABF7K8bFFlud2pcsEPvEyruP7NGQTuh38IbiajdVYUSViaDJrIkJVnv3vdjPA9YENp5w/132" width="30px"><span>leezer</span> 👍（7） 💬（0）<div>我觉得我更赞同wrapper类的理解，因为装饰器的主要功能是在原始的类上做功能增强，而代理模式更多关注对非业务功能的关注。通过组合的方式我们能实现更多的Wrapper模式。这时候就不只是算装饰器的设计模式了
。</div>2020-05-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（6） 💬（0）<div>老师给这个深拷贝和浅拷贝不是太形象。String 本身就是不可变的。
从这个例子可以看出的是guava 重新创建了list，jdk 是持有的原list的引用。那么guava 有没有进一步的深copy呢？答案是：没有。里面的对象存储的还是引用
也或许老师说的深copy和浅copy只是指collection的引用。</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（5） 💬（0）<div>在JDK中只是将list的地址赋给了UnmodifiableList
final List&lt;? extends E&gt; list;
UnmodifiableList(List&lt;? extends E&gt; list) {
 super(list);
 this.list = list;
}
在Guava中不可变集合是“保护性”拷贝，创建的不可变集合可以理解为常量。
要创建真正的不可变集合，集合中的对象还要是真正的不可变。
下面我举个反例，各位看看：
public static void main(String[] args) {
    List&lt;Student&gt; ori = new ArrayList&lt;&gt;();
    ori.add(new Student(&quot;xiaoqiang&quot;, 10));

    Student mutable = new Student(&quot;wangz&quot;, 8);
    ori.add(mutable);

    ori.add(new Student(&quot;lameda&quot;, 12));
    List&lt;Student&gt; jdkCopy = Collections.unmodifiableList(ori);

    List&lt;Student&gt; guavaCopy = ImmutableList.copyOf(ori);

    ori.add(new Student(&quot;wawa&quot;, 20));

    System.out.println(jdkCopy);
    System.out.println(guavaCopy);

    mutable.name = &quot;mutable&quot;;
    System.out.println(guavaCopy);
&#47;&#47;    [Student{age=10, name=&#39;xiaoqiang&#39;}, Student{age=8, name=&#39;mutable&#39;}, Student{age=12, name=&#39;lameda&#39;}]

  }</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（4） 💬（0）<div>JDK中的unmodifiableList的构造函数是对原始集合的浅拷贝，而Guava.ImmutableList.copyOf是对原始集合的深拷贝。从source code可以看出来：
UnmodifiableList
      UnmodifiableList(List&lt;? extends E&gt; list) {
            super(list);
            this.list = list;
        }
Guava.ImmutableList.copyOf
public static &lt;E&gt; ImmutableList&lt;E&gt; copyOf(Collection&lt;? extends E&gt; elements) {
    if (elements instanceof ImmutableCollection) {
      @SuppressWarnings(&quot;unchecked&quot;) &#47;&#47; all supported methods are covariant
      ImmutableList&lt;E&gt; list = ((ImmutableCollection&lt;E&gt;) elements).asList();
      return list.isPartialView() ? ImmutableList.&lt;E&gt;asImmutableList(list.toArray()) : list;
    }
    return construct(elements.toArray());
  }
  &#47;** Views the array as an immutable list. Checks for nulls; does not copy. *&#47;
  private static &lt;E&gt; ImmutableList&lt;E&gt; construct(Object... elements) {
    return asImmutableList(checkElementsNotNull(elements));
  }

  &#47;**
   * Views the array as an immutable list. Does not check for nulls; does not copy.
   *
   * &lt;p&gt;The array must be internally created.
   *&#47;
  static &lt;E&gt; ImmutableList&lt;E&gt; asImmutableList(Object[] elements) {
    return asImmutableList(elements, elements.length);
  }

  &#47;**
   * Views the array as an immutable list. Copies if the specified range does not cover the complete
   * array. Does not check for nulls.
   *&#47;
  static &lt;E&gt; ImmutableList&lt;E&gt; asImmutableList(Object[] elements, int length) {
    switch (length) {
      case 0:
        return of();
      case 1:
        return of((E) elements[0]);
      default:
        if (length &lt; elements.length) {
          elements = Arrays.copyOf(elements, length);
        }
        return new RegularImmutableList&lt;E&gt;(elements);
    }
  }</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（4） 💬（0）<div>jdk是浅拷贝，guava是深拷贝，在修改的时候报错</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/02/828938c9.jpg" width="30px"><span>Frank</span> 👍（2） 💬（0）<div>unmodifiableList 内部还是使用了Warpper模式，重新实现了某些方法，比如add,remove等，当调用这些方法时，抛出异常，而有些方法还是委托给原始list进行操作，比如get操作。所以这里在原始类添加元素后，使用不jdk的变类可以打印出新添加的元素。而Guava 中的ImmutableList 时采用拷贝的方式将原始集合中的数据拷贝到一个对象数组中，后续原始集合添加，删除元素，其结果都不会影响该ImmutableList。</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（2） 💬（1）<div>我觉得 ForwardingCollection 类就应该理解为缺省的装饰器类，前面的文章就说过代理模式、装饰器模式、适配器模式代码的写法几乎一样，差别就是各自的使用场景，我觉得ForwardingCollection这些类的使用场景就是作为装饰类来用的，不会应用到代理和适配器的场景，王老师貌似又掉入了以代码写法判断设计模式的自己说的陷阱中。</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b5/93/cf0fc8af.jpg" width="30px"><span>八年老萌新</span> 👍（1） 💬（0）<div>jdk的UnmodifiableCollection看起来更像是个装饰器，内部持有源集合的引用，对源集合的操作进行包装。所以直接操作源集合的同时也改变了不可变集合。而guava的ImmutableList则是通过Arrays.copyOf去创建新的不可变集合，所以改变源集合并不能改变不可变集合</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/d5/2fec2911.jpg" width="30px"><span>yu</span> 👍（1） 💬（0）<div>JDK与Guava的不可变集合都是属于普通不可变集合，试了一下，无法增减元素，但都是可以对集合中的对像的成员变量修改的。不同的是，原集合改动之后，JDK跟着改变，Guava不跟着变</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5b/a5/7c079c73.jpg" width="30px"><span>董大大</span> 👍（1） 💬（0）<div>深究设计模式，对阅读开源代码大有好处</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/aa/49/51790edb.jpg" width="30px"><span>落尘kira</span> 👍（1） 💬（0）<div>还有一点就是 作者觉得 不可变的例子，我看起来深拷贝和浅拷贝的代码是一摸一样的？深拷贝是对于对象类型的是否要加入 deepCopy（object）方法？</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/aa/49/51790edb.jpg" width="30px"><span>落尘kira</span> 👍（1） 💬（0）<div>JDK的是不允许在方法级别对不可变集合发生变更（抛出异常），其内部维护的是原集合对象，而原集合对象内部本身是浅拷贝；而Guava除了在方法级别限制不可变更外，其内部使用list.toArray（），该方法每次返回的数组对象都不一样</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/41/dbb7d785.jpg" width="30px"><span>xk_</span> 👍（1） 💬（0）<div>java 的设计模式应该出个新版本了。</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/9e/9337ca8e.jpg" width="30px"><span>jaryoung</span> 👍（1） 💬（0）<div>当原始集合增加数据之后，JDK 不变集合的数据随之增加，而 Google Guava 的不变集合的数据并没有增加。为啥要设置成跟jdk不一样？换句话说，我觉得应该是，如果jdk和guava功能都一摸一样，就没有存在的必要了。底层的实现，jdk如下：
final List&lt;? extends E&gt; list，guava是对集合内容的对象进行逐一拷贝。
本来不想查源码，但是不想误导别人，还是把源码看了一下。
</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/d7/b102034a.jpg" width="30px"><span>do it</span> 👍（1） 💬（0）<div>没看过源码，猜测是浅拷贝与深拷贝的区别</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（1） 💬（0）<div>1.两者都是生成一个新的集合对象。
2.前者相当于对原集合采用装饰者模式。通过复合方式限制掉原集合的写操作。实现，封装后的集合，在后续使用中不可变的特性。具有灵活性。
3.后者相当于新建一个不可变集合。通过原集合的元素，生成一个不可变集合。语义更加明确。

4.前者通过按需操作，具备灵活性。但在集合接口加缺省方法时，可能会有bug。毕竟它是以复合实现功能的。后者语义更明确，不具备前者的灵活性。但在集合接口加缺省方法时，一般不会有bug。因为它是操作自身数据结构实现的功能，与原集合无关联。</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/eb/e7127bb8.jpg" width="30px"><span>，</span> 👍（1） 💬（0）<div>课后题:
jdk的不变集合引用了原始的集合类,所以在原始集合类发生改变的时候他也会改变,他的不可变只是客户端不可变;
guava的不变集合,是在重新创建了一个原始集合对象的副本,所以改变原始类并不能改变他的数据</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（1） 💬（0）<div>通过阅读JDK源码, 发现UnmodifiableList内部使用原始List的浅拷贝, 所以当原始list增&#47;删时会影响UnmodifiableList. 额外说一句, UnmodifiableList实现并Override了List接口的add(), remove()等方法, 通过抛出UnsupportedOperationException来抑制add&#47;remove等改变数据源的操作.

Guava包下的ImmutableList.copyOf(Collection&lt;? extends E&gt; elements)内部调用了construct(elements.toArray())方法, 内部维护了源List的数组copy, 属于深拷贝范畴. 执行construct(elements.toArray())后, ImmutableList内部维护数组作为数据源, 与源List完全隔离, 所以源List的add&#47;remove等操作不会影响到ImmutableList.

源码参考:
java.util.collections 1337行开始;(内部类UnmodifiableList)
com.google.common.collect.ImmutableList 238行开始.(copyOf方法)</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/28/3b6546e8.jpg" width="30px"><span>Snway</span> 👍（1） 💬（0）<div>Jdk直接引用原来的集合，guava是拷贝了原来的集合</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/8c/1fec5fa2.jpg" width="30px"><span>一名小学生</span> 👍（1） 💬（0）<div>要多思考背后为什么要用这种设计模式，才能对使用的设计模式有更深刻的理解。打卡！</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（1） 💬（0）<div>思考题：我猜是深拷贝和浅拷贝的区别</div>2020-05-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epuTGFr2DKichlh7yU6ClmNjiadiaCCT1PqNXwoa8kgPK5mMIn7jbbsjmgGpjQZ9g2DMWYoRVC6Aa74A/132" width="30px"><span>Snow</span> 👍（0） 💬（0）<div>使用不可变集合的场景下为什么不用数组呢？没想通</div>2024-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/02/65/ddb6460e.jpg" width="30px"><span>柯里</span> 👍（0） 💬（0）<div>JDK中是将集合对象赋值给了UnmodifiableList的一个属性list，然后重写collection的变更方法，直接抛出异常，实际上读取的数据使用的仍然是原来的list，所有直接修改原始list，UnmodifiableList中的内容也是会改变的；而Guava中是将list的所有元素读取出来，做为一个新的数组赋值给ImmutableList的相关属性，已经和原来的list没有关系了，当然如果是复杂对象的话，修改对象的属性本身还是有影响的</div>2023-11-28</li><br/><li><img src="" width="30px"><span>Geek_7e0e83</span> 👍（0） 💬（0）<div>猜测：
1. 直接深度拷贝一份集合，这样就彻底隔离了两个集合的内存对象
2.维护一些状态变量 标记原始集合在生成不变对象时的边界。然后重写对应的迭代方法。

看了源码 是方案1</div>2022-11-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/fcftgBsticCicEEkuzB0GTkHIocX62YVTSvnhR1c94sccj42lVaYXrmcZyhzUI3l9NcvuN1rXLhXt2eBrZZ0Tw7A/132" width="30px"><span>idiot</span> 👍（0） 💬（1）<div>“我们可以在系统内部构建一个内存缓存，跟系统集成在一起开发、部署”，但是这样的话，这个系统&#47;模块就不是无状态的了，不利于扩缩容吧。</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/f2/3865fe28.jpg" width="30px"><span>李金鹏</span> 👍（0） 💬（0）<div>jdk的不变集合是从原始拿最新的快照，当原始类改变时，就会更新快照。而guava始终只拿一次快照，那就是在构建不变集合的时候，将原始类的快照信息初始化到不变集合中。之后原始类添加或删除元素，guava的不变集合就不再改变元素的个数。</div>2021-08-30</li><br/>
</ul>