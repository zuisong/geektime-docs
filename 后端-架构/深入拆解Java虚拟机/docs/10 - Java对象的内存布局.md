在Java程序中，我们拥有多种新建对象的方式。除了最为常见的new语句之外，我们还可以通过反射机制、Object.clone方法、反序列化以及Unsafe.allocateInstance方法来新建对象。

其中，Object.clone方法和反序列化通过直接复制已有的数据，来初始化新建对象的实例字段。Unsafe.allocateInstance方法则没有初始化实例字段，而new语句和反射机制，则是通过调用构造器来初始化实例字段。

以new语句为例，它编译而成的字节码将包含用来请求内存的new指令，以及用来调用构造器的invokespecial指令。

```
// Foo foo = new Foo(); 编译而成的字节码
  0 new Foo
  3 dup
  4 invokespecial Foo()
  7 astore_1
```

提到构造器，就不得不提到Java对构造器的诸多约束。首先，如果一个类没有定义任何构造器的话， Java编译器会自动添加一个无参数的构造器。

```
// Foo类构造器会调用其父类Object的构造器
public Foo();
  0 aload_0 [this]
  1 invokespecial java.lang.Object() [8]
  4 return
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/66/75/54bb858e.jpg" width="30px"><span>life is short, enjoy more.</span> 👍（81） 💬（2）<div>对象头

每个对象都有一个对象头，对象头包括两部分，标记信息和类型指针。

标记信息包括哈希值，锁信息，GC信息。类型指针指向这个对象的class。

两个信息分别占用8个字节，所以每个对象的额外内存为16个字节。很消耗内存。

压缩指针

为了减少类型指针的内存占用，将64位指针压缩至32位，进而节约内存。之前64位寻址，寻的是字节。现在32位寻址，寻的是变量。再加上内存对齐(补齐为8的倍数)，可以每次寻变量都以一定的规则寻找，并且一定可以找得到。

内存对齐

内存对齐的另一个好处是，使得CPU缓存行可以更好的实施。保证每个变量都只出现在一条缓存行中，不会出现跨行缓存。提高程序的执行效率。

字段重排序

其实就是更好的执行内存对齐标准，会调整字段在内存中的分布，达到方便寻址和节省空间的目的。

虚共享

当两个线程分别访问一个对象中的不同volatile字段，理论上是不涉及变量共享和同步要求的。但是如果两个volatile字段处于同一个CPU缓存行中，对其中一个volatile字段的写操作，会导致整个缓存行的写回和读取操作，进而影响到了另一个volatile变量，也就是实际上的共享问题。

@Contented注解

该注解就是用来解决虚共享问题的，被该注解标识的变量，会独占一个CPU缓存行。但也因此浪费了大量的内存空间。

</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（8） 💬（3）<div> 在默认情况下，Java 虚拟机中的 32 位压缩指针可以寻址到 2 的 35 次方个字节，也就是 32GB 的地址空间（超过 32GB 则会关闭压缩指针）。


这里为啥是 35 ？？？？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/71/c83d8b15.jpg" width="30px"><span>一个坏人</span> 👍（7） 💬（3）<div>老师好，请教一下：“自动内存管理系统为什么要求对象的大小必须是8字节的整数倍？”，即内存对齐的根本原因在于？</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/20/ae6979bd.jpg" width="30px"><span>大能猫</span> 👍（6） 💬（1）<div>最近研究String时遇到一个跟Java内存相关的问题：常量池里到底有没有存放对象？
常量池主要存放两大类常量：字面量（Literal）和符号引用（Symbolic Reference）；
如果常量池里有一个“hello”的字面量，这个字面量算是一个对象吗？如果不算对象，那么它所指向的对象又存放在哪里呢</div>2018-08-14</li><br/><li><img src="" width="30px"><span>everyok22</span> 👍（4） 💬（1）<div>你文章里说： 64位的JVM中，不采用压缩指针的方式，标记字段与类型指针分别占用8个字节，而采用了压缩指针标记字段与类型指针都会压成32位（8字节）那对象头不是只占用8个字节么，为什么你说是12个字节</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/4d/bd86bdc2.jpg" width="30px"><span>周仕林</span> 👍（3） 💬（1）<div>对象头的组成如果阅读过周志明的JVM虚拟机会发现作者说的有一些有失偏颇，对象头的组成是对象运行信息，类型指针（如果对象访问采用直接指针），数组长度（如果对象是数组）</div>2018-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/cb/7b6802cc.jpg" width="30px"><span>贾智文</span> 👍（2） 💬（1）<div>默认情况下32位可以寻址2的35次，应该是因为地址是32位乘以2的三次（默认对其为8），那么如果不采用压缩指针，能够寻址的范围应该是2的64次对吧。然后之前模糊的地方就是觉得两个寻址范围并不一致，是不是可以这么理解并没有通过压缩指针让两个寻址范围一致，而是通过压缩指针放大了32位的寻址空间使它够用了</div>2018-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/0e/de697f9b.jpg" width="30px"><span>熊猫酒仙</span> 👍（2） 💬（1）<div>接触过C&#47;C++的内存字节对齐，就比较好理解本章内容了。希望老师后面讲讲java内存在并发上的相关机制，譬如搞不懂的内存障是怎么实现的！</div>2018-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/cb/7b6802cc.jpg" width="30px"><span>贾智文</span> 👍（1） 💬（2）<div>有一点想不明白，既然内存对齐是八位而不是举例的两位为什么空间只是从64位变成32而不是从64变成8</div>2018-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/70/f59db672.jpg" width="30px"><span>槑·先生</span> 👍（70） 💬（25）<div>在极客时间买了不少课程了，这个系列算是难读的。</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（64） 💬（2）<div>小结
1:Java中创建对象的方式

1-1:new -通过调用构造器来初始化实例字段

1-2:反射-通过调用构造器来初始化实例字段

1-3:Object.clone-通过直接复制已有的数据，来初始化新建对象的实例字段

1-4:反序列化-通过直接复制已有的数据，来初始化新建对象的实例字段

1-5:Unsafe.allocateInstance-没有初始化对象的实例字段

2:Java对象的空间占用

2-1:通过new创建的对象，涵盖了它所有父类中的对象实例的字段

2-2:对象头，由标记字段和类型指针构成

2-3:标记字段，用于存储Java虚拟机有关该对象的运行数据，比如：哈希码、GC信息、锁信息等

2-4:类型指针，用于指向该对象的类

2-5:此对象的实例字段对应的内存空间

3:压缩指针
JVM的内存空间有限且昂贵，所以，能缩减的就缩减，通过一定的算法改进压缩类型指针的空间后仍可以寻址到对象的实例对应的类，所以，就采用了

4:字段重排
意思是JVM会重新分配字段的位置，和我们Java源码中属性声明的位置存在差异，猜想Java编译器编译后的字节码是没有改变源码中字段声明的位置的，这样做是为了更好的实现内存对齐，内存对齐本质上会浪费一定的内存空间，不过可以减少内存行的读取次数，通过一消一涨的比对发现这样对于JVM的性能有一定的提高，所以，也就使用了这种方式，浪费点空间能提高性能也是值得的

疑问❓
1:为什么一个子类即使无法访问父类的私有实例字段，或者子类实例字段隐藏了父类的同名实例字段，子类的实例还是会为这些父类实例字段分配内存呢？
另外，如果采用指针指向的方式定位父类实例的内容是否能更节省内存空间？

2:五种创建对象的方式，通过new指令新建出来的对象，他的内存其实涵盖了所有父类中的实例字段，其他的方式是怎样的哪？

</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/e0/3d5b28ef.jpg" width="30px"><span>清歌</span> 👍（41） 💬（0）<div>讲内存布局没有图示。如果能配一些图来说明就更清晰了，纯文字不直观</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/ca/2d8c4733.jpg" width="30px"><span>amourling</span> 👍（15） 💬（2）<div>作者大大辛苦了，货很干，搭配《深入理解java虚拟机》会很香</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/16/99a7045d.jpg" width="30px"><span>倔强</span> 👍（6） 💬（1）<div>也就是说默认情况下，小于32G的堆内存中的对象引用为4个字节，一旦堆内存大于32G，对象引用为8个字节</div>2018-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（5） 💬（0）<div>对象头：标记字段（哈希码、GC信息、锁信息等）+类型指针
压缩指针原理：对象间的填充需求（内存对齐）保证一个对象的起始地址需要对齐到8的倍数，而定址时并非逐字节而是逐8字节，从而保证32位就可定位到2 ^ 32 * 8 = 32GB的地址空间
内存对齐目的：对象的访问机制更为简单；避免跨缓存行字段出现
字段重排列目的：JVM重新分配字段先后顺序，在满足内存对齐的条件下尽可能提高内存利用率
虚共享：多线程访问同一对象的不同字段，却因共享缓存行而导致缓存行产生竞争</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/c5/69286d58.jpg" width="30px"><span>樱小路依然</span> 👍（5） 💬（2）<div>老师，问个问题，你在用小车举例的时候说，规定从 4 的倍数停起，那么小车可能会浪费2个车位，大车可能会浪费3个车位，那 XX:ObjectAlignmentInBytes 的默认值是 8，岂不是小车可能会浪费6个车位，大车可能会浪费7个车位？为什么这个 XX:ObjectAlignmentInBytes 的默认值不设置成2，而是设置成8了呢？</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（5） 💬（1）<div>有一个小白问题，new一个对象(继承一个类)会调用父类构造器，这个可以理解，因为对象可能调用父类方法。那么为什么new对象会调用到object呢？这有什么用意吗？</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/66/e8fb8ca2.jpg" width="30px"><span>xlogic</span> 👍（4） 💬（0）<div>字段重排列

其一，如果一个字段占据 C 个字节， 那么该字段的偏移量需要对齐至 NC。这里的偏移量指的是字段地址与对象的起始地址差值

以 long 类为例，它仅有一个 long 类型的实例字段。在使用了压缩指针的 64 位虚拟机中，尽管对象头的大小为 12 个字节，该 long 类型字段的偏移量也只能是 16，而中间空着的 4 个字节便会被浪费掉。

个人理解：1. 应该是 Long 类型；2. 因为 long 字段的占 8 个字节，所以偏移量是 N8，比12大的最接近的数就是 16，所以偏移量就是16，也就是说字段与对象的起始位置差是16。</div>2018-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4e/85/3096d893.jpg" width="30px"><span>hresh</span> 👍（2） 💬（0）<div>关于Java创建对象，自己基于本文做了一些内容上的补充，欢迎大家阅读：https:&#47;&#47;juejin.cn&#47;post&#47;7074578371123871781&#47;</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/93/3470fc43.jpg" width="30px"><span>Mr.钧👻</span> 👍（2） 💬（1）<div>想请教老师大大几个问题：
1、什么是CUP缓存行？
2、如果跨缓存行的字段，为什么会降低执行效率？是因为某些读取程序，一行一行的读效率较高？还是因为以行分割呢？
3、明显启用压缩指针，性能更高，但是为什么还会在64位情况下，不启用压缩指针的情况呢？ 是因为CPU运行速度更快，可以护士不压缩指针导致的内存浪费吗？</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（1） 💬（0）<div>字段内存对齐的可以让字段只出现在同一 CPU 的缓存行中</div>2021-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/91/80/bc38f890.jpg" width="30px"><span>珍妮•玛仕多</span> 👍（1） 💬（0）<div>老师能解释一下这句话吗，他是怎么实现的，为什么?在对压缩指针解引用时，我们需要将其左移 3 位，再加上一个固定偏移量，便可以得到能够寻址 32GB 地址空间的伪 64 位指针了。</div>2021-04-21</li><br/><li><img src="" width="30px"><span>Geek_05df73</span> 👍（1） 💬（0）<div>如果在讲解jvm带上手绘图，效果会好些。</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（1） 💬（0）<div>老师， 对象头中的类型指针只是为了指该对象的类 ， 使用了压缩指针还有32位  。可以有32g的地址空间， 一个类能用到 32 G的地址空间么?????</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/b5/8bc4790b.jpg" width="30px"><span>Geek_987169</span> 👍（1） 💬（0）<div>老师，请教您几个问题
1：每个类都有一个对应的class对象，那么这class对象是什么时候生成的，存储jvm的哪个区域？
2：类实例对象object header中的类型指针其实就是指向该类所属class的对象的指针吗？
3：class对象的内存结构又是什么样子的呢？类似于普通Java实例对象吗？
ps：这个指针压缩的原理有些困扰到我了。。。求解惑！！！</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/8d/377c106a.jpg" width="30px"><span>KW💤</span> 👍（0） 💬（0）<div>24年为了面试重读这章，几年前刚买的时候是一知半解的，今天理得自认为算是很清楚了。评论里很多人觉得难懂其实无可厚非，这个是要累积比较多其他知识才能搞懂的。这篇文章只适合积累比较多了的人看，因为它有两个特点：1、涉及的小点很多（像讲到缓存行，long、double在java中的特殊处理，32位64位操作系统的寻找存储特性...）；2、每个点都讲得不算太具体。不怀疑作者的技术水平，但行文把知识说清楚的能力可能还需要磨练下。当然如果知识点比较全备的人看是挺爽的</div>2024-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/03/c9b43b21.jpg" width="30px"><span>BewhY</span> 👍（0） 💬（0）<div>18年买的，当时看了几章发现是天书，然后自己慢慢去补充相关知识，19年回来再看下，有点云里雾里还是不懂，继续补充，20年再过来刷，终于可以看懂了，但是连在一起还是不懂，21年来看，基本所有名词都知道是干嘛的了，跟同事解释也能装下B了，但是人家多问两下就无法深入答解下去了，现在22年了，还是无法精通jvm</div>2022-09-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqJrZ9ic5vHOVfzqcA3Y454gicI2z7L1Ujp5hzFr9CbfTu6goHE7fUlbl3QjpEvXJj5qlvRAVcGRomw/132" width="30px"><span>zhmacn</span> 👍（0） 💬（0）<div>极客上有很多课程，我感觉郑老师的课质量真的很高</div>2021-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（0） 💬（0）<div>还是这个看懂了一点点，对象头包含标记信息和类型指针，这个指针应该指的对象在堆的一个内存地址吧</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/e6/40c67bcb.jpg" width="30px"><span>shuang</span> 👍（0） 💬（0）<div>压缩指针：老师，这里好像看着有点别扭。对象头中的类型指针也会被压缩成 32 位，使得对象头的大小从 8 字节降至 4 字节。java对象的内存占用大小从 16 字节降至 12 字节，</div>2021-03-05</li><br/>
</ul>