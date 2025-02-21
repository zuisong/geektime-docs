上一节课中，我们学习了模板模式的原理、实现和应用。它常用在框架开发中，通过提供功能扩展点，让框架用户在不修改框架源码的情况下，基于扩展点定制化框架的功能。除此之外，模板模式还可以起到代码复用的作用。

复用和扩展是模板模式的两大作用，实际上，还有另外一个技术概念，也能起到跟模板模式相同的作用，那就是**回调**（Callback）。今天我们今天就来看一下，回调的原理、实现和应用，以及它跟模板模式的区别和联系。

话不多说，让我们正式开始今天的学习吧！

## 回调的原理解析

相对于普通的函数调用来说，回调是一种双向调用关系。A类事先注册某个函数F到B类，A类在调用B类的P函数的时候，B类反过来调用A类注册给它的F函数。这里的F函数就是“回调函数”。A调用B，B反过来又调用A，这种调用机制就叫作“回调”。

A类如何将回调函数传递给B类呢？不同的编程语言，有不同的实现方法。C语言可以使用函数指针，Java则需要使用包裹了回调函数的类对象，我们简称为回调对象。这里我用Java语言举例说明一下。代码如下所示：

```
public interface ICallback {
  void methodToCallback();
}

public class BClass {
  public void process(ICallback callback) {
    //...
    callback.methodToCallback();
    //...
  }
}

public class AClass {
  public static void main(String[] args) {
    BClass b = new BClass();
    b.process(new ICallback() { //回调对象
      @Override
      public void methodToCallback() {
        System.out.println("Call back me.");
      }
    });
  }
}
```

上面就是Java语言中回调的典型代码实现。从代码实现中，我们可以看出，回调跟模板模式一样，也具有复用和扩展的功能。除了回调函数之外，BClass类的process()函数中的逻辑都可以复用。如果ICallback、BClass类是框架代码，AClass是使用框架的客户端代码，我们可以通过ICallback定制process()函数，也就是说，框架因此具有了扩展的能力。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/8e/a6/c3286b61.jpg" width="30px"><span>Java垒墙工程师</span> 👍（3） 💬（2）<div>回调的方式是不是打乱了系统调用的层次？相互依赖，依赖关系变得复杂</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（109） 💬（1）<div>模板方法和回调应用场景是一致的，都是定义好算法骨架，并对外开放扩展点，符合开闭原则；两者的却别是代码的实现上不同，模板方法是通过继承来实现，是自己调用自己；回调是类之间的组合。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/17/08/566fb246.jpg" width="30px"><span>L!en6o</span> 👍（79） 💬（4）<div>曾经重构代码对这模板模式和callback就很疑惑。个人觉得callback更加灵活，适合算法逻辑较少的场景，实现一两个方法很舒服。比如Guava 的Futures.addCallback 回调 onSuccess onFailure方法。而模板模式适合更加复杂的场景，并且子类可以复用父类提供的方法，根据场景判断是否需要重写更加方便。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（62） 💬（3）<div>callback和hook不是一个层面的东西，callback是程序设计方面的一种技术手段，是编程语言成面的东西，hook是通过这种技术手段实现的功能扩展点，其基本原理就是callback。比如windows api中提供的各种事件通知机制，其本身是windows开放给用户可以扩展自己想要的功能的扩展点，而实现这些功能的手段是callback。
只要编程语言支持传递函数作为参数，都可以支持callback设计，比如c，golang，javascript，python等。另外一些框架中提供的功能扩展点我们称之为hook，比如vue在其实例生命周期中提供的各种hook函数。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（44） 💬（5）<div>模板方法就是定义一个流程，每个流程结点可变的就是一个抽象spi，由不同实现去现。
解决的是一个复用与扩展问题。复用的是这个流程本身以及某些结点可以是默认实现。扩展的是有些结点是可以有不同实现的场景。
回调是一种交互方式，由调用者告诉被调用者：你做完后还要做一个事情，这个事情是什么。然后被调用者做完后就可以做这个指定的事情。回调倒不用强制和模板方法概念合在一起。</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/41/2d477385.jpg" width="30px"><span>柠檬C</span> 👍（20） 💬（2）<div>个人看法：模板模式关注点还是在类与对象上，通过继承与多态实现算法的扩展
回调关注点在方法上，虽然在java语言中不得不以匿名内部类的形式出现，但本质是将方法当做参数一样传递，有点函数式编程的意思了</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（12） 💬（2）<div>callback应该偏语言层面，hook偏业务层面，二者一个是概念，一个是具体的落地方式。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d0/e2/1d00c079.jpg" width="30px"><span>写代码的</span> 👍（11） 💬（2）<div>虽然模板模式和回调很像，甚至和可以互相替换，但是为了让它们的功能和名称更契合，我觉得按照这样原则来使用这两种方法是不是会更好些：如果预留的扩展点必须实现，因为这些扩展点包含和这个类本身相关的关键功能性代码，不实现的话这个类就是个半成品，无法使用，那么使用模板模式，因为模板模式使用的抽象类可以在与语言层面强制这些扩展点必须被实现；如果预留的扩展点可以不实现，或者这些扩展点的实现逻辑甚至可以和这个类完全无关，那么就使用回调,，回调使用的组合关系恰好可以让类和扩展点的实现进行解耦，比如按钮上的事件回调，回调中的逻辑和按钮这个类本身的功能并没有什么关系，甚至回调可以传 null。</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（6） 💬（1）<div>什么是“回调 ”？A注册一个函数到B，B执行某个函数时，会调用A注册的这个函数。
我见过的应用一般完全结束（关闭，收尾等）时用hook，其他情况用callback或者on...listener。这种区别更多是语意上的，不是实现上的。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（6） 💬（0）<div>Callback 是在一个方法的执行中，调用嵌入的其他方法的机制，能很好地起到代码复用和框架扩展的作用。在 JavaScript 中，因为函数可以直接作为另一个函数的参数，所以能经常看到回调函数的身影，比如定时器 setTimeout(callback, delay)、Ajax 请求成功或失败对应的回调函数等。不过如果滥用回调的话，会在某些场景下会因为嵌套过多导致回调地狱。

Hook 本质上也是回调，但它往往和一些场景性的行为绑定在一起。在浏览器环境中，我们可以通过 img.onload = func1 来让图片在加载完后执行函数 func1，某种意义上算是一种 Hook。此外在 js 的 vue 框架中，也提供了组件生命周期的 Hook，比如 beforeDestory 钩子函数会在组件即将被销毁前执行，常用于销毁一些当前组件才会用到的定时器。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/b5/ac717737.jpg" width="30px"><span>肖臧</span> 👍（5） 💬（0）<div>补充一下ResultSetExtractor类的extractData方法会回调RowMapper类的mapRow方法，在这里把ResultSet转成Entity实例，下面是具体的代码：
public List&lt;T&gt; extractData(ResultSet rs) throws SQLException {
	List&lt;T&gt; results = (this.rowsExpected &gt; 0 ? new ArrayList&lt;&gt;(this.rowsExpected) : new ArrayList&lt;&gt;());
	int rowNum = 0;
	while (rs.next()) {
		results.add(this.rowMapper.mapRow(rs, rowNum++));
	}
	return results;
}</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/73/a3/2b077607.jpg" width="30px"><span>Michael</span> 👍（5） 💬（1）<div>swift和OC的闭包也属于回调</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/c7/00e544c2.jpg" width="30px"><span>黄林晴</span> 👍（5） 💬（4）<div>打卡
回调接口如果定义了多个方法，不也需要全部实现吗

课后思考:
android 中有个hook 概念，多用于反射修改源码机制，进行插件化相关的开发</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/26/1015d573.jpg" width="30px"><span>gevin</span> 👍（3） 💬（0）<div>前面问老师一个在开发中，对模版模式和回调的使用如何取舍的问题。我自己思考如下：

1. 如果我们的业务场景是针对老师文中所说的“业务算法”，那两种方式都可以，如果回调不是太复杂，不会导致整个业务逻辑的混乱，那么回调可能是更优雅的一种方案
2. 有时我们面向的业务本身，可能就是一种模板，比如定义一种业务流程，具体实现是对这种模板的个性化，或者我们对场景是对一种工业加工工艺的数字化实现，这些场景，可以直接套用模版模式的逻辑，回调不能直观体现业务逻辑，就不用考虑了。</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/c4/8d1150f3.jpg" width="30px"><span>Richie</span> 👍（3） 💬（0）<div>Hook机制和观察者模式都是基于Callback来实现的，这两者又有什么区别呢？
是否可以理解为：
* Hook一般是同步阻塞回调，是对原应用、框架流程的干预和扩展；
* 观察者模式一般是异步非阻塞回调，主要实现的语义是当某个事件发生时，我可以做一些其他事情，比如发送通知、比如对事件源做一些额外的处理；
* Hook常用在框架层面，属于固定流程上一定会发生的；
* Event Listener则比较常用在具体应用中，事件是可能发生也可能不发生，而且不确定什么时候会发生的；</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（3） 💬（1）<div>回调函数是不是只能在同一个jvm下的 程序之间才能实现</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/27/32746bbf.jpg" width="30px"><span>大头</span> 👍（3） 💬（1）<div>java8支持参数传递，以及lambda的使用，也是对回掉的简化</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（2） 💬（1）<div> 模板方法的扩展是子类的实现，复用是父类的已有代码；而回调扩展是调用者传进来的调用对象，复用是被调用者的方法</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/cd/5363c8fa.jpg" width="30px"><span>Rain</span> 👍（2） 💬（0）<div>对于callback 和 hook 的提供意图来说，提供callback 的时候是希望在callback里面完成主要的工作。hook的目的则在于扩展。前者的提供者通常没我在默认实现，非常希望callback 完成具体任务，而hook是基本已经实现了大部分功能，如果需要特殊操作，那就在hook里面做。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/02/828938c9.jpg" width="30px"><span>Frank</span> 👍（2） 💬（0）<div>打卡 今日学习回调函数，收获如下: 回调是一种A调用B，B又回来调用A的一种机制。它有两种方式：同步回调和异步回调。它的功能与模版模式类似都是复用与扩展。回调采用的是组合方式，更加灵活。而模版模式采用的是继承，有单继承的局限，如果继承层次过深，后期不便于维护。自己在写JavaScript时，常常使用回调这种方式来完成需求，通过今日的学习，进一步加深了对回调机制的理解。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3d/00/7daa7403.jpg" width="30px"><span>Eden Ma</span> 👍（2） 💬（0）<div>CO中hook主要作用是AOP中插入其它的方法实现.Callback则一般指Block和通过协议在委托模式中传递数据等.</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/56/509535da.jpg" width="30px"><span>守拙</span> 👍（2） 💬（0）<div>打卡 Java和Kotlin中都是callback
Callback优于Template之处在于组合优于继承.
Callback的缺点是嵌套回调导致的回调地狱(Callback Hell)</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fe/2d/e23fc6ee.jpg" width="30px"><span>深水蓝</span> 👍（1） 💬（0）<div>突然觉得，模板模式像是设计好了流程，但没有设计细节，而这些细节如果不完成，框架是无法运行的。观察者模式则反过来，整个流程和细节都实现好了，有没有观察者整个流程都能正常运行。</div>2023-08-11</li><br/><li><img src="" width="30px"><span>Geek_7e0e83</span> 👍（1） 💬（0）<div>1.学习了这一节课，对于前一节课的答案有了新的回答。也就是对于有多个模板方法和需要实现的Method的类，我们可以重构为回调函数的形式。模板方法的入参是回调的接口，然后根据调用方的情况。选择自己要调用的模板方法，传入对应的回调接口的实现类即可完成。灵活，不需要实现其他的不使用的Method。

2.hook的函数一点像是异步的回调。不会阻塞原本的流程执行，算是回调的一种特殊情况吧。callback的话，就像文章中说的有同步回调和异步回调两种。hook是callback的一种表现形式。

我印象中git的版本控制软件中有提供hook的函数，供开发者可以再代码提交的时候加入hook事件，实现想要的需求，比如触发一下监控，记录提交日志、执行自定义的commit message的语法规范检查等。</div>2022-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/dc/58/81824956.jpg" width="30px"><span>meng</span> 👍（1） 💬（1）<div>java只能单继承，但是可以多实现接口，jdk1.8之后接口中提供了default方法，是否也可以用作模板方法模式</div>2021-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/41/411b1753.jpg" width="30px"><span>石仔</span> 👍（1） 💬（0）<div>从来没有把模板模式和回调模式拿来比较.只停留在语法技术层面没有从场景和功能方面考虑和比较.</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/13/80/2c9da1b1.jpg" width="30px"><span>L🚲🐱</span> 👍（1） 💬（0）<div>模板方法和回调应用场景一致, 两者的区别是代码实现上不一样, 模板方法是通过 继承来实现, 是自己调用自己, 回调是通过组合来实现, 是类之间的组合. java 中有 Callback的概念</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（1） 💬（0）<div>1.callback是一个语法机制的命名，hook是一个应用场景的命名。但我认为两者换下语义更强。hook描述语法机制，指的就是添加钩子方法这么一种语法机制。callback描述应用场景，特指调用方需要被调用方回调自己的这种场景，这属于钩子方法的应用。大白话就是，我在用callback语法机制时，时常是做一些任务编排的事，跟回调这个语义并不贴切，让我觉得很别扭。

2.java的jdbc其实操作数据库也有callback语法的应用。但现在都是用的orm框架，估摸也都忘了吧，不过也确实没有记忆的必要就是了。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7a/b6/f54bbfaa.jpg" width="30px"><span>花郎世纪</span> 👍（1） 💬（0）<div>深度学习pytorch框架，提供hook去获取特征层数据</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/08/52954cd7.jpg" width="30px"><span>丁乐洪</span> 👍（1） 💬（0）<div>模板类 与 模板模式 有啥关系，感觉干的是同类活</div>2020-03-18</li><br/>
</ul>