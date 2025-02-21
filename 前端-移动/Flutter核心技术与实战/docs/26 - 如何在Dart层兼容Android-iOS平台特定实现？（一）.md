你好，我是陈航。

在上一篇文章中，我与你介绍了在Flutter中实现数据持久化的三种方式，即文件、SharedPreferences与数据库。

其中，文件适用于字符串或者二进制流的数据持久化，我们可以根据访问频次，决定将它存在临时目录或是文档目录。而SharedPreferences则适用于存储小型键值对信息，可以应对一些轻量配置缓存的场景。数据库则适用于频繁变化的、结构化的对象存取，可以轻松应对数据的增删改查。

依托于与Skia的深度定制及优化，Flutter给我们提供了很多关于渲染的控制和支持，能够实现绝对的跨平台应用层渲染一致性。但对于一个应用而言，除了应用层视觉显示和对应的交互逻辑处理之外，有时还需要原生操作系统（Android、iOS）提供的底层能力支持。比如，我们前面提到的数据持久化，以及推送、摄像头硬件调用等。

由于Flutter只接管了应用渲染层，因此这些系统底层能力是无法在Flutter框架内提供支持的；而另一方面，Flutter还是一个相对年轻的生态，因此原生开发中一些相对成熟的Java、C++或Objective-C代码库，比如图片处理、音视频编解码等，可能在Flutter中还没有相关实现。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（7） 💬（1）<div>思考题：
flutter 端：
&#47;&#47; 处理按钮点击
handleButtonClick() async {
  int result;
  &#47;&#47; 异常捕获
  try {
    &#47;&#47; 异步等待方法通道的调用结果
    result = await platform.invokeMethod(&#39;openAppMarket&#39;, &lt;String, dynamic&gt;{
      &#39;appId&#39;: &quot;com.xxx.xxx&quot;,
      &#39;packageName&#39;: &quot;xxx.com.xxx&quot;,
    });
  } catch (e) {
    result = -1;
  }
  print(&quot;Result：$result&quot;);
}

Android 端：
if (call.method == &quot;openAppMarket&quot;) {
                    if (call.hasArgument(&quot;appId&quot;)) {
                        &#47;&#47;获取 appId
                        call.argument&lt;String&gt;(&quot;appId&quot;)
                    }
                    if (call.hasArgument(&quot;packageName&quot;)) {
                        &#47;&#47;获取包名
                        call.argument&lt;String&gt;(&quot;packageName&quot;)
                    }
                }</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/81/45/9aa91b75.jpg" width="30px"><span>矮个子先生😝</span> 👍（4） 💬（1）<div>看了下Flutter提供的api,动手实现了下,native调flutter的方法
Future&lt;String&gt; nativeCallFlutter(int a) async {
  print(&#39;success $a&#39;);
  return &#39;success&#39;;
}

platform.setMethodCallHandler((MethodCall call) async {
    if (call.method == &#39;nativeCallFlutter&#39;) {
     return await nativeCallFlutter(call.arguments);
    }
    return &#39;none&#39;;
  });

在iOS端调用:
[channel invokeMethod:@&quot;nativeCallFlutter&quot; arguments:@1 result:^(id  _Nullable result) {
        NSLog(@&quot;result = %@&quot;,result);
    }];</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/b0/2736225b.jpg" width="30px"><span>寂寞不点烟</span> 👍（1） 💬（1）<div>而原生代码在处理方法调用请求时，如果涉及到异步或非主线程切换，需要确保回调过程是在原生系统的 UI 线程（也就是 Android 和 iOS 的主线程）。在Android中UI现线程不一定是主线程。</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/44/dd534c9b.jpg" width="30px"><span>菜头</span> 👍（0） 💬（1）<div>如果是获取系统相册直接获取 图片对象
Dart 支持各个平台的 image 对象类型吗</div>2019-11-03</li><br/><li><img src="" width="30px"><span>辉哥</span> 👍（0） 💬（1）<div>问一下,Flutter和原生应用应该不处于同一个进程吧</div>2019-09-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epxMjZcn8LFy6PIT7uGzUOHTCZosTwh39jBKlyW3Ffzyscm14PQGh3QZ1GrEGF4UWxwKZrAib8AXCA/132" width="30px"><span>江宁彭于晏</span> 👍（0） 💬（1）<div>&#47;&#47; 声明 MethodChannel
const platform = MethodChannel(&#39;samples.chenhang&#47;utils&#39;);

&#47;&#47; 处理按钮点击
handleButtonClick(Map paramDic) async{
  int result;
  &#47;&#47; 异常捕获
  try {
    &#47;&#47; 异步等待方法通道的调用结果,Map 中插入appid和包名，跳转链接等信息
    result = await platform.invokeMethod(&#39;openAppMarket&#39;, [paramDic]);
  }
  catch (e) {
    result = -1;
  }
  print(&quot;Result：$result&quot;);
}
</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/89/e3/aa57d3b2.jpg" width="30px"><span>小水滴</span> 👍（0） 💬（1）<div>iOS系统创建多份FlutterViewController会有什么问题吗</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/18/ede273fe.jpg" width="30px"><span>ptlCoder</span> 👍（0） 💬（1）<div>methodChannelWithName:@&quot;samples.chenhang&#47;utils&quot; 
这个通道名称有什么要求嘛？还是说见名知意就好？
另外，如果flutter很多地方都用到了原生系统方法，岂不是在iOS或安卓flutter入口那做很多个判断？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>dart层通过platform.invokeMethod 第二个参数传入动态参数
native层可以通过call.argument拿到参数</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/61/9c5beba4.jpg" width="30px"><span>宇</span> 👍（0） 💬（1）<div>dart层：
platform.invokeMethod(&#39;openAppStore&#39;, {&quot;appId&quot;: &quot;com.tencent.mm&quot;});

native层：
String appId = call.argument(&quot;appId&quot;);
                            try {
                                Uri uri = Uri.parse(&quot;market:&#47;&#47;details?id=&quot; + appId);
                                Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                                startActivity(intent);
                            } catch (Exception e) {
                                result.error(&quot;UNAVAILABLE&quot;, &quot;没有安装应用市场&quot;, null);
                            }</div>2019-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLIdTsqPhlVH3TFElzic8422uBDelRjYiaktCJRmIRpLrgBBfBKnSO9PlbHibnHAc9cQEmLHes3fayEw/132" width="30px"><span>张训博-forrest</span> 👍（1） 💬（0）<div>result.success(0); 这个换了 现在参数要是map了</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/ef/3cdfd916.jpg" width="30px"><span>yu</span> 👍（1） 💬（0）<div>調用原生能力使得 flutter 如虎添翼，並不是要完全取代原生開發，而是採取共生共存的概念。利用原生龐大的生態系，第三方開源組件，為初生的 flutter 提供了擴充，原生調用的功能。使得很多原生開源組件的解決方案可以很好的引入 flutter，這是喜歡 flutter 的其中一個原因。</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/28/35/e37b8fae.jpg" width="30px"><span>Geek_4571a3</span> 👍（0） 💬（0）<div>可以使用pigeon: ^21.2.0这个库进行通信，更加类型安全</div>2024-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/c9/1bec2c98.jpg" width="30px"><span>Barry</span> 👍（0） 💬（0）<div>对比原生，使用方法通道性能怎么样，是否可能有明显的性能折损</div>2022-09-21</li><br/><li><img src="" width="30px"><span>吴开</span> 👍（0） 💬（0）<div>文章漏了点东西，FlutterStreamHandler这个监听，当原生经过某项事件后，回调给flutter</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（0） 💬（3）<div>老师，请问我的项目android编译后的语言是kotlin，而不是java，但是我们要接入的第三方是java，怎么能更改flutter编译后的android项目语言呢？</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/da/66/5858322e.jpg" width="30px"><span>满大大</span> 👍（0） 💬（1）<div>getFlutterView()这个方法找不到，老师这是啥原因啊</div>2020-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/36/f5/a10bfe05.jpg" width="30px"><span>神巅巅</span> 👍（0） 💬（0）<div>请问最新的1.12，新建flutterviewcontroller是不是不会新建engine了，而是可以复用初始化创建的engine</div>2020-01-10</li><br/>
</ul>