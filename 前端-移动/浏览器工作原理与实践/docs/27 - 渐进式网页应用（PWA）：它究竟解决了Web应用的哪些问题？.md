在专栏[开篇词](https://time.geekbang.org/column/article/113399)中，我们提到过浏览器的三大进化路线：

- 第一个是应用程序Web化；
- 第二个是Web应用移动化；
- 第三个是Web操作系统化；

其中，第二个Web应用移动化是Google梦寐以求而又一直在发力的一件事，不过对于移动设备来说，前有本地App，后有移动小程序，想要浏览器切入到移动端是相当困难的一件事，因为浏览器的运行性能是低于本地App的，并且Google也没有类似微信或者Facebook这种体量的用户群体。

但是要让浏览器切入到移动端，让其取得和原生应用同等待遇可是Google的梦想，那该怎么做呢？

这就是我们本节要聊的PWA。那什么是PWA？PWA又是以什么方式切入到移动端的呢？

PWA，全称是Progressive Web App，翻译过来就是渐进式网页应用。根据字面意思，它就是“渐进式+Web应用”。对于Web应用很好理解了，就是目前我们普通的Web页面，所以PWA所支持的首先是一个Web页面。至于“渐进式”，就需要从下面两个方面来理解。

- 站在Web应用开发者来说，PWA提供了一个渐进式的过渡方案，让Web应用能逐步具有本地应用的能力。采取渐进式可以降低站点改造的代价，使得站点逐步支持各项新技术，而不是一步到位。
- 站在技术角度来说，PWA技术也是一个渐进式的演化过程，在技术层面会一点点演进，比如逐渐提供更好的设备特性支持，不断优化更加流畅的动画效果，不断让页面的加载速度变得更快，不断实现本地应用的特性。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/fe/0c/f9cb1af4.jpg" width="30px"><span>李艺轩</span> 👍（1） 💬（1）<div>前面说【web应用就是普通的web页面】，后面说【让普通站点逐步过渡到web应用】，那么普通站点和普通web页面有什么区别？</div>2019-12-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqfenHHNSUm2lVWfeFKMjHNcd9PjGFFZ4e2mbsgkpDmwq1oxNic3ZmaDUda517HFYWsficeReL8aA2w/132" width="30px"><span>小黑彪Geek_070fb4</span> 👍（44） 💬（3）<div>感觉机会不大：首先这个东西需要浏览器的支持，苹果方面因该有顾虑，绕过审核直接上线；其次这个东西在国内推进也是困难重重，各大厂商定制化系统，再就是谷歌的东西太容易被墙；最后这个没有商业化的闭环，不能为开发者提供用户资源等，很难和国内BAT小程序和快应用等抗衡。 总之，前途堪忧。</div>2019-10-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTICu7auk7qLuLNXfgXlia9ptcqiaKMXVuUCZTKF0FHvLW0wsSe9QJrq6B6fBgPDL4HSqyaUfReJD4Kw/132" width="30px"><span>Taopoppy</span> 👍（18） 💬（1）<div>老师，后面来一门前端优化的课程，和这个课就搭上了</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（17） 💬（0）<div>如果要达到浏览器通吃的目标，除了老师文中讲的这三点（消息通知，离线存储，一级入口），浏览器还有几个问题需要解决：
1、硬件操作能力
2、系统底层调用能力
3、执行效率
4、沙箱管理能力
其中：
1硬件操作和2系统底层调用，现在一般用hybrid方式来解决，纯浏览器暂时没有好的方案
3执行效率，有两方面，一个是期待浏览器不断变强（比如OpenGL支持），一个是Web Assembly可以期待一下
4沙箱问题（网站隔离、用户隔离），现在并没有看到很好的解决方案

另外，我一直以来的另一个问题是，现在浏览器其实已经很复杂了，如果封装很多的系统功能到浏览器里面，那最终和Android&#47;IOS有什么区别呢，除了开发语言？是否会向这个方向发展呢？</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（9） 💬（0）<div>如果PWA能够从操作系统（andriod）层面切入应该会和当前的快应用、小程序分一杯羹。技术之间是互相学习和进步的，未来技术可能会趋同，找到一个浏览器应用（pwa）、大流量应用（微信、支付宝的小程序）、手机厂商（快应用）都满意的方案</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（3） 💬（1）<div>已经进入了呀，现在安卓各大应用商店很对应用都有提供快应用。免安装，无广告，用完即走</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/5d/9afdf648.jpg" width="30px"><span>Link</span> 👍（3） 💬（0）<div>我觉得 PWA 从商业角度和技术角度来看都没有足够的优势进入移动端，因为目前移动端的商业生态已经成熟，并且小程序技术和 Flutter 技术已经抢占了先机。商业上，目前的移动端生态已经成熟，iOS 会阻止 PWA 破坏它的生态，就像阻止小程序一样。Android 生态中，如果 Google 如果能把 Android 变成直接支持 PWA 的操作系统，可能会有一些帮助，但是帮助不大。技术上，微信等各大超级 App 都已经使用了小程序技术，也就是说小程序技术已经抢占了先机。另外，Flutter 技术也在进入移动端，所以 PWA 在技术上的竞争太激烈。</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/4e/3f/3e84f39e.jpg" width="30px"><span>Chin 是我啊</span> 👍（2） 💬（1）<div>三年了，PWA 并没有进入移动设备</div>2022-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/2e/332fee49.jpg" width="30px"><span>刘弥</span> 👍（2） 💬（0）<div>对于 PC 机来说的话：

我记得 google 有发行一个 chrome OS 的笔记本电脑，其给人的感觉就是一个电脑就是一个浏览器。

那么如果这个 chrome OS 能够得到很好的普及的话，也算是为 PWA 的发展道路铺开了一个非常不错的基础设施。

对于 chrome OS 的未来的话，我个人还是抱有一定的好感的，毕竟电信行业的发展还是很快速的，所以未来的应用网络传输可能越来越快速。

另外 WebAssembly 的发展也让人期待，未来一些相对底层的操作可以委托给 WebAssembly 来实现。

对于移动设备的话：

目前看起来并不乐观，如果 chrome OS 也能覆盖移动设备的话就另当别论了。</div>2020-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c9/73/a0db6d58.jpg" width="30px"><span>再学习</span> 👍（2） 💬（1）<div>作为新一代“浏览器”，国内有小程序，国外有PWA。
认为在国外PWA会发展的不错，国内因为用户对微信的依赖，可能还是小程序发展的更好。</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1f/f7be5246.jpg" width="30px"><span>大前端洞见</span> 👍（1） 💬（0）<div>通过一种说法，Web应用PWA技术等未能快速发展起来，很大的一部分原因是商业利益影响的。因为PWA应用起来了，会给APP和其他应用带来打击，各厂商为了保证利益，对PWA这种技术都会实行冷漠和阻拦的方式。比如苹果公司，是最不愿意PWA能发展起来的，苹果公司也不会积极的配合这方面技术的推进。</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（1） 💬（0）<div>老师，能否透露下您看好pwa的理由？</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ec/68/06d59613.jpg" width="30px"><span>柒月</span> 👍（1） 💬（0）<div>可以的。我觉得后面整个移动设备的系统就是一个浏览器。
好处的话就像现在的小程序，不用下载安装，随用随走。
难点的话一个是用户体验，流畅性方面。另一个的话就是跟手机底层硬件的交互能力了。</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3c/6d/70b0d892.jpg" width="30px"><span>是天才指挥官呀</span> 👍（0） 💬（0）<div>web应用是披着羊皮的狼</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/cd/b8/14597b01.jpg" width="30px"><span>西门吹雪</span> 👍（0） 💬（2）<div>web的一大缺点是离线能力 离开网络就啥也没了</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/75/e3/ef489d57.jpg" width="30px"><span>Roy</span> 👍（0） 💬（0）<div>除了要解决使用场景和本地app一样外，还需要说服开发者各大公司加入，形成生态。</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/66/16/b8e6436c.jpg" width="30px"><span>王晓蘅</span> 👍（0） 💬（0）<div>有一个疑问，小程序这样的技术，算不算是PWA的一种应用呢？消息提醒的部分其实通过公众号推送的，其实是分离。
PWA在国外的app出现的比较多，使用体验肯定是比不上原生的，但是基本功能是可以实现的，就是给对应的底层用户使用的。</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f1/0f/8b36016d.jpg" width="30px"><span>陈十二</span> 👍（0） 💬（0）<div>目前不看好，可以关注下相关信息，PWA 在能力更新方面很慢，目前来看离跨平台替代部分原生应用还有很长的路要走</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e6/5d/291dbf69.jpg" width="30px"><span>Geek_b63d98</span> 👍（0） 💬（0）<div>instgram twitter webpackdocumention</div>2019-10-09</li><br/>
</ul>