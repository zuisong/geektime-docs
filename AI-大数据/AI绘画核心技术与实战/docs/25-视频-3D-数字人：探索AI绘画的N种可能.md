你好，我是南柯。

在之前的课程中，我们已经探讨了AI绘画的各种常见技巧，包括文生图、图生图、定制化图像生成、ControlNet构图控制、图像编辑等。

其实这些图像相关的技能仅仅是AI绘画的基本能力。今天这一讲我会带你了解三个更高阶的AI绘画能力，分别是文生视频技术、通用3D生成技术和数字人技术。见识了这些更高级的技术，你对于AI绘画的无限潜能一定会有更清晰的认识。在之后的求职择业中，你也可以选择一个感兴趣的切入点，持续地深入下去。

## 视频类技能

对我们来说，无论是使用SD模型或者Midjourney，生成一张2D图像似乎并不费劲。很自然地我们会想：对于输入的prompt，如果生成一系列连续的2D图像以后，再将它们连在一起，能否得到精致的视频呢？这其实就是AI绘画的视频类技能。

### 体验文生视频

使用prompt来生成视频的技术，我们一般称之为文生视频（Text-to-Video）。事实上，这并不是一件容易的事情。文生视频需要满足两个约束条件。第一，生成的视频整体需要符合prompt指定的内容。第二，需要确保AI绘画模型生成的每一帧图像都连贯一致，这样最终生成的视频看起来才不会违和。

你可以点开 [Colab链接](https://colab.research.google.com/github/NightWalker888/ai_painting_journey/blob/main/lesson25/Text_to_Video_Demo.ipynb)，和我一起体验下文生视频的算法效果。首先，我们使用 [Hugging Face](https://huggingface.co/cerspense/zeroscope_v2_576w) 中能够实现文生视频的模型。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>本课所讲的这几种应用，有具体产品吗？</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/85/06/ded595d2.jpg" width="30px"><span>李小刀</span> 👍（0） 💬（0）<div>在短视频平台上一些视频风格化的效果，是如何实现的？有什么相关资料吗？</div>2023-10-25</li><br/>
</ul>