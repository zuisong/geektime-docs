你好，我是陈航。

在上一篇文章中，我与你介绍了Widget生命周期的实际承载者State，并详细介绍了初始化、状态更新与控件销毁，这3个不同阶段所涉及的关键方法调用顺序。深入理解视图从加载到构建再到销毁的过程，可以帮助你理解如何根据视图的状态在合适的时机做恰当的事情。

前面几次分享我们讲了很多关于Flutter框架视图渲染的基础知识和原理。但有些同学可能会觉得这些基础知识和原理在实践中并不常用，所以在学习时会选择忽视这些内容。

但其实，像视图数据流转机制、底层渲染方案、视图更新策略等知识，都是构成一个UI框架的根本，看似枯燥，却往往具有最长久的生命力。新框架每年层出不穷，可是扒下那层炫酷的“外衣”，里面其实还是那些最基础的知识和原理。

因此，**只有把这些最基础的知识弄明白了，修炼好了内功，才能触类旁通，由点及面形成自己的知识体系，也能够在框架之上思考应用层构建视图实现的合理性。**

在对视图的基础知识有了整体印象后，我们再来学习Flutter视图系统所提供的UI控件，就会事半功倍了。而作为一个UI框架，与Android、iOS和React类似的，Flutter自然也提供了很多UI控件。而文本、图片和按钮则是这些不同的UI框架中构建视图都要用到的三个最基本的控件。因此，在今天这篇文章中，我就与你一起学习在Flutter中该如何使用它们。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/23/74/e0b9807f.jpg" width="30px"><span>小米</span> 👍（36） 💬（3）<div>Button都是由RawMaterialButton承载视觉，Image都是RawImage，Text是RichText。它们都继承自RenderObjectWidget，而RenderObjectWidget的父类就是Widget。</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d4/8c/f227750b.jpg" width="30px"><span>欢</span> 👍（17） 💬（1）<div>老师，我想问下，不同手机的分辨率不同，对于同样是fontSize: 16的字号，显示的大小会不一样，这个问题一般会怎么处理。 问了下原生的开发，他们好像有库专门处理这类问题，而web中也有rem之类或其他的处理方式， flutter中我就不知道该怎么办了，求老师解答。 </div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/25/c4cc1e9f.jpg" width="30px"><span>巫山老妖</span> 👍（11） 💬（1）<div>**Text**

&gt; 比如Android中的TextView，iOS中的UILabel

Text参数分类：

- **控制整体文本布局的参数**
	- textAlign
	- textDirection
	- maxLines
	- overflow
	- ...
- **控制文本展示样式的参数**
	- fontFamily
	- fontSize
	- color
	- shadows

通过TextSpan来对Text继续分片样式处理。

**Image**

&gt; 比如Android中的ImageView，iOS里的UIImageView

- 加载本地资源图片
- 加载本地图片
- 加载网络图片

高级版本的Image
- FadeInImage（支持占位图、加载动态等）
- CacheNetworkImage（支持缓存到文件系统，更加强大的加载过程占位和加载错误占位）

**按钮**

- FloatingActionButton（圆形的按钮）
- FlatButton（扁平化的按钮）
- RaisedButton（凸起的按钮）

两个最重要的参数：
- onPressed（用于设置点击回调）
- child（用于设置按钮的内容）</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/3c/0e2a08b1.jpg" width="30px"><span>杨闯</span> 👍（7） 💬（1）<div>你好，我在使用控件的时候有一个疑问：对于一个字符串，我想在定宽的时候计算出它将会占据多大的高度，因为我们现在的项目是要根据高度进行特殊的处理，不知道您是否有什么解决办法</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/18/f8741048.jpg" width="30px"><span>我想静静</span> 👍（6） 💬（1）<div>在用Text或者Icon控件显示竖直方向居中时总会有一点偏下，设置了各种属性都没有修正，最后还是给控件加了paddingBottom强行改变了内容区域的空间才正常，这是什么原因？</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/bf/ec0705c5.jpg" width="30px"><span>李耀</span> 👍（4） 💬（1）<div>flutter 打包之后就简单一个页面，apk包感觉比正常的大号好多</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/71/4cf1b380.jpg" width="30px"><span>烘哄轰、</span> 👍（2） 💬（1）<div>Image.asset(‘images&#47;logo.png’)；的路径需要在配置文件里配置，当时被这个问题坑了好久😂</div>2019-08-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epxMjZcn8LFy6PIT7uGzUOHTCZosTwh39jBKlyW3Ffzyscm14PQGh3QZ1GrEGF4UWxwKZrAib8AXCA/132" width="30px"><span>江宁彭于晏</span> 👍（2） 💬（1）<div>Text、Image、FadeInImage、FlatButton、RaisedBUTTON
都由SingleChildRenderObjectWidget承载视觉
并且这些Widget都隐式的定义了 Semantics ，因为他们可能都直接或者间接的在 Screen Reader 引擎中被使用</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/79/e1/32d11876.jpg" width="30px"><span>🌻Arvin</span> 👍（1） 💬（1）<div>FlatButton(
    color: Colors.yellow, &#47;&#47; 设置背景色为黄色
    shape:BeveledRectangleBorder(borderRadius: BorderRadius.circular(20.0)), &#47;&#47; 设置斜角矩形边框
    colorBrightness: Brightness.light, &#47;&#47; 确保文字按钮为深色
    onPressed: () =&gt; print(&#39;FlatButton pressed&#39;), 
    child: Row(children: &lt;Widget&gt;[Icon(Icons.add), Text(&quot;Add&quot;)],)
)；

好像是版本更新了,背景色color细化成backgroundColor</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/8c/ffc4215e.jpg" width="30px"><span>sixgod</span> 👍（0） 💬（1）<div>老师有个问题 为什么container或者sizedbox有时候设置宽高不生效 在外面包裹一个align就生效了</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/56/07920099.jpg" width="30px"><span>微笑美男😄</span> 👍（0） 💬（1）<div>老师 怎么加载本地的图片。我设置好了之后 在pubspec.yaml中一直报警告,The asset images&#47;fapiaoshenhe.png does not exist.
Try creating the file or fixing the path to the file.
但是感觉设置的没错啊。有专门讲的没</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/1f/03fd5602.jpg" width="30px"><span>jlj</span> 👍（0） 💬（1）<div>老师请教个问题:
fontSize要怎么设置, 才能让字体大小不随系统字体大小改变而改变.?</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/89/a4/c816636c.jpg" width="30px"><span>llons</span> 👍（0） 💬（1）<div>FadeInImage设置gif占位符，会一直触发addPersistentFrameCallback，但远程图片已经加载完毕，占位符已经不显示了</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/6d/0a/8e7f0f04.jpg" width="30px"><span>刘洪林</span> 👍（14） 💬（0）<div>老师，浮动按钮和扁平按钮 v1.26.0-18.0后被废弃了，是不是应该更新一下课件
FlatButton =&gt; TextButton
RaisedButton =&gt; ElevatedButton</div>2021-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/2b/446ef7b6.jpg" width="30px"><span>许先森</span> 👍（3） 💬（0）<div>Text-&gt;RichText-&gt;LeafRenderObjectWidget-&gt;RenderObjectWidget-&gt;Widget
Image-&gt;RawImage-&gt;LeafRenderObjectWidget-&gt;RenderObjectWidget-&gt;Widget
Button-&gt;RawMaterialButton-&gt;Semantics-&gt;SingleChildRenderObjectWidget-&gt;RenderObjectWidget-&gt;Widget
</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b1/2b/9406d19a.jpg" width="30px"><span>小菜鸟学php</span> 👍（1） 💬（0）<div>感谢老师，讲的真是太好了，上个月用flutter做了一个app, 基本就是用组件堆出来的，对flutter理解并不深刻。
 跟着老师一路学下来，对flutter有了整体的认识，理解更加深刻了！</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/50/1f5154fe.jpg" width="30px"><span>无笔秀才</span> 👍（0） 💬（0）<div>老师，请问如果想用富文本编辑器，就是可以在里面写文章 标题，正文，图片，有格式的那种，有什么组件推荐吗？</div>2024-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/c9/833d5060.jpg" width="30px"><span>玉皇大亮</span> 👍（0） 💬（0）<div>&gt;&gt;&gt; flutter 3.2.16
Text build 依赖RichText 和 Semantics
Image build 依赖RawImage和 Semantics
Button build依赖ConstrainedBox 和 Semantics
而最终都会继承自MultiChildRenderObjectWidget 或者 SingleChildRenderObjectWidget，这两个又继承自RenderObjectWidget，RenderObjectWidget继承 Widget

印证了Widget 是构建 flutter 界面的基石这句话</div>2024-02-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKU8b6w5Y9WYpU68zJls0O5IapzJxA1LNicaKOJvbCVjwttPzKaln9oicleiaNPWBTxl17XN6dNo3GAA/132" width="30px"><span>溪风</span> 👍（0） 💬（0）<div>课堂文件在哪里下
</div>2024-01-09</li><br/><li><img src="" width="30px"><span>李克勤</span> 👍（0） 💬（0）<div>widget，yyds</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/58/07/784b31b5.jpg" width="30px"><span>..。野人</span> 👍（0） 💬（0）<div>老师，如果richText中多个片断高度不一样，怎么设置对齐方式？试过alignment: PlaceholderAlignment.top不生效</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（0） 💬（1）<div>老师，我们现在美术只输出3倍图，怎么才能做到资源只放3倍图的文件夹项目就可以用了。。。现在我在项目里面得在image文件夹和image&#47;3.0x文件夹放一模一样的图，然后图片引用image的路径，太麻烦了</div>2020-04-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLkpGLibHdMIcdiazlpF6JOL5ZUz13yuxWBFeZrlsbaiaDxJictNslF9ic87lLtZic3DsHEXxfmTIHNwYA/132" width="30px"><span>Geek_6b80e0</span> 👍（0） 💬（0）<div>button是通过继承RawMaterialButton来实现视觉，RawMaterialButton是statefull的，主要用来存储点击效果反应的改变。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/99/c0572424.jpg" width="30px"><span>🐑郑星星</span> 👍（0） 💬（0）<div>Colors爆红，说是没有定义怎么办</div>2020-01-11</li><br/>
</ul>