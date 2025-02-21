你好，我是戴铭。

在上一篇文章中，我和你分享了链接器的基础知识。今天我们再继续聊聊，动态库链接器的实际应用，也就是编译调试的提速问题。

iOS 原生代码的编译调试，都是通过一遍又一遍地编译重启 App 来进行的。所以，项目代码量越大，编译时间就越长。虽然我们可以通过将部分代码先编译成二进制集成到工程里，来避免每次都全量编译来加快编译速度，但即使这样，每次编译都还是需要重启 App，需要再走一遍调试流程。

对于开发者来说，提高编译调试的速度就是提高生产效率。试想一下，如果上线前一天突然发现了一个严重的bug，每次编译调试都要耗费几十分钟，结果这一天的黄金时间，一晃就过去了。到最后，可能就是上线时间被延误。这个责任可不轻啊。

那么问题来了，原生代码怎样才能够实现动态极速调试，以此来大幅提高编译调试速度呢？在回答这个问题之前，我们先看看有哪些工具是这么玩儿的。了解了它们的玩法，我们也就自然清楚这个问题的答案了。

## Swift Playground

说到iOS代码动态极速调试的工具，你首先能想到的估计就是 Playground。它是 Xcode 里集成的一个能够快速、实时调试程序的工具，可以实现所见即所得的效果，如下图所示：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/8f/abb7bfe3.jpg" width="30px"><span>bubble</span> 👍（2） 💬（2）<div>想问下老师 为什么只有模拟器可以 而真机不可以呢？</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2f/cf/33b3ac43.jpg" width="30px"><span>mqhong</span> 👍（2） 💬（1）<div>讲的有点深了 有没有推介的gnustep源码必读的类实现 和阅读的方法😂</div>2019-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7IvaucOdCqF6HLA3aC7YzYzv9GGJ26Wz5XESWMAoycSO2KQIibBxmaMc4E2icjJoO1gP5GqqJspt6ZPuxd5EKBag/132" width="30px"><span>Damon</span> 👍（1） 💬（1）<div>报错了，建议看看留言或者直接看github仓库中的issue看是否有你遇到的问题；看了留言我的问题完美解决</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/c4/0fcdad37.jpg" width="30px"><span>刘儒勇</span> 👍（0） 💬（1）<div>历尽千辛万苦，终于可以用了✌️</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（0） 💬（1）<div>这样审核能通过吗？ 是不是调试的时候用，提交App Store时候移除呢</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/30/03/60b78345.jpg" width="30px"><span>郑昊鸣</span> 👍（0） 💬（1）<div>感谢老师，对于已经模块化的项目，在pod的example project中开发，InjectionIII就不好用了。InjectionIII要求项目都在一个目录下，当项目加载本地pod进行开发的时候，本地pod和项目project不在同一目录下，InjectionIII该如何使用呢，谢谢~</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/b4/afcf095e.jpg" width="30px"><span>痞子胡</span> 👍（0） 💬（1）<div>接入到项目中，启动后直接crash，报bad access。找了一天还没找到原因，求解。</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3c/b9/42b228f8.jpg" width="30px"><span>徐秀滨</span> 👍（0） 💬（1）<div>接我上个问题，已经解决了。
使用通知接收就可以。
[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(test) name:@&quot;INJECTION_BUNDLE_NOTIFICATION&quot; object:nil];</div>2019-03-26</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（31） 💬（1）<div>Clone一下代码弄得有点懵，不知道怎么克隆。然后我用了另一种方式使用了injection

1.在App Store下载InjectionIII, 打开。
2.选择项目的根目录
3.项目的Appdelegate加入：
#if DEBUG
 &#47;&#47; iOS
    [[NSBundle bundleWithPath:@&quot;&#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection.bundle&quot;] load];
#endif

XCode10 是这个
#if DEBUG
 &#47;&#47; iOS
    [[NSBundle bundleWithPath:@&quot;&#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection10.bundle&quot;] load];
#endif

而后启动，修改，保存，就会卡到断点位置了。</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/96/d0/39502263.jpg" width="30px"><span>Daniel</span> 👍（21） 💬（0）<div>ios10之后由于沙盒的限制 应用无法加载自身bundle之外的动态库 这个工具只能在模拟器上使用</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/67/e91fe8d3.jpg" width="30px"><span>景天儿</span> 👍（17） 💬（2）<div>蛮好用的，但是有几个需要注意的地方：
1. 进行swizzling的类不要动态修改，否则二次交换，会引起死循环。
2. 不支持方法的删除：删除后，方法调用仍然有效，不抛异常。
3. 不支持新增类：新增类引入后使用无效。但类的重命名是有效的。
4. 属性新增、删除、修改：反射上体现不出来。
其中后三个的原因，不知道戴铭老师有没有什么见解。
在我的角度来看，应该不是InjectionIII的问题，可能与苹果动态库调用有关。</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/ba/23c9246a.jpg" width="30px"><span>mαnajay</span> 👍（13） 💬（0）<div>InjectionIII 上面有个 issue 是解决 pod 组件引入修改源码无法进行注入的问题  https:&#47;&#47;github.com&#47;johnno1962&#47;InjectionIII&#47;issues&#47;34,  https:&#47;&#47;github.com&#47;johnno1962&#47;InjectionIII&#47;issues&#47;53 , 使用组件后接入还是有点麻烦</div>2019-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoAMdDYvpo841AmtN3XOKyYHyrvMILdW02icN0tntDC3PkdzIOTic8dqODwZDibiaT2mbUkD5nLwPQVcA/132" width="30px"><span>Geek_48dbbf</span> 👍（7） 💬（0）<div>真机上如何实现注入动态库实时调试？</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/34/1b/3e4ffacc.jpg" width="30px"><span>Love mi</span> 👍（7） 💬（1）<div>1.在App Store下载InjectionIII, 打开。
2.选择项目的根目录
3.项目的Appdelegate加入：
    [[NSBundle bundleWithPath:@&quot;&#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection.bundle&quot;] load];
运行报
Error loading &#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection.bundle&#47;iOSInjection:  dlopen(&#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection.bundle&#47;iOSInjection, 265): Symbol not found: _$s19ArrayLiteralElements013ExpressibleByaB0PTl
  Referenced from: &#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection.bundle&#47;iOSInjection
  Expected in: &#47;Applications&#47;Xcode.app&#47;Contents&#47;Developer&#47;Toolchains&#47;XcodeDefault.xctoolchain&#47;usr&#47;lib&#47;swift&#47;iphonesimulator&#47;libswiftCore.dylib
 in &#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection.bundle&#47;iOSInjection</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/dd/5d473145.jpg" width="30px"><span>亡命之徒</span> 👍（6） 💬（0）<div>项目使用了cocopods、这个插件用不了呀，保存的时候报错😭，新建的demo使用就没问题,麻烦老师解答下</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/42/86/3f916a75.jpg" width="30px"><span>Hyman</span> 👍（6） 💬（2）<div>command+s就没有人报错误吗？
Loading .dylib ...
objc[4708]: Class ViewController is implemented in both &#47;Users&#47;hyman&#47;Library&#47;Developer&#47;CoreSimulator&#47;Devices&#47;7C19EFEC-F0B4-4405-979A-358FA75F4A4F&#47;data&#47;Containers&#47;Bundle&#47;Application&#47;A1A3313C-9092-4BBA-B2EF-604ECAD508D3&#47;MTInjectionOC.app&#47;MTInjectionOC (0x10f488d10) and &#47;Users&#47;hyman&#47;Library&#47;Containers&#47;com.johnholdsworth.InjectionIII&#47;Data&#47;eval104.dylib (0x12d168138). One of the two will be used. Which one is undefined.
💉 Loaded .dylib - Ignore any duplicate class warning ^</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/38/54/b0bca333.jpg" width="30px"><span>SLY</span> 👍（6） 💬（1）<div>@Link 回复楼上那位同学，把 file -&gt; Workspace Setting -&gt; Build System， 改为Legacy Build System模式，默认的New Build System(Default)模式，是不会编译pod 里面的改动的</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ba/2d/e0339b0a.jpg" width="30px"><span>Jersey、</span> 👍（5） 💬（0）<div>刚开始没重写 - (void)injected { } , 发现修改一直没反应, 控制台还收到了相应警告
💉 Injection connected, watching &#47;Users&#47;user&#47;JerseyCafe&#47;JerseyCafe&#47;MySampleCode&#47;JSDPlayground&#47;**
💉 *** Compiling &#47;Users&#47;user&#47;JerseyCafe&#47;JerseyCafe&#47;MySampleCode&#47;JSDPlayground&#47;JSDPlayground&#47;Class&#47;Launch&#47;JSDHomeVC.m ***
💉 Loading .dylib ...
objc[22080]: Class JSDHomeVC is implemented in both &#47;Users&#47;user&#47;Library&#47;Developer&#47;CoreSimulator&#47;Devices&#47;042DBB6D-8059-43E7-A609-3034F6D949AD&#47;data&#47;Containers&#47;Bundle&#47;Application&#47;4BCF4C6E-3650-484C-BAE8-7ACB3B3A3E6E&#47;JSDPlayground.app&#47;JSDPlayground (0x10695a278) and &#47;Users&#47;user&#47;Library&#47;Containers&#47;com.johnholdsworth.InjectionIII&#47;Data&#47;eval101.dylib (0x12cf821d8). One of the two will be used. Which one is undefined.
💉 Loaded .dylib - Ignore any duplicate class warning ^
然后找了下 github Issue  [Issue](https:&#47;&#47;github.com&#47;johnno1962&#47;InjectionIII&#47;issues&#47;101) 原来要在相应的文件下重写 injected 方法,  在 .m 下添加下列代码即可
Swift:
extension UIViewController {
  @objc func injected() {
    viewDidLoad()
    viewWillAppear(true)
    viewDidAppear(true)
  }
}
OC:
- (void)injected {
    
    [self viewDidLoad];
    [self viewWillAppear:YES];
    [self viewWillDisappear:YES];
}
直接修改代码即可, command + s 自动刷新。
不过还是收到相应警告。
</div>2019-04-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKicV7dO4eIrRXavpECHo5GoEGuHBP1rJENKriaOASW8AjrOKvQFnpzuughnlC1BEaW4cXcjic4twlUA/132" width="30px"><span>旺旺</span> 👍（4） 💬（0）<div>我这保存后悔报错
💉 *** Compiling &#47;Users&#47;zhaowangwang&#47;Documents&#47;中电科36所svn&#47;E-Mobile&#47;MeCenterViewController.m ***
💉 *** Re-compilation failed (&#47;Users&#47;zhaowangwang&#47;Library&#47;Containers&#47;com.johnholdsworth.InjectionIII&#47;Data&#47;command.sh)
fatal error: malformed or corrupted AST file: &#39;could not find file &#39;&#47;Users&#47;zhaowangwang&#47;Documents&#47;中电科36所svn&#47;E-Mobile&#47;RongIMLib.framework&#47;Headers&#47;RCAmrDataConverter.h&#39; referenced by AST file &#39;&#47;Users&#47;zhaowangwang&#47;Library&#47;Developer&#47;Xcode&#47;DerivedData&#47;E-Mobile-brkkzascastenicojgygpmgoepqm&#47;Build&#47;Intermediates.noindex&#47;PrecompiledHeaders&#47;SharedPrecompiledHeaders&#47;9438762758094351804&#47;E-Mobile-Prefix.pch.gch&#39;&#39;
1 error generated.
 ***
怎么破?</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/39/b4/b0cb712a.jpg" width="30px"><span>景迪</span> 👍（4） 💬（0）<div>起来第一件事就是看看有没有更新😄</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/92/0099c319.jpg" width="30px"><span>Melvins</span> 👍（3） 💬（4）<div>@drunkenMouse，用你的方法在xcode 10.2上会出现👇错误提示，求教！！！

Error loading &#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection10.bundle&#47;iOSInjection10:  dlopen(&#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection10.bundle&#47;iOSInjection10, 265): Symbol not found: _$SBOWV
  Referenced from: &#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection10.bundle&#47;iOSInjection10
  Expected in: &#47;Applications&#47;Xcode.app&#47;Contents&#47;Developer&#47;Toolchains&#47;XcodeDefault.xctoolchain&#47;usr&#47;lib&#47;swift&#47;iphonesimulator&#47;libswiftCore.dylib
 in &#47;Applications&#47;InjectionIII.app&#47;Contents&#47;Resources&#47;iOSInjection10.bundle&#47;iOSInjection10</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d8/29/56b3d0c8.jpg" width="30px"><span>语文化及</span> 👍（2） 💬（0）<div>我新建了一个swift 项目，能卡到@objc func injected() 这个方法里边， 但如果我尝试去修改viewDidLoad 里边的方法，貌似并没有起作用。
比如在viewDidLoad 里边修改一个label 的 文本 label.text = &quot;bbb&quot;，修改后显示Injected &#39;ViewController&#39; 了，但实际UI 上并没有改变。</div>2019-04-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJTOicFdCW2hgUwgfiaR9qSGabPvgLorp1Xcd7uLquXibWmKZxJibMsSeqibEpuHoSwusj2kOr86uLAzng/132" width="30px"><span>Geek_45fc02</span> 👍（2） 💬（0）<div>刚想试试手，就更新了Xcode和swift5，试了下发现不行。真心希望Apple能够把这位大牛收了，让iOS热重载成为一个内置的功能，还能以此杀杀flutter的气焰。</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3c/b9/42b228f8.jpg" width="30px"><span>徐秀滨</span> 👍（2） 💬（0）<div>请问为啥我保存后，断点执行到了，但是过了之后就闪了，一脸懵逼。。。</div>2019-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIeibOkdXV6XEQIib3XWAl9CBIiaZI0hbyQXvM07xl5ervCCZ72nrYIic3QFp1NXmP6Jh8JfoA9txrT7w/132" width="30px"><span>Geek_5gkz17</span> 👍（1） 💬（0）<div>崩溃的各位同学，看看项目中是否用了rac，这个会导致crash</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/bb/04/13f4c93e.jpg" width="30px"><span>韩小醋</span> 👍（1） 💬（1）<div>老师，是否可以讲解一下flutter attach 的原理，公司最近准备搞flutter 动态化</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3d/83/89ff35f9.jpg" width="30px"><span>1 OR 1=1</span> 👍（1） 💬（1）<div>- (void)injected
+ (void)injected
INJECTION_BUNDLE_NOTIFICATION
我这边所有的修改只有写在这3个方法里才会刷新，并不能像图片上那样随修随变，并一直报dylib 重复警告

inject(tmpfile: String) 方法的代码大都是新类替换旧类，但是当我在- (void)injected里写入[self viewDidLoad];后，会发现并没有替换，而是重新创建了一遍新的UI,有请踩过坑的老哥发言😂

</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/a4/dc91ff7c.jpg" width="30px"><span>以</span> 👍（1） 💬（0）<div>@Hyman 出现的问题怎么解决的？
💉 Loading .dylib ...
objc[10390]: Class ViewController is implemented in both &#47;Users&#47;lutaohua&#47;Library&#47;Developer&#47;CoreSimulator&#47;Devices&#47;37453FFB-A4BA-4761-B590-BFAEB3C54A5D&#47;data&#47;Containers&#47;Bundle&#47;Application&#47;342F3B0F-D638-4A99-89C6-3C8A04A25135&#47;Mach_O_test.app&#47;Mach_O_test (0x100b65ea8) and &#47;Users&#47;lutaohua&#47;Library&#47;Containers&#47;com.johnholdsworth.InjectionIII&#47;Data&#47;eval101.dylib (0x11e8e3218). One of the two will be used. Which one is undefined.
💉 Loaded .dylib - Ignore any duplicate class warning ^</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/a6/e46a062f.jpg" width="30px"><span>Tim叔</span> 👍（1） 💬（0）<div>xocde10.1下编译错误open &#47;~&#47;bin&#47;unhide no such file or </div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/1d/ed26272a.jpg" width="30px"><span>Chouee</span> 👍（1） 💬（0）<div>之前总抱怨Xcode编译太慢。。。原来是自己的见识太少🤣</div>2019-03-24</li><br/>
</ul>