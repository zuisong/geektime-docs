你好，我是南柯。

通过上一章的学习，我们已经掌握了AI绘画的基础知识，了解了扩散模型、CLIP模型、自回归模型等模块的基本原理。从今天开始我们进入进阶篇的学习，我会带你基于已经了解的基础知识，继续探索业界最新最火的AI绘画模型。学完这部分内容，AI绘画的黑魔法在你面前就不是秘密了。

这一讲，我们将要学习的是引爆本轮AI绘画技术热潮的明星模型：DALL-E 2。

DALL-E 2是2022年4月由OpenAI发布的AI绘画模型，它的绘画效果相比过去的工作有了质的飞跃，而且它提出的unCLIP结构、图像变体能力也被后来的方法所效仿。我们只有真正理解了DALL-E 2，才算拿到了进入AI绘画世界的钥匙。

## 初识DALL-E 2

DALL-E这个名字源自西班牙艺术家Salvador Dali和皮克斯动画机器人Wall-E的组合。如果你想体验OpenAI的DALL-E 2原汁原味的效果，可以使用Edge浏览器NewBing的AI绘画能力。目前，NewBing的AI绘画能力还没有向中国大陆地区开放，需要你发挥聪明才智来体验它。如果你有好的办法，也欢迎你分享在评论区。

比如我们要求DALL-E 2帮我们生成一只可爱的精灵。你可以点开图像查看效果。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/e1/30/56151c95.jpg" width="30px"><span>徐大雷</span> 👍（0） 💬（1）<div>老师，在初识 DALL-E 2 这个章节里面，生成图像变体，图像融合是怎么在微软必应里面操作的？谢谢</div>2023-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>本讲所说的DALL-E 2，其能力低于SD和Midjourney吧。</div>2023-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b1/f4/61a74269.jpg" width="30px"><span>不会数数</span> 👍（0） 💬（1）<div>关于必应生成图片的例子并不合适，red furry monster 翻译成中文应该是红毛怪兽, 和红发精灵的描述完全不一样，按照稍微正常点的翻译生成的图，得到的风格是相似的。</div>2023-08-16</li><br/>
</ul>