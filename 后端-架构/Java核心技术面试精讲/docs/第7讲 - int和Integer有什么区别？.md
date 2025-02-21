Java虽然号称是面向对象的语言，但是原始数据类型仍然是重要的组成元素，所以在面试中，经常考察原始数据类型和包装类等Java语言特性。

今天我要问你的问题是，int和Integer有什么区别？谈谈Integer的值缓存范围。

## 典型回答

int是我们常说的整形数字，是Java的8个原始数据类型（Primitive Types，boolean、byte 、short、char、int、float、double、long）之一。**Java语言虽然号称一切都是对象，但原始数据类型是例外。**

Integer是int对应的包装类，它有一个int类型的字段存储数据，并且提供了基本操作，比如数学运算、int和字符串之间转换等。在Java 5中，引入了自动装箱和自动拆箱功能（boxing/unboxing），Java可以根据上下文，自动进行转换，极大地简化了相关编程。

关于Integer的值缓存，这涉及Java 5中另一个改进。构建Integer对象的传统方式是直接调用构造器，直接new一个对象。但是根据实践，我们发现大部分数据操作都是集中在有限的、较小的数值范围，因而，在Java 5中新增了静态工厂方法valueOf，在调用它的时候会利用一个缓存机制，带来了明显的性能改进。按照Javadoc，**这个值默认缓存是-128到127之间。**

## 考点分析

今天这个问题涵盖了Java里的两个基础要素：原始数据类型、包装类。谈到这里，就可以非常自然地扩展到自动装箱、自动拆箱机制，进而考察封装类的一些设计和实践。坦白说，理解基本原理和用法已经足够日常工作需求了，但是要落实到具体场景，还是有很多问题需要仔细思考才能确定。

面试官可以结合其他方面，来考察面试者的掌握程度和思考逻辑，比如：

- 我在专栏第1讲中介绍的Java使用的不同阶段：编译阶段、运行时，自动装箱/自动拆箱是发生在什么阶段？
- 我在前面提到使用静态工厂方法valueOf会使用到缓存机制，那么自动装箱的时候，缓存机制起作用吗？
- 为什么我们需要原始数据类型，Java的对象似乎也很高效，应用中具体会产生哪些差异？
- 阅读过Integer源码吗？分析下类或某些方法的设计要点。

似乎有太多内容可以探讨，我们一起来分析一下。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/9f/9259a6b9.jpg" width="30px"><span>Kyle</span> 👍（141） 💬（2）<div>节选自《深入理解JAVA虚拟机》：
在HotSpot虚拟机中，对象在内存中存储的布局可以分为3块区域：对象头（Header）、实例数据（Instance Data）和对齐填充（Padding）。

HotSpot虚拟机的对象头包括两部分信息，第一部分用于存储对象自身的运行时数据，如哈希码（HashCode）、GC分代年龄、锁状态标志、线程持有的锁、偏向线程ID、偏向时间戳等，这部分数据的长度在32位和64位的虚拟机（未开启压缩指针）中分别为32bit和64bit，官方称它为&quot;Mark Word&quot;。

对象头的另外一部分是类型指针，即对象指向它的类元数据的指针，虚拟机通过这个指针来确定这个对象是哪个类的实例。并不是所有的虚拟机实现都必须在对象数据上保留类型指针，换句话说，查找对象的元数据信息并不一定要经过对象本身，这点将在2.3.3节讨论。另外，如果对象是一个Java数组，那在对象头中还必须有一块用于记录数组长度的数据，因为虚拟机可以通过普通Java对象的元数据信息确定Java对象的大小，但是从数组的元数据中却无法确定数组的大小。

接下来的实例数据部分是对象真正存储的有效信息，也是在程序代码中所定义的各种类型的字段内容。无论是从父类继承下来的，还是在子类中定义的，都需要记录起来。

第三部分对齐填充并不是必然存在的，也没有特别的含义，它仅仅起着占位符的作用。由于HotSpot VM的自动内存管理系统要求对象起始地址必须是8字节的整数倍，换句话说，就是对象的大小必须是8字节的整数倍。</div>2018-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/27/e5/2a820ec3.jpg" width="30px"><span>cookie。</span> 👍（195） 💬（13）<div>对象由三部分组成，对象头，对象实例，对齐填充。
其中对象头一般是十六个字节，包括两部分，第一部分有哈希码，锁状态标志，线程持有的锁，偏向线程id，gc分代年龄等。第二部分是类型指针，也就是对象指向它的类元数据指针，可以理解，对象指向它的类。
对象实例就是对象存储的真正有效信息，也是程序中定义各种类型的字段包括父类继承的和子类定义的，这部分的存储顺序会被虚拟机和代码中定义的顺序影响（这里问一下，这个被虚拟机影响是不是就是重排序？？如果是的话，我知道的volatile定义的变量不会被重排序应该就是这里不会受虚拟机影响吧？？）。
第三部分对齐填充只是一个类似占位符的作用，因为内存的使用都会被填充为八字节的倍数。

还是个初学者。以上是我了解，不知道有没有错，希望老师能告知。</div>2018-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（41） 💬（3）<div>1. Mark Word:标记位 4字节，类似轻量级锁标记位，偏向锁标记位等。
2. Class对象指针:4字节，指向对象对应class对象的内存地址。
3. 对象实际数据:对象所有成员变量。
4. 对齐:对齐填充字节，按照8个字节填充。

Integer占用内存大小，4+4+4+4=16字节。</div>2018-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/6c/874ca8ad.jpg" width="30px"><span>George</span> 👍（18） 💬（1）<div>计算对象大小可通过dump内存之后用memory analyze分析</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/98/d152b8c5.jpg" width="30px"><span>Gerald</span> 👍（15） 💬（5）<div>为什么我感觉都这么难啊😭</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（8） 💬（1）<div>杨老师，问个问题，如果使用原始类型int定义一个变量在-128和127之间，如int c = 64;会放入Integer 常量缓存吗(IntegerCache)？编译器是怎么操作的？</div>2018-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/31/dc/b7dbd926.jpg" width="30px"><span>云泥</span> 👍（5） 💬（2）<div>缓存的原理是怎样的？感觉这部分还没理解</div>2019-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/31/62/6f1bb71e.jpg" width="30px"><span>云飞</span> 👍（3） 💬（1）<div>想知道Integer 不就是4字节嘛？为什么要从对象角度考虑就变成了4+4+4+4＝16字节？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/60/309a4a6a.jpg" width="30px"><span>小浪</span> 👍（2） 💬（1）<div>那么请问杨老师，什么时候用基本类型，什么时候用包装类？</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/e6/a330d8b0.jpg" width="30px"><span>Darren</span> 👍（2） 💬（1）<div>老师，原始数据类型的包装类是对象吗？</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/5d/3519ec93.jpg" width="30px"><span>ZC叶😝</span> 👍（1） 💬（2）<div>想问下 自动装箱和自动拆箱是指类型转换吗？</div>2018-05-22</li><br/><li><img src="" width="30px"><span>Geek_6krw94</span> 👍（0） 💬（1）<div>想知道Integer 不就是4字节嘛？为什么要从对象角度考虑就变成了4+4+4+4＝16字节？

其实这个解读没太懂</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/e6/a330d8b0.jpg" width="30px"><span>Darren</span> 👍（0） 💬（1）<div>老师，反编译输出怎么理解的，看不懂语法</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/9e/380a01ea.jpg" width="30px"><span>tracer</span> 👍（0） 💬（1）<div>integer获取环境变量数值的方法，这个具体是指哪个方法？</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/8e/2b7d374f.jpg" width="30px"><span>梁作斌</span> 👍（0） 💬（1）<div>不是原子操作的基本类型是 float 、double？为啥不是 long、double？</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/bb/c0ed9d76.jpg" width="30px"><span>kursk.ye</span> 👍（432） 💬（20）<div>这篇文章写得比较零散，整体思路没有串起来，其实我觉得可以从这么一条线索理解这个问题。原始数据类型和 Java 泛型并不能配合使用，也就是Primitive Types 和Generic 不能混用，于是JAVA就设计了这个auto-boxing&#47;unboxing机制，实际上就是primitive value 与 object之间的隐式转换机制，否则要是没有这个机制，开发者就必须每次手动显示转换，那多麻烦是不是？但是primitive value 与 object各自有各自的优势，primitive value在内存中存的是值，所以找到primitive value的内存位置，就可以获得值；不像object存的是reference，找到object的内存位置，还要根据reference找下一个内存空间，要产生更多的IO，所以计算性能比primitive value差，但是object具备generic的能力，更抽象，解决业务问题编程效率高。于是JAVA设计者的初衷估计是这样的：如果开发者要做计算，就应该使用primitive value如果开发者要处理业务问题，就应该使用object，采用Generic机制；反正JAVA有auto-boxing&#47;unboxing机制，对开发者来讲也不需要注意什么。然后为了弥补object计算能力的不足，还设计了static valueOf()方法提供缓存机制，算是一个弥补。</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（164） 💬（3）<div>1 int和Integer

JDK1.5引入了自动装箱与自动拆箱功能，Java可根据上下文，实现int&#47;Integer,double&#47;Double,boolean&#47;Boolean等基本类型与相应对象之间的自动转换，为开发过程带来极大便利。

最常用的是通过new方法构建Integer对象。但是，基于大部分数据操作都是集中在有限的、较小的数值范围，在JDK1.5 中新增了静态工厂方法 valueOf，其背后实现是将int值为-128 到 127 之间的Integer对象进行缓存，在调用时候直接从缓存中获取，进而提升构建对象的性能，也就是说使用该方法后，如果两个对象的int值相同且落在缓存值范围内，那么这个两个对象就是同一个对象；当值较小且频繁使用时，推荐优先使用整型池方法（时间与空间性能俱佳）。

2 注意事项

[1] 基本类型均具有取值范围，在大数*大数的时候，有可能会出现越界的情况。
[2] 基本类型转换时，使用声明的方式。例：long result= 1234567890 * 24 * 365；结果值一定不会是你所期望的那个值，因为1234567890 * 24已经超过了int的范围，如果修改为：long result= 1234567890L * 24 * 365；就正常了。
[3] 慎用基本类型处理货币存储。如采用double常会带来差距，常采用BigDecimal、整型（如果要精确表示分，可将值扩大100倍转化为整型）解决该问题。
[4] 优先使用基本类型。原则上，建议避免无意中的装箱、拆箱行为，尤其是在性能敏感的场合，
[5] 	如果有线程安全的计算需要，建议考虑使用类型AtomicInteger、AtomicLong 这样的线程安全类。部分比较宽的基本数据类型，比如 float、double，甚至不能保证更新操作的原子性，可能出现程序读取到只更新了一半数据位的数值。</div>2018-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/8c/c86340ca.jpg" width="30px"><span>巴西</span> 👍（23） 💬（2）<div>其实除了存储空间的区别外，基本数据类型是有默认值的，而对象数据类型没有默认值。比如从数据库中查询用户年龄，如果用户并没有设置年龄信息，数据库中代表年龄的列age =null ，那么在使用基本数据类型接收年龄值的时候就无法区分用户是年龄为0还是未设置年龄的情况。

所以决定使用int还是integer的时候除了考虑性能因素，还要考虑业务场景。</div>2018-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/6c/874ca8ad.jpg" width="30px"><span>George</span> 👍（13） 💬（0）<div>java内存结构
对象头：
markword：用于存储对象自身的运行时数据，如哈希码、GC分代年龄、锁状态标志、线程持有的锁等。这部分数据长度在32位机器和64位机器虚拟机中分别为4字节和8字节；
lass指针：即对象指向它的类元数据的指针，虚拟机通过这个指针来确定这个对象属于哪个类的实例；
length：如果是java数组，对象头必须有一块用于记录数组长度的数据，用4个字节来int来记录数组长度；
实例数据
实例数据是对象真正存储的有效信息，也是程序代码中定义的各种类型的字段内容。无论是从父类继承下来还是在子类中定义的数据，都需要记录下来
堆积填充
对于hotspot迅疾的自动内存管理系统要求对象的起始地址必须为8字节的整数倍，这就要求当部位8字节的整数倍时，就需要填充数据对其填充。原因是访问未对齐的内存，处理器需要做两次内存访问，而对齐的内存访问仅需一次访问</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/08/855abb02.jpg" width="30px"><span>Seven.Lin澤耿</span> 👍（12） 💬（0）<div>你知道对象的内存结构是什么样的吗？比如，对象头的结构。如何计算或者获取某个 Java 对象的大小?
Java对象内存结构：
- 基本数据类型
- 对象类型
    - 对象头（Header）
        - MarkWord，4字节
        - Class对象指针，4字节
    - 实例数据（Instance Data）
    - 对齐数据（Padding）, 按8个字节对齐
- 数组类型
    -对象头（Header）
        - MarkWord，4字节
        - Class对象指针，4字节
    - 数组长度，4字节
    - 实例数据（Instance Data）
    - 对齐数据（Padding）, 按8个字节对齐
如何获取对象大小：
- Instrumentation + premain实现工具类：Instrumentation.getObjectSize()来获取
- Unsafe，Unsafe.objectFieldOffset()来获取
</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/11/68/ac0d2b05.jpg" width="30px"><span>柯伟</span> 👍（6） 💬（0）<div>int和Integer有什么区别？
	1. int：是Java的8个原始数据类型之一（boolean，byte，char，short，int，long，float，double）
	2. Integer：是int对应的包装类，是引用类型。在Java5中，引入了自动装箱和自动拆箱功能，Java可以根据上下文，自动进行转化，极大的简化了相关编程。自动装箱&#47;自动拆箱发生在编译期，自己调用valueOf和intValue方法来使用缓存机制（默认缓存是-128到127之间）。注意：new 不使用缓存
	3. int访问是直接访问数据内存地址，Integer是通过引用找到数据内存地址
	4. 内存空间占用：Integer大于int
	5. 数据操作效率上：int大于Integer
	6. 线程安全方面：int等原始数据类型需要使用并发相关手段。Integer等包装类可以使用类似AtomicInteger、AtomicLong等这样的线程安全类。
	7. int等原始数据类型和Java泛型不能配合使用
	8. Integer和String一样有final修饰，是不可变类型
	9. Integer中定义了bytes常量，避免了因为环境 64位或32位不同造成的影响
	实践中，建议避免无意中的装箱、拆箱行为

对象的内存结构是什么样的？
在HotSpot虚拟机中，对象在内存中存储的布局都可以分为3块区域。
	1. 对象头（Header）
		包含两部分信息：
		1. Mark Word：用于存储对象自身的运行时数据，如：哈希码（HashCode），GC分代年龄，锁状态标志，线程持有的锁，偏向线程ID，偏向时间戳等，
		2. 类型指针：即对象指向它的类元数据的指针，虚拟机通过这个指针来确定这个对象是哪个类的实例。
		另外，如果对象是Java数组，那在对象头中还必须有一块用国语记录数组长度的数据。
	2. 实例数据（Instance Data）：对象真正存储的有效信息，也是在程序代码中所定义的各种类型的字段内容。
	3. 对齐填充（Padding）：对齐填充并不是必然存在的，也没有特别的含义，它仅仅起着占位符的作用。使对象的大小必须是8字节的整数倍。</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（6） 💬（0）<div>JAVA的内存结构分为3部分：
1，对象头 有两部分,markWord和Class对象指针，
markwork包括存储对象自身的运行时数据， 如哈希码（HashCode）、GC分代年龄、锁状态标志、线程持有的锁、偏向线程ID、偏向时间戳，
2，实例数据 
3，对齐填充

获取一个JAVA对象的大小，可以将一个对象进行序列化为二进制的Byte，便可以查看大小，
Integer value = 10;

ByteArrayOutputStream bos = new ByteArrayOutputStream();
ObjectOutputStream oos = new ObjectOutputStream(bos);
oos.writeObject(value);
&#47;&#47; &#47;&#47; 读出当前对象的二进制流信息
System.out.println(bos.size());</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/28/de/54667f13.jpg" width="30px"><span>jutsu</span> 👍（6） 💬（1）<div>老师的讲解让我想起了科比主导的 细节栏目</div>2018-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（5） 💬（0）<div>本来是打算刷完这个专栏去面试拿 Offer 的，看了前七讲之后，我在考虑要不要从头学一遍 Java，也许我需要的是《零基础学 Java》。

其实也没有太困难的地方，一遍看不懂，多看几次就好了。其中有不少面试题，我估计在日常编码中其实也用不到，当然这些偏底层的知识，知道了总还是有帮助的。

这一篇应该是把 int&#47;Integer、double&#47;Double、boolean&#47;Boolean ……这些基本类型和相应对象之间的关系都讲到了，其实我以前也困惑来着。

课后思考问到了 Java 的内存结构（对象头、对象实例和对齐填充），有点好奇，为什么要问这个，是为后续的文章预热么？

看到现在发现，其实这个专栏的价值不光是作者的输出，也包括精选留言中的内容，甚至是留言中对于专栏的批评。</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a5/1f/d2f6a1f7.jpg" width="30px"><span>文</span> 👍（4） 💬（1）<div>老师能不能把jvm底层和基本使用拆开，一会儿说基本使用的时候太快东西讲得很少，突然间就转jvm里面，让对于jvm方面比较基础弱的同学看着会很痛苦，拆开便于理解和分情况浏览学习</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/fb/f6af3252.jpg" width="30px"><span>倚楼听风雨</span> 👍（3） 💬（4）<div>valueOf和parseInt有什么区别？</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/ae/430eb49b.jpg" width="30px"><span>麦田</span> 👍（3） 💬（1）<div>周末了是不是没人看文章了</div>2018-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/16/afff9a38.jpg" width="30px"><span>好孩子</span> 👍（2） 💬（0）<div>之前看一遍，不太理解再说什么。看完源码之后再回过头来看，又觉得讲的太浅显了，不如直接看代码好理解。建议看了不理解的同学，配合源码一起看，效率最高。</div>2020-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（2） 💬（0）<div>原来数组中如果保存的是引用地址，并不能发挥“局部性”优势，提升性能</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/62/954065d4.jpg" width="30px"><span>步＊亮</span> 👍（2） 💬（1）<div>缓存用得很巧秒，值得借鉴</div>2018-05-19</li><br/>
</ul>