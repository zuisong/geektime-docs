你好，我是陈航。今天，我和你分享的主题是，从夜间模式说起，如何定制不同风格的App主题。

在上一篇文章中，我与你介绍了组装与自绘这两种自定义Widget的方式。对于组装，我们按照从上到下、从左到右的布局顺序去分解目标视图，将基本的Widget封装到Column、Row中，从而合成更高级别的Widget；而对于自绘，我们则通过承载绘制逻辑的载体CustomPainter，在其paint方法中使用画笔Paint与画布Canvas，绘制不同风格、不同类型的图形，从而实现基于自绘的自定义组件。

对于一个产品来说，在业务早期其实更多的是处理基本功能有和无的问题：工程师来负责实现功能，PM负责功能好用不好用。在产品的基本功能已经完善，做到了六七十分的时候，再往上的如何做增长就需要运营来介入了。

在这其中，如何通过用户分层去实现App的个性化是常见的增长运营手段，而主题样式更换则是实现个性化中的一项重要技术手段。

比如，微博、UC浏览器和电子书客户端都提供了对夜间模式的支持，而淘宝、京东这样的电商类应用，还会在特定的电商活动日自动更新主题样式，就连现在的手机操作系统也提供了系统级切换展示样式的能力。

那么，这些在应用内切换样式的功能是如何实现的呢？在Flutter中，在普通的应用上增加切换主题的功能又要做哪些事情呢？这些问题，我都会在今天的这篇文章中与你详细分享。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（12） 💬（2）<div>import &#39;package:flutter&#47;cupertino.dart&#39;;
import &#39;package:flutter&#47;material.dart&#39;;

void main() =&gt; runApp(MyThemePage());

class MyThemePage extends StatelessWidget {
  &#47;&#47; iOS 浅色主题
  final ThemeData kIOSTheme = ThemeData(
      brightness: Brightness.light,
      accentColor: Colors.white,
      primaryColor: Colors.blue,
      iconTheme: IconThemeData(color: Colors.grey),
      textTheme: TextTheme(body1: TextStyle(color: Colors.black)));

  &#47;&#47; Android 深色主题
  final ThemeData kAndroidTheme = ThemeData(
      brightness: Brightness.dark, &#47;&#47; 深色主题
      accentColor: Colors.black, &#47;&#47;(按钮)Widget 前景色为黑色
      primaryColor: Colors.cyan, &#47;&#47; 主题色为青色
      iconTheme: IconThemeData(color: Colors.blue), &#47;&#47;icon 主题色为蓝色
      textTheme: TextTheme(body1: TextStyle(color: Colors.red)) &#47;&#47; 文本主题色为红色
      );

  Widget build(BuildContext context) {
    var theme = MyTheme(
      title: &#39;Flutter Demo Home Page&#39;,
      themes: [kIOSTheme, kAndroidTheme],
    );
    return MaterialApp(
      title: &#39;My Theme&#39;,
      theme: kAndroidTheme,
      home: theme,
    );
  }
}

class MyTheme extends StatefulWidget {
  MyTheme({Key key, this.title, this.themes}) : super(key: key);

  final String title;
  final List&lt;ThemeData&gt; themes;

  _MyThemeState createState() =&gt; _MyThemeState();
}

class _MyThemeState extends State&lt;MyTheme&gt; {
  bool isLight;

  @override
  void initState() {
    isLight = true;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Theme(
        child: Scaffold(
          appBar: AppBar(
            title: Text(&#39;Theme switch&#39;),
          ),
          floatingActionButton: FloatingActionButton(
            child: Text(isLight ? &#39;Night&#39; : &#39;Light&#39;),
            onPressed: () {
              setState(() {
                isLight = !isLight;
              });
            },
          ),
        ),
        data: isLight ? widget.themes[0] : widget.themes[1]);
  }
}
</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/80/ccf2f428.jpg" width="30px"><span>灰灰</span> 👍（5） 💬（2）<div>class _HomeState extends State&lt;Home&gt; with SingleTickerProviderStateMixin {
  TabController _controller;
  bool isNight = false;
  @override
  void initState() {
    super.initState();
    _controller = TabController(length: 2, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return
      Theme(
        data: ThemeData(
          brightness: isNight ? Brightness.dark : Brightness.light,
        ),
        child: Stack(
          children: &lt;Widget&gt;[
            Scaffold(
              ...
            ),
            Positioned(
              bottom: 20,
              right: 20,
              child: FloatingActionButton(
                onPressed: () {setState(() {
                  isNight = !isNight;
                });},
                child: Text(isNight ? &#39;日间&#39; : &#39;夜间&#39;),
              ),
            )
          ],
        ),
      );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/77/ff/4ce0aa51.jpg" width="30px"><span>Ω</span> 👍（2） 💬（1）<div>defaultTargetPlatform这个变量哪里来的，文章中没有说明清楚</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/74/e0b9807f.jpg" width="30px"><span>小米</span> 👍（2） 💬（1）<div>思考题：
1、增加一个布尔变量
      bool  _isLight = false
2、在ThemeData中，根据_isLight来显示是否为高亮或者暗色。
      brightness: _isLight ? Brightness.light : Brightness.dark
3、增加一个切换按钮，点击改变_isLight值。
      FlatButton(onPressed: (){setState(() { _isLight = !_isLight; });},child: Text(_isLight?&quot;白天&quot;:&quot;夜间&quot;))</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/06/d01b419f.jpg" width="30px"><span>文心雕龙</span> 👍（1） 💬（1）<div>第三方插件 https:&#47;&#47;pub.dev&#47;packages&#47;dynamic_theme#-readme-tab-</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/44/dd534c9b.jpg" width="30px"><span>菜头</span> 👍（0） 💬（1）<div>Theme.of(context) 方法将向上查找 Widget 树，并返回 Widget 树中最近的主题 Theme。如果 Widget
的父 Widget 们有一个单独的主题定义，则使用该 Theme
如果不是，就使用 App 全局 Theme。

这个表示没太懂。
最近？是表示其第一个 superWidget 吗？
父 Widget 们？一个 widget 有多个父 widget?


</div>2019-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJ3dLlYr6tznfnZXJNsD7Jw48BVnFSib3RO3VWEN0pgebRY1jaR8YXLQ6iaAjTsFiamOWSA3UPAa37A/132" width="30px"><span>Geek_e7jq8k</span> 👍（0） 💬（1）<div>请问下，目前主流的App内UI的样式应该不会局限于ThemeData中的定义的情况。比如有一个自定义的Button，是在代码中设置的特殊Color，不是Themedata里的，这种情况下的button（或类似实现的全部widget），对于日夜间切换这种动态处理的时候，有统一的换颜色的方法么？还是需要在每个widget中都要实现对应的颜色处理？同样的对于TextTheme，ThemeData只提供了textTheme,primaryTextTheme,accentTextTheme三种，如果App内有更多的通用TextTheme，如何动态的统一切换呢？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/e0/238fda97.jpg" width="30px"><span>🌝</span> 👍（0） 💬（1）<div>如果全局更改主题的话，那岂不是要把MaterialApp这个Widget设置成有状态的widget?这样子是不是更耗性能</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（0） 💬（1）<div>老师，这个全局主题的设置只是针对于布局中的对应 widget 没有设置样式才会生效吧？例如我在 ThemeData 里面设置了文字颜色为黑色？但是我在子 widget 里面设置了一个文字会红色，那么此时黑色是不生效的吧？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/01/1c/d638d46e.jpg" width="30px"><span>宋世通</span> 👍（0） 💬（2）<div>老师，在flutter1.8.2，1.8.3版本中增加了ThemeMode，是不是用这个来控制主题明暗会更好一点?</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（2）<div>老师你好，这个Theme应该是要定义为状态，在setState里面修改这个变量，但是代码不知道怎么写，老师能否给一下代码。</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/02/74cb0645.jpg" width="30px"><span>嘎啦儿。</span> 👍（0） 💬（1）<div>老师，final ThemeData kIOSTheme = ThemeData(...省略)，这些语法我没看明白，能给我解释下吗？或者可以提供参考链接地址？</div>2021-07-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epk6XJfVGqsW1b5oiatsuvSRkCF4yo2KxSUSf5LHRRTbuCPKJrRiblqRbMZBuicQMgDTO1bRp6vXW7Lg/132" width="30px"><span>jayce</span> 👍（0） 💬（0）<div>我来说个app切换夜间模式的,ThemeMode system, light, dark

Box mainBox;
void main() async {
  await Hive.initFlutter();
  mainBox = await Hive.openBox(&#39;main&#39;);
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    int modeIndex = mainBox.get(&#39;themeModeIndex&#39;);
    ThemeMode themeMode = modeIndex == null ? ThemeMode.system : ThemeMode.values[modeIndex];
    return MultiProvider(
      providers: [
        ChangeNotifierProvider&lt;ValueNotifier&lt;ThemeMode&gt;&gt;(
          create: (context) =&gt; ValueNotifier(themeMode),
        ),
      ],
      child: Consumer&lt;ValueNotifier&lt;ThemeMode&gt;&gt;(builder: (context, value, child) {
        mainBox.put(&#39;themeModeIndex&#39;, value.value.index);
        return MaterialApp(
          theme: ThemeData(
            brightness: Brightness.light,
            primaryColor: Colors.blue,
            scaffoldBackgroundColor: Colors.white,
          ),
          darkTheme: ThemeData(
            brightness: Brightness.dark,
            primaryColor: Colors.deepPurple,
            scaffoldBackgroundColor: Color(0xFF666666),
          ),
          themeMode: value.value,
          home: HomeScreen(),
        );
      }),
    );
  }
}</div>2021-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/aa/76/37c27871.jpg" width="30px"><span>木木京尤</span> 👍（0） 💬（0）<div>老司，请问调夜间模式的时候，如果想给所有的页面都加一层半透明的图层，应该怎么调参数。不可能每个页面都添加图层，目前知道可以在materialapp  themedata  scaffold  调参数。</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/bc/0e/c76861eb.jpg" width="30px"><span>jianwei</span> 👍（0） 💬（0）<div>在全局的theme中定义多个 textTheme: TextTheme(body1: TextStyle(color: Colors.grey), body2: TextStyle(color: Colors.white), ...)，然后内部widget按需加载相应的 theme.body1 or theme.body2</div>2020-01-07</li><br/>
</ul>