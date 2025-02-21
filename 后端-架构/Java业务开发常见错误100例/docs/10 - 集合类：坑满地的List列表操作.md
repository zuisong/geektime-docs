你好，我是朱晔。今天，我来和你说说List列表操作有哪些坑。

Pascal之父尼克劳斯 · 维尔特（Niklaus Wirth），曾提出一个著名公式“程序=数据结构+算法”。由此可见，数据结构的重要性。常见的数据结构包括List、Set、Map、Queue、Tree、Graph、Stack等，其中List、Set、Map、Queue可以从广义上统称为集合类数据结构。

现代编程语言一般都会提供各种数据结构的实现，供我们开箱即用。Java也是一样，比如提供了集合类的各种实现。Java的集合类包括Map和Collection两大类。Collection包括List、Set和Queue三个小类，其中List列表集合是最重要也是所有业务代码都会用到的。所以，今天我会重点介绍List的内容，而不会集中介绍Map以及Collection中其他小类的坑。

今天，我们就从把数组转换为List集合、对List进行切片操作、List搜索的性能问题等几个方面着手，来聊聊其中最可能遇到的一些坑。

## 使用Arrays.asList把数据转换为List的三个坑

Java 8中Stream流式处理的各种功能，大大减少了集合类各种操作（投影、过滤、转换）的代码量。所以，在业务开发中，我们常常会把原始的数组转换为List类数据结构，来继续展开各种Stream操作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（107） 💬（4）<div>哈哈，好巧，前两年有段时间比较闲，研究ArrayList和LinkedList，也对于所谓的ArrayList查询快，增删慢以及LinkedList查询慢，增删快提出过疑问，也做过类似的实验，然后去年给19年校招生入职培训的时候还专门分享过。要打破常规思维，多问为什么，要多听多看，多实验。
回答下问题：
1、int类型是index，也就是索引，是按照元素位置删除的；Integer是删除某个元素，内部是通过遍历数组然后对比，找到指定的元素，然后删除；两个都需要进行数组拷贝，是通过System.arraycopy进行的
2、以foreach为例说，遍历删除实质是变化为迭代器实现，不管是迭代器里面的remove()还是next()方法,都会checkForComodification();而这个方法是判断modCount和expectedModCount是否相等，这个modCount是这个list集合修改的次数，每一次add或者remove都会增加这个变量，然后迭代器每次去next或者去remove的时候检查checkForComodification();发现expectedModCount(这个迭代器修改的次数)和modCount(这个集合实际修改的次数)不相等，就会抛出ConcurrentModificationException，迭代器里面没有add方法，用迭代器时，可以删除原来集合的元素，但是！一定要用迭代器的remove方法而不是集合自身的remove方法，否则抛异常。</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cb/18/4877c08b.jpg" width="30px"><span>eazonshaw</span> 👍（39） 💬（1）<div>思考题：
1. 不一样。使用 ArrayList 的 remove方法，如果传参是 Integer类型的话，表示的是删除元素，如果传参是int类型的话，表示的是删除相对应索引位置的元素。
同时，做了个小实验，如果是String类型的ArrayList，传参是Integer类型时，remove方法只是返回false，视为元素不存在。
2. 原因：查看源码可以发现，remove方法会发生结构化修改，也就是 modCount 会增加。当循环过程中，比较当前 List 的 modCount 与初始的 modCount 不相等，就会报 ConcurrentModificationException。解决方法：1.使用 ArrayList 的迭代器 iterator，并调用之中的remove方法。查看源码可以发现，内部类的remove方法，会维护一个expectedModCount，使其与 ArrayList 的modCount保持一致。2.如果是java 8，可以使用removeIf方法进行删除操作。

```
int expectedModCount = modCount;
public void remove() {
    ...
    checkForComodification();

    try {
        ...
        expectedModCount = modCount;
    } catch (IndexOutOfBoundsException ex) {
        throw new ConcurrentModificationException();
    }
}
final void checkForComodification() {
    if (modCount != expectedModCount)
        throw new ConcurrentModificationException();
}
```</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（15） 💬（1）<div>思考题2：
便利通常的实现方式for冒号的实现，其实底层还是用Iterator 删除元素，查看class文件大概是这样：

Iterator var2 = list.iterator();
    while(var2.hasNext()) {
      Integer integer = (Integer)var2.next();
      list.remove(integer);
    }

删除元素后会调用next方法，next调用checkForComodification方法：
final void checkForComodification() {
            if (modCount != expectedModCount)
                throw new ConcurrentModificationException();
        }
expectedModCount是初始化时，数组的modCount ，也就是说——初始化的数组长度和调用next方法时数组长度不一样时，就会ConcurrentModificationException，理论上讲，不仅仅remove，甚至是add也一样会报错。

尝试测试，将remove改为add：
while(var2.hasNext()) {
      Integer integer = (Integer)var2.next();
      list.add(integer);
    }
确实会报错。

知道了报错的原因，要修复倒也不难。
首先，摒弃for冒号，使用迭代器（其实迭代器也是for冒号）
既然，迭代器在List长度与迭代器初始化时识别到的List长度不一致就会报错。那就顺着它的意思来处理，每次List长度修改时，重新初始化迭代器。相当于长度重新初始化。

假设数组初始长度时10，形成的结果就是：
Iterator 初始化 expectedModCount = 10；
然后删除某元素，数组长度9，Iterator 长度10，这时候如果调用next就会报错，所以，在这时候，重新初始化Iterator 
Iterator  长度初始化为9，与数组长度一致，就避免了报错。
代码实现如下：
Iterator var2 = list.iterator();
    while(var2.hasNext()) {
      Integer integer = (Integer)var2.next();
      if (integer.equals(2)){
        list.remove(integer);
        var2 = list.iterator();
      }
    }

代码写的比较随意，可能存在纰漏。欢迎指点

</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/aa/32fc0d54.jpg" width="30px"><span>失火的夏天</span> 👍（6） 💬（2）<div>1.remove包装类数字是删除对象，基本类型的int数字是删除下标。
2.好像是modcount和什么东西对不上来着，具体忘记了，看看其他大佬怎么说。解决这玩意就是改用迭代器遍历，调用迭代器的remove方法。

话说到这个linkedlist，真是感觉全面被arraylist压制。那这数据结构还留着干嘛呢？为什么不删掉算了。。。我个人感觉linekdlist只有在头尾加入删除元素的时候有一点点优势了吧。用队列或者双端队列的时候会偶然用到。但是感觉用对应的数组模式实现，效率会更高些，就是要考虑扩容的问题。

老师能帮忙解答一下linkedlist留下没删是因为什么吗？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（5） 💬（1）<div>感触颇深：
Arrays的asList和subList，使用过程中需要谨慎，甚至可以考虑直接不用。
要熟悉数据结构。ArrayList 和 HashMap就是典型对比，ArrayList更适合随机访问，节约内存空间，大多数情况下性能不错。但，因为其本质上是数组，所以，无法实现快速找到想要的值。
LinkedList  没有想象中好用，使用前请考虑清楚。
</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/79/01/e71510dc.jpg" width="30px"><span>hellojd</span> 👍（5） 💬（1）<div>学习到了老师的探索精神，linedlist随机插入性能居然不高，刷新了认知。</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（4） 💬（1）<div>老师这期的课程太让人产生共鸣了。之前生产就出过问题。调用方法，达到了用Arrays.asList返回的集合，然后对集合操作时就出了一场。当时看了asList的源码时才发现JDK居然还有这种坑。subList也确实是一个很容易采坑的地方，subList本质上就是把原List报了层皮返回了。关于ListList，头插的话性能应该是会碾压ArrayList，但是就看有没有这种场景了。
课后练习：
1.根据API可以看出，remove(int index) &#47; remove(Object element)
2.Iterator过程中集合结构不能发生变化，通常是遍历过程中其他线程对集合进行了add&#47;remove。可以用CopyOnWrite集合来避免。
</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/d5/1f5c5ab6.jpg" width="30px"><span>大大大熊myeh</span> 👍（3） 💬（1）<div>巧了，思考题1与我之前遇到的问题一样，List#remove方法竟然没删掉里面的元素，最后才发现原来是重载方法的锅，int是删List中该索引的元素，Integer是删除List中值为该Integer的元素。

当时还写了篇博客记录，恬不知耻的放上来：https:&#47;&#47;planeswalker23.github.io&#47;2018&#47;09&#47;10&#47;List-remove&#47;

本篇收获颇多，特别是关于LinkedList的增删复杂度，之前也没看过LinkedList源码，于是一直以为增删很快。

得到一个结论：任何总结，还是得以源码为基础。所有不看源码的总结都是耍流氓。</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（2） 💬（3）<div>int[] arr = {1, 2, 3};
List list = Arrays.asList(arr);
System.out.println(list + &quot; &quot; + list.size() + &quot; &quot; + list.get(0).getClass());


[1, 2, 3] 3 class java.lang.Integer 为何我本地和老师演示的不一样？？</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（2） 💬（1）<div>第二个问题，使用 for-each 或者 iterator 进行迭代删除 remove 时，容易导致 next() 检测的 modCount 不等于 expectedModCount 从而引发 ConcurrentModificationException。
在单线程下，推荐使用 next() 得到元素，然后直接调用 remove(),注意是无参的 remove; 多线程情况下还是使用并发容器吧😃</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（1） 💬（1）<div>问题二可以用迭代器进行删除。
看源码遍历的remove是代参数的remove方法,会导致ModCount++，但expectedModCount不会改变，next会检查两值是否相等，因此会抛异常。从代码上也可以读出作者的想法，就是通过此种方式来禁止遍历时直接remove。

迭代器删除是用的无参数remove，删除后会执行expectedModCount = modCount，将两值置为相等。</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/67/25/d413adc8.jpg" width="30px"><span>Avalon</span> 👍（1） 💬（1）<div>我有一个疑问，在LinkedList中addFirst方法调用的私有方法linkFirst方法如下：
```
    private void linkFirst(E e) {
        LinkedList.Node&lt;E&gt; f = this.first;
        LinkedList.Node&lt;E&gt; newNode = new LinkedList.Node((LinkedList.Node)null, e, f);
        this.first = newNode;
        if (f == null) {
            this.last = newNode;
        } else {
            f.prev = newNode;
        }

        ++this.size;
        ++this.modCount;
    }
```
这段代码里面仅针对一个位置进行了增加节点的操作，为什么addFirst的性能还是不及ArrayList的add方法呢？
</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/8f/5b224f54.jpg" width="30px"><span>LovePeace</span> 👍（1） 💬（1）<div>大量的业务开发其实没那么大的数据,linkendList在插入小量数据的时候还是比arraylist有优势的
        int loopCount = 100;
        StopWatch stopWatch = new StopWatch();
        stopWatch.start(&quot;linkedListadd&quot;);
        linkedListadd(loopCount);
        stopWatch.stop();
        stopWatch.start(&quot;arrayListadd&quot;);
        arrayListadd(loopCount);
        stopWatch.stop();
        System.out.println(stopWatch.prettyPrint());
    }

    private static void linkedListadd(int loopCount) {
        List&lt;Integer&gt; list = new LinkedList&lt;&gt;();
        for (int i = 0; i &lt; loopCount; i++) {
            list.add(i);
        }
    }

    private static void arrayListadd(int loopCount) {
        List&lt;Integer&gt; list = new ArrayList&lt;&gt;();
        for (int i = 0; i &lt; loopCount; i++) {
            list.add(i);
        }
    }
######################################
StopWatch &#39;&#39;: running time = 93300 ns
---------------------------------------------
ns         %     Task name
---------------------------------------------
000025500  027%  linkedListadd
000067800  073%  arrayListadd</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/12/6c/61a598e9.jpg" width="30px"><span>苏暮沉觞</span> 👍（1） 💬（1）<div>老师，对于ArrayList和LinkedList插入性能测试有点疑问：我们这是测量10W的数据量下的结果，如果数据量达到100W，推论还是成立吗？（想测试100W数据量，但是数据量逐步提高到30W以后，程序就运行很久很久）。判断两种数据类型的速度，能不能简单归纳为判断LinkedList查找下一个节点的时间和（ArrayList数组后移一个数据时间+扩容平均时间）哪个比较短？</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/bb/abb7bfe3.jpg" width="30px"><span>csyangchsh</span> 👍（1） 💬（1）<div>ArrayList分配的内存空间是连续的，对会CPU Cache很友好。LinkedList还要包装成Node，又增加了开销。这个测试使用JMH，根据CPU Cache大小，定义不同的元素个数，可能更严谨一点。</div>2020-03-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（1） 💬（1）<div>1. 刚好是看到案例时我想问的问题，答案知道，但是为什么呢？是规定为了区分？那为什么创建数组时可以自动装箱呢？
2.用迭代器可以，但是为什么其实也不能说出个所以然


我没想到的是linklist的性能问题，sublist也没想到，是不是这种很多返回的都是视图呀</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（1）<div>源码中的注释
@param &lt;T&gt; the class of the objects in the array
List&lt;T&gt; asList(T... a)
是不是因为基本类型是不能作为对象的,所以程序只能将int[]数组类型可以作为对象</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/f4/1bf8568e.jpg" width="30px"><span>学要有所用</span> 👍（0） 💬（2）<div>通常看到技术文章里会提到链表查找容易，增删困难，这是否不正确？</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dd/a1/222b0e4e.jpg" width="30px"><span>自暴自弃</span> 👍（0） 💬（1）<div>java很多人用了这么久的List都用错了！看完这篇文章小伙惊呼这么多年白学了！</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/84/be/0370eae1.jpg" width="30px"><span>秋水</span> 👍（32） 💬（0）<div>真的是迷信了LinkedList</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（11） 💬（0）<div>思考题1：
不一样，
remove 的两实现，
包装类型调用的是 boolean remove(Object o);方法，本质上是寻找集合中是否有该元素，有则删除。
基本类型int 调用的是public E remove(int index)方法，实现是直接删除下标。
另外返回值也有区别，
包装类型remove返回布尔，有该对象则返回true并删除，没有则返回false
基本类型的remove返回泛型对象，有则返回该对象，因为是跟据下标删除，所以不存在没有的情况，除非下标越界
</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（4） 💬（0）<div>Arrays.asList 返回的 List 不支持增删操作。 这个坑一直都知道，只是没去看源码，今天学到了，原来是Arrays的内部类ArrayList没有重写add方法，而是extends AbstractList的add()，后者会抛出UnsupportedOperationException</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（3） 💬（0）<div>1. int会调用 public E remove(int index)方法   Integer会调用public boolean remove(Object o)方法

2.modcount改变导致的异常  改用foreach的方式。</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（2） 💬（0）<div>真的是巧，在隔壁《设计模式》的迭代器模式里，也学了关于List的一些知识，今天的课后习题2，我又重新复习了两个课</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（1） 💬（0）<div>问题一传int是直接删除数组对应下标的元素，返回被删除的元素，传Object时需要遍历查询与Object equal的元素，再进行删除，返回true or false。
问题二不知道原因，可以用迭代器进行删除。

整理：
1、ArrayLists.asList无法将基础类型的数组打散重组，即参入基础类型数组时，会被构建成二维数组（仅一个元素，元素为输入数组）结构，而不是一维数组结构。
2、ArrayLists.asList 或subList实则是对原数据的强引用，会导致原数据无法回收，修改结果也会应用到原数组。可以用截取结果构建新的List，防止出现修改异常。
3、考虑时间与空间的关系，选择合理的数据结构。
4、算法大O时间只是理论上的时间，真实场景下可能还需要做额外的操作才能达到算法的启动条件，比如链表的理论插入时间为O(1)，但查找到前向节点还需要花费O(n)的时间。</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/19/89/20488013.jpg" width="30px"><span>hanazawakana</span> 👍（1） 💬（0）<div>第一个问题，remove int是删除下标元素，删除Integer是删除某个元素
第二个问题，因为迭代器为了防止在遍历时删除插入的操作导致漏遍历到某个元素，所以禁止在遍历时插入和删除元素，解决方法想到的是copy on write。</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/6e/6c5f5734.jpg" width="30px"><span>终结者999号</span> 👍（1） 💬（0）<div>在转成stream的时候，linkedlist是不是要好于ArrayList呢？</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/ea/5bfce6c5.jpg" width="30px"><span>mgs2002</span> 👍（1） 💬（0）<div>第二题可以使用并发容器CopyOnWriteArrayList解决，删除和添加都是在快照上面的，不会影响原有的List</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/14/384258ba.jpg" width="30px"><span>Wiggle Wiggle</span> 👍（1） 💬（0）<div>这么看来 LinkedList 没有什么优势，随机插入败了，随机删除也差不多，只剩尾插了。尾插其实也没有多少优势，最多就是arrayList底层满了以后需要扩容，linkedList 不需要。估算下来，大概只有在插入只是海量尾插、查询只是遍历的情况下才有点优势</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（0） 💬（0）<div>ArrayList和linkedlist的性能差异跟计算机内存访问的局部性原理有关</div>2022-07-16</li><br/>
</ul>