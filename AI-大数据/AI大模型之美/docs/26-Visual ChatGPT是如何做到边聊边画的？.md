你好，我是徐文浩。

过去三讲里，我们分别体验了CLIP、Stable Diffusion和ControlNet这三个模型。我们用这些模型来识别图片的内容，或者通过输入一段文本指令来画图。这些模型都是所谓的多模态模型，能够把图片和文本信息联系在一起。

不过，如果我们不仅仅是要随便找几个关键词画两张画玩个票，而是要在实际的工作环境里生成能用的图片，那么现在的体验还是远远不够的。对于画出来的图我们总有各种各样的修改和编辑的需求。比如，我们总是会遇到各个团队的人对着设计师的图指手画脚地提出各种各样的意见：“能不能把小狗移到图片的右边？”“能不能把背景从草地改成森林？”“我想要一个色彩斑斓的黑。”等等。

所以，**理想中的AI画画的功能，最好还能配上一个听得懂人话的AI，能够根据我们这些外行的指手画脚来修改生成的图片。**针对这个需求，我们就来介绍一下微软开源的Visual ChatGPT。

和之前我们自己写代码不同，这一讲我们一起来读一读 [Visual ChatGPT](https://github.com/microsoft/TaskMatrix) 这个开源项目的代码，看看它是如何做到能让我们聊着天就把图片给修改完了的。

## 体验 Visual ChatGPT

我们先来体验一下Visual ChatGPT的效果是怎么样的。这一次，Colab里的GPU也不够我们用了。Visual ChatGPT要加载很多个不同的图片相关的模型，这些模型加起来的显存得有40GB以上。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（11） 💬（1）<div>人工智能的快速发展带来各类相关模型的数量爆炸性增长，选择的多样性使得应用者总能挑选出几样趁手的工具，但同时也带来了一大痛点，哪个模型是最好的呢? Visual ChatGPT 的核心板块&quot;任务矩阵&quot;(Task Matrix)就是想为客户自动选出适合解决任务的模型。诚如论文的作者指出的&quot;TaskMatrix.AI 可以理解这些 API 并学习新的 API，然后根据用户说明推荐合适的API。作者举例中的用对话的形式帮助用户生成 PPT, 并根据要求不断修改，展示了 TaskMatrix.AI 方便之处，过程流畅，但实际上这里隐含了一个前提，即用户的问题非常明确，比如: &quot;对于每家公司，让我们创建一张幻灯片来介绍它的创始人、位置、使命、产品、子公司&quot; (Fig.6, 7)，在这样的情况下，TaskMatrix.AI 能给出准确的反应; 还有 Fig.3 的绘图任务，Fig.9 的智能家居场景也是如此。

ChatGPT3.5 以后的版本 AI 能够表现出很强的&quot;推理能力&quot;，这一能力本质是将自然语言中的&#39;字&#39;，&#39;语义&#39;，&#39;句子&#39;，&#39;位置&#39;，&#39;段落&#39; 等，经过大量的监督的无监督的&quot;阅读学习&quot;，在映射的高维空间中不断调整优化所形成的不断&quot;进化&quot;的模型，然后根据人们给出的问题或曰提示，&quot;猜出&quot;或称&quot;推断出&quot;后面的意思。通常情况下 AI有亮丽的表现，虽然不免夸夸其谈。但这带来 AI 另一大痛点，它不能对不清楚的问题进行反问。比如在用户提出这样的问题时:&quot;你知道如何从头开始写一篇文章并提供给我一个解决方案大纲？ 我有几篇论文的截止日期。 我只有题目以及每个的一些要点。 最好在其中包含图像。&quot;(Fig.4) TaskMatrix.AI 并没有提问&quot;你的题目是什么?&quot;，而是直接开聊。

AI 日新月异，各种模型为应对使用痛点而生，期待。

老师已先人一步用上ChatGPT4，它有反问或帮助用户捋清问题思路的能力了吗?</div>2023-05-10</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8qNibLrzJyrNv6C3BKRm0ibbibrSrcLxiaWOicQUEcUuk75hG5tdCnAYiapHrHuSdxyXhp1B5ZDKiahHIg/0" width="30px"><span>王永旺</span> 👍（3） 💬（1）<div>Semantic Kernel 老师有了解么，能不能也介绍一下这个项目？
</div>2023-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/ef/3cdfd916.jpg" width="30px"><span>yu</span> 👍（2） 💬（1）<div>剛看完先留言：先讓他判斷用戶的語言，然後翻譯成英文處理。</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ca/58/6fe1854c.jpg" width="30px"><span>金</span> 👍（1） 💬（1）<div>有编辑音频的chatgpt吗？最近ai孙燕姿很火，效果也不错，但是跟本人唱的还是差一些东西，旋律比较平，有办法调教吗？</div>2023-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师：网站想提供几首歌，是否有合适的软件能实现？即用软件唱歌，声音随便，用人声或机器自己产生的声音都可以。不仅仅限于chatGPT；如果chatGPT没有该功能，是否有其他软件能实现？</div>2023-05-10</li><br/><li><img src="" width="30px"><span>极客用户</span> 👍（0） 💬（0）<div>思考题答案：加一层能进行语种翻译的大模型就可以了</div>2024-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/ce/791d0f5e.jpg" width="30px"><span>张开元</span> 👍（0） 💬（0）<div>Visual ChatGPT的计算量和效果怎么样能平衡？</div>2023-09-15</li><br/>
</ul>