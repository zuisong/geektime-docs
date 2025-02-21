你好，我是戴铭。

提到Object-C中的Runtime，你可能一下就想到了iOS的黑魔法Method Swizzling。毕竟，这个黑魔法可以帮助我们在运行时进行方法交换，或者在原方法执行之前插入自定义方法，以保证在业务面向对象编程方式不被改变的情况下，进行切面功能的开发。但是，运行时进行方法交换同时也会带来一定的风险。所以，今天我就来和你详细聊聊Runtime Method Swizzling 的原理。

Runtime Method Swizzling 编程方式，也可以叫作AOP（Aspect-Oriented Programming，面向切面编程）。

AOP 是一种编程范式，也可以说是一种编程思想，使用 AOP 可以解决 OOP（Object Oriented Programming，面向对象编程）由于切面需求导致单一职责被破坏的问题。通过 AOP 可以不侵入 OOP 开发，非常方便地插入切面需求功能。

比如，我在专栏[第9篇文章](https://time.geekbang.org/column/article/87925)中介绍无侵入埋点方案时，就提到了通过 AOP 在不侵入原有功能代码的情况下插入收集埋点的功能。

除此之外，还有一些主业务无关的逻辑功能，也可以通过 AOP 来完成，这样主业务逻辑就能够满足 OOP 单一职责的要求。而如果没有使用 AOP，鉴于OOP的局限性，这些与主业务无关的代码就会到处都是，增大了工作量不说，还会加大维护成本。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/01/a8d3db35.jpg" width="30px"><span>Vicky</span> 👍（21） 💬（1）<div>戴老师：
   “第三个风险是，交换的方法如果依赖了 cmd，那么交换后，如果...”这句话有点不太理解，能做个详细的阐述吗？交换方法在什么情况会依赖cmd？不是特别理解，谢谢~</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e9/58/397a4ab2.jpg" width="30px"><span>daniel</span> 👍（19） 💬（0）<div>cmd是指每个函数中都会存在的一个隐藏参数，比如我们想要知道当前函数的名字可以通过在函数内部NSStringFromSelector(_cmd)打印当前函数名字，方法交换后显然原方法的cmd不同了，就跟评论其他人说的差不多，假如原函数有些逻辑是对_cmd进行的，这时候就会出现奇怪的错误。</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/51/870a6fcb.jpg" width="30px"><span>Trust me ҉҉҉҉҉҉҉❀</span> 👍（10） 💬（0）<div>aspect风险才多 bug也多</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/19/4f9dc4b5.jpg" width="30px"><span>帅气潇洒的豆子</span> 👍（7） 💬（1）<div>问题跟Vicky 朋友一样，我不清楚这里的cmd指的是什么，谢谢</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/15/88/e0845b51.jpg" width="30px"><span>Usama Bin Laden</span> 👍（6） 💬（0）<div>方法交换，都没用过库，都是直接写的。。。</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e8/15/c60311ab.jpg" width="30px"><span>Realtime</span> 👍（5） 💬（0）<div>老师，swift 有 相关功能么？ 没有的话，怎么做无侵入埋点呀。苹果为啥把动态功能去掉了，怎么考虑的呀？有相关的替代方法么？</div>2019-05-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoGRhUIWgJcgLOkpH6p4EfxVGvF0daA9r91CoEcJ0lRIAiad8FJFzf4WVHgJRh0OdicX5PZ2MpWCV0Q/132" width="30px"><span>bart</span> 👍（4） 💬（1）<div>@Vicky 我帮你举个栗子
当你在运行时替换某对象中的某函数实现时，如果需要在替换函数中调用原始函数实现，则可以使用cmd。

 1.创建新类继承老类实现相同的函数
 2.在老类的分类的函数中将被hook的类的isa指向新类(也就是修改了元类)
 此时的实例实际上就是新创建子类的实例了
 3.所以此时调用实例的函数就会调用子类的函数
 4.(可选：在子类中动态获取父类，调用父类的eat函数)就是这步，可以使用cmd。

</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/05/b662ff98.jpg" width="30px"><span>席🍐🍎</span> 👍（3） 💬（0）<div>@Vicky 那是指方法内部对cmd做了判断，运行特殊的逻辑，进行swizz之后原方法的cmd会变，可能会导致逻辑错误</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/6c/19/d6814107.jpg" width="30px"><span>王万杰</span> 👍（2） 💬（0）<div>Aspects性能不如Stinger，是大不如</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/1d/ed26272a.jpg" width="30px"><span>Chouee</span> 👍（1） 💬（0）<div>原来纯OC开发，Aspect无埋点统计用得66的。自从混编了之后。。。🕳🕳🕳</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/40/3f/63fc1b53.jpg" width="30px"><span>筇琼</span> 👍（1） 💬（2）<div>戴老师你好，用 Aspects 进行方法拦截时，如何实现带有返回值方法的替换？此时的返回值由我自己定义，而调用原方法的对象可以得到这个返回值。</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/58/abb7bfe3.jpg" width="30px"><span>Kai</span> 👍（1） 💬（0）<div>swift怎么进行类似method swizzling的技术呢？</div>2019-05-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epVhRFBLPOic3kUju3dkpmwEeI1aBxy7WSGtq5smkicKz4bTbicsSElekSjnBhCQvibncVOHBHeY6pnuA/132" width="30px"><span>hopestar90</span> 👍（1） 💬（0）<div>Aspects确实在做hook上很有想法，不仅能对类做hook，还能对单独实例做hook。但是本质上他用了消息转发流程，作者也说了 不适合于高频度调用的方法</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/01/cc4d66ea.jpg" width="30px"><span>马小平</span> 👍（0） 💬（0）<div>Runtime Method Swizzling 背后的原理是什么？怎么没看到</div>2023-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/26/77f1900a.jpg" width="30px"><span>小良</span> 👍（0） 💬（0）<div>我觉得文章所说的「风险」，应该是注意事项吧：① 在 +load 方法交换（调用前完成方法的交换）；② 需要避免父类交换；③ 这个的确我之前没想到，可能我没有试过在方法里使用 _cmd 来做一些业务逻辑吧；④ 方法交换命名冲突（注意加前缀）🐶</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b3/48/353f9e32.jpg" width="30px"><span>henry_shr</span> 👍（0） 💬（0）<div>类方法和实例方法可以交换么</div>2020-10-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epzwbJGbUmgEC77J6QY6A5pLPdPbw7sqk4DcsHK8qPw7OiaiaMD7pjzb8uHlkY5uLZRibWVvPDDAgM5A/132" width="30px"><span>mersa</span> 👍（0） 💬（0）<div>说的那个_cmd风险，Aspect也存在的。hook方法以后原方法打印_cmd是aliasSelector</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ff/d3/f249eefe.jpg" width="30px"><span>iHTC</span> 👍（0） 💬（0）<div>【Swift能不能用hook？】
我们与 Runtime 进行交互的只能通过下面三种方式：

1、Objective-C Source Code： 这个最直接，我们写的 OC 代码最终都会被转换为运行时的代码，在程序运行的时候执行的就是这些运行时代码。比如发送、转发消息等等。

2、NSObject Methods： OC 中，除了 NSProxy 这个类之外，其他所有的类都继承自 NSObject。而 NSObject 中有着类似 class,isKindOfClass,respondsToSelector 这样的方法，他们都是通过 Runtime 来实现的。

3、Runtime Functions： 在 &#47;usr&#47;include&#47;objc 这个目录中可以找到 Runtime 暴露出来的一些函数和数据结构，通过这些接口我们可以使用一些更高级的操作。比如 Method Swizzle,AssociatedObject 等等。

所以，如果用Swift写的代码继承于 NSObject就可以hook，了解更多，可以看这个文章 https:&#47;&#47;juejin.im&#47;entry&#47;5e3c30cd6fb9a07cad3b8d98</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/67/e91fe8d3.jpg" width="30px"><span>景天儿</span> 👍（0） 💬（0）<div>cmd就是_cmd吧，意思是swizz的方法中，使用了_cmd这个宏定义。</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/67/e91fe8d3.jpg" width="30px"><span>景天儿</span> 👍（0） 💬（0）<div>这篇关于Aspect为什么更安全，也就是他填坑的原理，讲的有点儿抽象……</div>2019-06-08</li><br/>
</ul>