你好！我是郑晔。

在前面，我们花了三讲的篇幅探讨程序设计语言，一方面是为了增进我们对程序设计语言的理解，另一方面，也希望从中学习到软件设计方面做得好的地方。除了借鉴一些语言特性之外，我们还能怎样应用程序语言，来帮我们做设计呢？

讲到程序设计语言模型时，我说过，程序设计语言的发展趋势，就是离计算机本身越来越远，而离要解决的问题越来越近。但通用程序设计语言无论怎样逼近要解决的问题，它都不可能走得离问题特别近，因为通用程序设计语言不可能知道具体的问题是什么。

这给具体的问题留下了一个空间，**如果我们能把设计做到极致，它就能成为一门语言**，填补这个空间。注意，我这里用的并不是比喻，而是真的成为一门语言，一门解决一个特定问题的语言。

![](https://static001.geekbang.org/resource/image/fd/c6/fd861a726b8a85d1d22ca56b78515cc6.jpg?wh=2284%2A1191)

这种语言就是领域特定语言（Domain Specific Language，简称 DSL），它是一种用于某个特定领域的程序设计语言。这种特定于某个领域是相对于通用语言而言的，通用语言可以横跨各个领域，我们熟悉的大多数程序设计语言都是通用语言。

我在[第8讲](https://time.geekbang.org/column/article/245868)说过，它们都是图灵完备的，但DSL不必做到图灵完备，它只要做到满足特定领域的业务需求，就足以缩短问题和解决方案之间的距离，降低理解的门槛。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/cc/ca22bb7c.jpg" width="30px"><span>蓝士钦</span> 👍（37） 💬（1）<div>SQL也是一种DSL，他屏蔽了计算机存储的底层实现，提供了易于操作数据的接口。
一些ORM框架对SQL这些DSL进行了进一步的封装提供了声明式注解，相当于构建在DSL之上的DSL翻译器。面向对象编程将面向关系的DSL进行更高层次的封装，使得在编程这个特定领域更加易于使用。</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/92/ce/9d24cb2c.jpg" width="30px"><span>峰回路转</span> 👍（21） 💬（1）<div>普通程序员的关注点只在于功能如何实现，而优秀的程序员会懂得将不同层次的代码分离开来，将意图和实现分离开来，而实现可以替换。

老师 意图和实现具体指什么还是不太明白，</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/61/76b1b888.jpg" width="30px"><span>被雨水过滤的空气</span> 👍（13） 💬（1）<div>高级编程语言是低级编程语言的DSL。</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/4f/bce0d5bc.jpg" width="30px"><span>哈哈</span> 👍（13） 💬（1）<div>我觉得markdown应该算一个</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/8d/a2a4e97e.jpg" width="30px"><span>Atong</span> 👍（9） 💬（1）<div>许多同学的评论里列举了许多场景，例如UML,markdown虽不能执行，不能算是DSL。但其中将意图和实现分离的理念，应该是一致的。 
DSL的一个深意是在于描述意图而不是描述过程。 那其实取名字也可以理解为一种意图的表现。例如菜单上的蓝莓蛋糕，就是一种意图描述，而不是过程描述：我要一个蛋糕，然后上面要加上一些蓝莓。</div>2020-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（7） 💬（2）<div>1.k8s和docker-compose的yml文件，就是声明试编程。算是外部dsl。

2.本章疑问： dsl和接口有何异同点？

首先dsl和接口都做了一件事，就是意图和实现的分离。但是dsl的语义（意图）是可以灵活组织的，而接口的语义基本靠接口命名和方法命名来阐述，在灵活性上明显是不足的。

如何去实现dsl？第一感觉就是建造者模式。这里实现就有分支。第一种是将要执行的业务逻辑（实现）写在dsl实体bean内部。在所有业务功能都由实体内部属性决定时，这是可行的（领域模型的行为）；第二种是将执行的业务功能注入要创建的dsl实体，然后回调。毕竟复杂业务流程的组织不该是单个实体能够囊括的，而且我们的功能代码大部分还是面向过程的（java就是一个service注入一个service，然后嵌套调用）；第三种就是将dsl实体作为入参传入接口方法，然后通过其属性调整业务流向，控制代码逻辑。这种方式我认为是开发维护成本最低的（面向过程不好，但他简单呀，不需要什么设计知识背书，懂语法就能看懂），但是我在某本书看到过，“程序的逻辑不该由入参去控制”。是定制多个接口方法。还是提供统一方法由入参调度逻辑，真的不好说孰好孰劣。

</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/c5/3c/d589ef4d.jpg" width="30px"><span>蜗牛不会飞</span> 👍（6） 💬（1）<div>Quartz等调度框架常用的Cron表达式也是一种DSL吧</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2e/01/14a478bb.jpg" width="30px"><span>happychap</span> 👍（6） 💬（1）<div>drone.io用的.drone.yml，jenkins用的pipefile都算是轻量级的dsl。uml算不算是一种重量级的dsl呢？</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（5） 💬（1）<div>DSL是为了解决某个特定领域的程序设计语言。
作为一个客户端APP开发者，最常用到的莫过于gradle。
现在JAVA后端程序主要是通过pom配置构建，它其实就是通过xml来实现DSL，
我觉得后端程序通过gradle构建也将会成为主流。它比xml更加灵活，表达性更强
要设计一个DSL就要构建一个模型，通过接口将能力暴露出来。
如何暴露接口就可以分为内部DSL和外部DSL，内部DSL使用编程语言如JAVA来实现，外部则使用类似xml语言来实现，或者自己设计语法
实现内部DSL要将意图与实现区分开，这在程序设计中一个重要的原则</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/f2/2a9a6e9a.jpg" width="30px"><span>行与修</span> 👍（4） 💬（1）<div>lambda，网络协议描述算不算是dsl呢？</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（3） 💬（1）<div>我还没有到“设计一个 DSL”的高度，而且可能日常工作中遇到的问题也没有需要一门新的 DSL 来解决。

正则表达式、配置文件和 SQL 都可以算作 DSL，这些都是受众比较广泛的，如果是自己设计一个，使用的人没有那么多，还有意义么？

看了内部 DSL 的 Computer 的例子，感觉 DSL 不那么可怕了；顺便理解了为什么这“一连串的方法调用”可以被接受——因为这是一段声明 What。

反之，如果是一连串的动作，就应该避免了。

虽然短时间内估计不会有设计 DSL 的机会，不过“编写有表达性的代码”，“分离意图和实现”是我可以追求的目标。

看到留言里面有同学说可以把 Markdown 也当做一种 DSL，那么其针对的领域是什么呢，排版？</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（1） 💬（1）<div>老师能否分享一个自定义的DSL？</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/84/0d/4e289b94.jpg" width="30px"><span>三生</span> 👍（1） 💬（1）<div>sdk也应当是一种dsl</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/56/05459f43.jpg" width="30px"><span>Geek_h6mwnx</span> 👍（1） 💬（1）<div>ansible-playbooks的yml文件应该也能看成dsl</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/63/487f537e.jpg" width="30px"><span>PM2</span> 👍（1） 💬（1）<div>1、redis的指令应该不算是dsl，而只是接口吧
2、linux的awk应该算是一种dsl。
</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f7/dd/c85f2065.jpg" width="30px"><span>阿崔cxr</span> 👍（1） 💬（1）<div>全文读完就感觉 DSL 其实就是个间接层，为什么要有这个间接层，为了就是能更简单的更快捷的解决问题。</div>2020-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/e1/b7be5560.jpg" width="30px"><span>sam</span> 👍（1） 💬（1）<div>如果这么说，移动端开发常用的Cocoapods也是一种DSL。</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/d0/4c/3e86714d.jpg" width="30px"><span>哦耶</span> 👍（0） 💬（1）<div>react的jsx和vue的template</div>2022-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/91/d0/35bc62b1.jpg" width="30px"><span>无咎</span> 👍（0） 💬（1）<div>Android Manifest, Layout以及其它的资源描述通过XML来表达的，其实也是一种DSL，使用aapt来编译，android.content.res.Resources来获取。</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/90/de8c61a0.jpg" width="30px"><span>dongge</span> 👍（0） 💬（1）<div>ansibe等一些自动化运维工具是运维领域的dsl</div>2021-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/d3/67bdcca9.jpg" width="30px"><span>林铭铭</span> 👍（1） 💬（0）<div>内部DSL：groovy，scala，jruby，外部DSL：xml，json，yml。</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/9c/a4bc748d.jpg" width="30px"><span>Janenesome</span> 👍（1） 💬（4）<div>业务开发中，经常会被问到一个问题：为什么实现上面要加多一层接口，面向接口和面向实现有什么区别？我们用的是贫血模式，的确看不出太大的区别，好像还多此一举了。

面向接口应该也算是分离意图和实现，现在我还没能回答这个问题，希望看完专栏之后能写出更好的代码，并能回答同事们的这个问题。</div>2020-10-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJRCtuJkpyy2NTTABPFibg2k9tZscOOKx9wu80a85d5HspCorO9Nibj7Z7q9v1icPTVm5ia52r0RCzEaA/132" width="30px"><span>Stay_Gold</span> 👍（0） 💬（0）<div>其实这个地方我个人的理解，DSL不是相当于接口。
DSL相当于一个模型，加上一个解析器也就是文中说的接口。</div>2025-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>看完内容和评论，对 DSL 的理解就是：用容易理解的语言去表达，至于表达背后的具体实现不需要描述</div>2023-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/33/b71635c1.jpg" width="30px"><span>锋子</span> 👍（0） 💬（0）<div>之前写过一个内部DSL，其实做的事情就是把各类客户端的查询条件，通过自己涉及的解析逻辑，转换成类似SQL的语句去查某种库。 
它表现形式其实就是借个几个大的接口。 比如分页查询，查全部，查数量等。
之所以区别于业务接口，就是它做了一些通用化设计，可以用在各种业务，而不仅限于某种特定的业务。</div>2023-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3c/1a/1806ef25.jpg" width="30px"><span>皇家救星</span> 👍（0） 💬（0）<div>markdown不能执行就不算dsl吗？那配置文件也不能执行呀。 感觉markdown语法跟sql语法一样，声明效果，由程序根据声明执行，也算dsl</div>2022-12-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/QvyPibAqLH5uEr7GNL6Lg9jT9sUs9jtub4LvO575nHuT3viagzmvKLCwGQRicsiadic3n9lM62qQ6n5shHfXUYib8Ktg/132" width="30px"><span>Geek_0ba253</span> 👍（0） 💬（0）<div>mybatis 应该是属于外部DSL，JPA属于内部DSL，这样看JPA才是趋势。</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/bd/9e568308.jpg" width="30px"><span>Jim</span> 👍（0） 💬（0）<div>最近用json去描述一个抽象层次业务需求，把可配置的东西告诉业务可以怎么配置去实现功能，后面就确定交付边界了，然后就是不断完善解析这个json接口的代码逻辑。不知道算不算一个特定领悟的dsl</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>好的设计要迈向 DSL，我们可以从编写有表达性的代码起步--记下来</div>2022-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f7/0b/403fbeba.jpg" width="30px"><span>小凯</span> 👍（0） 💬（0）<div>有点晕</div>2021-10-17</li><br/>
</ul>