你好，我是南柯。

我们知道Stable Diffusion可以用文本引导图像生成。除了使用prompt这种比较原始的方式，还有没有控制能力更强的方法呢？

其实早在第2讲，我就留过一个思考题，AI 绘画生成的图像在手部和脸部细节存在瑕疵有哪些解决方式。而我们今天要讲的技术—— [ControlNet](https://github.com/lllyasviel/ControlNet) 就可以解决这个问题，对图像结构做出一定的限制，比如手部的关键点信息、五官信息等。

2023年2月，ControlNet这个方法一经提出，便凭借其对于AI绘画效果的控制能力火遍全网。最初的ControlNet主要用于线稿上色、图像风格化、可控姿态的人体生成等任务。如今各路网友脑洞大开，使用ControlNet做出了创意二维码、将文字自然地融入照片等趣味效果。

这一讲，我们一起来探讨ControlNet背后的技术原理和各种应用场景。掌握了ControlNet这个“大杀器”，你对于AI绘画效果的控制能力会上一个台阶，在下个实战篇实现创意AI绘画任务时也会更加得心应手。

## 初识ControlNet

如果说prompt是对于AI绘画模型指令级的控制，ControlNet无疑是构图级的控制。为了让你对它建立感性认识，我们先结合一些图片例子，感受一下ControlNet的构图控制能力。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLCw3A7VvAGA7XyRKsdTAfg7K2olLibzOJaiasD1119SiacIqsHXNRBrq9N4WvVWw1ybpydtIdVLxNQRQ/132" width="30px"><span>Geek_fbb96d</span> 👍（0） 💬（1）<div>老师你好，我在 Stable Diffusion 的界面上没有找到 ControlNet 的位置？请问在哪里？</div>2024-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/8c/f029535a.jpg" width="30px"><span>hallo128</span> 👍（0） 💬（1）<div>ControlNet官方GitHub：https:&#47;&#47;github.com&#47;lllyasviel&#47;ControlNet
ControlNet论文原文：https:&#47;&#47;arxiv.org&#47;abs&#47;2302.05543</div>2024-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：ControlNet可以独立使用吗?
Q2：ControlNet只能配合SD使用吗？还是可以和其他模型配合?</div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/8c/f029535a.jpg" width="30px"><span>hallo128</span> 👍（0） 💬（0）<div>老师，想请问下，如何训练自己的ControlNet插件呢？如果要更精细化的控制一些不一样的场景，而不是直接调用已训练好的ControlNet插件</div>2024-04-25</li><br/>
</ul>