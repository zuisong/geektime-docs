你好，我是南柯。

前面我们已经学习了扩散模型加噪和去噪的过程，也了解了Transformer的基本原理。之前我还埋下了一个伏笔，那便是使用UNet网络预测每一步的噪声。

今天我就来为你解读UNet的核心知识。在这一讲，我们主要解决后面这三个问题。

- UNet模型的工作原理是怎样的？
- 在各种AI绘画模型里用到的UNet结构有什么特殊之处？
- UNet与Transformer要如何结合？

搞懂了这些，在你的日常工作中，便可以根据实际需求对预测噪声的模型做各种魔改了，也会为我们之后训练扩散模型的实战课打好基础。

## 初识UNet

在正式认识UNet之前，我们有必要先了解一下图像分割这个任务。

图像分割是计算机视觉领域的一种基本任务，它的目标是将图像划分为多个区域，对应于原图中不同的语义内容。比如下面这个例子，就是针对自动驾驶场景的图像分割效果。

![](https://static001.geekbang.org/resource/image/e9/33/e9da2b60ea977b8ceda96e5c008ccb33.jpg?wh=4137x2096 "图片来源：https://www.cityscapes-dataset.com/")

图像分割与我们熟悉的图像分类任务目标有所不同，图像分类任务的目标是为整张图像分配一个整体标签，而图像分割任务的目标是为每个像素分配对应的类别标签。

UNet出现之前，图像分割采用的主要方法是2015年提出的 [FCN](https://arxiv.org/pdf/1411.4038.pdf)（全卷积网络）。与传统的CNN（卷积神经网络）不同，FCN去掉了最后的全连接层，而是使用转置卷积层实现上采样的过程。通过这样的操作，FCN可以获得与输入图像相同尺寸的输出。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/e1/30/56151c95.jpg" width="30px"><span>徐大雷</span> 👍（3） 💬（0）<div>想请问一下老师，你这边的头像使用的啥模型生成的呀，还有对应的提示词是啥呀，谢谢</div>2023-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/f6/d6c1a0c2.jpg" width="30px"><span>海杰</span> 👍（0） 💬（1）<div>会讲下CLIP 模型吗？看网上不少范例的参数都有说用CLIP skip step 2,想知道原理。谢谢。</div>2023-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/6e/efb76357.jpg" width="30px"><span>一只豆</span> 👍（0） 💬（1）<div>这也太绝妙了吧！“在 Stable Diffusion 中，我们将 Z_{T} 视为目标序列，得到 Q；将 prompt 描述经过 CLIP 模型得到的特征向量作为源序列，得到 K 和 V。” 语义信息就这样把注意力跨模态的映射到图片信息了……</div>2023-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/c3/3385cd46.jpg" width="30px"><span>Ericpoon</span> 👍（0） 💬（1）<div>为什么说unet，或AI画画的模型学习，要用decoder输出喿声？</div>2023-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师两个问题：
Q1：跳跃连接，是两个对等层的数据会有关系吗？比如，右边的层会使用左边的层的数据作为输入。
Q2：有能唱歌的AI吗？</div>2023-08-02</li><br/>
</ul>