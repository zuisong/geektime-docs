大家好，我是陆晓明，现在在一家互联网手机公司担任Android系统开发工程师。很高兴可以在极客时间Android开发高手课专栏里，分享一些我在手机行业9年的经验以及学习Android的方法。

今天我要跟你分享的是Framework的学习和调试的方法。

首先，Android是一种基于Linux的开放源代码软件栈，为广泛的设备和机型而创建。下图是Android平台的[主要组件](https://developer.android.google.cn/guide/platform)。

![](https://static001.geekbang.org/resource/image/90/df/90763fd9662c8a75553dc92a78112ddf.png?wh=1384%2A2038)

从图中你可以看到主要有以下几部分组成：

- **Linux内核**
- **Android Runtime**
- **原生C/C++库**
- Java API框架（后面我称之为Framework框架层）
- **系统应用**

我们在各个应用市场看到的，大多是第三方应用，也就是安装在data区域的应用，它们可以卸载，并且权限也受到一些限制，比如不能直接设置时间日期，需要调用到系统应用设置里面再进行操作。

而我们在应用开发过程中使用的四大组件，便是在Framework框架层进行实现，应用通过约定俗成的规则，在AndroidMainfest.xml中进行配置，然后继承对应的基类进行复写。系统在启动过程中解析AndroidMainfest.xml，将应用的信息存储下来，随后根据用户的操作，或者系统的广播触发，启动对应的应用。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（9） 💬（1）<div>我就是有个毛病，遇到难的，更底层的东西总想着绕过去，而不是迎头而上，所以很多时候不能很好的解决问题。惧怕看源码，调试，到现在不一样了，我也知道很多高手都是能轻松看源码和调试，所以我也试着改变自己了</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/c2/e8ac8b6d.jpg" width="30px"><span>亮</span> 👍（23） 💬（0）<div>以前总以为调试源码需要下载源代码，编译工程，今天才知道原来还可以这样，新技能get√</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b9/76/bc5f8468.jpg" width="30px"><span>品牌运营|陆晓明</span> 👍（12） 💬（0）<div>如果调试某个具体的流程，就将关联的文件放到对应的包名下即可。找对你要调试的进程，就可以在这些文件的具体方法下断点，进行调试跟踪。

当发现没有调试上的时候，可以确定下是否源码不匹配？是否调试的进程不对（可以通过干掉你调试的进程，看看是否你调试的东西会挂掉，当然systemserver干掉手机就软重启啦。你想调试systemserver的启动过程，倒是可以这么干）在调试的过程中，使用源码阅读工具，将相关联的代码放入环境，在可疑地方，或者方法调用的地方设断点，做个简单判定即可，然后使用多个断点的设定，来卡住具体走到哪个流程，在断住之后，使用堆栈回溯，看看调用顺序，帮你梳理整个流程。</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/24/07/380666e3.jpg" width="30px"><span>bytecode</span> 👍（8） 💬（2）<div>调试Android Framework的Java部分代码，以调试源码android-28为例，需要一个API 28的模拟器配合使用。
1、下载源码
下载源码方式很多，由于调试Framework只需要java代码即可，这里使用Android Studio的SDK Manager下载android-28为例，sdk&#47;sources下看到android-28源码。
2、新建一个项目，包名cn.test.demo，避免com开头是因为源码有com，等下拷贝源码是避免重复。
3、拷贝源码到项目的java目录下。
4、新建一个与源码对应的模拟器。
5、启动模拟器，选择debug的进程。
6、选择某一个源码类进行调试。
更多查看：https:&#47;&#47;github.com&#47;libill&#47;DebugAndroidFramework</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b9/76/bc5f8468.jpg" width="30px"><span>品牌运营|陆晓明</span> 👍（7） 💬（1）<div>楼上说的官方是在8.1，需要自己切换分支，下载9.0的就行了。 国内的可以先使用清华镜像下载，下载好了切换到9.0的代码上。

有问题欢迎在官方安卓进阶开发微信群@ 我，随时等待大家的交流。</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b9/76/bc5f8468.jpg" width="30px"><span>品牌运营|陆晓明</span> 👍（3） 💬（1）<div>看到很多朋友留言，让我感觉受宠若惊。不时在看着留言又有哪些问题，想给大家更好的解答。
极客没有专门针对一条留言回复的功能，导致回复的有些乱。
如果有机会，欢迎大家加我微信，帮你解答调试中的任何疑问。
再次感谢！
我的微信

code_gg_boy

</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/0e/0db41dda.jpg" width="30px"><span>tt716</span> 👍（3） 💬（0）<div>有一个问题，如何能下到与genymotion中镜像对应的源码呢？不然debug的时候有的行会对不上</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/42/f510bb91.jpg" width="30px"><span>wang_acmilan</span> 👍（3） 💬（0）<div>支持明哥，前排占座。调试framework是系统工程师必备技能。</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/b7/a3468e61.jpg" width="30px"><span>OF</span> 👍（0） 💬（0）<div>我去，过了两年才看到这个，两年白瞎了</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/ce/e22e2cda.jpg" width="30px"><span>河里的枇杷树、</span> 👍（0） 💬（0）<div>豁然开朗啊</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/5d/a45f1e49.jpg" width="30px"><span>想不出名字</span> 👍（0） 💬（0）<div>有什么好的framework的书介绍吗？framework的资源好难找</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/37/55/606bc5f7.jpg" width="30px"><span>邱</span> 👍（0） 💬（0）<div>以前一直以为只有对应源码，对应手机版本才能调试 framework。这时才恍然大悟，可以用 Genymotion，加官方代码</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c0/f0/1aabc056.jpg" width="30px"><span>Jiantao</span> 👍（0） 💬（1）<div>模拟器+对应sdk版本源码+调试进程 ，就可以debug了。感谢分享。</div>2019-05-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/B30fTWp3jZVV1UJP4Kwd0DXYDohhoN2IHB4YN3B09hmKvibentQYyr5p0AEsqfgEpGZ4czHPnphLJqtibmjTodibQ/132" width="30px"><span>abero</span> 👍（0） 💬（0）<div>真机可以调试源码吗</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e1/f9/6e8203fe.jpg" width="30px"><span>h波</span> 👍（0） 💬（3）<div>我在实际操作中，在 Attach debugger to Android process 中找不到 system_process 这个进程，这是怎么回事呀</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5c/91/22b90232.jpg" width="30px"><span>张曦</span> 👍（0） 💬（0）<div>涨姿势，支持明哥！</div>2019-03-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTISkR0XDibLuwwl6PibTpQmDrnV7feN1YibqvrnpCE8fVk5cPPuUUxqvW4IZicrmTKXueTW6LpSNrxt4w/132" width="30px"><span>一片羽毛</span> 👍（0） 💬（0）<div>回去实验下</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/51/9073faa5.jpg" width="30px"><span>seven</span> 👍（0） 💬（0）<div>🐮🐮🐮
赞了收藏再说！</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/89/207cc841.jpg" width="30px"><span>HI</span> 👍（0） 💬（0）<div>长见识了。。不过对于native的函数还是挺麻烦的，不知道是否有好的办法</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/39/b47b1bc0.jpg" width="30px"><span>奚岩</span> 👍（0） 💬（0）<div>文中提到的到 androidxref 下载的源码，是一个个下载么，怎么全部下载呢？
官方的 aosp 网站（ https:&#47;&#47;source.android.com&#47;setup&#47;build-numbers.html#source-code-tags-and-builds ）最新的是 8.1 的。</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/e6/6a88c8a3.jpg" width="30px"><span>刘伟</span> 👍（0） 💬（0）<div>这两天遇到一个问题：
framework.jar 应该就是framework的源码，但是这两天我遇到一个崩溃，这个崩溃打印出来的线程调用栈 和 framework.jar 中反编译的源码不一样，这是为什么呢？

这个  framework.jar  是我从出现崩溃的手机上导出的







</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8b/85/e50b98f1.jpg" width="30px"><span>张乐</span> 👍（0） 💬（0）<div>很好的介绍，可以再具体介绍单个模块的？</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/34/abb7bfe3.jpg" width="30px"><span>再前进一点</span> 👍（0） 💬（0）<div>您好，如果是看一个特定启动流程，是不是得把涉及到的类都copy到studio</div>2019-03-12</li><br/>
</ul>