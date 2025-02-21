你好，我是南柯。

学完前两章内容，我们已经掌握了AI绘画的基本原理，也熟悉了AI绘画的经典解决方案。从这一讲开始，我们正式进入课程的综合演练篇，一起探讨图像定制化生成与编辑的经典算法方案。

使用Stable Diffusion模型的时候，基于prompt生成图像已经是我们比较熟悉的模式，比如一个人在某个地方做某件事。这种方式生成的图像类似开盲盒，因为我们在看到效果之前，并不确定图中生成的物体和风格是什么样的。

而接下来我们要学习的定制化图像生成技术就不同了，它的目标是控制指定的一个人在某个地方做某件事，或者控制生成的图片是某只动物，再或者生成的图像是某个确定的风格。

可不要小看了这个定制化的思想，海外非常流行的LensaAI和国内风靡一时的“妙鸭相机”，它们都是定制化图像生成的具体产品方案。今天这一讲，我们要学习三种经典的定制化算法方案，分别是Textual Inversion、DreamBooth和LoRA。

## Textual Inversion

为了帮你更好地理解Textual Inversion这个算法，我先带你回顾下SD词嵌入向量的使用方式。

在SD AI绘画过程中，我们输入的prompt首先会经过tokenizer完成分词，得到每个分词的token\_id。之后在预训练的词嵌入库中根据token\_id拿到词嵌入向量，并将这些词嵌入向量拼接在一起，输入到CLIP的文本编码器。接着，经过CLIP文本编码器提取到的文本表征，便可以通过交叉注意力机制控制图像生成。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/c2/5c/791d0f5e.jpg" width="30px"><span>易企秀-郭彦超</span> 👍（5） 💬（3）<div>老师，关于Textual Inversion您有没有这方面的研究：
目前S需要输入几张图像进行训练才能获取对应的特征，去替换对应位置的clip embedding输入，那有没有一种不需要训练的方案， 比如我给一张或多张图，通过一个模型去提取对应的特征，然后将这些特征替换输入的文本token embedding，进而实现类似的效果，大大降低了使用成本，交互上也更便捷了</div>2023-08-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKlicd6xoiaozzsTEH0l2s4epW4zXacqmwAlOrVApGCSIIdReaKwibqxhicqvlEK2vh56sCDvVhEFOlLQ/132" width="30px"><span>Seeyo</span> 👍（3） 💬（2）<div>老师，请教两个问题


1、关于dreambooth和lora，除了计算能耗外，dreambooth的效果是否基本优于lora？

2、人物定制方面，我想定制多个人物，比如甲乙丙丁，在我实验dreambooth时，我先训练了甲，然后拿甲得到的模型去训练乙之后，发现模型的画质和画风大幅下降。请问多人物训练该如何通过dreambooth制定？ 

如果走lora路线，比如制作十个lora，让模型一同加载，是否会影响人物人脸的一致性？（这部分我还未开始实验）

想听听老师对于多人物定制的建议，因为线上部署时，希望模型初始化只发生在服务启动环节，后续不做模型的切换。</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（1） 💬（1）<div>当训练某个LoRA1 时，基础模型W1 的参数保持不变。如果W1的维度是d1xd1, 训练LoRA1时调整两个矩阵 A1 和矩阵 B1 的权重，最后A1xB1的维度也将是d1xd1，因此输出的结果就可以表示为W1+ A1xB1。

问题1: 在使用LoRA1 时，基础模型只能选W1? 
问题2: 使用LoRA1 时，如果选择了另一个基础模型W2，其具有d2xd2的维度，输出W2+ A1xB1是否会严重偏离预期? 如何评估这样的结果?</div>2023-08-29</li><br/>
</ul>