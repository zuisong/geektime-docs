你好，我是南柯。

[第18讲](https://time.geekbang.org/column/article/690349)和[第19讲](https://time.geekbang.org/column/article/691354)我们学习了定制化图像生成的常见方法，初步了解了如何训练LoRA，得到代表内容和风格的定制化模型。经过训练LoRA模型的实战，我们发现训练一个LoRA并不困难，但是想实现LensaAI或者妙鸭相机类似的效果却并不容易。

今天这一讲，我们将目光聚焦到人像生成上，继续探讨使用LoRA进行定制化图像生成的技巧。你可不要小看这些技巧，它们正是很多商业产品惊艳效果下的黑魔法。

通过这一讲的实战，我们的LoRA模型效果也会大为改观。最后，我们会训练出一个能高度还原人像效果的LoRA模型，有了这个模型，你就能实现一个梦幻照相馆的项目。课程讲解里的目标形象我们设置为奥黛丽赫本，当然你也可以使用自己的几张照片或者是宠物的照片来制作你的专属照相馆。

## 如何做一个梦幻照相馆

在正式开始实战前，按照惯例，我们需要先准备训练数据，并选好基础模型。

### 模型和数据

和上一个实战项目不同，今天我们要做的梦幻照相馆希望呈现出真人风格，我向你推荐一个名为“墨幽人造人”的模型，你可以点开 [Colab](https://civitai.com/models/86232?modelVersionId=143001) 通过图中的方式获取[下载链接](https://civitai.com/api/download/models/143001)。当然你也可以尝试自己喜欢的其他基础模型。

![](https://static001.geekbang.org/resource/image/1e/49/1ed0de5e9f11650b96c378b2846ab049.png?wh=2549x1313)

在Colab中，我们可以通过后面这两行代码指定模型的保存路径，并下载模型。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/95/71/20b96bc8.jpg" width="30px"><span>王大叶</span> 👍（0） 💬（1）<div>Prompt：masterpiece, best quality, 1girl moyou (ink sketch) fantasy, surreal muted color (Russ Mills Anna Dittmann)Negative Prompt：masterpiece, best quality, 1girl moyou (ink sketch) fantasy, surreal muted color (Russ Mills Anna Dittmann)采样器：Eular a随机种子：1024采样步数：20分辨率：512x768CFG Scale: 7LoRA：hb_pro.safetensors [使用Colab训练]LoRA weight：1.0
---
这里 Negative Prompts 写错了？</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/95/71/20b96bc8.jpg" width="30px"><span>王大叶</span> 👍（0） 💬（1）<div>老师好，触发词 &lt;sks&gt; 带不带尖括号有什么说法吗？会对训练有什么影响？</div>2023-09-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKuaZauv0hcyH9e51azzYTt2rFQPia1ryfupuAVYYeDaicp1ictV7dciarbAXUb2bz2x0qu9x6tL4VVhA/132" width="30px"><span>Geek_7401d2</span> 👍（0） 💬（1）<div>老师，有什么技术能自动选出AI绘制的质量好的图片</div>2023-09-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/lJR3Ba9EuTLRSry9sajEeRcvfwuiaPDr41KicHYGxcsXnRcTxaTp3OHq24AebUR9MS016zSEmqAyws5iaQiaj5TDdQ/132" width="30px"><span>Geek_cbcfc8</span> 👍（0） 💬（1）<div>老师你后面妙鸭相机的例子里用的是ly261666&#47;cv_portrait_model并不是墨幽的模型，这里可以换成下载厚的墨幽文件吗？另外训练人物的相关参数有讲究吗，设置为多少效果比较好，是否需要开启训练text_encoder</div>2023-09-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIxD4lHNc9y1bnVDqpYtSpRZZPoLZxGNX56HjLFtaqps0NtOXxQw5dbYFjAatUQMllibNiaP4rXTBiag/132" width="30px"><span>Geek_077fc1</span> 👍（0） 💬（0）<div>datasets.data_files.EmptyDatasetError: The directory at &#47;mnt&#47;workspace&#47;facechain&#47;worker_data&#47;qw&#47;training_data&#47;ly261666&#47;cv_portrait_model&#47;person2_labeled doesn&#39;t contain any data files
运行官方的notebook出现这个错误怎么解决</div>2024-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/8e/0f/b6067c0b.jpg" width="30px"><span>爱笑</span> 👍（0） 💬（0）<div>google Colab的脚本中系统环境安装的时候会报错，请问怎么解决呢？PyTorch版本和Xformers版本提示不兼容。</div>2024-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/c7/6a/bfb5cc44.jpg" width="30px"><span>S.Sir</span> 👍（0） 💬（0）<div>老师好，我想问一下如果是是想做双人的照相馆，是不是可以针对每个人训练一个单独的lora,然后用controlnet来实现呢？</div>2023-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKuaZauv0hcyH9e51azzYTt2rFQPia1ryfupuAVYYeDaicp1ictV7dciarbAXUb2bz2x0qu9x6tL4VVhA/132" width="30px"><span>Geek_7401d2</span> 👍（0） 💬（1）<div>老师你好，facechain中在训练模型之前的图片处理中的面部旋转的作用是什么呢，感觉面部旋转也是对整体图片进行了旋转，不知道对训练lora模型的影响是什么
原图：https:&#47;&#47;user-images.githubusercontent.com&#47;22190543&#47;271165646-8a26b8fc-eb5f-49d8-be63-2cfdbd0c2d21.png
旋转后：https:&#47;&#47;user-images.githubusercontent.com&#47;22190543&#47;271165752-67c75301-b1d8-4a8e-84b7-5ebb6bd1016d.png</div>2023-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/bd/f3977ebb.jpg" width="30px"><span>John</span> 👍（0） 💬（0）<div>如果一个人的脸与肩宽比例异于常人咋办 或者是杨过独臂呢</div>2023-09-27</li><br/>
</ul>