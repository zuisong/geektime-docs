你好，我是戴铭。

我已经在专栏的第一篇文章中，和你梳理了一份iOS开发的知识体系框架图。今天，我们就正式从基础出发，开始自己的iOS开发知识体系构建之路吧。接下来，我就先和你聊聊与App启动速度密切相关的那些事儿。希望你听我说完启动速度的事儿之后，在专栏里的学习状态也能够快速地启动起来。

在文章开始前，我们先设想这么一个场景：假设你在排队结账时，掏出手机打开App甲准备扫码支付，结果半天进不去，后面排队的人给你压力够大吧。然后，你又打开App乙，秒进，支付完成。试想一下，以后再支付时你会选择哪个App呢。

不难想象，在提供的功能和服务相似的情况下，一款App的启动速度，不单单是用户体验的事情，往往还决定了它能否获取更多的用户。这就好像陌生人第一次碰面，第一感觉往往决定了他们接下来是否会继续交往。

由此可见，启动速度的优化必然就是App开发过程中，不可或缺的一个环节。接下来，我就先和你一起分析下App在启动时都做了哪些事儿。

## App 启动时都干了些什么事儿？

一般情况下，App的启动分为冷启动和热启动。

- 冷启动是指， App 点击启动前，它的进程不在系统里，需要系统新创建一个进程分配给它启动的情况。这是一次完整的启动过程。
- 热启动是指 ，App 在冷启动后用户将 App 退后台，在 App 的进程还在系统里的情况下，用户重新启动进入 App 的过程，这个过程做的事情非常少。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/3a/6b936a95.jpg" width="30px"><span>Glenn•D</span> 👍（3） 💬（1）<div>模拟器上试了一下耗时检查没有效果</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2e/88/0f0c19b2.jpg" width="30px"><span>好多余先生丶</span> 👍（117） 💬（3）<div>完了，上来就懵逼</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/50/a512d08d.jpg" width="30px"><span>Neo</span> 👍（27） 💬（1）<div>不错  提纲挈领  希望汇编那块能稍微细讲一下  没有太多写汇编的经验</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/37/32/758ef1c7.jpg" width="30px"><span>西京富贵兔</span> 👍（33） 💬（2）<div>看完这篇我膨胀了，我都敢去点 objc_msgSend 源码文件了，嗯，不出意料，一句没看懂。。。</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/38/d2/c6438ae9.jpg" width="30px"><span>星空</span> 👍（30） 💬（1）<div>友情提示：想要尝试SMCallTrace的朋友，需要在SMCallTrace.m中打开第54行的注释。</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/73/68d063b3.jpg" width="30px"><span>嗨</span> 👍（21） 💬（2）<div>只有C和OC基础，学起来很吃力</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/36/7b/3788ca13.jpg" width="30px"><span>冰风落叶</span> 👍（19） 💬（3）<div>大佬们 这是我的写的总结和课后作业 不知道写的对不对 恳请各位大佬指正
总结：https:&#47;&#47;www.jianshu.com&#47;p&#47;f26c4f16692a
课后作业：https:&#47;&#47;github.com&#47;308823810&#47;BSMonitorTimeTool</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2f/50/b46a9b6a.jpg" width="30px"><span>哈</span> 👍（19） 💬（1）<div>说swift没有main函数那位，其实swift是有main函数的，只不过苹果把它精简成了一个@NSApplicationMain了而已，不信去你的AppDelegate.swift最上面看！</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ee/27/58171269.jpg" width="30px"><span>Justin</span> 👍（17） 💬（5）<div>戴老师：多个动态库进行合并，具体怎么合并了，没弄过动态库合并该功能</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2f/fc/5e181fa8.jpg" width="30px"><span>Kam</span> 👍（15） 💬（2）<div>这个方法耗时计算的工具很赞，白天要花点时间实践一下才行。

有个让我疑惑的地方是关于“热启动”的概念，我再去看了下 WWDC 上的说法，里面提到热启动应该也包括“启动后退出 App 再启动”这种情况，不知道我下面这段话的理解是否正确：

“And a warm launch is an app where the application is already in memory, either because it&#39;s been launched and quit previously, and it&#39;s still sitting in the discache in the kernel, or because you just copied it over.”
- https:&#47;&#47;developer.apple.com&#47;videos&#47;play&#47;wwdc2016-406&#47;?time=1484

</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/4e/ef406442.jpg" width="30px"><span>唯她命</span> 👍（10） 💬（1）<div>hook 了 objc_msgSend 方法，就可以 hook  oc全部方法，这句话我不赞成，看objc源码，你会发现有的oc方法直接通过函数指针调用的,这时候hook 了 objc_msgSend 方法，是没有用的</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/af/50c3e8dd.jpg" width="30px"><span>登品</span> 👍（8） 💬（3）<div>公司项目启动70+的pod库 ，光pre-main时间都要3.x s了
所以光优化下main后面的 没啥卵用。 大佬main前的优化 有什么资料嘛 谢谢</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/40/70/9de7e26e.jpg" width="30px"><span>流逝……</span> 👍（8） 💬（1）<div>有点懵……不知道从哪下手。这个得有啥技术储备才能看的明白点……</div>2019-03-16</li><br/><li><img src="" width="30px"><span>Geek_d744d2</span> 👍（8） 💬（1）<div>戴铭老师，fishhook部分代码我看不大懂，我是需要补哪方面的知识呢？</div>2019-03-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLBb60HEtcav8eZb0LuMZiaVmuCBkpFGeP7XjHtgRxDMZeR7wnWNWy2jOUyA1oKWA5DuZ7UbMUqA67w/132" width="30px"><span>Ke哀</span> 👍（7） 💬（3）<div>今天看到大佬的课程，发现说的hook objc_msgSend的汇编部分，但是发现在教程中的部分和之前大神17年博客部分是一样的，都是InspectiveC&#47;InspectiveCarm64.mm的汇编代码。然后跑去大神的github找到开源项目已阅，拿出里边hook objc_msgSend的汇编实现，然后有些部分不太理解。希望大神可以解答一下（这些是已阅里边拿出来的汇编）
1.为什么这里要把lr移到x2，x4移到x3呢？
__asm volatile (&quot;mov x2, lr\n&quot;);
__asm volatile (&quot;mov x3, x4\n&quot;);
2.为什么要在调用before_objc_msgSend，orig_objc_msgSend，after_objc_msgSend方法前后把x8，x9的值存入栈中呢？
__asm volatile (&quot;stp x8, x9, [sp, #-16]!\n&quot;);
__asm volatile (&quot;mov x12, %0\n&quot; :: &quot;r&quot;(&amp;before_objc_msgSend));
__asm volatile (&quot;ldp x8, x9, [sp], #16\n&quot;);
3.为什么在三个方法执行完之后呢，最后x0会存储最后的函数返回地址呢？我打断点看到每次都是这样的，不太理解，然后把x0，移到lr确实是为了执行之前objc_msgSend执行后下一条执行的代码段段地址。
__asm volatile (&quot;mov lr, x0\n&quot;);</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/d7/12/416b60ba.jpg" width="30px"><span>Sean Ma</span> 👍（7） 💬（1）<div>上来就汇编，营养跟不上。想问个问题，文中提到首屏渲染渲染后指的是“这个阶段就是从渲染完成时开始，到didFinishLaunchingWithOptions方法域结束而结束”，我自己跑demo的时候，看到首页viewcontroller完成加载渲染出来能看到都要等到didFinishLaunchingWithOptions return true，所以我这里对首屏渲染后的界定有疑惑</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/ba/23c9246a.jpg" width="30px"><span>mαnajay</span> 👍（6） 💬（1）<div>sunnyxx 中翻译的main 函数之前 系统执行顺序是
----
从 kernel 留下的原始调用栈引导和启动自己
将程序依赖的动态链接库递归加载进内存，当然这里有缓存机制
non-lazy 符号立即 link 到可执行文件，lazy 的存表里
Runs static initializers for the executable
找到可执行文件的 main 函数，准备参数并调用
程序执行中负责绑定 lazy 符号、提供 runtime dynamic loading services、提供调试器接口
程序main函数 return 后执行 static terminator
某些场景下 main 函数结束后调 libSystem 的 _exit 函数
---
多了不少东西</div>2019-03-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xVcA2wzqLYZaeTo7cSA2k3cJVylT3sibmcauzQRUVpJqfxkIJetkCUV7iaVWQuSuCSBICV2AfF2AS5xl1Fgo0pcw/132" width="30px"><span>枫林</span> 👍（6） 💬（1）<div>最多6 个非系统动态库合并为一个，目前项目中很很多模块，基本都是动态库，怎么合并成一个呢？</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/ba/23c9246a.jpg" width="30px"><span>mαnajay</span> 👍（6） 💬（1）<div>如何合并动态库，是将多个业务动态库代码全挪到一个动态库模块还是有其他方法？</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9b/49/33b2da58.jpg" width="30px"><span>学无止境</span> 👍（6） 💬（1）<div>一上来就这么干，有点难吸收啊。
没个几年的iOS深入学习的话，这课还真的不好懂。
能在文章中多提供点资料么或者再讲的细点。
瞬间感觉自己是个渣渣</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fb/35/bfe3a609.jpg" width="30px"><span>lfsoul</span> 👍（5） 💬（3）<div>+load为啥会增加4毫米那，求详解一下</div>2019-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/iaYibsvL94uobwgXsHVUnFh0AzibQAmWQicibytkmIEvmFhAPBpj8lXnjmYcJySqgDPoIeLAAicQFrIJVS9uNZbD7gmw/132" width="30px"><span>灬路上</span> 👍（5） 💬（1）<div>有毒！为了不漏学每个知识，我把每条评论都看了，并把有用的Mark下来，深耕！</div>2019-03-15</li><br/><li><img src="" width="30px"><span>大官人</span> 👍（5） 💬（1）<div>最好的学习就是自己动手啊，课后作业的得做，不然感觉啥都没记住……</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/9c/7afa883f.jpg" width="30px"><span>李小草</span> 👍（4） 💬（1）<div>我知道可以借助三方工具类BSBacktraceLogger获取主线程调用栈（[BSBacktraceLogger bs_backtraceOfMainThread];），然后定时0.01秒计算各方法的调用耗时。但是具体不知道该怎么计算啊，望老师指点！</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/a9/122d6266.jpg" width="30px"><span>✨嘿o大远</span> 👍（4） 💬（2）<div>听的比较费力,感觉要用很多时间来研究了,加油</div>2019-03-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIhZpScfeGfqAlyrd2kRkSWhDJu39yWFCG17yKWFC26WwvJJfpUNLAd11yqEWrHmOxl6M1rzgFxTg/132" width="30px"><span>Geek_vmrkge</span> 👍（4） 💬（1）<div>看完感觉老师您讲的我好像能听懂，实际要上手又懵了。。。感觉自己好像没有抓住点实质性的东西</div>2019-03-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo6Pv01Of8dF6dGjmuyqnYXUhCdKTcaFDEr5B70EmN7HyrxjQ84iaQB8wuh5ePvelezzFB6A9qLZGQ/132" width="30px"><span>PerTerbin</span> 👍（3） 💬（1）<div>获取主线程堆栈你是用什么方法，我这边使用BSBacktraceLogger提供的方法，但是在公司真实项目里跑获取主线程堆栈的方法耗时远超0.01s（真机大概在0.03s），这样统计出来的时间就没什么意义，有什么比较不耗时的的获取堆栈方法吗？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/30/7c/25782d96.jpg" width="30px"><span>弈林丶修特</span> 👍（3） 💬（1）<div>这个我看完完全理解不了怎么去hook objc_msgSend啊   汇编部分调用说符号表确实pre 和post对应的  也没看到讲述中怎么实现这两个</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3c/f9/3c2561db.jpg" width="30px"><span>Drunkard</span> 👍（2） 💬（2）<div>大佬 帮忙看看这个做法对不对？
https:&#47;&#47;github.com&#47;308823810&#47;BSMonitorTimeTool</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/9d/1b6f2ae1.jpg" width="30px"><span>风一样的人</span> 👍（2） 💬（1）<div>作业有点摸不着头脑，方便提供下思路不？
目前有两个问题：如何定时获取函数栈？
                        获取函数栈后如何计算函数调用时间？
</div>2019-03-25</li><br/>
</ul>