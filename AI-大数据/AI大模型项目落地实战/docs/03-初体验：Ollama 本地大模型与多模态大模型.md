你好，我是金伟。

前面两节课我们分别聊到大模型的基础架构Transformer，以及ChatGPT是如何在Transformer基础上做的工程创新，最终做到了智能涌现。

需要说明的是，我自身也是一个应用开发人员，对于这些基础原理的需求就是了解即可，我会把更多的精力用在实战开发上。喜欢动手的工程师可能都会想自己训练一次大模型，本节课正是为此准备的。

Ollama是一个全新的本地可运行的大模型框架，适合零基础的同学体验多种大模型，你可以把它看做一个可以本地运行的 “ChatGPT”。

这节课我们还会用到GPT-SoVITS。这是一个TTS（Text-to-Speech，文本转语音）‌大模型，也可以在本地运行。你可能也都听说过多模态这个词，GPT-SoVITS就是一个语音类的多模态模型。

咱们这节课的任务，就是结合Ollama的文本能力和GPT-SoVITS的语音能力，开发一个可以本地运行的实时语音聊天助手，实现一个类似ChatGPT的语音助手。

## Ollama 本地大模型

传统的大模型开发需要大量的GPU资源，以参数量最小的Llama 2 7B为例，也需要14G显存，而且每一种大模型都有自己的开发接口，这导致普通人很难在自己的本地环境构建大模型、体验大模型。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkwbyTYtSCx6Qc7cQPnnRWv38Jybh3etziaPmuP8gHcgS6FMxcdftrKgWiamH6fc2iciaicDKDVEwcEibQ/132" width="30px"><span>sami</span> 👍（5） 💬（1）<div>
这个过程与许多图像生成模型（如扩散模型）的工作方式有关。这些模型通常从随机噪声开始，然后通过多步迭代来逐渐&quot;去噪&quot;，形成有意义的图像。先生成低分辨率图像再提高清晰度的方法，可以看作是这个去噪过程的可视化表现。
这种渐进式生成方法与深度学习中的&quot;分层表示&quot;（多头注意力）概念相关。较低的层次捕获基本形状和结构，而较高的层次则负责细节和纹理。通过从低分辨率到高分辨率的过程，模型可以更好地控制图像的整体结构和细节。
文本输入被用来指导整个图像生成过程。在初始阶段，模型从文本中提取关键概念和大致布局，这反映在低分辨率草图中。随后，模型进一步解析文本中的细节信息，用于指导高分辨率细节的生成。
</div>2024-08-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKsz8j0bAayjSne9iakvjzUmvUdxWEbsM9iasQ74spGFayIgbSE232sH2LOWmaKtx1WqAFDiaYgVPwIQ/132" width="30px"><span>2xshu</span> 👍（2） 💬（4）<div>老师可以提供源代码吗？感谢感谢呐</div>2024-08-12</li><br/><li><img src="" width="30px"><span>8000tank</span> 👍（0） 💬（1）<div>“微调 GPT-SoVITS 训练自己的 TTS 模型。这里你可以自由发挥，直接在界面上操作”，这个“微调”具体都做了什么操作、干了什么事情，老师能稍微解释说明一下么？</div>2024-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/60/20c6a3f2.jpg" width="30px"><span>expecting</span> 👍（0） 💬（1）<div>老师，使用云计算训练完TTS语音大模型后是把大模型下载到本地运行吗？</div>2024-08-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIofiaCAziajdQnbvrfpEkpCKVFgO62y6zicamhjF1BAWZSRcCVaTBXLIerLsGeZCic7XS7KOEkTN4fRg/132" width="30px"><span>zahi</span> 👍（0） 💬（1）<div>1750 亿个参数 是否是第一节中Ci x Di？</div>2024-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（1）<div>先确认结构和布局，在通过一层层的输入输出能更好的生成跟文字内容相关的图片。就像画画，也是先画框架再画细节。训练大模型也是类似的吧，模型会先学习简单的框架，在学习填充的细节，这样才能学会推理？不知道理解对不对。</div>2024-08-14</li><br/>
</ul>