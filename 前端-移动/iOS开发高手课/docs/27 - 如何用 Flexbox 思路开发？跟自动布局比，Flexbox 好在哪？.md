你好，我是戴铭。今天，我要和你跟你聊聊 Flexbox。

你很有可能不知道Flexbox 是啥，但一定不会对 React Native、Weex 和 Texture（AsyncDisplayKit） 感到陌生，而Flexbox就是这些知名布局库采用的布局思路。不可小觑的是，苹果公司官方的UIStackView，也是采用Flexbox思路来实现布局的。

接下来，我们就一起来看看Flexbox布局思路有什么优势，以及如何用它来实现布局。

## Flexbox 好在哪？

目前来看，iOS 系统提供的布局方式有两种：

- 一种是 Frame 这种原始方式，也就是通过设置横纵坐标和宽高来确定布局。
- 另一种是自动布局（Auto Layout），相比较于 Frame 需要指出每个视图的精确位置，自动布局对于视图位置的描述更加简洁和易读，只需要确定两个视图之间的关系就能够确定布局。

通过 [Masonry](https://github.com/SnapKit/Masonry)和 [SnapKit](https://github.com/SnapKit/SnapKit)这些第三方库，自动布局的易用性也有了很大提升。而且iOS 12 以后，苹果公司也已经解决了自动布局在性能方面的问题（这里，你可以再回顾下前面第4篇文章[《Auto Layout 是怎么进行自动布局的，性能如何？》](https://time.geekbang.org/column/article/85332)中的相关内容）。

那么在这种情况下，**我们为什么还要关注其他布局思路呢？**关于原因，我觉得主要包括以下两个方面。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/41/e7d5ee4e.jpg" width="30px"><span>豆豆斗地主</span> 👍（0） 💬（1）<div>老师您好 请问在实际开发中 是否以删除 storyboard的方式进行开发？</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2e/b1/85bbfa6b.jpg" width="30px"><span>Jeffrey</span> 👍（8） 💬（0）<div>肯定frame效率高 </div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4a/52/5e8972b6.jpg" width="30px"><span>K</span> 👍（6） 💬（3）<div>以下是个人理解，如有问题请指正，谢谢。
yoga是对frame的封装，内部实现了Flexbox算法（理念），texture是对yoga的封装，增加了异步渲染等。 性能上，由于frame是线性的，所以yoga和texture也应该是线性的，或者更优。而autolayout属于指数级的，这可能跟两者算法有关。所以，在使用上，在简单的布局页面或者性能要求不高的页面可以直接使用autolayout。相反，性能要求高的页面，可以选择frame, texture, yoga.</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/c5/0e4845b5.jpg" width="30px"><span>Z</span> 👍（5） 💬（1）<div>react native 里面的布局确实比较好用，比原生节省了开发效率</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/34/95/73639020.jpg" width="30px"><span>powerGuo</span> 👍（3） 💬（0）<div>作者的怎么看flexlib这个库，我已经在我自己开始使用了，就是把flexbox编写的xml通过解析转换成Yoga的iOS原布局</div>2020-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e9/25/876c5b16.jpg" width="30px"><span>最强小鲁班</span> 👍（2） 💬（2）<div>UIStackView真的巨好用</div>2019-10-30</li><br/><li><img src="" width="30px"><span>Geek_2844bd</span> 👍（2） 💬（0）<div>Texture和frame对比，性能如何？</div>2019-05-11</li><br/><li><img src="" width="30px"><span>lvv</span> 👍（1） 💬（0）<div>推荐一下我基于 Facebook 的 yoga 修改的版本，支持 iOS macOS tvOS 项目地址：https:&#47;&#47;github.com&#47;cntrump&#47;yoga</div>2020-05-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKHFicKDOJk2zN9tJglk8eoP1wXicpRHVicNg1DycjjfcxEN02ZZ1MBWPbLSyvBMsYyIc7fVg1qbjhKg/132" width="30px"><span>Geek_8e8cbf</span> 👍（1） 💬（2）<div>那现阶段想在iOS中使用Flexbox布局，是用Yoga，还是Texture呢？</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/0b/2ccf7908.jpg" width="30px"><span>...</span> 👍（0） 💬（0）<div>flexbox相比自动布局的具体好处是?（除了前端生态之外的）</div>2021-09-04</li><br/><li><img src="" width="30px"><span>文培定</span> 👍（0） 💬（0）<div>貌似HTML本身就支持Flex吧</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/e9/bf/c968c358.jpg" width="30px"><span>秦~政</span> 👍（0） 💬（0）<div>原来UIStackView 是用来布局的啊，从来没有往这方面想过，以为就是一个方便给几个按钮啥的排一条直线的哈哈，没想过，互相嵌套；</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/f2/465a80c0.jpg" width="30px"><span>往来谁是白丁</span> 👍（0） 💬（0）<div>flutter也是类似flex box布局</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（0） 💬（0）<div>今天终于知道啥是flexbox了</div>2019-05-11</li><br/>
</ul>