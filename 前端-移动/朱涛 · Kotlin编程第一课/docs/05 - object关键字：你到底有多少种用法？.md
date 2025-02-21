你好，我是朱涛。这节课我们来学习Kotlin当中object关键字的三种语义，以及它的具体使用场景。

在前面课程中，我们学习了Kotlin语言的基础语法和面向对象相关的语法，其中涵盖了很多不同类型的关键字。比如说，fun关键字代表了定义函数，class关键字代表了定义类，这些都是一成不变的。但是今天我们要学习的object关键字，却有三种迥然不同的语义，分别可以定义：

- 匿名内部类；
- 单例模式；
- 伴生对象。

之所以会出现这样的情况，是因为Kotlin的设计者认为，这三种语义本质上都是**在定义一个类的同时还创建了对象**。在这样的情况下，与其分别定义三种不同的关键字，还不如将它们统一成object关键字。

那么，理解object关键字背后的统一语义，对我们学习这个语法是极其关键的，因为它才是这三种不同语义背后的共同点。通过这个统一语义，我们可以在这三种语义之间建立联系，形成知识体系。这样，我们在后面的学习中才不会那么容易迷失，也不会那么容易遗忘。

接下来，我们就一起来逐一探讨这三种情况吧。

## object：匿名内部类

首先是object定义的匿名内部类。

Java当中其实也有匿名内部类的概念，这里我们可以通过跟Java的对比，来具体理解下Kotlin中对匿名内部类的定义。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="" width="30px"><span>InfoQ_0880b52232bf</span> 👍（23） 💬（2）<div>”由于static{}代码块当中的代码，是在类加载的时候被执行的...“

这句话是有问题的，静态代码块不是在类加载的时候执行的，而是在类初始化时执行的。</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/f4/27a5080a.jpg" width="30px"><span>7Promise</span> 👍（9） 💬（5）<div>BaseSingleton有一个缺点：限制了单例的构造函数只有一个参数。因此可以将p改为函数类型传入。</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2a/57/6629c858.jpg" width="30px"><span>阿康</span> 👍（8） 💬（1）<div>我感觉可以把P换成高级函数当做参数传入，未必每个单例的creator 内部方法都是一样的，是吧？
</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/06/e5/51ef9735.jpg" width="30px"><span>A Lonely Cat</span> 👍（7） 💬（1）<div>class DatabaseManager private constructor() {

    companion object {
        @JvmStatic
        val instance by lazy { DatabaseManager() }
    }
}

这样写也行</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（6） 💬（3）<div>1、文章中说&quot;Kotlin 还是为我们提供了伴生对象，来帮助实现静态方法和变量&quot; --- 请问伴生对象(companion object)和静态有关系吗？我感觉只是 @JvmStatic 和静态有关系。
2、文章中说&quot;伴生对象，是嵌套单例的一种特殊情况&quot; --- 请问伴生对象还能叫单例吗？反编译后，他都有 public 的构造方法了，而且 static 代码块也不见了
3、文章中说&quot;@JvmStatic修饰的方法或属性会被挪到伴生对象外部的类当中&quot; --- 这里不应该称为【挪到】吧，因为内部类中的 foo 方法还在那里，说【拷贝】更合适
4、请问【伴生对象 + @JvmStatic】有什么意义？单纯拷贝一个成员到外部类中并没有什么意义吧？</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a1/31/ca97e229.jpg" width="30px"><span>louc</span> 👍（2） 💬（1）<div>BaseSingleton 的提取之前，getInstance 在子类的companion object中可以加 @JvmStatic，但是提取后就无法加这个注解了，造成java代码调用不友好了，这个算个缺点吧</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（2） 💬（1）<div>使用 object 定义匿名内部类的时候，可以在继承一个抽象类的同时，来实现多个接口，但是反编译后为啥语法不正确？

   public static final void main() {
      &lt;undefinedtype&gt; item = new A() {
         public void funA() {
         }

         public void funB() {
         }

         public void findMan() {
         }
      };
      item.findMan();
   }</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（2） 💬（1）<div>creator 是唯一一个需要实现的方法，我们可以使用 SAM 转换，最终使用 Lambda 表达式来简化它的写法。 

open class BaseSingleton&lt;in P, out T : Any&gt;(private val creator: (P) -&gt; T) {
  @Volatile private var instance: T? = null

  fun getInstance(param: P): T =
    instance ?: synchronized(this) {
      instance ?: creator(param).also { instance = it }
    }
}</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（1） 💬（1）<div>companion 只是为了将 @jvmstatic 修饰的方法，挪到外面么？？</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a6/f0/50d0931d.jpg" width="30px"><span>木易杨</span> 👍（1） 💬（3）<div>class Utils{
    @JvmStatic
    fun foo(){
        println(&quot;foo&quot;)
    }
}
为啥@JvmStatic不能再class中写了？只能在object中。</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/af/e0/69a94af6.jpg" width="30px"><span>zeki</span> 👍（1） 💬（4）<div>在伴生对象的内部，如果存在“@JvmStatic”修饰的方法或属性，它会被挪到伴生对象外部的类当中，变成静态成员。 这句话是不是有问题呢？我通过查看java代码，发现，属性无论有没有被修饰，都会在外部类中变成静态成员</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/37/15baf151.jpg" width="30px"><span>neo</span> 👍（0） 💬（1）<div>class Person {
    companion object {
        fun foo(): String {
            return &quot;ZCL&quot;
        }
        
        @JvmStatic
        fun staticMethod(): String {
            return &quot;staticMethod&quot;
        }
    }
}
fun main(){
    println(Person.foo())
    println(Person.staticMethod())
}
如果单单的是在写法上的话，不加@JvmStatic也是可以从最外层调用的。
但是反编译之后foo()方法就没有出现在最外层的函数内。</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/37/15baf151.jpg" width="30px"><span>neo</span> 👍（0） 💬（1）<div>为什么工具类中的静态的无参静态函数会被转换成属性，这样子不是会多一个静态对象的开销么</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/37/15baf151.jpg" width="30px"><span>neo</span> 👍（0） 💬（1）<div>我将我们日常项目中的utils类直接转换成kotlin的时候，转换出来的是如下格式的。直接使用object+@JvmStatic，而没有出现companion。这是什么原因呢，是建议用这种写法写静态方法么
object Utils {
      @JvmStatic
      fun dp2px(){
      }
}
</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/37/15baf151.jpg" width="30px"><span>neo</span> 👍（0） 💬（1）<div>&#47;&#47; Kotlin当中这样调用Person.InnerSingleton.foo(）
&#47;&#47; 等价&#47;&#47; 
java 当中这样调用Person.InnerSingleton.INSTANCE.foo()
此处为什么非要如此转换呢，一个非静态的方法为什么非要看起来像静态的调用呢</div>2022-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/8b/94/09dca97d.jpg" width="30px"><span>故事与酒</span> 👍（0） 💬（1）<div>为什么在伴生对象时，没有了类名了，有类名的时候可不可以直接用外部类名调用</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/bf/da/fede41ea.jpg" width="30px"><span>苍王</span> 👍（0） 💬（2）<div>java 单例有一种静态内部类实现的方式，那么用kotlin是不是可以这样写
class SingleInstance private constructor() {

    companion object {
        @JvmStatic
        fun getInstance(): SingleInstance = Holder.instance
    }

    private object Holder {
        val instance = SingleInstance()
    }

}</div>2022-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（0） 💬（1）<div>in P 这个param 可以使用函数，这样就不需要creator 了，也不会限制单例的构造只能用一个入参</div>2022-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f0/a0/43168e73.jpg" width="30px"><span>Gavin</span> 👍（0） 💬（1）<div>既然伴生对象针对于@JvmStatic修饰的方法在外部类创建了一个同名静态方法进行对单例类转接，那么为什么反编译之后java中依然是通过 “外部类.内部单例类实例.方法” 的形式去调用，而不是 “外部类.外部类同名方法”的形式调用</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/d0/749a57e2.jpg" width="30px"><span>xiaomengjie</span> 👍（0） 💬（3）<div>要是这么调用的话：
UserManager.getInstance(&quot;user1&quot;)
UserManager.getInstance(&quot;user2&quot;)
不是只有第一次调用时传递的name参数才是有效的了？
后续调用传递的name参数就没有意义了啊</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/68/7c/d4b4ed31.jpg" width="30px"><span>Kuz~</span> 👍（1） 💬（2）<div>“同时它还被注解“@Volatile”修饰了，这可以保证 INSTANCE 的可见性”
volatile在双重锁中不是为了禁止指令重排吗？</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/00/1df7bb5d.jpg" width="30px"><span>yvanbu</span> 👍（0） 💬（1）<div>「在日常的开发工作当中，我们有时会遇到这种情况：我们需要继承某个类，同时还要实现某些接口，为了达到这个目的，我们不得不定义一个内部类，然后给它取个名字。但这样的类，往往只会被用一次就再也没有其他作用了」关于这个场景能举一个例子吗，如果我只知道这种写法，却不知道具体的应用场景，这样我还是无法理解和掌握</div>2022-09-02</li><br/>
</ul>