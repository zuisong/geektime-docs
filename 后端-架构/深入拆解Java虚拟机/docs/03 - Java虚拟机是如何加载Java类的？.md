听我的意大利同事说，他们那边有个习俗，就是父亲要帮儿子盖栋房子。

这事要放在以前还挺简单，亲朋好友搭把手，盖个小砖房就可以住人了。现在呢，整个过程要耗费好久的时间。首先你要请建筑师出个方案，然后去市政部门报备、验证，通过后才可以开始盖房子。盖好房子还要装修，之后才能住人。

盖房子这个事，和Java虚拟机中的类加载还是挺像的。从class文件到内存中的类，按先后顺序需要经过加载、链接以及初始化三大步骤。其中，链接过程中同样需要验证；而内存中的类没有经过初始化，同样不能使用。那么，是否所有的Java类都需要经过这几步呢？

我们知道Java语言的类型可以分为两大类：基本类型（primitive types）和引用类型（reference types）。在上一篇中，我已经详细介绍过了Java的基本类型，它们是由Java虚拟机预先定义好的。

至于另一大类引用类型，Java将其细分为四种：类、接口、数组类和泛型参数。由于泛型参数会在编译过程中被擦除（我会在专栏的第二部分详细介绍），因此Java虚拟机实际上只有前三种。在类、接口和数组类中，数组类是由Java虚拟机直接生成的，其他两种则有对应的字节流。

说到字节流，最常见的形式要属由Java编译器生成的class文件。除此之外，我们也可以在程序内部直接生成，或者从网络中获取（例如网页中内嵌的小程序Java applet）字节流。这些不同形式的字节流，都会被加载到Java虚拟机中，成为类或接口。为了叙述方便，下面我就用“类”来统称它们。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/dd/60/a6a4f79a.jpg" width="30px"><span>笨鸟</span> 👍（114） 💬（5）<div>1.虚拟机必须知道（加载）有这个类，才能创建这个类的数组（容器），但是这个类并没有被使用到（没有达到初始化的条件），所以不会初始化。
2.新建数组的时候并不是要使用这个类（只是定义了放这个类的容器），所以不会被链接，调用getInstance(false)的时候约等于告诉虚拟机，我要使用这个类了，你把这个类造好（链接），然后把static修饰的字符赋予变量（初始化）。
老师看看理解对不对，指点一下。</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/db/c4edf697.jpg" width="30px"><span>曲东方</span> 👍（95） 💬（4）<div>1. 新建数组会加载元素类LazyHolder；不会初始化元素类

2. 新建数组不会链接元素类LazyHolder；在getInstance(false)时才真正链接和初始化
-----------------
链接的第一步：验证字节码，awk把字节码改为不符合jvm规范
初始化调用&lt;clinit&gt;(即class init)



PS:好像二个问题包含了第一个问题的答案</div>2018-07-25</li><br/><li><img src="" width="30px"><span>mover</span> 👍（46） 💬（2）<div>到目前为止，讲解的内容没有超出周志明老师的 深入理解JAVA虚拟机这本书的内容，老师可以讲解的更深入一点吗？可以介绍一下类加载后在meta区的大概布局吗？class类对象与meta区的类数据结构是什么关系？当我们创建类，使用类时，类实例，类对象，meta区类数据结构是如何交互的？</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/51/6eef2ad1.jpg" width="30px"><span>韩恩同</span> 👍（30） 💬（3）<div>忍着瞌睡把内容看完了。
全是复习了一遍。
作者对 类加载中的 链接(验证、准备、解析)讲解不太到位吧？
另外，对一个的初始化发生在第一次主动使用该类时，作者列出的几种情况都属于主动使用类。感觉应该有被动使用的举例，并告知大家这样做是不会执行初始化的。</div>2018-07-27</li><br/><li><img src="" width="30px"><span>conce2018</span> 👍（28） 💬（7）<div>为什么叫双亲委派呀，明明只给了父类加载应该是单亲呀</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/0e/de697f9b.jpg" width="30px"><span>熊猫酒仙</span> 👍（20） 💬（5）<div>有几个疑问，请老师指点迷津。
1.扩展类加载器的父类，是启动类加载器，而后者是C++实现的，java继承C++的类？不大能理解。
2.虚方法的概念在C++中有了解过，java中的虚方法该如何定义呢？以前没接触过java虚方法的概念
3.我以前的理解是，有一个零值(0&#47;null)初始化，针对于类的静态成员变量，如果是final修饰的静态成员变量，也就是常量，是初始化为代码中指定的值比如10。非final修饰的静态成员变量，在clint执行过程中赋值为代码中指定的值，请问老师是这样的吗？</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/f0/06ecce19.jpg" width="30px"><span>Skysper</span> 👍（18） 💬（5）<div>每次new一个类都是一次初始化吧？加载和链接以后生成的是什么样的数据结构？存储在什么地方？
</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/dd/eebeb4ef.jpg" width="30px"><span>Super丶X</span> 👍（13） 💬（2）<div>老师，你说可以通过不同的类加载器加载同一个类得到类的不同版本，我有个疑问，类是通过包名加类名来使用的，那怎么样区分不同的类加载器加载的类呢？</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/22/5a483755.jpg" width="30px"><span>小蛋壳</span> 👍（9） 💬（1）<div>加载阶段都加载哪些类呢，那么多类，全部加载吗？</div>2018-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/0d/14d9364a.jpg" width="30px"><span>L.B.Q.Y</span> 👍（8） 💬（3）<div>从大的方面讲，类加载的结果是把一段字节流变换成Class结构并写方法区，实际写方法区具体是发生在加载、链接、初始化的哪个环节呢？</div>2018-07-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoZqcVJzUjfu5noOW6OPAh6ibrBicibLmicibnVyVLHdf7GwAzf2th5s1oQ9pUbLpmq2mlVBauUZn8QUnw/132" width="30px"><span>funnyx</span> 👍（6） 💬（1）<div>有两个问题想问一下老师，在类加载的过程中，有一个委派模式，这里严格来说应该不是使用的继承方式，应该是组合。另一个就是类中的静态字段，如果没有被jvm标记为常量，那么这部分内存是如何分配的？</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/74/7e787607.jpg" width="30px"><span>scutware</span> 👍（5） 💬（2）<div>您在评论回复说.class在加载后已经写入方法区（元空间），但是我理解在方法区里类代码的方法调用应该是实际的调用地址吧？而取得实际调用地址不是在链接阶段吗？这里不太理解，求解答～</div>2018-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6c/28/a1f9f0ad.jpg" width="30px"><span>陈树义</span> 👍（5） 💬（2）<div>新建数组不会导致初始化，但是否会链接不清楚。不知道有什么方式可以验证？</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/1a/579c941e.jpg" width="30px"><span>志远</span> 👍（4） 💬（1）<div>请问，关于双亲委派类加载器的情况，与周志明的深入理解java虚拟机矛盾啊，到底听哪个呢？周志明书籍中lib&#47;ext是由扩展类加载器加载，你这里是启动类加载器加载，到底哪个是正确的呢？</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/42/39fa3b84.jpg" width="30px"><span>liuyitao</span> 👍（3） 💬（1）<div>clinit执行时的锁，是什么锁，跟synchronized一样吗？</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/ca/1a1e190a.jpg" width="30px"><span>Nu11PointerEx</span> 👍（3） 💬（6）<div>老师，根据《深入理解Java虚拟机》一书的描述，被static final修饰的常量字段的赋值行为应该发生在&quot;准备&quot;阶段，但文中说是在初始化阶段赋值，与我理解的有出入，麻烦老师解答下</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（2） 💬（1）<div>触发类初始化条件的第八条(“当初次调用MethodHandle”实例时)，这里的MethodHandle是什么意思呢？</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/71/c83d8b15.jpg" width="30px"><span>一个坏人</span> 👍（1） 💬（1）<div>老师好，请教一个问题。&quot;在加载阶段就已经生成class结构了，所以我认为应该已经写入了方法区，只是被标记为未链接而暂不能使用。&quot; 如果验证失败怎么办？</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/85/8b221758.jpg" width="30px"><span>郑杰</span> 👍（1） 💬（1）<div>”除此之外的直接赋值操作，以及所有静态代码块中的代码，则会被 Java 编译器置于同一方法中，并把它命名为”   这一句是不是没写完啊，应该加上 cinit方法吧</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/c0/517781b8.jpg" width="30px"><span>左岸🌸开</span> 👍（1） 💬（1）<div>“除此之外的直接赋值操作，以及所有静态代码块中的代码，则会被 Java 编译器置于同一方法中，并把它命名为”。请问一下这里是命名是什么？</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/f6/7c943c5f.jpg" width="30px"><span>以我之姓贯你之名</span> 👍（1） 💬（1）<div>延迟初始化单例那个是因为LazyHolder是静态私有内部类的关系吗 如果我把LazyHolder作为一个public class是不是就不一样了</div>2018-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/5d/1ccee378.jpg" width="30px"><span>茫农</span> 👍（0） 💬（1）<div>叫双亲委派应该是为了遵从男女平等,貌似以前在哪看过</div>2018-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/ba/0a423b3c.jpg" width="30px"><span>北纬30⁰</span> 👍（0） 💬（1）<div>双亲委派模式，因该是指的爸爸辈分和爷爷辈分这两个亲人吧
</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/4a/e8519ff4.jpg" width="30px"><span>darling</span> 👍（0） 💬（1）<div>new LazyHolder[2] 是什么意思啊???没这么用过</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/95/4948f80f.jpg" width="30px"><span>bhfjf</span> 👍（0） 💬（2）<div>老师你好，我有个问题，既然初始化是线程安全的，那为什么我当时学的时候老师要让我们这么写单例模式来保证安全呢？这样再加锁是不是就多余了呀？
public class Single{
     private Single(){}
     private Single single;
     public static Single getInstance(){
          if(single==null){
              synchronized(Single.class){
                   if(single==null){
                      single = new Single();
                   }
              }
          }
          return single;
     }
}</div>2018-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/f2/ca989d6f.jpg" width="30px"><span>Leon Wong</span> 👍（0） 💬（1）<div>老师你好，有个问题特来请教，《深入理解Java虚拟机》一书中提到ConstantValue是在准备阶段赋值（不仅仅是初始化为0值），而您这边说ConstantValue是在类加载的最后一步即初始化阶段中赋值，请问哪一个说法是正确的呢？</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（0） 💬（1）<div>您好，文中提到类初始化是线程安全的，请我虚拟机是如何实现这一点的呢</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/24/1e4883c6.jpg" width="30px"><span>dingwood</span> 👍（0） 💬（1）<div>java -cp &#47;path&#47;to&#47;asmtools.jar org.openjdk.asmtools.jdis.Main Foo.class &gt; Foo.jasm.1，执行这句报错：java.lang.UnsupportedClassVersionError: org&#47;openjdk&#47;asmtools&#47;jdis&#47;Main : Unsupported major.minor version 52.0。。支持什么版本的jdk啊。</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/5d/e50cf9c7.jpg" width="30px"><span>Kenneth</span> 👍（0） 💬（1）<div>老师你好，awk……这些在哪里可以学习呢？指令看不懂怎么办，谢谢！</div>2018-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/a2/cdd182e5.jpg" width="30px"><span>迈克擂</span> 👍（89） 💬（0）<div>学习了！可以的话希望老师能附上一些图解，便于更理解</div>2018-07-29</li><br/>
</ul>