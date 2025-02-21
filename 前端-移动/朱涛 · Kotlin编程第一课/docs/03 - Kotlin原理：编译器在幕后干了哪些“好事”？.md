你好，我是朱涛。

在前面两节课里，我们学了不少Kotlin的语法，其中有些语法是和Java类似的，比如数字类型、字符串；也有些语法是Kotlin所独有的，比如数据类、密封类。另外，我们还知道Kotlin和Java完全兼容，它们可以同时出现在一个代码工程当中，并且可以互相调用。

但是，这样就会引出一个问题：**Java是如何识别Kotlin的独有语法的呢？**比如，Java如何能够认识Kotlin里的“数据类”？

这就要从整个Kotlin的实现机制说起了。

所以，今天这节课，我会从Kotlin的编译流程出发，来带你探索这门语言的底层原理。在这个过程中，你会真正地理解，Kotlin是如何在实现灵活、简洁的语法的同时，还做到了兼容Java语言的。并且你在日后的学习和工作中，也可以根据今天所学的内容，来快速理解Kotlin的其他新特性。

## Kotlin的编译流程

在介绍Kotlin的原理细节之前，我们先从宏观上看看它是如何运行在电脑上的，这其实就涉及到它的编译流程。

那么首先，你需要知道一件事情：你写出的Kotlin代码，电脑是无法直接理解的。即使是最简单的`println("Hello world.")`，你将这行代码告诉电脑，它也是无法直接运行的。这是因为，Kotlin的语法是基于人类语言设计的，电脑没有人的思维，它只能理解二进制的0和1，不能理解println到底是什么东西。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/a6/679b3c6b.jpg" width="30px"><span>Renext</span> 👍（66） 💬（4）<div>思考题：
转换成 java代码就一清二楚，两种方式的isAdult本质不是同一个东西：
1-通过自定义 getter 来实现的方式，isAdult其实是一个方法。外部每一次调用，都是拿最新的age进行计算，所以age的值有变动，isAdult()的结果是最新的。
2- val isAdult = age &gt;= 18 这种方式，isAdault是一个final变量，只会在对象新建时，在构造方法中，根据age的值赋值一次。所以，之后age的值如果有变动，isAdault值是永远不变的。

</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（12） 💬（1）<div>思考题：
如果采用 val isAdult = age &gt;= 18 这种写法，那么错误会表现在给某个 Person 对象的 age 属性二次赋值时，isAdult 属性仍会是一个旧的 Boolean 值。原因：从反编译出的 Java 代码可以看出，isAdult 属性会被转换成一个 final 修饰的 Java 属性且在构造方法里赋好值了，那么意味着即使 age 属性后期修改一万遍，isAdult 属性也只会是它原来的那个初始值。
而如果用 getter 的方式则不会有这个问题，因为 getter 方式会把 isAdult 属性转换成 getter 方法而不是 final 修饰的属性，每一次调用，isAdult 属性就会动态的根据 age 属性来判断返回值。</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/04/a557d4f0.jpg" width="30px"><span>阶前听雨</span> 👍（11） 💬（1）<div>太赞了，看了很多书和博客，基本都在讲kotlin多好用。从根本上讲kotlin的还是这门课，很多以前懵懵懂懂的概念都豁然开朗，太赞了。</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/c6/c86e70d9.jpg" width="30px"><span>逢庆</span> 👍（8） 💬（1）<div>1.
val isAdult
     get() = age &gt;= 18
反编译后可以看到，会生成方法:
   public final boolean isAdult() {
      return this.age &gt;= 18;
   }

2.
val isAdult = age &gt;= 18
反编译后，可以看到：
会定义一个isAdult属性：
private final boolean isAdult;
并在构造函数里根据age来赋值：
this.isAdult = this.age &gt;= 18;


</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/7e/231c9fa2.jpg" width="30px"><span>文茂权</span> 👍（6） 💬（1）<div>JVM 由于存在多种实现，依赖的是一套标准规范。尽管学习 Kotlin 不需要直接接触 JVM ，但参考 JVM 的设计规范对于我们学习 JVM 编程语言的设计是很有作用的。
这里附上 JVM 不同版本的设计规范文档：https:&#47;&#47;docs.oracle.com&#47;javase&#47;specs&#47;index.html</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/3d/8120438b.jpg" width="30px"><span>3.141516</span> 👍（5） 💬（1）<div>kotlin 的一些语法特性在编译为字节码后会增多 class 数量，所以会增加字节码的大小。

想请教下老师，在 Android 中，Kotlin 还有哪些方面会增加包大小呢？谢谢</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/7b/db/7cfa21ad.jpg" width="30px"><span>droidYu</span> 👍（4） 💬（1）<div>Kotlin语言的简洁得益于Kotlin编译器的强大，之所以Java和Kotlin能完全兼容，是因为Java和Kotlin编译后的成果都是Java字节码。</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（3） 💬（1）<div>You can define custom accessors for a property. 
If you define a custom getter, it will be called every time you access the property (this way you can implement a computed property). 
If you define a custom setter, it will be called every time you assign a value to the property, except its initialization.</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（2） 💬（2）<div>直觉上反编译都是有损的，不知道有没有遇到过反编译结果不对的例子？</div>2022-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（2） 💬（2）<div>关于 Kotlin 包装类型优化原始类型，我的实验结果和老师的结论有一点出入，不知道是不是编译器版本的原因。🌚
var a: Long = 1 &#47;&#47; private static long a = 1L;
val b: Long = 2 &#47;&#47; private static final long b = 2L;
var c: Long? = 3 &#47;&#47; private static Long c = 3L; 未优化成原始类型
val d: Long? = 4 &#47;&#47; private static final Long d = 4L; 未优化成原始类型</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2a/57/6629c858.jpg" width="30px"><span>阿康</span> 👍（2） 💬（1）<div>对象属性：具有get的是可读属性，具有set的是可写属性，同时具有get、set的是可读写属性。没有get、set的那是字段，不是属性。</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/37/15baf151.jpg" width="30px"><span>neo</span> 👍（1） 💬（1）<div>转换成java的话val isAdult = age &gt;= 18相当于在初始化函数中对isAdult进行赋值，并且本身为final属性，不再具有可变性。
val isAdult get() = age &gt;= 18 才是一个正常对应一个方法，后面的语句就是方法体</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e5/e1/a5064f88.jpg" width="30px"><span>Geek_Adr</span> 👍（1） 💬（1）<div>&#47;&#47; kotlin 代码

&#47;&#47; 用 val 定义可为空、不可为空的Long，并且赋值
val a: Long = 1L
val b: Long? = 2L
&#47;&#47; 加上方法调用
a.equals(b)

&#47;&#47; 反编译后的 Java 代码
long a = 1L;
Long b = 2L;
Long.valueOf(a).equals(b);

&#47;&#47; 是不是可以认为val一定被转成成基本类型 可空类型遇到和对象相关操作的都会被转成包装类型</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/12/46/f361c795.jpg" width="30px"><span>陈彬</span> 👍（1） 💬（1）<div>class Person(val name: String, var age: Int) {
    val isAdult = age &gt;= 18
}
经过老师教的方法把Kotlin 对应的字节码反编译之后代码如下:
public final class Person {
   private final boolean isAdult;
   @NotNull
   private final String name;
   private int age;

   public final boolean isAdult() {
      return this.isAdult;
   }

   @NotNull
   public final String getName() {
      return this.name;
   }

   public final int getAge() {
      return this.age;
   }

   public final void setAge(int var1) {
      this.age = var1;
   }

   public Person(@NotNull String name, int age) {
      Intrinsics.checkParameterIsNotNull(name, &quot;name&quot;);
      super();
      this.name = name;
      this.age = age;
      this.isAdult = this.age &gt;= 18;
   }
}
可以看到这种写法在初始化构造函数的时候就对isAdult属性进行赋值，导致以后不管如何修改age的值，isAdult()返回值永远不会改变。
我理解之所以这样的原因是在kotlin中，val定义的属性默认会生成getter方法，而第一种方式没问题是因为其重写了属性的getter方法。</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4d/5e/5e66ca3f.jpg" width="30px"><span>Xeon</span> 👍（1） 💬（1）<div>个人理解：上面那个自定义getter的方式最终会被编译成一个isAdult()方法，return this.age &gt;= 18; 并没有实际的isAdult属性产生（之前的文章中有提到过），此时isAdult的值是会根据age值的变化而变化的。
而下面那种方式是真的会存在一个被final修饰的isAdult属性，而final修饰的属性值一旦确定后是不能修改的，也就是说首次给age赋值的时候，isAdult的值就已经确定了，哪怕后面再更改age的值，isAdult的值也不会随着age的值变化而变化。所以，日常开发中这样用一不小心就会出错。</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/10/365ea684.jpg" width="30px"><span>聪明的傻孩子</span> 👍（0） 💬（1）<div>豁然开朗，大佬分析得太牛了</div>2022-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c2/88/78df5b1c.jpg" width="30px"><span>凌宇之蓝</span> 👍（0） 💬（1）<div>val isAdult = age &gt;= 18 反编译后成为一个final值且在构造函数中默认添加；val isAdult
        get() = age &gt;= 18是一个正常的方法，可以根据传入值动态改变返回值</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ec/b0/4e22819f.jpg" width="30px"><span>syz</span> 👍（0） 💬（1）<div>val isAdult = age &gt;= 18 这样写没毛病,等价于
class Person(val name: String, var age: Int, val isAdult: Boolean = age &gt;= 18)
------------
 val isAdult
        get() = age &gt;= 18
这样写class Person有两个参数，附带一个方法    
public final boolean isAdult() {
      return this.age &gt;= 18;
}
</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/85/7e174dd0.jpg" width="30px"><span>imxilife</span> 👍（0） 💬（1）<div>外部获取isAdult的值的时候会自动调它的get()方法，所以不重写get()方法是无效的</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2a/57/6629c858.jpg" width="30px"><span>阿康</span> 👍（0） 💬（1）<div>如果不用getter 实现，Person实例化后isAdult值就固定了，即使在重新给age赋值，isAdult也不会变。
1、通过自定义 getter 来实现：
  var man = Person(&quot;男孩&quot;,16)
  println(man.isAdult)
  man.age = 20
  println(man.isAdult)
&#47;&#47;========输出结果=======
false
true
&#47;&#47;=====================
2、val isAdult = age &gt;= 18 实现：
  var man = Person(&quot;男孩&quot;,16)
  println(man.isAdult)
  man.age = 20
  println(man.isAdult)
&#47;&#47;========输出结果=======
false
false
&#47;&#47;=====================</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/eb/ae/09841320.jpg" width="30px"><span>仇无恨</span> 👍（0） 💬（1）<div>第二种写法相当于在类初始化时候给isAdult进行了初始化赋值，isAdult的结果只与类初始化时传入的age参数有关。
第一种写法相当于重写了isAdult的get函数，每次获取时都会通过当前的age的值来判断结果</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c7/5c/94cb3a1a.jpg" width="30px"><span>$Kotlin</span> 👍（0） 💬（1）<div>val isAdult get() = age &gt;= 18
生成的是对应的get方法
public final boolean isAdult() {
	return this.age &gt;= 18;
}

val isAdult = age &gt;= 18
生成的是不可变属性加方法
private final boolean isAdult;
public final boolean isAdult() {
	return this.isAdult;
}
初始化中赋值后不可更改
this.isAdult = this.age &gt;= 18;</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c7/5c/94cb3a1a.jpg" width="30px"><span>$Kotlin</span> 👍（0） 💬（1）<div>val isAdult get() = age &gt;= 18 生成的是对应的方法public final boolean isAdult() {
         return this.age &gt;= 18;
      }</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/94/5f3460cd.jpg" width="30px"><span>Marten</span> 👍（0） 💬（1）<div> val isAdult = age &gt;= 18 这样写，java会认为isAdult是成员属性，如果不初始化person，isAdult的get方法返回是有问题的。</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/ed/9cc44242.jpg" width="30px"><span>JakePrim</span> 👍（0） 💬（1）<div>赞，有种豁然开朗的感觉</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c4/bd/44757daf.jpg" width="30px"><span>墨方</span> 👍（0） 💬（1）<div>又仔细看了一下, 我理解错老师说的错误的意思了, 因为如果重写了isAdult的get方法之后,isAdult会被编译为一个方法,而不是一个属性. 这样即使age发生变化,也会获知到isAdult的正确值, 不重写isAdult的get方法,改变了age之后,获取的isAdult有可能会出现错误</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/d0/749a57e2.jpg" width="30px"><span>xiaomengjie</span> 👍（0） 💬（1）<div>
class Person(val name: String, var age: Int) {
    val isAdult
        get() = age &gt;= 18
}
编译后idAdult会转换为方法
public final boolean isAdult() {
      return this.age &gt;= 18;
   }
person对象改变age值，isAudlt会变换


class Person(val name: String, var age: Int) {
    val isAdult = age &gt;= 18
}
编译后：
private final boolean isAdult;
public final boolean isAdult() {
      return this.isAdult;
   }
   public Person(@NotNull String name, int age) {
      Intrinsics.checkNotNullParameter(name, &quot;name&quot;);
      super();
      this.name = name;
      this.age = age;
      this.isAdult = this.age &gt;= 18;
   }
额外生成final字段isAdult，构造函数中初始化
person对象改变age值，isAdult()不会变</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c4/bd/44757daf.jpg" width="30px"><span>墨方</span> 👍（0） 💬（1）<div>class Person(val name: String, val age: Int) {
    val isAdult = age &gt;= 18
}
这种写法不会出错了,估计是因为版本的问题,
通过反编译后的代码可以看到,isAdult被声明成final, 然后会在Person的构造方法中根据age的值去判断赋值
public final class Person {
   private final boolean isAdult;
   &#47;&#47;省略.........
   public Person(@NotNull String name, int age) {
   &#47;&#47;省略 .......
      this.isAdult = this.age &gt;= 18;
   }
}</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/10/365ea684.jpg" width="30px"><span>聪明的傻孩子</span> 👍（0） 💬（0）<div>二刷打卡</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/3d/8120438b.jpg" width="30px"><span>3.141516</span> 👍（0） 💬（0）<div>class Person(val name: String, var age: Int) {
    val isAdult = age &gt;= 18
}

这种写法错误是因为 isAdult 编译后作为类的的属性，在构造方法中它的值就确定了。后续修改 age 后，它的值是不变的。</div>2023-08-16</li><br/>
</ul>