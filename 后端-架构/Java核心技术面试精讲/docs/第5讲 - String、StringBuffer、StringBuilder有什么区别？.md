今天我会聊聊日常使用的字符串，别看它似乎很简单，但其实字符串几乎在所有编程语言里都是个特殊的存在，因为不管是数量还是体积，字符串都是大多数应用中的重要组成。

今天我要问你的问题是，理解Java的字符串，String、StringBuffer、StringBuilder有什么区别？

## 典型回答

String是Java语言非常基础和重要的类，提供了构造和管理字符串的各种基本逻辑。它是典型的Immutable类，被声明成为final class，所有属性也都是final的。也由于它的不可变性，类似拼接、裁剪字符串等动作，都会产生新的String对象。由于字符串操作的普遍性，所以相关操作的效率往往对应用性能有明显影响。

StringBuffer是为解决上面提到拼接产生太多中间对象的问题而提供的一个类，我们可以用append或者add方法，把字符串添加到已有序列的末尾或者指定位置。StringBuffer本质是一个线程安全的可修改字符序列，它保证了线程安全，也随之带来了额外的性能开销，所以除非有线程安全的需要，不然还是推荐使用它的后继者，也就是StringBuilder。

StringBuilder是Java 1.5中新增的，在能力上和StringBuffer没有本质区别，但是它去掉了线程安全的部分，有效减小了开销，是绝大部分情况下进行字符串拼接的首选。

## 考点分析

几乎所有的应用开发都离不开操作字符串，理解字符串的设计和实现以及相关工具如拼接类的使用，对写出高质量代码是非常有帮助的。关于这个问题，我前面的回答是一个通常的概要性回答，至少你要知道String是Immutable的，字符串操作不当可能会产生大量临时字符串，以及线程安全方面的区别。

如果继续深入，面试官可以从各种不同的角度考察，比如可以：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/9d/3b/bc67bfbe.jpg" width="30px"><span>Bin</span> 👍（87） 💬（12）<div>jdk1.8中，string是标准的不可变类，但其hash值没有用final修饰，其hash值计算是在第一次调用hashcode方法时计算，但方法没有加锁，变量也没用volatile关键字修饰就无法保证其可见性。当有多个线程调用的时候，hash值可能会被计算多次，虽然结果是一样的，但jdk的作者为什么不将其优化一下呢？</div>2018-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（635） 💬（18）<div>今日String&#47;StringBuffer&#47;StringBuilder心得:


1 String

(1) String的创建机理
由于String在Java世界中使用过于频繁，Java为了避免在一个系统中产生大量的String对象，引入了字符串常量池。其运行机制是：创建一个字符串时，首先检查池中是否有值相同的字符串对象，如果有则不需要创建直接从池中刚查找到的对象引用；如果没有则新建字符串对象，返回对象引用，并且将新创建的对象放入池中。但是，通过new方法创建的String对象是不检查字符串池的，而是直接在堆区或栈区创建一个新的对象，也不会把对象放入池中。上述原则只适用于通过直接量给String对象引用赋值的情况。

举例：String str1 = &quot;123&quot;; &#47;&#47;通过直接量赋值方式，放入字符串常量池
String str2 = new String(“123”);&#47;&#47;通过new方式赋值方式，不放入字符串常量池

注意：String提供了inter()方法。调用该方法时，如果常量池中包括了一个等于此String对象的字符串（由equals方法确定），则返回池中的字符串。否则，将此String对象添加到池中，并且返回此池中对象的引用。


(2) String的特性
[A] 不可变。是指String对象一旦生成，则不能再对它进行改变。不可变的主要作用在于当一个对象需要被多线程共享，并且访问频繁时，可以省略同步和锁等待的时间，从而大幅度提高系统性能。不可变模式是一个可以提高多线程程序的性能，降低多线程程序复杂度的设计模式。

[B] 针对常量池的优化。当2个String对象拥有相同的值时，他们只引用常量池中的同一个拷贝。当同一个字符串反复出现时，这个技术可以大幅度节省内存空间。

2 StringBuffer&#47;StringBuilder

StringBuffer和StringBuilder都实现了AbstractStringBuilder抽象类，拥有几乎一致对外提供的调用接口；其底层在内存中的存储方式与String相同，都是以一个有序的字符序列（char类型的数组）进行存储，不同点是StringBuffer&#47;StringBuilder对象的值是可以改变的，并且值改变以后，对象引用不会发生改变;两者对象在构造过程中，首先按照默认大小申请一个字符数组，由于会不断加入新数据，当超过默认大小后，会创建一个更大的数组，并将原先的数组内容复制过来，再丢弃旧的数组。因此，对于较大对象的扩容会涉及大量的内存复制操作，如果能够预先评估大小，可提升性能。

唯一需要注意的是：StringBuffer是线程安全的，但是StringBuilder是线程不安全的。可参看Java标准类库的源代码，StringBuffer类中方法定义前面都会有synchronize关键字。为此，StringBuffer的性能要远低于StringBuilder。


3 应用场景	

[A]在字符串内容不经常发生变化的业务场景优先使用String类。例如：常量声明、少量的字符串拼接操作等。如果有大量的字符串内容拼接，避免使用String与String之间的“+”操作，因为这样会产生大量无用的中间对象，耗费空间且执行效率低下（新建对象、回收对象花费大量时间）。

[B]在频繁进行字符串的运算（如拼接、替换、删除等），并且运行在多线程环境下，建议使用StringBuffer，例如XML解析、HTTP参数解析与封装。

[C]在频繁进行字符串的运算（如拼接、替换、删除等），并且运行在单线程环境下，建议使用StringBuilder，例如SQL语句拼装、JSON封装等。</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/00/db92d343.jpg" width="30px"><span>愉悦在花香的日子里</span> 👍（54） 💬（2）<div>getBytes和String相关的转换时根据业务需要建议指定编码方式，如果不指定则看看JVM参数里有没有指定file.encoding参数，如果JVM没有指定，那使用的默认编码就是运行的操作系统环境的编码了，那这个编码就变得不确定了。常见的编码iso8859-1是单字节编码，UTF-8是变长的编码。</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/9e/d2ddf667.jpg" width="30px"><span>Van</span> 👍（39） 💬（1）<div>String myStr = &quot;aa&quot; +&quot;bb&quot; + &quot;cc&quot; +&quot;dd&quot;;反编译后并不会用到StringBuilder，老师反编译结果中出现StringBuilder是因为输出中拼接了字符串System.out.println(&quot;My String:&quot; + myStr);</div>2018-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/c8/c2343cb6.jpg" width="30px"><span>DoctorDeng</span> 👍（32） 💬（8）<div>		String s = new String(&quot;1&quot;);
		s.intern();
		String s2 = &quot;1&quot;;
		System.out.println(s == s2);

		String s3 = new String(&quot;1&quot;) + new String(&quot;1&quot;);
		s3.intern();
		String s4 = &quot;11&quot;;
		System.out.println(s3 == s4);
  这道面试题不错，即考察了 intern() 的用法，也考察了字符串常量池在不同版本 JDK 的实际存储，具体可以看看美团博客：https:&#47;&#47;tech.meituan.com&#47;in_depth_understanding_string_intern.html，</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（29） 💬（1）<div>特别喜欢这句话：“仅仅是字符串一个实现，就需要 Java 平台工程师和科学家付出如此大且默默无闻的努力，我们得到的很多便利都是来源于此。”

我想说，同学们，写代码的时候记得感恩哦😄

对于字符串的研究，我觉得能很好的理解计算机的本质和训练计算机思维，提升自己解决问题的能力。

小小的字符串有着诸多巨人的影子</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/e5/605f423f.jpg" width="30px"><span>肖一林</span> 👍（14） 💬（1）<div>这篇文章写的不错，由浅入深，把来龙去脉写清楚了</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/51/9d5cfadd.jpg" width="30px"><span>好运来</span> 👍（9） 💬（1）<div>老师，可以讲解这一句话的具体含义吗，谢谢！
你可以思考下，原来 char 数组的实现，字符串的最大长度就是数组本身的长度限制，但是替换成 byte 数组，同样数组长度下，存储能力是退化了一倍的！还好这是存在于理论中的极限，还没有发现现实应用受此影响。</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/dc/9bd86256.jpg" width="30px"><span>©®</span> 👍（7） 💬（1）<div>String s2=new String(&quot;AB&quot;)，，如果，常量池中没有AB,那么会不会去常量池创建，望解答</div>2018-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/0f/b75e839c.jpg" width="30px"><span>So Leung</span> 👍（5） 💬（3）<div>经过验证new String时，不会再常量池中创建对象。</div>2018-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/2f/b7a3625e.jpg" width="30px"><span>Len</span> 👍（4） 💬（1）<div>老师，这章学习到了 Java 8 以后，字符串常量池被移到了堆中，那么，如果通过 String.intern() 产生了大量的字符串常量，JVM 会对它们进行垃圾回收吗？</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/69/a0707c76.jpg" width="30px"><span>嘎哈</span> 👍（4） 💬（1）<div>char 数组的实现，字符串的最大长度就是数组本身的长度限制，但是替换成 byte 数组，同样数组长度下，存储能力是退化了一倍的！
怎么理解呢？ 举个例子呗</div>2018-05-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI4lQqXdFkO0ke8vCxL1lAfy5qAOseO1af7rSZyQBcibI8pMfbj1u9pXAdxHZkvomuaqGhPrkJs9FA/132" width="30px"><span>淡定</span> 👍（3） 💬（1）<div>  public class StringConcat {
        public static void main(String[] args) {
             String myStr = &quot;aa&quot; + &quot;bb&quot; + &quot;cc&quot; + &quot;dd&quot;;   
             System.out.println(&quot;My String:&quot; + myStr);   
        } 
  }
作者举得的这个例子,和后面的解释有迷惑性 ,首先 ,第一句  String myStr = &quot;aa&quot; + &quot;bb&quot; + &quot;cc&quot; + &quot;dd&quot;;    编译器已经帮你合并为 myStr = &quot;aabbccdd&quot; 了,所谓后面的StringBuilder 是因为System.out.println 里面有字符串拼接..... </div>2018-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/c7/e12ed041.jpg" width="30px"><span>Nick</span> 👍（3） 💬（1）<div>请问老师该怎么证明new String(&quot;ABCDE&quot;)不会将&quot;ABCDE&quot;放在常量池中呢？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/4d/37116342.jpg" width="30px"><span>晓</span> 👍（3） 💬（1）<div>数组的大小是int型的，所以int最大值就是它的限制吗？</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/e5/aa579968.jpg" width="30px"><span>王磊</span> 👍（3） 💬（1）<div>假如我执行如下操作, 并且常量池里确实已缓存过&quot;abc&quot;, 那么执行intern()后s会指向常量池的&quot;abc&quot;, 堆中的&quot;abc&quot;会被回收，是这样吗？
String s = new String(&quot;abc&quot;);
s.intern()

这样的话就会多产生一个垃圾。不想产生垃圾的话，就创建时直接指向常量池中的&quot;abc&quot;
String s = &quot;abc&quot;;

请老师确实理解是否正确。

</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（2） 💬（1）<div>JDK8反编译看到了字符串相加会优化成stringBuilder那么是否可以认为，在JDK8中字符串拼接可以直接相加了哦？不需要自己写stringbuilder了？</div>2018-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/5d/83b615f3.jpg" width="30px"><span>过冬</span> 👍（2） 💬（1）<div>老师，是退化还是进化？
替换成 byte 数组，同样数组长度下，存储能力是退化了一倍的！
char变byte，数组长度不变，占用空间更小才对啊？</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（2） 💬（1）<div>杨老师，问个问题：
String str1 =&quot;abc&quot;;
String str2 = new String(&quot;abc&quot;);
理论上,str1是放入字符串长量池，str2是新增一个对象，新开辟一块地址。
但是通过代码调试，他们的HashCode一样，就说明他们是引用同一个地址。
请帮忙分析一下。</div>2018-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/f5/b19dd1d4.jpg" width="30px"><span>雪未央</span> 👍（2） 💬（1）<div>char占两个byte,同样长度的char数组和byte数组容量差两倍，不知道这样理解对不对？</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/51/f309515c.jpg" width="30px"><span>冬末未末</span> 👍（2） 💬（1）<div>用过String最大的坑就是subString方法，在1.6版本导致的内存泄露，老师都没有讲</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（2） 💬（1）<div>思考题里的平台默认编码，平台指的是JVM所在的操作系统，还是指语言平台本身呢？
</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/0e/2a7a422c.jpg" width="30px"><span>小墨迹</span> 👍（1） 💬（1）<div>
Jdk1.8
String str = &quot;aa&quot;;
str = str + &quot;bb&quot;;
与
String str = &quot;aa&quot;+&quot;bb&quot;
反编译结果不一样，求解，谢谢哒，
什么格式的书写会智能优化</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/99/6e05432a.jpg" width="30px"><span>debugable</span> 👍（1） 💬（1）<div>java9讲字符串内部使用字节数组保存，取一个中文字符串字符个数是不是就不能用length了？</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/1e/01a794cb.jpg" width="30px"><span>DavidWhom佳传</span> 👍（1） 💬（1）<div>老师，就这样面试题多讲讲挺好的</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/28/de/54667f13.jpg" width="30px"><span>jutsu</span> 👍（1） 💬（1）<div>地铁上看起来啦，从来没有string类型的线程问题，受教了</div>2018-05-15</li><br/><li><img src="" width="30px"><span>流沙和小胖几</span> 👍（0） 💬（1）<div>string是immutable的，对它的任何操作都不会改变string内部的成员。如果进行string的拼接会造成生成多个临时string。因此引入了stringbuffer和stringbuilder来实现拼接，他们都是通过内部维持一个数组来实现的。stringbuffer是线程安全的，stringbuilder不是，可以根据具体使用场景来选择合适的类。</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/3c/1bec447d.jpg" width="30px"><span>фщэьшух</span> 👍（0） 💬（1）<div>这种便利甚至体现在拷贝构造函数中，由于不可变，Immutable 对象在拷贝时不需要额外复制数据。

拷贝构造函数，没明白老师～
可不可以举例说明</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/3b/714cc8a5.jpg" width="30px"><span>沉梦昂志</span> 👍（0） 💬（1）<div>上面那个问为什么不把“aa”+“bb”+“cc”优化成aabbcc的 据我所知 JDK8中已经实现了这种默认优化</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/b5/137f25a9.jpg" width="30px"><span>kkllor</span> 👍（0） 💬（1）<div>很不错，深入浅出，涉及到的技术原理都覆盖了，告诉了读者技术方向，想深入的可以继续翻阅更多资料</div>2018-05-22</li><br/>
</ul>