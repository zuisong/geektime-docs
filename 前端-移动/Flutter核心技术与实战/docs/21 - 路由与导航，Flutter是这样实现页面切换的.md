你好，我是陈航。

在上一篇文章中，我带你一起学习了如何在Flutter中实现跨组件数据传递。其中，InheritedWidget适用于子Widget跨层共享父Widget数据的场景，如果子Widget还需要修改父Widget数据，则需要和State一起配套使用。而Notification，则适用于父Widget监听子Widget事件的场景。对于没有父子关系的通信双方，我们还可以使用EventBus实现基于订阅/发布模式的机制实现数据交互。

如果说UI框架的视图元素的基本单位是组件，那应用程序的基本单位就是页面了。对于拥有多个页面的应用程序而言，如何从一个页面平滑地过渡到另一个页面，我们需要有一个统一的机制来管理页面之间的跳转，通常被称为**路由管理或导航管理**。

我们首先需要知道目标页面对象，在完成目标页面初始化后，用框架提供的方式打开它。比如，在Android/iOS中我们通常会初始化一个Intent或ViewController，通过startActivity或pushViewController来打开一个新的页面；而在React中，我们使用navigation来管理所有页面，只要知道页面的名称，就可以立即导航到这个页面。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/08/dfda5266.jpg" width="30px"><span>YJ</span> 👍（46） 💬（1）<div>使用的是Navigator.push
 A-&gt;B-&gt;C-&gt;D,
请问如何 D页面 pop 到 B 呢?</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（15） 💬（2）<div>在敲代码时候的有两点需要注意的地方。

1、在传入 runApp 里面的 widget 里面做路由跳转的时候所使用的的 BuildContext 不能是 App 的，必须得是 widget 的，否则会报 Navigator operation requested with a context that does not include a Navigator 这样子的错。

2、使用命名路由或者注册表的方式，最好是在传入 runApp 里面的 widget 的MaterialApp 里面做 routes 的配置，为的是 APP 一启动的时候就注册上，否则可能会存在要使用命名，可是还没注册的情况，就会报 Could not find a generator for route RouteSettings(&quot;second_page&quot;, null) in the _WidgetsAppState 这样的错误。</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1c/31/8b5b8fbb.jpg" width="30px"><span>高超</span> 👍（6） 💬（1）<div>问：对于基本路由，如何传递页面参数？
答：1.  使用构造函数传参
      2.  MaterialPageRoute 加入参数 setting: RouteSettings 。第二个页面获取逻辑和命令路由就一样了。</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/50/1b/acd941fb.jpg" width="30px"><span>入魔的冬瓜</span> 👍（2） 💬（1）<div>自己手动push一个route的话，可以通过构造函数进行传参数。
使用命名路由的话，参数的读取通过ModalRoute.of(context).settings.arguments，这个操作要放在build里面操作。这种情况，有没有什么办法也是通过构造函数传参数，在build之前就可以拿到参数。（类似第三方fluro框架）</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/5c/4f35bdfe.jpg" width="30px"><span>巫</span> 👍（1） 💬（1）<div>把所有命名路由都定义在一起会很多，也不利于模块化，能否在模块中定义路由呢？另外，有没有子路由的概念呢？</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/ff/1489d0fb.jpg" width="30px"><span>肖</span> 👍（1） 💬（1）<div>老师你好，showdialog也是进行了路由跳转，为什么会出现在当前界面上面，而普通的都是跳到另外一个新的界面</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/25/c4cc1e9f.jpg" width="30px"><span>巫山老妖</span> 👍（1） 💬（1）<div>第二道思考题：
传参：
RaisedButton(
            child: Text(&#39;命名路由（参数&amp;回调）&#39;),
            onPressed: () =&gt;
                Navigator.pushNamed(context, &quot;third_page&quot;, arguments: [1, 2])
                    .then((msg) {
              setState(() {
                _msg = msg;
              });
            })

计算并返回：

class ThirdPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var args = ModalRoute.of(context).settings.arguments as List&lt;int&gt;;

    int sum = args[0] + args[1];
    print(sum);

    return Scaffold(
      appBar: AppBar(
        title: Text(&#39;Third Screen&#39;),
      ),
      body: Column(
        children: &lt;Widget&gt;[
          Text(&#39;Message from first screen:  $args&#39;),
          RaisedButton(
            child: Text(&#39;back&#39;),
            onPressed: ()=&gt; Navigator.pop(context, &quot;${sum}&quot;),
          )
        ],
      ),
    );
  }
}
</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/2f/5d93a37b.jpg" width="30px"><span>严旭珺</span> 👍（1） 💬（2）<div>老师好，请问一下，如果是类似于Android中打开页面 A-&gt;B-&gt;A，标准的启动模式，栈中有2个A页面该怎么办呢？我试了试B页面Navigator.pushName(context,A),会黑屏</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（1） 💬（1）<div>第二个问题：可以构造一个 list 传递过去，然后对 list 中数据的两个数字求和再把结果带回上个页面。

另外老师通过 arguments 是不是只能传递一个参数呀？</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/08/dfda5266.jpg" width="30px"><span>YJ</span> 👍（0） 💬（3）<div>陈老师请问？
使用的是Navigator.push
 A-&gt;B-&gt;C-&gt;D,
如何 让D页面 pop 到 B 呢?</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/29/a85c2853.jpg" width="30px"><span>汪帅</span> 👍（0） 💬（1）<div>其实我一直想知道这个课程的样例代码在哪里？之前见过有人留言中问过但是也没看到有回复具体地址。现在找那条留言也找不到了，其它课程都有对应的样例代码在github上面，如果有在每篇下面附加上代码地址不可以么？</div>2019-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLBKSykSmNnspVs5OvAUGLecibeiczo7sQYJ4XoJXNa2jWUwvwiaHz8yM3iak0ErUSUIJrGfzNUJ7P79Rg/132" width="30px"><span>竹之同学</span> 👍（0） 💬（1）<div>对于基本路由，其实路由返回的就是那个新页面初始化的实例，所以可以在页面 Widget 定义变量，然后在路由返回，也就是实例化的时候传值进去。</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/55/e4/7061abd5.jpg" width="30px"><span>Mr.J</span> 👍（0） 💬（1）<div>在新建页面的时候通过构造函数传的参数</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/dd/5d473145.jpg" width="30px"><span>亡命之徒</span> 👍（0） 💬（1）<div>class MySecondPage extends StatelessWidget {
  String msg;
  MySecondPage({
    Key key,
    this.msg
  }):super(key:key);
  @override
  Widget build(BuildContext context) {
    &#47;&#47; TODO: implement build
    MyThreePage tsp = new MyThreePage();
    &#47;&#47;基本路由传递参数
    tsp.msg = &quot;我来自第二个页面&quot;;
    return Scaffold(
      appBar: AppBar(title: Text(&quot;SecondPage&quot;),),
      body: RaisedButton(
        child: Text(&quot;MyEvent Bus$msg&quot;),
        onPressed: () {
          myEventBus.fire(MyCustomEvent(&quot;Hello World&quot;));
          Navigator.pop(context);
        },
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.pages),
        onPressed: (){
          Navigator.push(context, MaterialPageRoute(builder: (context)=&gt;tsp));
        },
      ),
    );
  }
}

MySecondPage sp = new MySecondPage();
    sp.msg = &quot;我传给你了哈哈哈&quot;;
onPressed: ()=&gt;Navigator.push(context,MaterialPageRoute(builder: (context)=&gt;sp)),
可以通过这种方式传递</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/6e/be1bb682.jpg" width="30px"><span>colin</span> 👍（0） 💬（1）<div>context 会细讲吗？ 感觉不是很懂</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>对于基本路由，如何传递页面参数？
能过MaterialPageRoute 的 settings 属性。</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/d0/3d5696d8.jpg" width="30px"><span>无嘴小呆子</span> 👍（0） 💬（0）<div>老师你好，为何在实际开发中使用flutter嵌套Android自定义View时点击跳转到另外一个Flutter界面时，过度动画存在卡UI的情况，黑屏过渡中会偶现底部界面部分UI闪烁的问题呢</div>2024-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/55/249c3abd.jpg" width="30px"><span>包美丽</span> 👍（0） 💬（0）<div>求问如何销毁指定路由？
如何脱离context启动路由？</div>2021-09-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLkpGLibHdMIcdiazlpF6JOL5ZUz13yuxWBFeZrlsbaiaDxJictNslF9ic87lLtZic3DsHEXxfmTIHNwYA/132" width="30px"><span>Geek_6b80e0</span> 👍（0） 💬（0）<div>基本路由，可以通过传递构造函数参数，直接传递。
</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/95/357702d7.jpg" width="30px"><span>晓蜻蜓</span> 👍（0） 💬（1）<div>老师你好，我今天有个问题不知道怎么解决，就是如何返回跟路由？根页面—A—B，如何返回根页面？</div>2020-03-17</li><br/><li><img src="" width="30px"><span>Geek_0d53ed</span> 👍（0） 💬（0）<div>老师，您好，请问下，如何在用户点击appbar上的返回按键时，添加返回参数给上一个页面尼？</div>2020-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLEIsgI4ub1VOKWtVOfouAzSqx8Yt8ibQEsAnwNJsJHmuJzzpQqG79HullvYwpic8hgiclgON2GwXSjw/132" width="30px"><span>cv0cv0</span> 👍（0） 💬（0）<div>WP 真是最优雅的系统。</div>2019-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/08/dfda5266.jpg" width="30px"><span>YJ</span> 👍（0） 💬（0）<div>原来是个使用是可以混合使用的
Navigator.push(context, MaterialPageRoute(builder: (BuildContext context){
                      return CarStockPage();
                    }));
Navigator.pushNamed(context, YJRouters.clue_page);
两种方式结合场景可以混合使用，就可以满足相当复杂的路由跳转逻辑了！！！</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/71/591ae170.jpg" width="30px"><span>大恒</span> 👍（0） 💬（0）<div>讲的简单了一点，YJ同学的问题才是实际场景遇到的</div>2019-08-28</li><br/>
</ul>