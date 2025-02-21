你好，我是陈航。

通过上一篇文章，我们已经深入理解了Widget是Flutter构建界面的基石，也认识了Widget、Element、RenderObject是如何互相配合，实现图形渲染工作的。Flutter在底层做了大量的渲染优化工作，使得我们只需要通过组合、嵌套不同类型的Widget，就可以构建出任意功能、任意复杂度的界面。

同时，我们通过前面的学习，也已经了解到Widget有StatelessWidget和StatefulWidget两种类型。StatefulWidget应对有交互、需要动态变化视觉效果的场景，而StatelessWidget则用于处理静态的、无状态的视图展示。StatefulWidget的场景已经完全覆盖了StatelessWidget，因此我们在构建界面时，往往会大量使用StatefulWidget来处理静态的视图展示需求，看起来似乎也没什么问题。

那么，StatelessWidget存在的必要性在哪里？StatefulWidget是否是Flutter中的万金油？在今天这篇文章中，我将着重和你介绍这两种类型的区别，从而帮你更好地理解Widget，掌握不同类型Widget的正确使用时机。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/83/e8/f726c635.jpg" width="30px"><span>加温后的啤酒</span> 👍（39） 💬（2）<div>老师，有一个疑问没有理解。你文中提到如果根布局是StatefulWidget，如果调用setState,就会触发子widet的销毁和重建，影响性能。但是在真实业务场景中，我把跟控制器写成StatefulWidget，但我默认他是不可变的，所以我肯定不会主动去调用setState方法啊，那如果我不主动调用setState的话，那不就不会有应能影响了吗。这没法说明StatelessWidget的存在是必要的的？？老师能解释一下吗？</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/55/e4/7061abd5.jpg" width="30px"><span>Mr.J</span> 👍（11） 💬（1）<div>构建界面时，抛开业务，光看界面，把界面按层次拆分，需要动态更新的地方，用Stateful，然后将其统一放在Stateless中，做到例如在一个小区域中，根布局也是Stateless，其中有一个控件为stateful，刷新时只刷新这个小部分，这样吗老师</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/97/80740db0.jpg" width="30px"><span>JW</span> 👍（8） 💬（1）<div>Element是Widget层的一个抽象用来处理真正需要重建的的Widget，它是如何来决定谁要重建谁不要重建的逻辑的？</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/de/27/21b37e99.jpg" width="30px"><span>陈致瀚</span> 👍（7） 💬（1）<div>简单来说StatelessWidget就是为了提升性能而被设计出来，而完全使用StatefulWidget可能对性能有影响，所以在使用前一定要评估一下用哪个比较合适，这样理解对吗？</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/6d/928b0ffd.jpg" width="30px"><span>、轻</span> 👍（3） 💬（1）<div>这两个widget与react中的容器和组件很类似</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5b/5b/75f4a04f.jpg" width="30px"><span>格格</span> 👍（3） 💬（1）<div>现在Image里已经找不到_handleImageChanged方法了，好像被_handleImageFrame取代了</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/06/287d77dd.jpg" width="30px"><span>承香墨影</span> 👍（3） 💬（1）<div>老师，你好，有个疑问希望解答。
既然 StatefulWidget 需要区分场景来使用，并且 Widget 的销毁和重建应该是 Flutter 的常态。那么在使用中，应该将 StatefulWidget 尽量的拆小，让其影响范围，尽可能的小。
这是不是就对应到 “04 | Flutter 区别于其他方案的关键技术是什么” 中讲到的 布局边界 和 重绘边界 概念。其实在实际代码中，是依赖 StatelessWidget 进行设定边界，从而隔离布局和重绘的？</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/81/45/9aa91b75.jpg" width="30px"><span>矮个子先生😝</span> 👍（2） 💬（1）<div>```
  const Image({
    Key key,
    @required this.image,
    &#47;&#47; 其他参数
  }) : assert(image != null),
       super(key: key);
```
老师可以介绍下这个构造方法吗, 第一个Key key, : assert(image != null),super(key: key); 这三部分</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9c/1d/34c96367.jpg" width="30px"><span>G</span> 👍（2） 💬（2）<div>我查了下资料，好像是说虽然widget是不可变的，但是state是可变的，也就是说state实例会被复用，并且在setstate重新生成widget树时会检查节点是否有变化，没有变化就停止遍历。另外我认为stateful的实例相比stateless更轻，毕竟没有build方法。
Ps: 在递归下降生成子树的时候，我有个疑问，flutter如何判断子树一样呢？算法是如何的？</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/59/ed/15465917.jpg" width="30px"><span>Captain</span> 👍（1） 💬（1）<div>有个问题请教“虽然 Flutter 内部通过 Element 层可以最大程度地降低对真实渲染视图的修改，提高渲染效率，而不是销毁整个 RenderObject 树重建。但，大量 Widget 对象的销毁重建是无法避免的”这里 如果根节点用了Stateful，根节点setState，来改变其中变化的子节点状态（子节点状态中没有耗时操作），那Element会帮助diff出变化的子节点，避免重新构建，这样也不影响性能呀？</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/2f/5d93a37b.jpg" width="30px"><span>严旭珺</span> 👍（1） 💬（1）<div>感觉项目的一个优化方向就是尽量用statelesswidget</div>2019-08-08</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqr5ibqxYwcSgqPA7s49MZb1vEKKXT4mPTojwiclXkJf3ug26NuzTa6A5gbicR2rAUHdEkUAn13Rr2KQ/132" width="30px"><span>吴小安</span> 👍（1） 💬（2）<div>请问这种声明式编程在ios和安卓业界有没有简单的框架能用的？
感觉现在ios使用的面向数据开发也都是命令式编程，界面绑定某个值，kvo变化了在回调里做刷新ui的操作，怎样能向这种声明式转移</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/88/4dfad2fd.jpg" width="30px"><span>徐西文</span> 👍（1） 💬（1）<div>Dart为什么不设计一种可以自动选择状态的widget</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6a/71/d28392a9.jpg" width="30px"><span>Bula</span> 👍（1） 💬（1）<div>StatefulWidget感觉很难减少使用频率啊  现在的设计标题栏的标题都是要跟着状态改变动态更改  😓</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/45/c0/b7ced73a.jpg" width="30px"><span>Eren</span> 👍（1） 💬（1）<div>学到现在，真的是受益匪浅，之前的一些疑惑都从中得到了答案，有种恍然大悟的感觉，希望老师能在未来的学习中，分享一下 Flutter 的从业情况和面试题，感谢之至。</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/58/27/1188e017.jpg" width="30px"><span>Egos</span> 👍（1） 💬（1）<div>思考题里面是将MyApp 替换成StatefulWidget，然后需要在点击FloatingActionButton 的时候更新MyApp 的State 么？这样需要将MyApp 的State 一直传递到_MyHomePageState？</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e3/b6/44760ef9.jpg" width="30px"><span>干就完事</span> 👍（0） 💬（1）<div>老师，就是StatefulWidget拆小……不是造成整个树的子节点深度变多了嘛。</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/44/dd534c9b.jpg" width="30px"><span>菜头</span> 👍（0） 💬（1）<div>State&lt;Image&gt; 这种声明是什么意思？</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e8/95/13b88119.jpg" width="30px"><span>面向加薪学习</span> 👍（0） 💬（1）<div> _handleImageChanged 这个方法是谁来调用，什么时候调用？</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/18/7cbc34eb.jpg" width="30px"><span>davidzhou</span> 👍（0） 💬（1）<div>老师，现在我创建了两个widget，widget a里面有个方法func（），我希望在widget b里面的button事件能够触发func（），怎么一个实现方案</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2d/c9/0d8983f3.jpg" width="30px"><span>张简</span> 👍（0） 💬（2）<div>您说的文案数据集就是state吧？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/55/48de9a24.jpg" width="30px"><span>Carlo</span> 👍（0） 💬（1）<div>那所有的button都是stateful widget对么? 那一个提示错误的弹出框中包含一个OK button。那这个弹出框可以是stateless吗？</div>2019-08-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoibW0Cougnv3Hjl8n1EWoUHloXu5lMicuPm1FcJ0qyXWEaqwXv4Z09ARaeDRicbicL9RTIXnoNARibSxw/132" width="30px"><span>mq</span> 👍（0） 💬（1）<div>状态管理的话使用Redux是不是可以替代StatefulWidget？</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/8b/35ea4275.jpg" width="30px"><span>熊爸爸</span> 👍（0） 💬（1）<div>请问老师，我看到有人用 StatelessWidget + Provide 能取代一部分 StatefulWidget 的功能，而对于自定义控件的封装，StatefulWidget 能发挥出一定优势，不知这样理解对不对？
我在布局界面时是否能大量使用 StatelessWidget + Provide？</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f5/1e/f0780b61.jpg" width="30px"><span>永生</span> 👍（0） 💬（2）<div>A是一个statefulwidget,从A页面跳转到B页面，A会rebuild,然后从B页面返回A页面，A又rebuild一次，我想问一下A为什么要rebuild呢？</div>2019-07-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIAQdjCbZN4X6cJuicGia0zGMWN22TjagIZLBNgZII09wMyVPSX0fmsicelI9nGhds1vECGkynYOnJag/132" width="30px"><span>不拘小节</span> 👍（0） 💬（1）<div>&#47;&#47; Android 设置某文本控件展示文案为 Hello World
TextView textView = (TextView) findViewById(R.id.txt);
textView.setText(&quot;Hello World&quot;);

&#47;&#47; iOS 设置某文本控件展示文案为 Hello World
UILabel *label = (UILabel *)[self.view viewWithTag:1234];
label.text = @&quot;Hello World&quot;;

&#47;&#47; 原生 JavaScript 设置某文本控件展示文案为 Hello World
document.querySelector(&quot;#demo&quot;).innerHTML = &quot;Hello World!&quot;;

有个疑问，ios（androin）在渲染的时候，是需要变化的地方更改渲染，而Flutter则是这整个页面渲染，是不是Flutter的渲染效率比原生低啊，而且这样分析，如果大量使用StatefulWidget的话，做到变化的子widget才进行部分渲染，那不是StatefulWidget用的越多，效率越高？</div>2019-07-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIAQdjCbZN4X6cJuicGia0zGMWN22TjagIZLBNgZII09wMyVPSX0fmsicelI9nGhds1vECGkynYOnJag/132" width="30px"><span>不拘小节</span> 👍（0） 💬（3）<div>有个疑惑，一个StatefulWidget中有一个子StatefulWidget的widget，如果我子的StatefulWidget调用setState刷新，回影响到父级的渲染吗？</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/ed/9cc44242.jpg" width="30px"><span>JakePrim</span> 👍（19） 💬（0）<div>就喜欢这种讲解加举例的方式，非常清晰</div>2019-07-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/uyyCHGeo0gayHkjPqr5wlcB0BulhNwkSHkvq0vWOvRlArTBb4dGTE8kvtJzAbbNkwZreiab3Mq1BibayhfujU4Ww/132" width="30px"><span>Lgh</span> 👍（4） 💬（4）<div>有个比较尴尬的问题，我想问问老师，为什么text是statelesswidget？Text的文案变化不应该属于可变的吗？</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/3b/fa/2cebefff.jpg" width="30px"><span>曾家二女婿</span> 👍（1） 💬（0）<div>【思考题】
void main() =&gt; runApp(MyApp());

class MyApp extends StatefulWidget {
  MyApp({Key key}) : super(key: key);
  @override
  _MyApp createState() =&gt; _MyApp();
}

class _MyApp extends State&lt;MyApp&gt; {
  bool check = true;
  void _updateIndeView() {
    setState(() {
      check = !check;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: &#39;Flutter Demo&#39;,
      &#47;&#47; 应用的名字
      theme: ThemeData(
        &#47;&#47; 蓝色主题
        primarySwatch: Colors.red,
      ),
      &#47;&#47; 首页路由
      home: Scaffold(
        &#47;&#47; 点击 切换 主页
        body: Container(
          child: InkWell(
            onTap: _updateIndeView,
            child: check ? MyHomePage(title: &#39;Flutter Demo Home Page&#39;) : _MyHomePageDemo(),
          )
          &#47;&#47; check ? MyHomePage(title: &#39;Flutter Demo Home Page&#39;) : _MyHomePageDemo(),
        ),
      ),
    );
  }
}</div>2020-01-10</li><br/>
</ul>