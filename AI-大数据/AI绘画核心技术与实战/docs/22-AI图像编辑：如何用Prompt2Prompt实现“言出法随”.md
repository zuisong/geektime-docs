你好，我是南柯。

前面，我们已经掌握了以DreamBooth为代表的定制化图像生成技术，也学习了使用ControlNet控制AI绘画的构图。这两种技术都是从整体上控制图像的生成。

今天，我们来探究微调图像的技术，也就是指令级修图——使用prompt实现对图像的局部修改。这一讲的学习我们将围绕 [Prompt2Prompt](https://prompt-to-prompt.github.io/)、[InstructPix2Pix](https://www.timothybrooks.com/instruct-pix2pix) 和 [Null-Text Inversion](https://null-text-inversion.github.io/) 这三项技术展开。这三项技术就像是金庸先生笔下的“射雕三部曲”，有着千丝万缕的联系。

在我看来，头部企业最想拥有的AI绘画能力，无非是媲美Midjourney的AI绘画模型、超越LensaAI的定制化图像生成技术以及指令级修图能力。

学完今天这一讲，你就能对这些最热门的AI绘画技术有一个清楚的认识。而且你掌握了指令级修图的技术之后 ，就算不会用Photoshop也能随心所欲地编辑图像。

## Prompt2Prompt：用Prompt修图

我们熟知的DALL-E 2、Imagen和Stable Diffusion等技术虽然可以实现出惊艳的文生图效果，但是用来做图像编辑却很困难。即使是在prompt上做一点细微的改动，得到的结果也会截然不同。这种情况下，如果我们想要做图像局部编辑，就需要使用图像补全的方式，先手工画一个遮罩（mask）区域，然后使用prompt引导图像生成。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/lJR3Ba9EuTLRSry9sajEeRcvfwuiaPDr41KicHYGxcsXnRcTxaTp3OHq24AebUR9MS016zSEmqAyws5iaQiaj5TDdQ/132" width="30px"><span>Geek_cbcfc8</span> 👍（2） 💬（2）<div>老师 ，目前Null-Text Inversion相关的模型目前有哪些？</div>2023-09-06</li><br/>
</ul>