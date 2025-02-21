你好，我是蒋宏伟。

点按组件的设计与我们的用户体验息息相关。有人会因为机械键盘的敲击感好，不买百来块的薄膜键盘，而花上贵十倍的价格去买 HHKB、Filco，也有人会因为某个应用的点按体验不好，而转投竞品应用。

如果你仔细观察过世界上那些流行的、口碑很好 App，比如微信，你会看到它们在点按组件的体验的细节上都做得特别好。

比如，微信的点按组件都是有交互反馈的，无论是背景颜色的加深，还是那些舒服的震动，又或者是动画。又比如，微信顶部右上角的加号按钮是很容易点击的，它的点击区域是比显示图标大上那么一丢丢，而且点到后，即使把手指挪开图标的位置再松开也是能触发点击的。

所有的这些设计都是“懂”用户的。担心你因为网络卡、机器卡不知道有没有自己点中，在你点完后给你视觉或触觉上的反馈；担心你走路的时候想点点不到，把事件的“可触发区域”、“可保留区域 ”设置得比视觉上的“可见区域”大上那么一些。

作为直接和用户打交道的工程师，**我们也得“懂”用户，**也得去优化我们负责的 App、页面的体验，**还得在技术上搞懂点按组件使用方法和背后的原理，把这种最常用的人机交互体验给做到及格，做到优秀。**

所以，今天这节课，我会以三个问题为脉络进行讲解：
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（5） 💬（1）<div>透明度会重新变为 1 ？应该是不透明度变为 1 吧。</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/5f/06671a0d.jpg" width="30px"><span>python4</span> 👍（4） 💬（1）<div>我按官网的顺序看的, 所以用了Touchble做按钮. 看到这里才知道按钮的最佳实践, 官网顺序有点坑啊</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/6e/d0/6875ea5a.jpg" width="30px"><span>小天儿</span> 👍（1） 💬（1）<div>作业二：个人感觉是因为手指与鼠标的差异，手指点击的范围更大，不似鼠标那么精准，所以就要添加防误触的处理逻辑（不能在第一时间进行处理，以方便用户取消），而双击手势，在移动端并不常用（我猜可能是因为两次点按的位置大概率会有偏移，提高了操作成本）</div>2022-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/8e/e75ecc5e.jpg" width="30px"><span>浩明啦</span> 👍（1） 💬（0）<div>想问一下，ios 里按钮组件点按出现轻微震动的效果</div>2022-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（1） 💬（0）<div>可保留区域 默认与 可触发区域一样大吧？</div>2022-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/67/abb7bfe3.jpg" width="30px"><span>涂海生</span> 👍（1） 💬（0）<div>能不能多提供些 demo 和项目，可以多学习代码规范和用法</div>2022-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/35/f6/fc3881e7.jpg" width="30px"><span>稀饭</span> 👍（0） 💬（1）<div>动态样式怎么改变按钮的文字呢？</div>2024-09-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJsnP3W12jSoGYBoAbjMW7kKqWsD1Imnic4TX9nOR0kvkTq5ap4n0aNfuicXibKDJib0zl0PEvhcBHe3g/132" width="30px"><span>demoker</span> 👍（0） 💬（0）<div>老师 可不可以单独出一节分享一下前端开发者提效的用法，作为一个原生开发者来说，希望学了课程之后可以少走弯路。</div>2023-12-17</li><br/><li><img src="" width="30px"><span>Geek_ca7af8</span> 👍（0） 💬（0）<div>1.Pressable组件可以通过style样式的pressed参数来区分设置点击的样式和非点击的样式
2.Pressable的扩大点击区域，可以通过其HitSlop属性来实现
3.Pressable的允许用户点击button后并且及时取消button的点击(允许用户反悔)，可以通过PressRetentionOffset属性来设置，当手指最后touch屏幕的点不在PressRect之间的话，就不会触发点击操作。</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ba/5c/ca8f01b4.jpg" width="30px"><span>Wcly👺</span> 👍（0） 💬（0）<div>如果从TouchableWithoutFeedback直接替换成Pressable组件，要注意样式上的差异</div>2022-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（0）<div>Pressable
默认带动画吗</div>2022-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（1）<div>甚至还可以把“按钮”的文字改了

这是怎么改呢</div>2022-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/b5/abb7bfe3.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（1）<div>默认情况下，可点击区域就是可保留区域，因为都是可见区域，offest =0,那可点击区域可以理解成是可保留区域的子集？</div>2022-05-19</li><br/>
</ul>