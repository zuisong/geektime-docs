你好，我是陈航。

在上一次分享中，我们认识了Flutter中最常用也最经典的布局Widget，即单子容器Container、多子容器Row/Column，以及层叠容器Stack与Positioned，也学习了这些不同容器之间的摆放子Widget的布局规则，我们可以通过它们，来实现子控件的对齐、嵌套、层叠等，它们也是构建一个界面精美的App所必须的布局概念。

在实际开发中，我们会经常遇到一些复杂的UI需求，往往无法通过使用Flutter的基本Widget，通过设置其属性参数来满足。这个时候，我们就需要针对特定的场景自定义Widget了。

在Flutter中，自定义Widget与其他平台类似：可以使用基本Widget组装成一个高级别的Widget，也可以自己在画板上根据特殊需求来画界面。

接下来，我会分别与你介绍组合和自绘这两种自定义Widget的方式。

## 组装

使用组合的方式自定义Widget，即通过我们之前介绍的布局方式，摆放项目所需要的基础Widget，并在控件内部设置这些基础Widget的样式，从而组合成一个更高级的控件。

这种方式，对外暴露的接口比较少，减少了上层使用成本，但也因此增强了控件的复用性。在Flutter中，**组合的思想始终贯穿在框架设计之中**，这也是Flutter提供了如此丰富的控件库的原因之一。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqr5ibqxYwcSgqPA7s49MZb1vEKKXT4mPTojwiclXkJf3ug26NuzTa6A5gbicR2rAUHdEkUAn13Rr2KQ/132" width="30px"><span>吴小安</span> 👍（16） 💬（1）<div>大前端的界面不是提倡尽量减少图层的数量？这样一直嵌套下去图层似乎太多，这些布局的控件是不是不算图层？不参与渲染？</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（12） 💬（4）<div>关于第二道思考题目的解决方法，请老师看一下：

&#47;&#47;绘制自定义view，其中画笔 paint ，画布 canvas，而 CustomPainter 负责具体的绘制逻辑处理
class WheelPainter extends CustomPainter {
  List&lt;double&gt; _list;
  List&lt;Color&gt; _listColor;
  double _total; &#47;&#47;总份数

  WheelPainter(this._list, this._listColor);

  @override
  void paint(Canvas canvas, Size size) {
    double wheelSize = min(size.width, size.height) &#47; 2; &#47;&#47;饼图的尺寸
    &#47;&#47;用一个矩形框来包裹饼图
    Rect boundingRect = Rect.fromCircle(
        center: Offset(wheelSize, wheelSize), radius: wheelSize);
    &#47;&#47;求出数组中所有数值的和
    _total = _list.reduce((value, element) =&gt; value + element);
    print(&quot;总份额是：$_total&quot;);
    &#47;&#47;求出每一份所占的角度
    double radius = (2 * pi) &#47; _total; &#47;&#47;求出每一份的弧度
    print(&quot;总角度是${2 * pi},每份额角度是:$radius&quot;);
    &#47;&#47;循环绘制每一份扇形
    for (int i = 0; i &lt; _list.length; i++) {
      &#47;&#47; 求出初始角度
      double startRadius;
      if (i == 0) {
        startRadius = 0;
      } else {
        startRadius =
            _list.sublist(0, i).reduce((value, element) =&gt; value + element) *
                radius;
      }
      &#47;&#47;求出滑过角度，即当前份额乘以每份所占角度
      double sweepRadius = radius * _list[i];
      print(&quot;起始角度：$startRadius,划过角度：$sweepRadius&quot;);

      &#47;&#47;&#47; 绘制扇形，第一个参数是绘制矩形所在的矩形，第二个参数是起始角度，第三个参数是矩形划过的角度
      &#47;&#47;&#47; 第三个参数代表扇形是否是实心，否则就只是绘制边框是空心的，最后一个参数是画笔
      canvas.drawArc(boundingRect, startRadius, sweepRadius, true,
          getPaintByColor(_listColor[i]));
    }
  }

  &#47;&#47;根据不同的 color 来获取对应的画笔
  Paint getPaintByColor(Color color) {
    Paint paint = Paint();
    paint.color = color;
    return paint;
  }

  &#47;&#47;判断是否需要重绘
  @override
  bool shouldRepaint(CustomPainter oldDelegate) =&gt; oldDelegate != this;
}

Padding getCustomPaint() {
  return Padding(
      padding: EdgeInsets.all(10),
      child: CustomPaint(
        size: Size(200, 200), 
        painter: WheelPainter(
            List.of([1.0, 2.0, 3.0, 4.0, 20]),
            List.of([
              Colors.red,
              Colors.blue,
              Colors.green,
              Colors.amber,
              Colors.black54
            ])),
      ));
}</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/69/10/0c6f68d7.jpg" width="30px"><span>wanggw</span> 👍（5） 💬（3）<div>功能算是差不多实现了，但是还存在一个核心的问题不知道应该解决，就是我怎么获取Text展示文本的行数，我需要行数才能控制 more 按钮的显示和隐藏，否则我默认超过2行显示 more 按钮，当文本只有1行的时候，more 按钮也显示了😂。暂时还没找到解决方案。这是我写的例子：https:&#47;&#47;github.com&#47;wanggw911&#47;flutter_hello&#47;blob&#47;master&#47;lib&#47;widget&#47;Listview02.dart</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/18/7cbc34eb.jpg" width="30px"><span>davidzhou</span> 👍（4） 💬（2）<div>我的思路这样，先自定义一个statefulwidget，里面用过一个变量控制两个text，因为text是statelesswidget，无法动态去刷新，一个widget设置Maxlines=2，另一个不设置，more是一个floatbutton，点击事件里面实现setstate改变先前定义的变量就行了</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/c6/238570f9.jpg" width="30px"><span>獸丶</span> 👍（3） 💬（1）<div>老师，Flutter代码规范方面会讲吗，如果代码全写在一个Dart文件里，有点太冗杂了，还是说遵循SRP，一个类一个Dart文件？</div>2019-08-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJ3dLlYr6tznfnZXJNsD7Jw48BVnFSib3RO3VWEN0pgebRY1jaR8YXLQ6iaAjTsFiamOWSA3UPAa37A/132" width="30px"><span>Geek_e7jq8k</span> 👍（2） 💬（3）<div>请问下，再混合开发的场景下,module类型的对于root Widget，我们必须使用MaterialApp或者CupertinoApp二选一么？如果不使用这两个基础的widgetApp，除了不能享受封装好的Theme、封装好的Widget组件这些便利外，是否有无法实现的基础功能（比如在iOS中的右滑返回等等）？ 同时想问下目前国内很多App在安卓上的表现都不是Material风格的，同时也不完全是Cupertino风格，所以在实际应用中，主流的做法是使用 MaterialApp&#47;CupertinoApp&#47;完全自定义 这三种的哪一种呢？以及在开发过程中的是否有什么弊端呢？</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/5f/ecf0e687.jpg" width="30px"><span>Neil 陈荣</span> 👍（1） 💬（2）<div>老师，我想绘制一个围棋游戏的棋盘，并在上面实现落子、提子等各种操作。大致估计了一下，如果用组合的方案，算上棋子，棋盘，各种线，至少会有接近400个 widget. 这种情况下性能会有问题吗？我想知道 widget 数量一般在多少以内采用组合不会出现性能问题，这个有没有一个指导性的最佳实践？如果一上来就用自绘的方案的话，担心各种操作的交互功能不容易实现。谢谢！</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/6e/23/9fce5f72.jpg" width="30px"><span>毛哥来了</span> 👍（1） 💬（3）<div>我是用Builder(builder: (Buildcontext context){})来创建description那个Text组件，然后就可以通过context.size.height获取Text的高度，然后就能判断按钮何时展示了</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/cf/baa4ee4d.jpg" width="30px"><span>浣熊特工队</span> 👍（1） 💬（2）<div>请问老师，more按钮那里的左右渐隐是怎么实现的啊，我用TextOverflow.fade是向下渐隐的啊</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/83/b2/e83dd93c.jpg" width="30px"><span>🌙</span> 👍（1） 💬（1）<div>如果说尽量使用stateless，但是只要需要交互都必须是stateful吧？怎么尽量来使用成stateless呢？</div>2019-08-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/sgEfkeMSIIibeH4l0HS8uwM6PGY3DSHoW5tV9l1hDQ06tr3OnI7F545Wdxsh59rqOKnzjLUpCcEqic3P9zZbKzPQ/132" width="30px"><span>楼外楼</span> 👍（1） 💬（1）<div>哪些算是非可视容器呢？</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/a9/eede1288.jpg" width="30px"><span>Simon</span> 👍（1） 💬（2）<div>老师，Flutter其中一个游戏引擎flame，也是通过自绘的方式实现的吗？</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/59/ed/15465917.jpg" width="30px"><span>Captain</span> 👍（0） 💬（1）<div>老师，pi是在哪里定义的？</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1f/86/3a7eeac4.jpg" width="30px"><span>leslee</span> 👍（0） 💬（2）<div>老师我把你的案例跑起来了, 但是我把 我把计数器那个案列的代码里面的 MaterialApp 的 themeData 的 primaryColor 的颜色改成你的 ligjtblue[800] 后他报错, 报 type color is not a subtype of type materialcolor 我看了文档确实颜色是分好几个类型,   可是为什么你的可以运行我的不可以运行........</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/16/20562cdf.jpg" width="30px"><span>离尘不离人คิดถึง</span> 👍（0） 💬（1）<div>功能都实现了，抽象了一个有状态的组件：https:&#47;&#47;github.com&#47;lichenbuliren&#47;flutter_study&#47;blob&#47;master&#47;lib&#47;components&#47;appUpdateItemCard.dart；
基本思路：
1、用 Contaner  的 decoration 绘制一个圆角白色渐变的白底；
2、抽取 UI 组件，内部维护一个 『showMore』 状态
3、描述文本组件根据 『showMore』 来动态设置 『maxLines』属性值，并且设置 『overflow』为省略号
唯一存在的小瑕疵就是我的 FlatButton  控件中的文本一直存在 padding；手动设置了 0 也不生效；因为我看该章节里面的 『more』文本应该是靠右对齐的，这里麻烦老师帮忙看下，我尝试了各种方案都没法实现</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/e0/238fda97.jpg" width="30px"><span>🌝</span> 👍（0） 💬（1）<div>我把描述信息这块提成了一个有状态的widget，这样性能应该会更好些

class DescriptionModel extends StatefulWidget {
  String desc;

  DescriptionModel({Key key, this.desc}) : super(key: key);

  _DescriptionModelState createState() =&gt; _DescriptionModelState();
}

class _DescriptionModelState extends State&lt;DescriptionModel&gt; {

  bool flag = false;

  void changeFlag (){
    print(flag);
    setState(() {
      flag = !flag;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: &lt;Widget&gt;[
        Text(widget.desc, maxLines: flag ? null : 2,),
        Positioned(
          bottom: 0,
          right: -5,
          child: FlatButton(
            &#47;&#47; color: Colors.white,
            highlightColor: Colors.transparent,
            splashColor: Colors.transparent,
            onPressed: changeFlag,
            child: Container(child: Text(&#39;More&#39;, style: TextStyle(color: Colors.blue),), padding: EdgeInsets.fromLTRB(5,0,5,0), color: Colors.white,)
          ),
        )
      ],
    );
  }
}

功能是实现了，但是这个按钮摆放的位置让我很头疼，而且 按钮的样式也不知道该怎么去改变，我想去改变按钮的宽高以便让按钮显示的更正常些。</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（0） 💬（1）<div>老师，没太明白第二道题的意思，传入的数组的值是弧度吗？那这样的话，传入的数组的所有元素加起来得够 2π 是吗？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/80/ccf2f428.jpg" width="30px"><span>灰灰</span> 👍（0） 💬（2）<div>class UpdateItemWidget extends StatefulWidget {
  final model;
  final onPressed;

  UpdateItemWidget({Key key, this.model, this.onPressed}) : super(key: key);
  @override
  State&lt;StatefulWidget&gt; createState() {
    return _UpdateItemState();
  }
}
class _UpdateItemState extends State&lt;UpdateItemWidget&gt; {
  bool collapse = true;
  @override
  void initState() {
    super.initState();
  }
  @override
  Widget build(BuildContext context) {
    return Column(
      children: &lt;Widget&gt;[
        buildTopRow(context),
        buildBottomRow(context),
      ],
    );
  }
 ....
  Widget buildBottomRow(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(15, 0, 15, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: &lt;Widget&gt;[
          Row(
            children: &lt;Widget&gt;[
              Expanded(
                child: Text(
                  widget.model.appDescription,
                  maxLines: collapse ? 2 : null,
                  overflow: collapse ? TextOverflow.ellipsis : null),
              ),
              Container(
                width: !collapse ? 0 : null,
                child: FlatButton(
                  onPressed: () {
                    setState(() {collapse = false;});
                    },
                  child: Text(&#39;More&#39;, style: TextStyle(color: Colors.blue),),
                )
              ),
            ],
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(0, 10, 0, 0),
            child: Text(&quot;${widget.model.appVersion} • ${widget.model.appSize} MB&quot;),
          )
        ],
      ),
    );
  }
}
</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>老师，用Positioned组件设置
right: 0,
bottom: 0,
FlatButton组件总对齐不了最下边。</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（2）<div>class BottomRow extends StatefulWidget {
  const BottomRow({
    Key key,
    this.model,
  }): super(key: key);

  final UpdatedItemModel model;

  @override
  State&lt;StatefulWidget&gt; createState() {
    return _BottomRow();
  }
}

class _BottomRow extends State&lt;BottomRow&gt; {

  UpdatedItemModel model;
  bool open = false;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(15, 0, 15, 0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: &lt;Widget&gt;[
          Stack(
            children: &lt;Widget&gt;[
              Container(
                child: Text(widget.model.appDescription, maxLines: open ? 100 : 2,),
              ),
              Positioned(
                right: 0,
                bottom: 0,
                child: FlatButton(
                  onPressed: () {
                    setState(() {
                      open = !open;
                    });
                  },
                  child: Container(
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: &lt;Color&gt;[
                          Colors.white,
                          Colors.grey,
                        ]
                      )
                    ),
                    child: Text(&#39;OPEN&#39;, style: TextStyle(color: Color(0xFF007AFE), fontSize: 14),),
                    padding: EdgeInsets.all(2),
                  ),

                )
              )
            ],
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(0, 10, 0, 0),
            child: Text(&#39;${widget.model.appDate} • ${widget.model.appSize} MB&#39;),
          ),
        ],
      ),
    );
  }

}</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/b6/58a450f6.jpg" width="30px"><span>Geek_ymdxk2</span> 👍（0） 💬（1）<div>老师，flutter的textfield长按复制，把输入框的内容删除后长按就不弹出复制了，有什么解决方案吗</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（5） 💬（2）<div>一看到Canvas，就知道又把rn和weex给秒杀了，这两家伙没有画布。。。没法绘制</div>2019-08-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gYGeUZCuibranJRR5aL5ib5w48hXibEMb8MZDZjF5icOK7n48WkfIjT9lF5iaiaptIfTPvUp7Qp9ibn1m3f7icmFroYz8g/132" width="30px"><span>朱文博</span> 👍（4） 💬（0）<div>class UpdateItemInfoRender extends StatefulWidget {
  final String info;

  UpdateItemInfoRender({Key key, this.info}) : super(key: key);

  @override
  State&lt;StatefulWidget&gt; createState() {
    &#47;&#47; TODO: implement createState
    return _UpdateItemInfoRender();
  }
}

class _UpdateItemInfoRender extends State&lt;UpdateItemInfoRender&gt;
    with WidgetsBindingObserver {
  bool flag = false;

  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      setState(() {
        flag = context.size.height &gt; 40.0;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    &#47;&#47; TODO: implement build
    return Stack(
      children: &lt;Widget&gt;[
        Text(
          &#39;${widget.info}&#39;,
          style: TextStyle(fontSize: 14),
          maxLines: flag ? 2 : null,
        ),
        flag ? Positioned(
                right: -5,
                bottom: 0,
                child: FlatButton(
                  onPressed: () =&gt; setState(() {
                    flag = !flag;
                  }),
                  child: Container(
                    width: 60,
                    padding: EdgeInsets.only(left: 20),
                    decoration: BoxDecoration(
                        gradient: LinearGradient(colors: [
                      Colors.white.withOpacity(.7),
                      Colors.white.withOpacity(1),
                      Colors.white.withOpacity(1),
                      Colors.white.withOpacity(1),
                    ])),
                    alignment: Alignment.center,
                    child: Text(
                      &#39;more&#39;,
                      style: TextStyle(color: Colors.blueAccent, fontSize: 14),
                    ),
                  ),
                ),
              )
            : Container()
      ],
    );
  }
}</div>2020-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gYGeUZCuibranJRR5aL5ib5w48hXibEMb8MZDZjF5icOK7n48WkfIjT9lF5iaiaptIfTPvUp7Qp9ibn1m3f7icmFroYz8g/132" width="30px"><span>朱文博</span> 👍（2） 💬（0）<div>第二题
class WheelPainter extends CustomPainter {
  List&lt;double&gt; list;

  WheelPainter(this.list);

  &#47;&#47;设置不同颜色的画笔
  Paint getColorPint(Color color) {
    return Paint()..color = color;
  }

  @override
  void paint(Canvas canvas, Size size) {
    &#47;&#47;计算饼图半径
    double wheelSize = min(size.width, size.height) &#47; 2;
    int num = list.length;
    double sum = list.reduce((current, next) =&gt; current + next);
    Rect rect = Rect.fromCircle(center: Offset(wheelSize, wheelSize), radius: wheelSize);
    double start = 0;
    double step = 0;
    for (var i = 0; i &lt; num; i++) {
      step = (2 * pi) * (list[i] &#47; sum);
      canvas.drawArc(rect, start, step, true,
          getColorPint(i % 2 == 0 ? Colors.red : Colors.green));
      start += step;
    }
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) {
    &#47;&#47; TODO: implement shouldRepaint
    return oldDelegate != this;
  }
}

class Cake extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    &#47;&#47; TODO: implement build
    return CustomPaint(
      size: Size(200, 200),
      painter: WheelPainter([1, 2, 3, 4, 4, 2]),
    );
  }
}</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ab/1c3dc64b.jpg" width="30px"><span>夏目🐳</span> 👍（0） 💬（1）<div>为什么我的谷歌图片那行高度很小，怎么自定义高度呢？</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ab/1c3dc64b.jpg" width="30px"><span>夏目🐳</span> 👍（0） 💬（0）<div>怎么画k线图呢</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ab/1c3dc64b.jpg" width="30px"><span>夏目🐳</span> 👍（0） 💬（0）<div>赞👍</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/2e/f317f6ad.jpg" width="30px"><span>伊利丹怒风</span> 👍（0） 💬（0）<div>有了CustomPainter可以开发游戏了…</div>2020-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/97/1d/4bac8dbf.jpg" width="30px"><span>VI jolie</span> 👍（0） 💬（0）<div>老师关于思考题有没有您的解决方法啊</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ab/16/0f83cab6.jpg" width="30px"><span>smilingmiao</span> 👍（0） 💬（0）<div>交个作业

class WheelPainter extends CustomPainter {
  final List&lt;double&gt; arcs; &#47;&#47; 存放各个圆弧所占整体的比例值
  WheelPainter(this.arcs);

  &#47;&#47; 设置画笔颜色
  Paint getColoredPaint(Color color) { &#47;&#47; 根据颜色返回不同的画笔
    Paint paint = Paint();
    paint.color = color;
    return paint;
  }

  int random(int maxBound) {
    return Random().nextInt(maxBound);
  }
  
  Color randomColor() {
    return Color.fromARGB(255, random(255), random(255), random(255));
  }

  double min(a, b) {
    if (a &gt;= b) {
      return b;
    } else {
      return a;
    }
  }

  @override
  void paint(Canvas canvas, Size size) { &#47;&#47; 绘制逻辑
    double wheelSize = min(size.width, size.height) &#47; 2;
    Rect boundingRect = Rect.fromCircle(center: Offset(wheelSize, wheelSize), radius: wheelSize);

    double startAngle = 0;
    arcs.forEach((arc) {
      print(arc);
      double sweepAngle = (2 * pi) * arc;
      canvas.drawArc(boundingRect, startAngle, sweepAngle, true, getColoredPaint(randomColor()));
      startAngle = startAngle + (2 * pi) * arc;
    });
  }

  &#47;&#47; 判断是否需要重绘，这里我们简单的做下比较即可
  @override
  bool shouldRepaint(CustomPainter oldDelegate) =&gt; oldDelegate != this;
}</div>2020-05-27</li><br/>
</ul>