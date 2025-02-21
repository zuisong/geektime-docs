你好，我是陈航。

俗话说，工欲善其事，必先利其器。任何一门新技术、新语言的学习，都需要从最基础的工程环境搭建开始，学习Flutter也不例外。所以，作为专栏的第一篇文章，我会与你逐一介绍Flutter的开发环境配置，并通过一个Demo为你演示Flutter项目是如何运行在Andorid和iOS的模拟器和真机上的。如果你已经掌握了这部分内容，那可以跳过这篇预习文章，直接开始后面内容的学习。

由于是跨平台开发，所以为了方便调试，你需要一个可以支持Android和iOS运行的操作系统，也就是macOS，因此后面的内容主要针对的是在macOS系统下如何配置Flutter开发环境。

如果你身边没有macOS系统的电脑也没关系，在Windows或Linux系统上配置Flutter也是类似的方法，一些关键的区别我也会重点说明。但这样的话，你就只能在Android单平台上开发调试了。

## 准备工作

### 安装Android Studio

Android Studio是基于IntelliJ IDEA的、Google官方的Android应用集成开发环境(IDE)。

我们在[官网](https://developer.android.com/studio/index.html?hl=zh-cn)上找到最新版（截止至本文定稿，最新版为3.4），下载后启动安装文件，剩下的就是按照系统提示进行SDK的安装和工程配置工作了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/0e/2b987d54.jpg" width="30px"><span>蜉蝣</span> 👍（16） 💬（3）<div>第一次搞移动端的东西，搭建环境花费了些时间。成功后我把过程记录了下来，希望能帮到搭环境时遇到问题的朋友：http:&#47;&#47;youguanxinqing.xyz&#47;index.php&#47;archives&#47;95&#47;</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/a3/af469d27.jpg" width="30px"><span>Qilin Lou</span> 👍（14） 💬（3）<div>我用的VS Code写，也挺方便的</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f7/e3/17212dce.jpg" width="30px"><span>国良</span> 👍（4） 💬（1）<div>Xcode用了n年，前两年开始用native script、react native做跨平台，以及后端的node js开发都是用vscode，对于android studio不慎了解，没有仔细的学习过，它比VS code好吗？</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/66/31629628.jpg" width="30px"><span>MaO</span> 👍（2） 💬（2）<div>是不是还要装dart SDK</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/3f/3ed9119b.jpg" width="30px"><span>Eagle~</span> 👍（2） 💬（2）<div>感觉环境配置有点简略了，忽略了安装中可能出现的问题，不如https:&#47;&#47;book.flutterchina.club&#47;chapter1&#47;install_flutter.html这篇文章详细。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/83/b2/e83dd93c.jpg" width="30px"><span>🌙</span> 👍（2） 💬（1）<div>在xcode上运行hello world项目提示could not find included file &#39;Generated.xcconfig&#39; in search paths (in target &#39;Runner&#39;)，这个怎么解决？</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/7a/64f1c75a.jpg" width="30px"><span>红烧清蒸</span> 👍（2） 💬（2）<div>输入flutter emulators --launch Nexus_6P_API_27命令后报错：
emulator: ERROR: Running multiple emulators with the same AVD is an experimental
feature.
Please use -read-only flag to enable this feature.
请问需要怎么解决</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（1） 💬（1）<div>冒个泡，win的Android studio没有这个preference的选项，安装插件要到file里面的setting中去搜索安装flutter。
据说mdp今年要改模具，不想用旧的，又不想当小白鼠，难受。</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/bb/019c18fc.jpg" width="30px"><span>徐云天</span> 👍（1） 💬（1）<div>我一直以为fluter是在web的基础上打包，然后andriod，ios上运行，，，，，</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/93/58/7c35e395.jpg" width="30px"><span>泰山</span> 👍（0） 💬（1）<div>老师能不能提供下androidstudio 创建完flutter后，整体的界面结构的讲解呢？</div>2019-12-09</li><br/><li><img src="" width="30px"><span>Geek_0ea3e4</span> 👍（0） 💬（1）<div>怎么创建带podfile和ios  第三方库比如引入高德的flutter工程</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/78/2828195b.jpg" width="30px"><span>隰有荷</span> 👍（0） 💬（1）<div>在windows上开发Flutter是完全无法将项目运行在ios系统上吗？比如我在android上运行没问题了，有没有办法实现让app在ios上跑起来？</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/66/31629628.jpg" width="30px"><span>MaO</span> 👍（0） 💬（1）<div>flutter doctor运行时间很长吗，无反应</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6b/91/c7f1f0a2.jpg" width="30px"><span>西伯利亚大风车</span> 👍（0） 💬（1）<div>纯flutterApp上AppStore能审核通过吗？</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ee/27/58171269.jpg" width="30px"><span>Justin</span> 👍（0） 💬（1）<div>无法打开“idevice_id”，因为无法验证其完整性。
flutter run会出现这个错误，怎么解决</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/53/b4590ccc.jpg" width="30px"><span>阿文</span> 👍（0） 💬（1）<div>windows上，一直报
No connected devices found; please connect a device, or see flutter.io&#47;setup for getting started instructions.
网上各种方法，弄了没啥用</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/00/4093f39a.jpg" width="30px"><span>杨赛</span> 👍（0） 💬（1）<div>android studio 运行demo项目的时候,各种错误
aunching lib&#47;main.dart on Android SDK built for x86 in debug mode...
Initializing gradle...
Resolving dependencies...
* Error running Gradle:
ProcessException: Process &quot;&#47;Users&#47;json&#47;dev&#47;flutter&#47;flutter_app&#47;android&#47;gradlew&quot; exited abnormally:

FAILURE: Build failed with an exception.

* What went wrong:
A problem occurred configuring root project &#39;android&#39;.
&gt; Could not resolve all artifacts for configuration &#39;:classpath&#39;.
   &gt; Could not resolve com.android.tools.build:gradle:3.2.1.
     Required by:
         project :
      &gt; Could not resolve com.android.tools.build:gradle:3.2.1.
         &gt; Could not get resource &#39;https:&#47;&#47;dl.google.com&#47;dl&#47;android&#47;maven2&#47;com&#47;android&#47;tools&#47;build&#47;gradle&#47;3.2.1&#47;gradle-3.2.1.pom&#39;.
            &gt; Could not GET &#39;https:&#47;&#47;dl.google.com&#47;dl&#47;android&#47;maven2&#47;com&#47;android&#47;tools&#47;build&#47;gradle&#47;3.2.1&#47;gradle-3.2.1.pom&#39;. Received status code 504 from server: Couldn&#39;t connect: Connection refused
   &gt; Could not resolve org.jetbrains.kotlin:kotlin-gradle-plugin:1.2.71.
     Required by:
         project :
      &gt; Could not resolve org.jetbrains.kotlin:kotlin-gradle-plugin:1.2.71.
         &gt; Could not get resource &#39;https:&#47;&#47;dl.google.com&#47;dl&#47;android&#47;maven2&#47;org&#47;jetbrains&#47;kotlin&#47;kotlin-gradle-plugin&#47;1.2.71&#47;kotlin-gradle-plugin-1.2.71.pom&#39;.
            &gt; Could not GET &#39;https:&#47;&#47;dl.google.com&#47;dl&#47;android&#47;maven2&#47;org&#47;jetbrains&#47;kotlin&#47;kotlin-gradle-plugin&#47;1.2.71&#47;kotlin-gradle-plugin-1.2.71.pom&#39;. Received status code 504 from server: Couldn&#39;t connect: Connection refused

* Try:
Run with --stacktrace option to get the stack trace. Run with --info or --debug option to get more log output. Run with --scan to get full insights.

* Get more help at https:&#47;&#47;help.gradle.org

BUILD FAILED in 0s
  Command: &#47;Users&#47;json&#47;dev&#47;flutter&#47;flutter_app&#47;android&#47;gradlew app:properties

Finished with error: Please review your Gradle project setup in the android&#47; folder.</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/69/2d/2d9ec7f1.jpg" width="30px"><span>三月四晴</span> 👍（0） 💬（2）<div>flutter emulators  找不到ios的模拟器 但是 我能用xcode 把项目运行到模拟器</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/01/d9cb531d.jpg" width="30px"><span>这得从我捡到一个鼠标垫开始说起</span> 👍（0） 💬（1）<div>公司的网络运行flutter doctor一直都没反应，用了手机热点就可以了，这是什么原因啊</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/36/55/2dac36fb.jpg" width="30px"><span>Echo Zuo</span> 👍（0） 💬（1）<div>你好，我想问一下。我现在学习flutter用的IDE是 VScode以及IntelliJIDEA，我发现VSCode写dart的时候代码提示特殊快速，但是IDEA很多都没提示，不知道是不是哪里设置的有问题呢？</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/18/7cbc34eb.jpg" width="30px"><span>davidzhou</span> 👍（0） 💬（2）<div>我把flutter 1.5.2换了成最新的1.7.8后，运行启动模拟器会报一大堆文件找不到的错误
Compiler message:
file:&#47;&#47;&#47;Users&#47;zhouh001&#47;Documents&#47;flutter&#47;packages&#47;flutter&#47;lib&#47;src&#47;material&#47;bottom_navigation_bar.dart:9:8: Error: Error when reading &#39;file:&#47;&#47;&#47;Users&#47;zhouh001&#47;Documents&#47;flutter&#47;.pub-cache&#47;hosted&#47;pub.flutter-io.cn&#47;vector_math-2.0.8&#47;lib&#47;vector_math_64.dart&#39;: No such file or directory
import &#39;package:vector_math&#47;vector_math_64.dart&#39; show Vector3;</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/83/b2/e83dd93c.jpg" width="30px"><span>🌙</span> 👍（0） 💬（1）<div>只用Android studio或者xcode写代码就行了吗？</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/dd/cc78f200.jpg" width="30px"><span>卢三</span> 👍（0） 💬（1）<div>安卓虚拟机跑不起来，iOS可以，安卓报错，

Resolving dependencies...
* Error running Gradle:
ProcessException: Process &quot;&#47;Users&#47;luyang&#47;flutter&#47;examples&#47;hello_world&#47;android&#47;gradlew&quot; exited abnormally:

&gt; Configure project :app
Checking the license for package Android SDK Build-Tools 28.0.3 in &#47;Users&#47;XX&#47;Library&#47;Android&#47;sdk&#47;licenses
Warning: License for package Android SDK Build-Tools 28.0.3 not accepted.
Checking the license for package Android SDK Platform 28 in &#47;Users&#47;luyang&#47;Library&#47;Android&#47;sdk&#47;licenses
Warning: License for package Android SDK Platform 28 not accepted.
  Command: &#47;Users&#47;XX&#47;flutter&#47;examples&#47;hello_world&#47;android&#47;gradlew app:properties

Finished with error: Please review your Gradle project setup in the android&#47; folder.
请教怎么解决</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5d/d2/11a12e7a.jpg" width="30px"><span>F.M.Rong</span> 👍（0） 💬（1）<div>老师，麻烦老师解答下，谢谢。
我装的3.4版本，cmd命令行flutter run ，模拟器能正常运行了。但在AS中，改热更新时，有以下几个问题：
1、工具栏没有Target selector和add configuration，也没有找到怎么添加出来；
2、老师的AS是什么版本；
3、我的运行run按钮是置灰的；
4、run按钮旁边的是add configuration；
另外，我的.grandle是网上下载放到C盘用户下的。</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/59/e8/53805867.jpg" width="30px"><span>妲己姥姥</span> 👍（0） 💬（3）<div>在公司电脑上配置环境几乎把坑都踩遍了，不过绝大部分都解决了，只剩最后一个，运行flutter doctor检查时提示Android Studio
    X Flutter plugin not installed; this adds Flutter specific functionality.
    X Dart plugin not installed; this adds Dart specific functionality.
然而确认as上这两个插件都是装了的并且卸了重装了几遍，但还是没用=。=请问有人遇到这问题吗，现在卡在这了</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/10/0c/0064aadd.jpg" width="30px"><span>Banana คิดถึง</span> 👍（0） 💬（1）<div>这是我的安装过程记录，有需要的朋友可以看下😁,https:&#47;&#47;glud.netlify.com&#47;2018&#47;11&#47;20&#47;flutter%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA&#47;</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/36/f5/a10bfe05.jpg" width="30px"><span>神巅巅</span> 👍（0） 💬（1）<div>请问老师为什么hot reload没有用？配置了export NO_PROXY=localhost,127.0.0.1
Android studio中hot reload的按钮也是灰色的</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>Failed to create provisioning profile.
There are no devices registered in your account on the developer website. Plug in and select a device to have Xcode register it.

No profiles for &#39;jiang.flutter.examples.hello-world&#39; were found
Xcode couldn&#39;t find any iOS App Development provisioning profiles matching &#39;jiang.flutter.examples.hello-world&#39;.

Mac Xcode 添加完账户后，证书下载失败的，这怎么解决呢？</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>我想用vscode 开发， 必须要安装Android Studio吗？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5a/7f/c50d520e.jpg" width="30px"><span>颜为晨</span> 👍（0） 💬（2）<div>我的电脑上，iOS 模拟器用 flutter emulators 找不到，而会被 flutter devices 会列举出来。装的是 v1.7.8+hotfix.3</div>2019-07-15</li><br/>
</ul>