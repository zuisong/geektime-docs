你好，我是南柯。

在上一讲，我们详细探讨了Stable Diffusion模型的核心技术，包括无分类器引导、UNet模块构成、负向描述词原理等。

事实上，随着AI绘画技术的不断发展，Stable Diffusion模型也在持续进化，比如2023年6月刚刚发布的SDXL模型。参考上一讲的叫法，为了方便，我们还是将Stable Diffusion简称为SD。

在SD模型家族中，有两个具有特殊能力的模型，也就是我们今天要探讨的SD图像变体（Stable Diffusion Reimagine）和“神雕侠侣”（SDXL）。SD图像变体模型用来对标DALL-E 2的图像变体功能，SDXL模型则用来和Midjourney这个最强画师掰掰手腕。

在我看来，生成图像变体和生成通用高美感图片，是当前多数开源垂类模型都做不好的事情。所以这一讲，我们把这SD中的两个特殊模型单独拿出来，用显微镜分析它们的能力和背后的算法原理。理解了这些之后，也会给我们向自己的SD模型引入新能力带来启发。

## SD图像变体

你是否还记得，在关于DALL-E 2的解读中（可以回顾[第13讲](https://time.geekbang.org/column/article/686873)内容），我们提到了一种名为图像变体的图像生成策略。

我带你快速回忆一下这个策略的设计理念。用户输入一张图像，使用CLIP的图像编码器提取图像表征作为图像解码器的输入，这样就实现了生成图像变体的能力。图像变体能力在实际工作中能快速生成相似图像效果，激发我们的设计灵感。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/58/f8/8b9bb574.jpg" width="30px"><span>Wiliam</span> 👍（2） 💬（1）<div>老师，能从原理上解释一下为什么加入Refiner 模型之后，效果能更好呢？</div>2023-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（1） 💬（1）<div>目前最新版本的webui中，这两个特殊模型是否已经集成进去了啊？</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7d/20/abb7bfe3.jpg" width="30px"><span>Geek_55d08a</span> 👍（0） 💬（1）<div>&quot;SDXL 模型没有沿用 SD1.x 和 SD2.x 模型中使用的 VAE 模型，而是基于同样的模型架构，&quot; 这句话是有笔误么？</div>2023-09-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKlicd6xoiaozzsTEH0l2s4epW4zXacqmwAlOrVApGCSIIdReaKwibqxhicqvlEK2vh56sCDvVhEFOlLQ/132" width="30px"><span>Seeyo</span> 👍（0） 💬（1）<div>老师请问一下，关于batch处理的问题。

测试阶段：

1、我目前的理解是不能用batch进行不同text prompt对应图片的处理，是因scheduler的处理方式是自回归吗？

2、当使用相同的promot时，因为webui支持批量生成，为什么此时可以使用batch的生成方式？虽然text产生的embedding相同，但每个推理时刻，产生的x_t-1是不一样的。

训练阶段：

要使用ddpm采样器，为什么能使用batch训练呢？


以上是目前的个人理解，期待老师的回答指正</div>2023-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1:模型的数学推导主要用哪些方面的知识？微积分吗？
Q2：图像变体每次运行的结果都是不同的吗？</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/f6/d6c1a0c2.jpg" width="30px"><span>海杰</span> 👍（0） 💬（1）<div>老师，既然提到SDXL, 会讲下ComfyUI 的使用吗？</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/79/f098c11d.jpg" width="30px"><span>YX</span> 👍（0） 💬（0）<div>SDXL 更进一步，使用了两个文本编码器，分别是 OpenCLIP 的 ViT-G&#47;14 模型（参数量 694M）和 OpenAI 的 ViT-L&#47;14 模型。在实际使用中，分别提取这两个文本编码器倒数第二层的特征，将 1280 维特征（Vit-G&#47;14）和 768 维特征（ViT-L&#47;14）进行拼接，得到 2048 维度的文本表征。
------
老师请问下，这句话是不是意味着对于SDXL模型，clip skip可以不需要再设置了呢</div>2024-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/0d/06/970cc957.jpg" width="30px"><span>Charles</span> 👍（0） 💬（1）<div>老师，怎么实现将中文嵌入图片中呢？这些都是只支持英文的，对中文不友好。
比如：生日卡片，有气球和生日蛋糕，卡片上写着“XX生日快乐”</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/58/f8/8b9bb574.jpg" width="30px"><span>Wiliam</span> 👍（0） 💬（0）<div>老师，能从原理上解释一下，为什么引入了Refiner 模型，效果能更好呢？</div>2023-09-29</li><br/>
</ul>