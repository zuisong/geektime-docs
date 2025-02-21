你好，我是陈航。

在专栏的第一篇预习文章中，我和你一起搭建了Flutter的开发环境，并且通过自带的hello\_world示例，和你演示了Flutter项目是如何运行在Android和iOS模拟器以及真机上的。

今天，我会通过Android Studio创建的Flutter应用模板，带你去了解Flutter的项目结构，分析Flutter工程与原生Android和iOS工程有哪些联系，体验一个有着基本功能的Flutter应用是如何运转的，从而加深你对构建Flutter应用的关键概念和技术的理解。

如果你现在还不熟悉Dart语言也不用担心，只要能够理解基本的编程概念（比如，类型、变量、函数和面向对象），并具备一定的前端基础（比如，了解View是什么、页面基本布局等基础知识），就可以和我一起完成今天的学习。而关于Dart语言基础概念的讲述、案例分析，我会在下一个模块和你展开。

## 计数器示例工程分析

首先，我们打开Android Studio，创建一个Flutter工程应用flutter\_app。Flutter会根据自带的应用模板，自动生成一个简单的计数器示例应用Demo。我们先运行此示例，效果如下：

![](https://static001.geekbang.org/resource/image/3a/24/3afe6b35238d1e57c8ae6bec9be61624.png?wh=828%2A1792)

图1 计数器示例运行效果
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/83/e8/f726c635.jpg" width="30px"><span>加温后的啤酒</span> 👍（39） 💬（2）<div>老师，想请教一个问题， 关于setState的。
下面两种写法有什么本质的区别吗？？两种写法都对吗？
第一种：
_counter++;
setState(() {
});
第二种：
setState(() {
  _counter++;
});
我用第一种方法运行，发现也没什么问题。。。也可以刷新UI
</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/06/c70bf7e0.jpg" width="30px"><span>梦付千秋星垂野</span> 👍（18） 💬（3）<div>Scaffold 快捷实现一个简单页面还是蛮好的，但是看Demo里面的用法，appBar body floatButton 三个是封装在一个层级里面的，也就是说改变了body里面的值，也顺带刷新了appBar 和 floatButton,感觉没这个必要，本身appBar和floatButton是加载一次后不用变化的。如果把Scaffold变成一个自定义的weight，可以把body再包一个层级，把数据源定义到body内部去，这样是否可行？</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/56/03fb63d9.jpg" width="30px"><span>于留月</span> 👍（17） 💬（2）<div>以内联的方式完成了 Scaffold 页面元素的构建：

首先，代码简洁，直观，容易阅读；
其次，类似模板类代码，减少重复冗余代码编写；
再就是现代语言的“语法糖”。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/47/73/63a3cb41.jpg" width="30px"><span>信仰年轻</span> 👍（10） 💬（1）<div>没看出内联，，kotlin和C++的内联都有关键字inline，，这里哪里体现内联了啊？？、</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（6） 💬（5）<div>我想问下，现在国内有没有比较成熟的纯flutter开发的App。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/fd/41eb3ecc.jpg" width="30px"><span>奔跑的徐胖子</span> 👍（4） 💬（3）<div>老师，我有个疑问，既然flutter是从上至下的有自己的UI渲染的闭环，那么您说的，最终程序运行是以原生的方式进行的又是什么意思呢，flutter也是调用的原生功能进行功能实现吗</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/f0/5dc3afdb.jpg" width="30px"><span>啵一个草莓</span> 👍（4） 💬（1）<div>请教一个问题：我iOS真机运行一直报错，模拟器能成功，自己的个人apple ID（不是开发者） ，手机也是这个ID，不是可以在真机上运行么？</div>2019-08-09</li><br/><li><img src="" width="30px"><span>方海栋</span> 👍（4） 💬（1）<div>什么叫以内联的方式</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7a/90/dc3537e7.jpg" width="30px"><span>神经蛙</span> 👍（4） 💬（3）<div>关于“在_MyHomePageState类中，直接在build函数里内联的方式完成Scaffold页面元素的构建”，我有一个问题：
前文提到“setState方法会通知Flutter更新界面，Flutter收到通知后，会执行Widget的build方法，重新构建”，那么如果在_MyHomePageState类的build函数里内联整个Scaffold页面元素构建，是否就意味着setState后整个Scaffold及其子节点都会重新构建？如果Scaffold的子节点很多，是不是就会带来性能损耗？</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/8b/35ea4275.jpg" width="30px"><span>熊爸爸</span> 👍（4） 💬（1）<div>1. 老师在回复中多次提到的“共享状态”指的是什么，是 context 相关的能力吗？
2. 希望老师能顺带讲讲代码和功能的封装等最佳实战（包括继承、Mixin）；
3. 3个月的时间感觉有点长，要是能加快更新进度就好了。不过还是要说：老师辛苦了！
</div>2019-07-10</li><br/><li><img src="" width="30px"><span>Miracle_</span> 👍（2） 💬（1）<div>老师请问下目前Flutter对各种不同屏幕尺寸适配有好的方案吗？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/a9/eede1288.jpg" width="30px"><span>Simon</span> 👍（2） 💬（1）<div>我认为好处是，状态只在当前的Widget中能使用并修改，不会受到Widget外的影响。如果放到组件外来管理，状态那就相当于一个全局状态，其它的Widget也可以修改这个状态。不知道说的对不对，还望老师指正</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c9/a9/c7f73138.jpg" width="30px"><span>晨鹤</span> 👍（1） 💬（3）<div>现在 Android 原生主推 MVVC 架构，也实现了数据驱动 UI，很爽。</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/bd/e28f8ce5.jpg" width="30px"><span>ls</span> 👍（1） 💬（2）<div>当一个复杂的页面，用这种代码形式来构建ui，维护起来感觉会很吃力。</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9c/1d/34c96367.jpg" width="30px"><span>G</span> 👍（1） 💬（1）<div>老师，为什么要多一个createstate来创建State类呢，像react里面一样直接引用类不行吗？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/c5/2f359dc3.jpg" width="30px"><span>Young</span> 👍（1） 💬（1）<div>内联的方式，代码看起来更加直观，如果再增加一个类和方法，只需要将Scaffold的代码抽取到新方法中，在build方法中调用即可</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/ab/981ca927.jpg" width="30px"><span>雷声大</span> 👍（0） 💬（2）<div>想问下State 中的widget 是什么时候传过来的？莫非是框架设置的，我们new _MyHomePageState()的时候没有把 widget 传进来，但是State 里面就可以调用 widget.title</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/0c/2ebdc487.jpg" width="30px"><span>魔兽rpg足球</span> 👍（0） 💬（1）<div>声名式ui与命令式ui能举个例子不 不太明白啥意思</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/83/b2/e83dd93c.jpg" width="30px"><span>🌙</span> 👍（0） 💬（1）<div>创建应用时提示无法打开kernel-service.dart.snapshot，怎么解决呢？</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（0） 💬（1）<div>老师，我在那个main.dart这个文件里面打了断点，然后发现每次点击加号按钮时候，Scaffold 类里面的appBar之类的几乎都会走一遍，理论上来说不是只应该只走下面这段代码吗？
Text(
              &#39;$_counter&#39;,
              style: Theme.of(context).textTheme.display1,
            )
难道是说只是走了，但是那些不需要的走的不重绘刷新吗？</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/1b/fa287ed5.jpg" width="30px"><span>半桶水</span> 👍（0） 💬（2）<div>请教个问题，通过android studio进行调试，出现error connecting to the service protocol：HttpException：connection closed before full header was received。环境是ubuntu 19.04，flutter v1.7.8，Android studio 3.4.2</div>2019-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epsQbE6IFa4uu2yvPzibxowbUKV0n31VffHwicOLrgQ22k12aAgRb3cyApqX9zt3xFicegPicGZqrTNhw/132" width="30px"><span>晓磊</span> 👍（0） 💬（2）<div>找到小闪电图标了。但一直是灰色不可用状态。鼠标悬浮提示的快捷键是ctrl-\，按下去不起作用。真机调试。windows系统，AndroidStudio</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/56/b7/4258025c.jpg" width="30px"><span>top_founder</span> 👍（0） 💬（1）<div>中间层收敛上层UI配置何解？</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a2/89/7098b532.jpg" width="30px"><span>wilson</span> 👍（0） 💬（1）<div>有没有关于stream rxdart  block 等相关的分享</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/25/0fd94f9b.jpg" width="30px"><span>无尘</span> 👍（0） 💬（1）<div>咨询一下老师，main.dart里面的main()方法可以有多个吗？比如我在lib下面新建一个main1.dart里面也写一个一样的main()方法，那么会执行哪个main()方法呢？flutter又是如何找到这个入口方法的呢？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/25/c8/7a950a91.jpg" width="30px"><span>淡～</span> 👍（0） 💬（1）<div>Flutter 对这个机制做了优化，其框架内部会通过一个中间层去收敛上层 UI 配置对底层真实渲染的改动，从而最大程度降低对真实渲染视图的修改，提高渲染效率，而不是上层 UI 配置变了就需要销毁整个渲染视图树重建。
没有明白这句话真正意思，可以具体解释下吗？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/f4/7d74c9bb.jpg" width="30px"><span>Longwei243</span> 👍（0） 💬（1）<div>NotificationListener监听不到发出的自定义事件可能是什么原因呢？</div>2019-07-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL7KLt8chh8F9D4y3zXJiaTicGicBGwdpoFKTU0CpW6D2mav5HPDkHTbWA6bZ61ZBXAlgR08Y5IsU1kQ/132" width="30px"><span>卡特</span> 👍（0） 💬（2）<div>我一直有个问题比较好奇，现在很多公司都在研究flutter的动态化，也都是照RN那套把flutter弄得更乱了，没人考虑从flutter的热重载那里入手吗</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/25/2f6c53bc.jpg" width="30px"><span>dks</span> 👍（0） 💬（1）<div>使用build 函数里内联的方式，可以拿到 BuildContext 对象。那么 BuildContext 是用来做什么的呢？</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/ef/3cdfd916.jpg" width="30px"><span>yu</span> 👍（0） 💬（1）<div>1. 我想好處是直觀，易讀
2. 建立一個 function or variable，返回 Widget，再將該函式填入 build 中。這是 flutter 常用的組件手法。</div>2019-07-09</li><br/>
</ul>