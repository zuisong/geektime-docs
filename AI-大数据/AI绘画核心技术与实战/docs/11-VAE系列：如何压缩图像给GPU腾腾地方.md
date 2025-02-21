你好，我是南柯。

在前几讲中，我们已经学习了Transformer、UNet、Clip三个关键模块。在Stable Diffusion的知识地图上，还差最后的一环，便是今天的主角VAE模块。

在Stable Diffusion中，所有的去噪和加噪过程并不是在图像空间直接进行的。VAE模块的作用便是将图像“压缩”到一个特殊的空间，这个空间的“分辨率”要低于图像空间，便于快速地完成加噪和去噪的任务。之后，还能便捷地将特殊空间“解压”到图像空间。

这一讲，我们将一起了解VAE的基本原理。学完VAE，我们便了解了Stable Diffusion模型的全部核心模块。之后我们训练自己的Stable Diffusion模型时，也会用上VAE这个模块。

## 初识VAE

VAE的全称是变分自动编码器（Variational Autoencoder），在2013年被提出，是自动编码器（AE，Autoencoder）的一种扩展。你可能听过很多不同的名词，比如AE、VAE、DAE、MAE、VQVAE等。其实这些带 “AE” 的名字，你都可以理解成是一个编码器和一个解码器。

提到编码器和解码器，你也许会联想到我们在[第7讲](https://time.geekbang.org/column/article/682762)中学过的Transformer结构。这里我需要提醒你注意，尽管术语一样，但是VAE和Transformer中的编码器、解码器解决的是不同类型的问题，并具有不同的结构和原理。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/7d/d0/48c13a76.jpg" width="30px"><span>xingliang</span> 👍（4） 💬（1）<div>结构：VAE通常是简单的全连接网络或卷积神经网络；Transformer基于多头注意力机制，结构更复杂。
原理：VAE关注于在潜在空间中建立数据的概率分布；Transformer通过自注意力机制捕获长距离的依赖关系。
功能：VAE主要是为了生成数据和降维；而Transformer则是为了处理序列到序列的任务，捕获序列中的依赖关系。</div>2023-08-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLhs7ykGEy46a8ljg3LPvXTRxpgMLEhvZoAYIQL6I46OEqbNV4U1mXryhJt1bE3mhf7ey6jfl3IyQ/132" width="30px"><span>cmsgoogle</span> 👍（1） 💬（1）<div>遇到问题：
1. 重建和差值部分的代码，在colab上第一次运行正常，但是到了第二次就OOM了，是代码没有处理释放显存空间吗？
2. 文本的例子，体感很不好，只给了一段训练代码，建议加上实例，包括训练+推理。</div>2023-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：VAE可以用来处理音频数据吗？
Q2：VAE可以用来处理电磁频谱数据吗？
用电磁检测设备采集无线电信号，然后用VAE来处理。
Q3：源码在哪里？</div>2023-08-10</li><br/>
</ul>