你好，我是朱涛。

高阶函数在Kotlin里有着举足轻重的地位。**它是Kotlin函数式编程的基石，是各种框架的关键元素。**高阶函数掌握好了，我们理解协程的launch、async函数就会轻松一些，阅读协程的源代码也会不那么吃力；高阶函数理解透彻了，我们学习Jetpack Compose也会得心应手，在特定业务场景下，我们甚至可以用它来实现自己的DSL（Domain Specific Language）。

不过，如果你没有函数式编程的相关经验，在初次接触高阶函数的时候，很可能会被绕晕。因为它是一个全新的概念，你很难从经典的C/Java里找到同等的概念迁移过来（Java从1.8开始才引入相关概念）。然而，对于高阶函数这么重要的概念，Kotlin官方文档又惜字如金。

文档里只是突兀地介绍了高阶函数、函数类型、Lambda表达式的简单用法，接着就丢出一段复杂的代码案例，然后丢出一个更复杂的概念，“带接收者的函数类型”（Function Types With Receiver），接着又丢出了一段更复杂的代码案例。说实话，这真的让人难以理解。

所以今天这节课，我会采用Java和Kotlin对照的方式，来给你讲解Kotlin高阶函数的核心概念。并且我会通过一个实际案例，来帮助你理解其中最晦涩难懂的“带接收者的函数类型”，为你今后的Kotlin学习之路打下坚实的基础。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/71/7b/4b6079e6.jpg" width="30px"><span>侯金博</span> 👍（13） 💬（4）<div>遭了，是要掉队的感觉</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/77/a2/7e9ae0b9.jpg" width="30px"><span>讲道理嘛</span> 👍（8） 💬（1）<div>老师你好，关于带接收者的函数类型，我这样理解不知道对不对？
fun User.test1(block: (user: User) -&gt; Unit){}
fun User.test2(block: User.() -&gt; Unit){}

上面这两个高阶函数其实是等价的，只是在 lambda 表达式的使用时有区别。
前者的参数是 it，后者是 this(this 可以省略)</div>2022-05-20</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（6） 💬（1）<div>run：调用一个函数，作用仅仅限于构建lambda方便一点
带receiver的run：调用一个带receiver的函数，把this传给这个函数
with：用第一个参数调用第二个带receiver的函数，把this设定为第一个参数
apply：带receiver的函数高阶函数，参数为带receiver的函数，接受一个对象，把这个对象作为this传给参数并调用，返回this
also：和apply类似，但是参数是带一个参数的函数，接受对象传给参数，其余和apply一样
let：和apply类似，但是返回值不是this，而是函数的返回
takeIf：带receiver的函数高阶函数，参数是一个判断函数，结果判断结果为真就返回this，否者null
takeUnless：和take相反
repeat：参数为次数和函数，for循环执行函数
</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/01/05/b70b8ea1.jpg" width="30px"><span>女孩子家家</span> 👍（6） 💬（1）<div>简化了页面跳转~
private const val FRIEND_ID = &quot;friendId&quot;

fun goto(mContext: Context, userId: Long) {
    mContext.goto&lt;ChatActivity&gt; {
		putExtra(FRIEND_ID, userId)
    }
}

inline fun &lt;reified T&gt; Context.goto(block: Intent.() -&gt; Unit) {
    this.startActivity(intent&lt;T&gt;(this, block))
}

inline fun &lt;reified T&gt; intent(mContext: Context, block: Intent.() -&gt; Unit): Intent {
    val intent = Intent(mContext, T::class.java)
    intent.block()
    return intent
}</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/47/b0/8c301d00.jpg" width="30px"><span>H.ZWei</span> 👍（5） 💬（1）<div>带接收者的函数类型能不能理解成是这个类的扩展函数，只不过是一个匿名函数。</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/45/e3dd6a83.jpg" width="30px"><span>大顺子</span> 👍（2） 💬（1）<div>1.第一个 run ，返回值为函数体最后一行，或指定 return 表达式
2.第二个 run ,在函数体中可以用 this 指代该对象，返回值为函数体最后一行，或指定 return 表达式
3.with 是将对象作为参数，在函数体中可以用 this 指代该对象，返回值为函数体最后一行，或指定 return 表达式
4.apply 在函数体内可以用 this 指代该对象，返回值为对象本身
5.also 在函数体内可以用 it 指代该对象,返回值为对象本身
6.let 在函数体内可以用 it 指代该对象,返回值为函数体最后一行，或指定 return 表达式
理解了上面那些，剩下的 takeIf 、takeUnless、repeat 就很好理解了。</div>2022-01-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqT3pba9RQEXAOHiaOMm3ibSicngJj3LAHaAQ9pa5N1I6A4RwNQ97LQeFAnLkQgaXBjHpW9xPYQVTaIA/132" width="30px"><span>Geek_518c5c</span> 👍（1） 💬（3）<div>
fun User.apply(block: User.() -&gt; Unit): User{   请教这里的 User.()中的（）代表什么意思。
</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/37/15baf151.jpg" width="30px"><span>neo</span> 👍（1） 💬（1）<div>&#47;&#47; 函数引用 
override val creator = ::PersonManager
函数引用中需要怎么去理解参数呢，因为并没有传参的地方</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（1） 💬（1）<div>感觉带接收者函数类型讲的太复杂了，单独抽出来放到后面某个章节讲更好一点。</div>2022-02-13</li><br/><li><img src="" width="30px"><span>20220106</span> 👍（1） 💬（3）<div>apply和also这两个比较典型的，上下文对象作为【接收者】和作为【参数】，这两个的区别没太领会到</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/af/e0/69a94af6.jpg" width="30px"><span>zeki</span> 👍（1） 💬（2）<div>“第4种写法 由于 Kotlin 支持类型推导，所以 View 可以被删掉：”大佬您好，这句话是否不太准确？我的理解是：正常情况下，Kotlin的参数类型是不可以省略的，这里的View可以被删掉的原因不是因为“Kotlin 支持类型推导，所以 View可以被删掉”，而是因为如下代码所示：
fun setOnClickListener(l: ((View!) -&gt; Unit)?) 
这个方法的参数变量 l 声明了函数类型为((View!) -&gt; Unit)?,所以Lambda的参数部分（：View）可以省略
就像
val test={x,y-&gt;x+y} 是错误的
而
val test:(Int,Int)-&gt;Int={x,y-&gt;x+y}是正确的一样
我理解的类型推导是“根据具体值来推导出类型”，而参数的值是不定的，所以参数的类型必须显式声明，返回值的类型是由参数的类型和值具体得出来的值,所以可以不需要显式声明,我这么想是否正确呢？</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/25/da/f8eb4742.jpg" width="30px"><span>没有昵称</span> 👍（0） 💬（4）<div>fun handleTwoParameters(a: Int,b: Int):(Int,Int) -&gt;Int{
    return plusTwo
}
val plusTwo:(Int,Int)-&gt;Int={x,y-&gt;x+y}

各位大佬，如何把a和b的入参传给plusTwo使用</div>2022-05-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqT3pba9RQEXAOHiaOMm3ibSicngJj3LAHaAQ9pa5N1I6A4RwNQ97LQeFAnLkQgaXBjHpW9xPYQVTaIA/132" width="30px"><span>Geek_518c5c</span> 👍（0） 💬（1）<div>老师，
&#47;&#47;              带接收者的函数类型
&#47;&#47;                     ↓  
fun User.apply(block: User.() -&gt; Unit): User{    问1：User.()是什么意思 问2这一个行代表定义了一个User的扩展函数，对吗
&#47;&#47;  不用再传this  
&#47;&#47;       ↓ 
    block()
    return this ------问3，这个this指向的是什么
}
</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>顶级扩展函数编译成字节码，是 static 方法，参数多了一个 this

带接收者的函数类型编译成字节码，是一个匿名内部类，实现了 Functionx 接口，invoke 参数由编译器传入接收者实例；</div>2022-04-04</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（1）<div>带接受者的函数，和C++的成员函数指针很像，限定了函数必须是类成员函数或者扩展函数。这带来了定义者和调用者两方面的变化:定义者可以方便的的引用类的公有成员和函数，调用者只能是类的成员函数或者扩展函数。apply函数是高阶函数，接受一个带接受者的函数，然后调用这个函数，并输出接受者对象。利用Lambda表达式,这个带接受者的函数在调用apply的地方构建出扩展函数，并传入apply，apply注入了this，调用函数和输出。如果没有带接受者的函数，函数就没法注入this和返回this，这对于apply这样的函数，就必须增加一个参数处理调用者，会繁琐很多。
</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/01/50/c1556a25.jpg" width="30px"><span>爱学习的小羊</span> 👍（0） 💬（1）<div>我怎么感觉这样代码事简洁了，但是对于不了解Lambda的人来说，阅读更费劲了</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/4e/1c654d86.jpg" width="30px"><span>Omooo</span> 👍（0） 💬（1）<div>老师想问一下，如果把 creator 定义成参数有多个的函数类型，该怎么去做呀？也没办法写成 
protected abstract val create: (vararg params: P) -&gt; T 呀？</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/4c/05/4fe55808.jpg" width="30px"><span>没名儿</span> 👍（0） 💬（1）<div>对于初学者,好多关键字,根本不知道,只能说理解概念吧,能看懂没天分还是放弃吧....</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f2/c7/c5855ff3.jpg" width="30px"><span>l-zesong</span> 👍（0） 💬（1）<div>带接收者函数类型，看完了，我感觉像是把扩展函数当做参数来传递，就是省了去写一个扩展函数？</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（0） 💬（1）<div>感觉高阶函数的作用就是能作为参数传递..</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/5c/a786deb5.jpg" width="30px"><span>提醒圈圈去看书</span> 👍（0） 💬（1）<div>老师，想要请教下，为什么user?.apply{}
为什么不能反推成
fun User.apply(block: (User) -&gt; Unit): User {
    block(this)
    return this
}呢</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/a7/ac23f5a6.jpg" width="30px"><span>better</span> 👍（0） 💬（1）<div>17年，我们内部组织培训kt，讲到这个 带接受者的函数类型，实在不好理解，大家晕乎乎滴。。。
看了老师的这个课，就很好理解啊，哎，自己太笨了，太笨了~~~。感谢分享~</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/06/e5/51ef9735.jpg" width="30px"><span>A Lonely Cat</span> 👍（0） 💬（1）<div>
import androidx.recyclerview.widget.RecyclerView

&#47;**
 * Returns `true` if this adapter content is not empty.
 *&#47;
inline fun &lt;reified VH : RecyclerView.ViewHolder&gt; RecyclerView.Adapter&lt;VH&gt;.isNotEmpty() =
    itemCount != 0

&#47;**
 * Returns `true` if this adapter content is empty.
 *&#47;
inline fun &lt;reified VH : RecyclerView.ViewHolder&gt; RecyclerView.Adapter&lt;VH&gt;.isEmpty() =
    itemCount == 0
</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c7/5c/94cb3a1a.jpg" width="30px"><span>$Kotlin</span> 👍（0） 💬（1）<div>看了3遍，才感觉好像刚刚摸到了门槛。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/8c/3c/bb79b9d7.jpg" width="30px"><span>Will</span> 👍（0） 💬（1）<div>宁缺毋滥，但愿后面都是能将复杂问题说清晰的文章。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/06/e5/51ef9735.jpg" width="30px"><span>A Lonely Cat</span> 👍（0） 💬（1）<div>repeat 
原理：给定的 Lambda（action） 表达式本质上是一个匿名类的单抽象方法，该扩展函数通过 for 循环调用。由于有 inline 关键字，所以在编译后该段代码的逻辑会复制到使用的地方，这样在性能上也能够得到满足。
意义：将给定的 Lambda（action） 表达式执行 times 次，简化 kotlin 中的 for 循环。</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/4c/05/4fe55808.jpg" width="30px"><span>没名儿</span> 👍（17） 💬（9）<div>作者你好,提个意见,授课本来是一个循循渐进的事情,你这讲到最后,待接收者的函数类型,感觉直接垮了一个坑,各种概念都不清楚就直接拿来用了,我感觉十个人有九个都会掉坑里,本来感觉是一步一步的学习,这样一下就掉坑里了...希望这些跨度比较大的可以放到后面再讲....</div>2022-02-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIGQglR97QjFRXUIn1Qc3PcjcGhV4YCiaJoNv72RCUZEteMMSazdF6MsglUNkjfiaPM5GBicek8nAo8IaPHAhuFryQeDDrEZPRX3GVYjxJiauFiclg/132" width="30px"><span>程序员999</span> 👍（0） 💬（0）<div>你好作者，View！后面这个感叹号怎么理解？</div>2024-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ed/c5/036cb044.jpg" width="30px"><span>墨水</span> 👍（0） 💬（0）<div>突然想起在effective java中描述过，如果函数对象都是相同的处理逻辑，可以使用方法引用（this::gotoPreview）</div>2023-06-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qYNE3cTy33hHGfKor4e8ICIWupD5lBE7LRTBhabko3MAXXua9rBd86BYzlC9C5jeLNgnzmoG8o3RNSFPRWbqXQ/132" width="30px"><span>Geek_4f3885</span> 👍（0） 💬（0）<div>大佬，如果是多个参数的单例，有示例吗，单例那块没看懂</div>2022-10-25</li><br/>
</ul>