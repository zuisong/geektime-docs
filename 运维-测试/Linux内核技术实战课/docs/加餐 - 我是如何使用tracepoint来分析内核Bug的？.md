你好，我是邵亚方。

我们这个系列课程的目标受众是应用开发者和运维人员，所以，你可以看到课程里的案例在分析应用问题的时候，都在尽量避免分析内核bug，避免把内核代码拿过来逐个函数地解析为什么会这样。我希望这个课程可以降低内核的门槛，让更多人可以更加容易地了解内核机制，从而更好地解决应用难题、提升应用性能。

不过，在我们这个课程的学习者中还是有一些内核开发者的，因此，我写了这篇加餐来分析内核bug，希望能把分析内核bug的一些经验分享给这些内核开发者们。

通过对课程的学习，你应该能发现，我对tracepoint和ftrace是极其推崇的。我对它推崇备至不是没有道理的，这节课我就带你来看下我是如何借助tracepoint来分析内核bug的。

## 炫技般存在的tracepoint内核源码

如果你看过tracepoint的内核代码，相信你一定对它炫技般存在的[宏定义](https://elixir.bootlin.com/linux/v5.9-rc6/source/include/linux/tracepoint.h#L229)印象深刻。我在第一眼看到这些宏定义时，也是一脸懵逼，不知从何下手，但是很快我就看懂了。为了证明我看懂了，我还特意给tracepoint的这些宏定义[又增加了一些定义](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?h=v5.9-rc8&id=163363455b42a1cf833742177149d1352dfe673e)，我增加的这个宏定义，其关键部分如下：

![](https://static001.geekbang.org/resource/image/51/5e/51b5c43325b69edae6ae5a73cd20b75e.png?wh=1206%2A840)

如果你能看明白这些，那就说明你对这些tracepoint宏的工作机制一清二楚了。当然，这节课我不是来剖析tracepoint内核源码的。如果你不懂tracepoint内核源码，也不妨碍你使用它，不过这对一名内核开发者而言终究是一件憾事。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIt0nAFvqib3fpf9AIKUrEJMdbiaPjnKqCryevwjRdqrbzAIxdOn3P5wCz28MNb5Bgb2PwEdCezLEWg/132" width="30px"><span>KennyQ</span> 👍（3） 💬（1）<div>后续能不能再开个课程专门讲讲 tracepiont,kprobe和ePBF?网上的内容都太碎片化，不成体系。
作为一个背锅的自身运维工程狮，基本经常要和开发刚正面，急需这方面的知识。
</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（1）<div># 这几个值合并起来是 0x100450 不是 0x104050呀。

此时的 GFP flags 是 0x104050，对应于下面这几项：
#define ___GFP_WAIT             0x10u
#define ___GFP_IO               0x40u
#define ___GFP_REPEAT           0x400u
#define ___GFP_KMEMCG           0x100000u

</div>2020-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/61/677e8f92.jpg" width="30px"><span>xianhai</span> 👍（0） 💬（2）<div>能不能讲讲zone的概念？
为什么要右移5？(205324kB &gt;&gt; 5)</div>2020-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/9e/aa0cd6dc.jpg" width="30px"><span>镜</span> 👍（0） 💬（0）<div>除了cpu篇都大概看完了，老师功力深厚，点赞👍</div>2021-10-08</li><br/><li><img src="" width="30px"><span>Geek_e4c979</span> 👍（0） 💬（0）<div>tracepoint这些一会define一会undef咋理解呀</div>2021-04-21</li><br/>
</ul>