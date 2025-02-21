如果你了解面向对象语言的发展史，那你可能听说过Smalltalk这门语言。它的影响力之大，以至于之后诞生的面向对象语言，或多或少都借鉴了它的设计和实现。

在Smalltalk中，所有的值都是对象。因此，许多人认为它是一门纯粹的面向对象语言。

Java则不同，它引进了八个基本类型，来支持数值计算。Java这么做的原因主要是工程上的考虑，因为使用基本类型能够在执行效率以及内存使用两方面提升软件性能。

今天，我们就来了解一下基本类型在Java虚拟机中的实现。

```
public class Foo {
  public static void main(String[] args) {
    boolean 吃过饭没 = 2; // 直接编译的话javac会报错
    if (吃过饭没) System.out.println("吃了");
    if (true == 吃过饭没) System.out.println("真吃了");
  }
}
```

在上一篇结尾的小作业里，我构造了这么一段代码，它将一个boolean类型的局部变量赋值为2。为了方便记忆，我们给这个变量起个名字，就叫“吃过饭没”。

赋值语句后边我设置了两个看似一样的if语句。第一个if语句，也就是直接判断“吃过饭没”，在它成立的情况下，代码会打印“吃了”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/04/b2/002398d6.jpg" width="30px"><span>丨落灬小莫</span> 👍（342） 💬（13）<div>当替换为2的时候无输出
当替换为3的时候打印HelloJava及HelloJVM
猜测是因为将boolean 保存在静态域中,指定了其类型为&#39;Z&#39;,当修改为2时取低位最后一位为0,当修改为3时取低位最后一位为1
则说明boolean的掩码处理是取低位的最后一位</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/9f/9259a6b9.jpg" width="30px"><span>Kyle</span> 👍（69） 💬（2）<div>老师，文中看你说到：
“也就是说，boolean、byte、char、short 这四种类型，在栈上占用的空间和 int 是一样的，和引用类型也是一样的。因此，在 32 位的 HotSpot 中，这些类型在栈上将占用 4 个字节；而在 64 位的 HotSpot 中，他们将占 8 个字节。”

但是我记得boolean在内存中占1字节，char占2字节，这里是什么个意思？</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/2a/31e0085f.jpg" width="30px"><span>LC</span> 👍（59） 💬（3）<div>老师可以讲下ASM、Unsafe和CAS的底层原理吗？这块儿一直是个拦路虎，谢谢！</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/db/c4edf697.jpg" width="30px"><span>曲东方</span> 👍（38） 💬（2）<div>Unsafe.putBoolean和Unsafe.puByte是native实现

putBoolean和putByte也是通过宏SET_FIELD模板出的函数

#define SET_FIELD(obj, offset, type_name, x) \
  oop p = JNIHandles::resolve(obj); \
  *(type_name*)index_oop_from_field_offset_long(p, offset) = truncate_##type_name(x)

unsafe.cpp中定义宏做truncate
#define truncate_jboolean(x) ((x) &amp; 1)
#define truncate_jbyte(x) (x)
#define truncate_jshort(x) (x)
#define truncate_jchar(x) (x)
#define truncate_jint(x) (x)
#define truncate_jlong(x) (x)
#define truncate_jfloat(x) (x)
#define truncate_jdouble(x) (x)

综上：unsafe.Put*不会对值做修改
------------------------------------------------------------------------------------
getBoolean和getByte也是通过宏GET_FIELD模板出的函数

#define GET_FIELD(obj, offset, type_name, v) \
  oop p = JNIHandles::resolve(obj); \
  type_name v = *(type_name*)index_oop_from_field_offset_long(p, offset)

综上，unsafe.Get*不会对值做修改
------------------------------------------------------------------------------------
验证：
unsafe.putByte(foo, addr, (byte)2); &#47;&#47; 设置为: 2
System.out.println(unsafe.getByte(foo, addr)); &#47;&#47; 打印getByte: 2
System.out.println(unsafe.getBoolean(foo, addr)); &#47;&#47; 打印getBoolean: true

unsafe.putByte(foo, addr, (byte)1); &#47;&#47; 设置为: 1
System.out.println(unsafe.getByte(foo, addr)); &#47;&#47; 打印getByte: 1
System.out.println(unsafe.getBoolean(foo, addr)); &#47;&#47; 打印getBoolean: true
------------------------------------------------------------------------------------
疑问：
if(foo.flag)判断，使用getfield	Field flag:&quot;Z&quot;，执行逻辑等于：0 ！= flag
if(foo.getFlag())判断，使用invokevirtual	Method getFlag:&quot;()Z&quot;，执行逻辑等于： 0 != （(flag) &amp; 1）

求大神帮忙解答

--------------------------
附getFlag jasm码：
public Method getFlag:&quot;()Z&quot;
	stack 1 locals 1
{
		aload_0;
		getfield	Field flag:&quot;Z&quot;;
		ireturn;
}



https:&#47;&#47;gist.github.com&#47;qudongfang&#47;49635d86882c03e49cff2b0f7d833805
</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/cf/e82cd26b.jpg" width="30px"><span>Geek_dde3ac</span> 👍（34） 💬（2）<div>你好，在内存中都是0，那么是如何区别是哪种类型数据的呢？</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（21） 💬（1）<div>其实那个boolean的true虚拟机里面为1，也就是if(true==吃了没)其实可以替换成if(1==2)这样理解吧</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/23/abb7bfe3.jpg" width="30px"><span>dong</span> 👍（18） 💬（1）<div>感觉&quot;吃饭了&quot;例子，弄得有点饶了。也有些地方语句的起承转合不是很通顺，个人理解。</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/a0/e6c2adac.jpg" width="30px"><span>别处</span> 👍（16） 💬（1）<div>以下两个引至本文内容：
1、在 Java 虚拟机规范中，boolean 类型则被映射成 int 类型。
2、在 HotSpot 中，boolean 字段占用一字节，

问题：一个是int类型，一个是一个字节(32位系统的话就是byte类型)，是没讲透还是错误？</div>2018-07-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoDkJkd9xYU4aiaTS5P49UmWOM1Nu4KYeTeHRiakf0Z1D2Y93usfavclvGo3I1CHWY26AjMlhVM1cJQ/132" width="30px"><span>Invincible、</span> 👍（12） 💬（1）<div>为什么我不能让boolvalue＝2或者3……</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/3c/c2c72e28.jpg" width="30px"><span>星星</span> 👍（6） 💬（1）<div>long，double，float三种类型存入操作数栈有做转化操作吗？还是做浮点运算会有特殊处理，本文没有提及呀。</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/1a/579c941e.jpg" width="30px"><span>志远</span> 👍（6） 💬（1）<div>NaN 有一个有趣的特性：除了“!= 始终返回 true”之外，所有其他比较结果都会返回 false。这句话好拗口啊，双引号的标点符号有问题吧</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/11/52a78856.jpg" width="30px"><span>D→_→M</span> 👍（5） 💬（1）<div>老师您在文中提到除了long,double以外，boolean,byte,char,short这四种类型在栈上占用的空间与int一样，那float也是一样的吗？
还有您说的byte,char,short这三种类型在堆上占用的空间与这些类型的值域吻合，那其他的哪几种类型也是如此吗？
最后还有就是加载那部分的内容只提到了boolean,byte,char以及short会加载到操作数栈上，将其值当成int类型来运算，并没有提到double,long和float类型，这三中类型与前四种类型相同吗？
</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/76/93/c78a132a.jpg" width="30px"><span>果然如此</span> 👍（3） 💬（2）<div>不错，针对知识点分析的很深入！很有收获，所谓“一沙一世界”！
我购买的另一个java面试题总结课程“看起来大而全”，而实际看了却感觉没有收获！</div>2018-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/e4/1c441aeb.jpg" width="30px"><span>Oswww</span> 👍（3） 💬（1）<div>char -&gt; character -&gt; &#47;ˈkerə&#47;</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/ba/b71cb1db.jpg" width="30px"><span>乔伟</span> 👍（3） 💬（1）<div>Double long 占用两个数组单位 64位的数组单位是8个字节 是不是说在解释栈上面 64位的情况下double占用16个字节？</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（3） 💬（1）<div>使用基本类型能够在执行效率以及内存使用两方面提升软件性能？具体是什么原理呢？占的空间更小，不需要类型转换吗？</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/33/7cb10236.jpg" width="30px"><span>rainbow</span> 👍（2） 💬（2）<div>最后例子里，true改为2或3是直接在源代码里改吗？编译报类型错误啊</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/03/ef0efcc4.jpg" width="30px"><span>EidLeung</span> 👍（2） 💬（1）<div>https:&#47;&#47;adopt-openjdk.ci.cloudbees.com&#47;view&#47;OpenJDK&#47;job&#47;asmtools&#47;lastSuccessfulBuild&#47;artifact&#47;asmtools-6.0.tar.gz</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/ff/cae1fd01.jpg" width="30px"><span>6686APP官网</span> 👍（2） 💬（1）<div>下载asm.jar那个，点开右边下载链接是个jenkins页面，已经显示有构建好的包，点击就直接下了</div>2018-07-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK6JnM4HA6sk8ql2vEbeYlUfxl251DKhBqA8tjKurP5guMDzw7xNzic0DNdE0xWngWjGqn12DpGHJQ/132" width="30px"><span>Geek_d76af3</span> 👍（1） 💬（1）<div>我想问下  if (吃过饭没)  翻译成的字节码是  ifeq 14;if (true == 吃过饭没) 翻译的字节码是：if_icmpne 27。请问老师：为什么是14 和 27  可解释下为什么是这两个数字吗</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/e0/25ce76a6.jpg" width="30px"><span>羊飞</span> 👍（1） 💬（1）<div>老师，我昨天那个好像试的不对。。。我是直接bool=true,抱歉。。。忽略我之前的话😂</div>2018-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/e0/b37f0e89.jpg" width="30px"><span>Mark Wong</span> 👍（0） 💬（1）<div>文中:在32位hotspot中，short在栈中和int一样占8字节。
我很好奇，int类型不是4字节的吗？难道是根据系统改变的吗</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/57/449e76fb.jpg" width="30px"><span>QlDoors</span> 👍（0） 💬（1）<div>        float sn1 = 0.0f &#47; 0.0f;
        float f1 = 0.0f;
        float sn2 = f1 &#47; f1;
        System.out.println(&quot;sn1 hex = &quot; + Integer.toHexString(Float.floatToRawIntBits(sn1)));
        System.out.println(&quot;sn2 hex = &quot; + Integer.toHexString(Float.floatToRawIntBits(sn2)));

老师，请问这段代码为何输出是
sn1 hex = 7fc00000
sn2 hex = ffc00000

我的运行环境是idea jdk8</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/01/0ccb7a7c.jpg" width="30px"><span>Ghoul Zhou</span> 👍（0） 💬（1）<div>“第二个 if 语句则会被编译成条件跳转字节码 if_icmpne，也就是说，如果局部变量的值和整数 1 不相等，那么跳过打印“真吃了”的语句。”
不相等，应该是不打印“真吃了”的语句，这里是不是想表达，阐述字节码执行顺序过程呀？</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/8d/10d7b878.jpg" width="30px"><span>Living  as a naturalist</span> 👍（0） 💬（1）<div>老师，百度没有找到AsmTools这个工具，是你们特用的吗</div>2018-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/75/9f80409f.jpg" width="30px"><span>追梦</span> 👍（97） 💬（7）<div>有个地方初看不易看懂，我来解释下：
    作者一开始放的“吃没吃饭”的例子中boolean变量是局部变量，存放在Java方法栈的栈帧中的局部变量区，占据一个数据单元，无需做掩码；最后的例子中boolean变量是成员变量，存储在堆中的对象实例里，占有一个字节，且需要对最后一位做掩码</div>2018-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/a1/4e063c44.jpg" width="30px"><span>匿名小板凳</span> 👍（34） 💬（0）<div>这节看的很吃力，对什么掩码，子码，反码，补码都换给大学老师了。</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/75/54bb858e.jpg" width="30px"><span>life is short, enjoy more.</span> 👍（12） 💬（6）<div>老师你好，我刚来订阅，所以才开始看。
有一个疑问，您的原文“因此，在 32 位的 HotSpot 中，这些类型在栈上将占用 4 个字节；而在 64 位的 HotSpot 中，他们将占 8 个字节。”。但是有一句话，java一次编译，到处运行。计算机位数不一样的话，导致一样类型的size不一样，还可以到处运行吗？这里指的到处运行，是不是需要同位啊？比如32位的编译只能在32位的机器上运行，64只能在64的上运行。能互相兼容运行嘛？</div>2018-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ca/40/91fdbc7d.jpg" width="30px"><span>andy</span> 👍（9） 💬（1）<div>我替换成2和3,都只能打印出一个Hello Java为什么呢？下面是AsmTools反编译代码
super public class Foo
        version 52:0
{

static Field boolValue:Z;

public Method &quot;&lt;init&gt;&quot;:&quot;()V&quot;
        stack 1 locals 1
{
                aload_0;
                invokespecial   Method java&#47;lang&#47;Object.&quot;&lt;init&gt;&quot;:&quot;()V&quot;;
                return;
}

public static Method main:&quot;([Ljava&#47;lang&#47;String;)V&quot;
        stack 2 locals 1
{
                iconst_2;
                putstatic       Field boolValue:&quot;Z&quot;;
                getstatic       Field boolValue:&quot;Z&quot;;
                ifeq    L18;
                getstatic       Field java&#47;lang&#47;System.out:&quot;Ljava&#47;io&#47;PrintStream;&quot;;
                ldc     String &quot;Hello, Java!&quot;;
                invokevirtual   Method java&#47;io&#47;PrintStream.println:&quot;(Ljava&#47;lang&#47;String;)V&quot;;
        L18:    stack_frame_type same;
                getstatic       Field boolValue:&quot;Z&quot;;
                iconst_1;
                if_icmpne       L33;
                getstatic       Field java&#47;lang&#47;System.out:&quot;Ljava&#47;io&#47;PrintStream;&quot;;
                ldc     String &quot;Hello, JVM!&quot;;
                invokevirtual   Method java&#47;io&#47;PrintStream.println:&quot;(Ljava&#47;lang&#47;String;)V&quot;;
        L33:    stack_frame_type same;
                return;
}

} &#47;&#47; end Class Foo</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/52/00/cd5c0ff6.jpg" width="30px"><span>迷上尼古丁的味道</span> 👍（8） 💬（1）<div>下面这段中0x8000000是不是少写了一个0呢

前者在 Java 里是 0，后者是符号位为 1、其他位均为 0 的浮点数，在内存中等同于十六进制整数 0x8000000（即 -0.0F 可通过 Float.intBitsToFloat(0x8000000) 求得）。</div>2019-02-22</li><br/>
</ul>