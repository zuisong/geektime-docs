你好，我是陈航。

在上一篇文章中，我与你介绍了方法通道，这种在Flutter中实现调用原生Android、iOS代码的轻量级解决方案。使用方法通道，我们可以把原生代码所拥有的能力，以接口形式提供给Dart。

这样，当发起方法调用时，Flutter应用会以类似网络异步调用的方式，将请求数据通过一个唯一标识符指定的方法通道传输至原生代码宿主；而原生代码处理完毕后，会将响应结果通过方法通道回传至Flutter，从而实现Dart代码与原生Android、iOS代码的交互。这，与调用一个本地的Dart 异步API并无太多区别。

通过方法通道，我们可以把原生操作系统提供的底层能力，以及现有原生开发中一些相对成熟的解决方案，以接口封装的形式在Dart层快速搞定，从而解决原生代码在Flutter上的复用问题。然后，我们可以利用Flutter本身提供的丰富控件，做好UI渲染。

底层能力+应用层渲染，看似我们已经搞定了搭建一个复杂App的所有内容。但，真的是这样吗？

## 构建一个复杂App都需要什么？

别急，在下结论之前，我们先按照四象限分析法，把能力和渲染分解成四个维度，分析构建一个复杂App都需要什么。

![](https://static001.geekbang.org/resource/image/d1/cc/d1826dfb3a8b688db04cbf5beb04f2cc.png?wh=1022%2A802)

图1 四象限分析法
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/51/61/9c5beba4.jpg" width="30px"><span>宇</span> 👍（6） 💬（1）<div>思考题实现思路

dart层设置颜色参数的方法：
changeBackgroundColor(int r, int g, int b) async
  {
    _channel.invokeMethod(&#39;changeBackgroundColor&#39;, {&quot;r&quot;:r, &quot;g&quot;:g, &quot;b&quot;:b});
  }

dart层调用：
controller.changeBackgroundColor(0, 255, 255)

android native层实现：
if (methodCall.method.equals(&quot;changeBackgroundColor&quot;)) {
      int r = methodCall.argument(&quot;r&quot;);
      int g = methodCall.argument(&quot;g&quot;);
      int b = methodCall.argument(&quot;b&quot;);
      view.setBackgroundColor(Color.rgb(r, g, b));
      result.success(0);
    }else {
      result.notImplemented();
    }
</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0b/73/4f1c9676.jpg" width="30px"><span>舒大飞</span> 👍（3） 💬（2）<div>反过来，可以在原生页面中嵌入一小块Flutter视图吗</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/56/f9/597cc541.jpg" width="30px"><span>kennen</span> 👍（0） 💬（1）<div>iOS中的frame参数并没有用到，flutter是怎么把宽高传给iOS来展示的呢？</div>2019-11-26</li><br/><li><img src="" width="30px"><span>Miracle_</span> 👍（0） 💬（1）<div>请问下，嵌入了原生视图后，如果嵌入的是较为复杂的视图，视图带走点击等交互事件，应该在哪边设置监听或者处理呢？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（0） 💬（1）<div>思考题如下：

&#47;&#47;声明修改原生控件背景的方法
  changeBgColor() async {
    try {
      _methodChannel.invokeMethod(&quot;changeBgColor&quot;, {
        &quot;color1&quot;: Random().nextInt(255),
        &quot;color2&quot;: Random().nextInt(255),
        &quot;color3&quot;: Random().nextInt(255)
      });
    } catch (e) {
      print(e);
    }
  }

override fun onMethodCall(p0: MethodCall, p1: MethodChannel.Result) {
            when (p0.method) {
                &quot;changeBgColor&quot; -&gt; {
                    view.setBackgroundColor(Color.rgb(p0.argument&lt;Int&gt;(&quot;color1&quot;)!!, p0.argument&lt;Int&gt;(&quot;color2&quot;)!!, p0.argument&lt;Int&gt;(&quot;color3&quot;)!!))
                    p1.success(0)
                }
                &#47;&#47;如果是别的方法则返回未实现
                else -&gt; p1.notImplemented()
            }
        }</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（5） 💬（1）<div>妙啊，通过平台视图，Flutter就可以使用原生视图了，这样，基本所有需求都可以实现了。如果社区再繁荣一点，许多组件都可以拿来即用，那开发需求的速度就是相当快了。</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/bd/cb2fb958.jpg" width="30px"><span>Verios</span> 👍（2） 💬（1）<div> 每次 widget 重建，都会create一个原生 view 吗？
</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/bc/0e/c76861eb.jpg" width="30px"><span>jianwei</span> 👍（2） 💬（0）<div>floatingActionButton: FloatingActionButton(
	onPressed: () =&gt; controller.changeBackground(&#39;#FFFFFF&#39;),
),

Future&lt;void&gt; changeBackground(String colorString) async {
	try {
	  return _channel.invokeMethod(&#39;changeBackgroundColor&#39;, &lt;String, dynamic&gt; {
	    &#39;color&#39;: colorString
	  });
	} catch (e) {
	}
}

- (void)onMethodCall:(FlutterMethodCall*)call result:(FlutterResult)result {
    if ([call.method isEqualToString:@&quot;changeBackgroundColor&quot;]) {
        NSString *colorString = call.arguments[@&quot;color&quot;];
        if (colorString.length != 0) {
            _templcateView.backgroundColor = [UIColor colorWithHexString:colorString];
            result(@0);
            return;
        }
    }
    result(FlutterMethodNotImplemented);
}</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（1） 💬（0）<div>iOS 平台视图中：-(NSObject&lt;FlutterPlatformView&gt; *)createWithFrame:(CGRect)frame viewIdentifier:(int64_t)viewId arguments:(id)args{}
为何frame的值都是(0.0, 0.0, 0.0, 0.0)，为何没有宽高？这里不应该是显示的视图大小吗？
</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/3c/c2c72e28.jpg" width="30px"><span>星星</span> 👍（1） 💬（1）<div>这个在io.flutter.embedding.android.FlutterActivity中如何绑定呢，没有响应的方法啊</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>这个是不是一个 NativeViewController 对应一个 Widgt？？因为 id 不一样</div>2023-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/71/6f/07e1452a.jpg" width="30px"><span>微尘</span> 👍（0） 💬（0）<div>这一节含金量高啊，不知道windows 是否也可以提供插件给dart端使用呢？</div>2022-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/89/33/6c66ed4a.jpg" width="30px"><span>五十度灰黑</span> 👍（0） 💬（0）<div>Flutter 页面嵌入原生视图，有滚动条的情况，原生视图定位问题怎么解决？</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/6d/0a/8e7f0f04.jpg" width="30px"><span>刘洪林</span> 👍（0） 💬（1）<div>对前端来说是不是还要学安卓和iOS开发啊</div>2021-05-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6ADlY3IFt3Rs1aVDyrTO2BiaV8wiabypPwbXhbPcyqicCvnTV9lUYHULVqUab7ww4taX5QbmFyatLQ/132" width="30px"><span>Geek_cc0a3b</span> 👍（0） 💬（0）<div>内嵌原生空间，事件响应比如onClick是直接在原生层响应了吧，flutter不需要负责处理原生事件的响应吧？</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/46/c0/cdc50180.jpg" width="30px"><span>小强</span> 👍（0） 💬（0）<div>&#47;&#47;原生视图销毁回调    @Override    public void dispose() {    }
安卓上有这个回调，怎么iOS没有对应的回调，刚好项目遇到这个问题了，期待老师解惑</div>2021-04-25</li><br/><li><img src="" width="30px"><span>lala</span> 👍（0） 💬（0）<div>  _onPlatformViewCreated(int id) {
    if (widget.controller == null) {
      return;
    }
    widget.controller.onCreate(id);
  }
示例中id传值是多少呢？请老师解答下������������������</div>2020-08-12</li><br/><li><img src="" width="30px"><span>Geek_fdd35e</span> 👍（0） 💬（1）<div>registrarFor(&quot;com.hangchen&#47;NativeViews&quot;); 
registrarFor这个方法找不到了,说没有声明, flutter 1.0.0</div>2020-07-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/akIbCt3y9ssJWI17UoalPcCICJboZoibSybpR3f6RoNYSFhLchLA0Kib0N1q15DI3DW8vF6K6wpt0TPh81Au44HQ/132" width="30px"><span>zeqin</span> 👍（0） 💬（0）<div>那怎么实现原生和futter间互相传值？</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（0） 💬（0）<div>iOS 中FlutterPlatformViewFactory的func create(withFrame frame: CGRect, viewIdentifier viewId: Int64, arguments args: Any?)方法中的frame值都为0，那么这个参数是干什么用的呢？什么情况下会有值？</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/97/80740db0.jpg" width="30px"><span>JW</span> 👍（0） 💬（2）<div>在flutter工程下 .android打开的java文件无法编译和提示，编写本地代码不友好，有什么办法吗？</div>2020-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/30/432a7288.jpg" width="30px"><span>mqh</span> 👍（0） 💬（1）<div>现在注册插件的话需要用FlutterPlugin，用新接口的话如何进行注册？</div>2020-01-06</li><br/>
</ul>