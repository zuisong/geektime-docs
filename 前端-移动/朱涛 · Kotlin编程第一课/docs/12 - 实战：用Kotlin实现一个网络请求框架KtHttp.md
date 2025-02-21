你好，我是朱涛，又到了实战环节。

在前面几节课当中，我们一起学习了Kotlin的委托、泛型、注解、反射这几个高级特性。那么今天这节课，我们将会运用这些特性，来写一个**Kotlin版本的HTTP网络请求框架**。由于它是纯Kotlin开发的，我们就把它叫做是KtHttp吧。

事实上，在Java和Kotlin领域，有许多出色的网络请求框架，比如 [OkHttp](https://github.com/square/okhttp)、[Retrofit](https://github.com/square/Retrofit)、[Fuel](https://github.com/kittinunf/fue)。而我们今天要实现的KtHttp，它的灵感来自于Retrofit。之所以选择Retrofit作为借鉴的对象，是因为它的底层使用了大量的**泛型、注解和反射**的技术。如果你能跟着我一起用泛型、注解、反射来实现一个简单的网络请求框架，相信你对这几个知识点的认识也会更加透彻。

在这节课当中，我会带你从0开始实现这个网络请求框架。和往常一样，为了方便你理解，我们的代码会分为两个版本：

- 1.0 版本，我们会用Java思维，以最简单直白的方式来实现KtHttp的基础功能——同步式的GET网络请求；
- 2.0 版本，我们会用函数式思维来重构代码。

另外，在正式开始学习之前，我也建议你去clone我GitHub上面的KtHttp工程：[https://github.com/chaxiu/KtHttp.git](https://github.com/chaxiu/KtHttp.git)，然后用IntelliJ打开，并切换到**start**分支跟着课程一步步敲代码。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（8） 💬（1）<div>勉强能看明白，但这代码谁能手写的出来呀？

就算写出来了，谁保证没 bug？谁能保证别人能看明白？谁能保证后续能维护？</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a6/f0/50d0931d.jpg" width="30px"><span>木易杨</span> 👍（3） 💬（1）<div>Kotlin这语法越写越变态。Java啰嗦吧，起码能看懂，没那么多语法题</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c7/5c/94cb3a1a.jpg" width="30px"><span>$Kotlin</span> 👍（3） 💬（1）<div>动图看起来不太方便，不能暂停，而且这个动图好长。</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ec/b0/4e22819f.jpg" width="30px"><span>syz</span> 👍（2） 💬（1）<div>动态代理的那张动图，播放中不能暂停，要懂这样过一遍没毛病。建议将每一次停顿变成带序号的标注，贴代码上来感觉会好点。</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/3c/d72b0d26.jpg" width="30px"><span>面无表情的生鱼片</span> 👍（2） 💬（1）<div>请教老师，如果 method.genericType 是 kotlin 的 Basic Type 的话（例如：String、Int），要怎么做兼容比较好呢？</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2a/57/6629c858.jpg" width="30px"><span>阿康</span> 👍（2） 💬（3）<div>Lambda 表达式当中的返回语法 能讲下吗？或者给个相关的博客连接</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/92/76/343c8497.jpg" width="30px"><span>河山</span> 👍（1） 💬（1）<div>请问老师 像如下代码 
fun &lt;T&gt; Int.toType():T{
    return (this as T)
}
class Animal{}
fun main() {
    println(100.toType&lt;Animal&gt;())
}
这个不应该有类型转换异常吗 为什么我运行没有报异常 而且会输出100  但是debug模式 去运行100.toType&lt;Animal&gt;()  这个表达式 却的确会提示类型转换异常 老师 为什么运行没问题啊 </div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（0） 💬（3）<div>操作符太多了，日常写业务不常用的话很快就忘了。不知道老师是如何知道这么多没听过的操作符（filterIsInstance、fold）🥲。</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/95/f9/0d4801ce.jpg" width="30px"><span>山河入梦</span> 👍（0） 💬（1）<div>&#47;&#47; 这种写法是有问题的，但这节课我们先不管。
我想问下老师，这种写法的问题在哪，因为我一直这样写来着，从昨天看了文章，就一直纠结着</div>2022-02-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Urc67zDC8R6dh9U1ZFTF36icXewM1seehvOUYUs4hyWSsFzS5WQc2RcrE1Mzs8qtgib5SM5wFrVh22QcQd0JUUBw/132" width="30px"><span>jim</span> 👍（0） 💬（1）<div>kotlin确实很优雅，有时候写着写着看不懂了！</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/99/f133c8ff.jpg" width="30px"><span>梦佳</span> 👍（0） 💬（3）<div>运行不起来</div>2022-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/52/ba/25f8f998.jpg" width="30px"><span>只为你停留</span> 👍（0） 💬（3）<div>mapIndexed { index, it -&gt; Pair(it, args[index]) }
这个函数中 it -&gt; Pair(it, args[index] 怎么理解呢，尤其不理解 it -&gt;</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f2/c7/c5855ff3.jpg" width="30px"><span>l-zesong</span> 👍（0） 💬（1）<div>return@newProxyInstance  是什么意思啊？没看懂</div>2022-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/d5/93b704b6.jpg" width="30px"><span>sunlight</span> 👍（0） 💬（2）<div>有个地方疑惑，动态代理一般会有两种使用方式吗？

方式一 create()方法中会多传个被代理对象，通过method.invoke(被代理对象)，实现拦截。外层返回代理对象
方式二 create()方法中只会有接口，没有手动实现被代理对象。因为我们不关心接口的具体实现，只关心接口中的注解参数，拦截获取到参数即可

文中是使用第二种，并没有手动实现被代理对象，只是最终返回了代理对象。请问这样理解对么
</div>2022-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/f4/27a5080a.jpg" width="30px"><span>7Promise</span> 👍（0） 💬（1）<div>深奥的东西在经过学习原理后都是会有恍然开朗的感觉。</div>2022-01-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/OYhGKRZF1Afr76s8VZzVPCuN0icckfnk6L30e70hnmauDMRWDCOHicUicl6WaH071MSB525U2JqfWpYic5VbglHWRQ/132" width="30px"><span>Geek_981acf</span> 👍（0） 💬（0）<div>好难啊</div>2023-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/09/cc/3543fb8f.jpg" width="30px"><span>独饮敌敌畏丶</span> 👍（0） 💬（0）<div>一下子把困扰我多年的动态代理、反射和retrofit原理解决了，牛！！！</div>2023-02-19</li><br/><li><img src="" width="30px"><span>Geek_416c20</span> 👍（0） 💬（0）<div>现在的基地址是有效的吗? 请求发生了这个错误
 javax.net.ssl.SSLProtocolException: Connection reset, javax.net.ssl.SSLProtocolException: Connection reset</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1b/f9/018197f1.jpg" width="30px"><span>小江爱学术</span> 👍（0） 💬（0）<div> val url = baseUrl + annotation.value
这行代码循环拿的是get注解的值，只能拿到path，拿不到parameters吧。

感觉可以再加一个注解，就像feignclient一样，作用在接口上，可以指定baseurl。</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（0） 💬（0）<div>mapIndexed -&gt; zip

    fun invoke(url: String, method: Method, args: Array&lt;Any&gt;): Any? =
        method.parameterAnnotations
            .takeIf { it.size == args.size }
            ?.zip(args)
            ?.fold(url, ::parseUrl)
            ?.let { Request.Builder().url(it).build() }
            ?.let { okHttpClient.newCall(it).execute().body?.string() }
            ?.let { gson.fromJson(it, method.genericReturnType) }
}</div>2022-07-28</li><br/>
</ul>