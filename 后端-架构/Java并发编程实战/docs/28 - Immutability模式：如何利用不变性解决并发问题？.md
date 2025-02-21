我们曾经说过，“多个线程同时读写同一共享变量存在并发问题”，这里的必要条件之一是读写，如果只有读，而没有写，是没有并发问题的。

解决并发问题，其实最简单的办法就是让共享变量只有读操作，而没有写操作。这个办法如此重要，以至于被上升到了一种解决并发问题的设计模式：**不变性（Immutability）模式**。所谓**不变性，简单来讲，就是对象一旦被创建之后，状态就不再发生变化**。换句话说，就是变量一旦被赋值，就不允许修改了（没有写操作）；没有修改操作，也就是保持了不变性。

## 快速实现具备不可变性的类

实现一个具备不可变性的类，还是挺简单的。**将一个类所有的属性都设置成final的，并且只允许存在只读方法，那么这个类基本上就具备不可变性了**。更严格的做法是**这个类本身也是final的**，也就是不允许继承。因为子类可以覆盖父类的方法，有可能改变不可变性，所以推荐你在实际工作中，使用这种更严格的做法。

Java SDK里很多类都具备不可变性，只是由于它们的使用太简单，最后反而被忽略了。例如经常用到的String和Long、Integer、Double等基础类型的包装类都具备不可变性，这些对象的线程安全性都是靠不可变性来保证的。如果你仔细翻看这些类的声明、属性和方法，你会发现它们都严格遵守不可变类的三点要求：**类和属性都是final的，所有方法均是只读的**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/87/57236a2d.jpg" width="30px"><span>木卫六</span> 👍（88） 💬（3）<div>这段代码应该是线程安全的，但它不是不可变模式。StringBuffer只是字段引用不可变，值是可以调用StringBuffer的方法改变的，这个需要改成把字段改成String这样的不可变对象来解决。
</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（44） 💬（1）<div>---总结---
1. 不可变类的特点：类、属性都是final的，方法是只读的
2. 为了解决有些不可变类每次创建一个新对象导致内存浪费的问题：享元模式&#47;对象池
3. 注意事项：区别引用不可变和实际内容不可变
4. 更简单的不可变对象：无状态对象</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/71/f0/be872719.jpg" width="30px"><span>炎炎</span> 👍（16） 💬（1）<div>这个专栏一直看到这儿，真的很棒，课后问题也很好，让我对并发编程有了一个整体的了解，之前看书一直看不懂，老师带着梳理一遍，看书也容易多了，非常感谢老师，希望老师再出专栏</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（15） 💬（1）<div>final StringBuffer user;

StingBuffer 是 引用 类型， 当我们说它final StingBuffer user 不可变时，实际上说的是它user指向堆内存的地址不可变， 但堆内存的user对象，通过sub append 方法实际是可变的……</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/2f/2f73fd52.jpg" width="30px"><span>水滴s</span> 👍（10） 💬（2）<div>老师，问下 Bar这个类的foo属性的设值在多线程下为什么会有原子性问题，我理解的只会有可见性问题？</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（5） 💬（1）<div>随着课程的深入，越来越看不懂了。我不嫌丢人，不藏拙，这专栏，我一定会二刷，三刷，直到啃下来这块硬骨头！</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（2） 💬（1）<div>老师五一节日快乐。

思考题 ：
不可变类的三要素 ：类、属性、方法都是不可变的。 思考题这个类虽然是final ，属性也是final并且没有修改的方法 ， 但是 stringbuffer这个属性的内容是可变的 ， 所以应该没有满足三要素中的属性不可变 ， 应该不属于不可变类 。


另外老师我有个问题想问下， 我看jdk一些源码里，也用了对象做锁。 例如 我有个变量 final  ConcurrentHashMap cache , 有些方法中会对 cache变量 put新的值 ， 但是还有用这个对象做 synchronized(cache) 对象锁 ， 这种做法对么？ 如果对的话，是因为管程只判断对象的首地址没有改变的原因么 ，希望老师指点一下😁</div>2019-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/f8/38/904952ac.jpg" width="30px"><span>pg逆袭的小红帽是谁</span> 👍（1） 💬（1）<div>“String 和 Long、Integer、Double 等基础类型的包装类都具备不可变性，这些对象的线程安全性都是靠不可变性来保证的。”
这里有点不太理解，既然String 和 Long、Integer、Double具备不可变，不可变意味着线程安全，那不就可以说String 和 Long、Integer、Double 是线程安全的了？</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/1f/e9fbc712.jpg" width="30px"><span>嗨喽</span> 👍（0） 💬（2）<div>上面得SafeWM类代码会不会有ABA问题呢，老师</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/7b/2d4b38fb.jpg" width="30px"><span>Jialin</span> 👍（117） 💬（5）<div>根据文章内容,一个类具备不可变属性需要满足&quot;类和属性都必须是 final 的,所有方法均是只读的&quot;,类的属性如果是引用型,该属性对应的类也需要满足不可变类的条件,且不能提供修改该属性的方法,
Account类的唯一属性user是final的,提供的方法是可读的,user的类型是StringBuffer,StringBuffer也是final的,这样看来,Account类是不可变性的,但是去看StringBuffer的源码,你会发现StringBuffer类的属性value是可变的&lt;String类中的value定义:private final char value[];StringBuffer类中的value定义:char[] value;&gt;,并且提供了append(Object object)和setCharAt(int index, char ch)修改value.
所以,Account类不具备不可变性</div>2019-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（25） 💬（0）<div>具不具备不可变性看怎么界定边界了，类本身是具备的，StrnigBuffer的引用不可变。但是因为StringBuffer是一个对象，持有非final的char数组，所以底层数组是可变的。但是StringBuffer是并发安全的，因为方法加锁synchronized</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/6e/897bd526.jpg" width="30px"><span>对象正在输入...</span> 👍（8） 💬（1）<div>不可变类的三个要求 : 类和属性都是 final 的，所有方法均是只读的
这里的StringBuffer传进来的只是个引用，调用方可以修改，所以这个类不具备不可变性。

</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bc/6d/f6f0a442.jpg" width="30px"><span>汤小高</span> 👍（6） 💬（3）<div>Immutability模原理弄清楚了，但是对于Immutability模式的应用场景还不是很明白，我的疑惑是既然共享变量是只读的，那就没必要加锁了，各个线程都读就行了，为啥还要用Immutability模式了，因为如果共享变量存在读写情况，就会加锁了，也不会用到Immutability模式，希望老师解惑，谢谢</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1b/2c/6b3c0911.jpg" width="30px"><span>Hour</span> 👍（6） 💬（3）<div>&#47;&#47;Foo 线程安全
final class Foo{
  final int age=0;
  final int name=&quot;abc&quot;;
}
&#47;&#47;Bar 线程不安全
class Bar {
  Foo foo;
  void setFoo(Foo f){
    this.foo=f;
  }
}
老师好，对foo的引用和修改在多线程环境中并不能保证原子性和可见性，这句话怎么理解，能用具体的例子说明一下吗？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/12/f0c145d4.jpg" width="30px"><span>Rayjun</span> 👍（6） 💬（1）<div>不是不可变的，user 逃逸了</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/c8/c2343cb6.jpg" width="30px"><span>DoctorDeng</span> 👍（4） 💬（0）<div>实现不可以变类主要有如下几步：
1. 类增加 final 修饰符，让类无法被继承
2. 类中的所有成员变量必须私有（增加 private 关键字）并增加 final 修饰符，让属性无法被修改（属性内容依然可以被修改，通过 4 解决该问题）
3. 不提供修改成员变量的方法包括 setter
4. 通过构造器初始化所有成员，进行深拷贝(deep copy)
5. 在 getter 方法中，不要直接返回对象本身，而是克隆对象，并返回对象的拷贝</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/dd/c9413f59.jpg" width="30px"><span>铿然</span> 👍（3） 💬（0）<div>关于final的理解
1. 域并不是都需要定义为final才能线程安全，只要是私有的并且只读，也能保证线程安全
2.类被继承，那么实际上是子类不一定安全，和当前这个类无关，如果当前类是安全的，用不用final修饰都是安全的
3.final修饰容器类，对象时，引用不可变，兑现内容可变，也不能保证线程安全。

Java 并发编程实战中对final的描述个人感觉不是那么准确。</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/76/256bbd43.jpg" width="30px"><span>松花皮蛋me</span> 👍（3） 💬（0）<div>Stringbuffer虽然逃出来了，但是没有引用其他对象，另外它本身也是线程安全的，所以具有不可变性</div>2019-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/f2/26/a8ac6b42.jpg" width="30px"><span>听风有信</span> 👍（2） 💬（0）<div>user逃逸了，应该用保护性拷贝</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/9f/f4b06bd5.jpg" width="30px"><span>见南山</span> 👍（2） 💬（0）<div>不可变对象需要保证类中属性都是不可变的，且只有可读方法。个人理解只有可读方法的作用就是避免对象存在被修改属性的可能性。文末的问题: Stringbuffer对象的引用是不可变的，但他的值却是可以改变的。get方法得到引用后它的值还可以改变。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（2） 💬（0）<div>打卡。</div>2019-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（2） 💬（0）<div>不具备不可变性,原因是stringbuffer类存在更改user对象方法</div>2019-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/a7/ac5a0f9d.jpg" width="30px"><span>bluea</span> 👍（1） 💬（0）<div>老师好，可否给个例子，如何使用无状态的对象。</div>2022-03-24</li><br/><li><img src="" width="30px"><span>Jayden Lin</span> 👍（1） 💬（0）<div>老師好，SafeWM 的例子可以這樣理解嗎？

SafeWM 引用 WMRange，在執行 WMRange 建構子的時候，設定upper 跟 lower 沒有原子性，因此要把 WMRange 內部值 (upper 跟 lower ) 的設定透過 AtomicReference 來做</div>2021-12-19</li><br/><li><img src="" width="30px"><span>Jayden Lin</span> 👍（1） 💬（0）<div>老師好，想問一下 Foo 被 Bar 引用的例子，我可以這樣理解嗎?

- 問題 1: 可見性問題
    - 線程 A 用 `bar.setFoo(new Foo())`，另一個線程 B 可能不知道，可以加上 violate 來解決

- 問題 2: 原子性問題
    - 如果 Foo 的 new 裡面有組合操作，可能會有原子性問題，這時候要用 AtomicReference 替換掉，這個原子性問題跟 Foo 有沒有被 Bar 引用無關
</div>2021-12-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bOhve1DBV2oShl2JrXDib4J1T7LciagcB8jogD5c7pvt8Zv7Bq23Zfnl70cf2R81r8ia947Hbib9FZia56sdx9wcEibA/132" width="30px"><span>小样</span> 👍（1） 💬（0）<div>&quot;Java 语言里面的 String 和 Long、Integer、Double 等基础类型的包装类都具备不可变性&quot;，这几个类型这样大写不就是包装类了吗</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/b6/46a5bbf3.jpg" width="30px"><span>俺能学个啥</span> 👍（1） 💬（0）<div>由于account对象持有stringbuffer引用，对外暴露了该引用方法，可以操作修改内容，所以不具备不可变性，应该只是无状态对象吧</div>2021-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e1/9d/3ec0adec.jpg" width="30px"><span>喃寻</span> 👍（1） 💬（0）<div>这段代码是引用的是final的StringBuffer对象，文中说了不可变对象虽然是线程安全的，但是并不意味着引用这些不可变对象的对象就是线程安全的。我们发现仍然可以通过调用StringBuffer的append方法来改变它的值，所以整体来说这个类是不是具备不可变性的，建议引用不可变的基本数据类型String作为替换，此类才能真正达到不可变性。</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3a/1a/ae3c1492.jpg" width="30px"><span>🌾🌾🌾小麦🌾🌾🌾</span> 👍（1） 💬（1）<div>&#47;&#47;Bar线程不安全
class Bar { 
Foo foo; 
void setFoo(Foo f){
 this.foo=f;  &#47;&#47;对 foo 这个引用的修改在多线程中并不能保证可见性和原子性. 引用赋值不具有原子性吗？
}
}
https:&#47;&#47;docs.oracle.com&#47;javase&#47;specs&#47;jls&#47;se7&#47;html&#47;jls-17.html#jls-17.7
Writes to and reads of references are always atomic, regardless of whether they are implemented as 32-bit or 64-bit values.</div>2020-11-29</li><br/><li><img src="" width="30px"><span>Geek_89e362</span> 👍（1） 💬（0）<div>不具备不可变性，因为通过 getUser()方法获取到StringBuffer后可以通过 append()方法追加值。从而导致值的修改。</div>2020-11-23</li><br/>
</ul>