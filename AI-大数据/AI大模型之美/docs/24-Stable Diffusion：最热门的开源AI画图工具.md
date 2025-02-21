你好，我是徐文浩。

[上一讲](https://time.geekbang.org/column/article/653489)，我们一起体验了CLIP这个多模态的模型。在这个模型里，我们已经能够把一段文本和对应的图片关联起来了。看到文本和图片的关联，想必你也能联想到过去半年非常火热的“文生图”（Text-To-Image）的应用浪潮了。相比于在大语言模型里OpenAI的一枝独秀。文生图领域就属于百花齐放了，OpenAI陆续发表了DALL-E和 [DALL-E 2](https://labs.openai.com/)，Google也不甘示弱地发表了 [Imagen](https://imagen.research.google/)，而市场上实际被用得最多、反馈最好的用户端产品是 [Midjourney](https://midjourney.com/home/)。

不过，在整个技术社区里，最流行的产品则是Stable Diffusion。因为它是一个完全开源的产品，我们不仅可以调用Stable Diffusion内置的模型来生成图片，还能够下载社区里其他人训练好的模型来生成图片。我们不仅可以通过文本来生成图片，还能通过图片来生成图片，通过文本来编辑图片。

那么今天这一讲，我们就来看看如何使用Stable Diffusion，做到上面这些事情。

## 使用Stable Diffusion生成图片

### 文生图

可能你还没怎么体验过文生图的应用，那我们先用几行最简单的代码体验一下。在这一讲里，我建议一定要用Colab或者其他的GPU环境，因为用CPU来执行的话，速度会慢到让人无法接受。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（9） 💬（3）<div>老师，为什么要加了噪声，再去除噪声？</div>2023-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（5）<div>请教老师几个问题：
Q1：stable Diffusion采用的CLIP是自身的吗？还是调用chatGPT？
Q2：先加噪声，再去掉，有什么意义？吃一口再吐一口，有意思吗？
“先往前面的用 CLIP 模型推理出来的向量里添加很多噪声，再通过 UNet+Scheduler 逐渐去除噪声，最后拿到了一个新的张量”。
Q3：本课的代码是在本机上运行的吗？我的笔记本上是普通配置，能运行并生成图吗？（或者，图的生成是调用了某个服务器？）
Q4：可以对图片进行加工吗？ 比如在一个照片的头上加一个帽子。</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（2）<div>老师 如何 手动把模型下载,然后再上传到服务器 ? 我服务器本地liunx的,发现下载很慢..... DiffusionPipeline.from_pretrained</div>2023-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/92/69c2c135.jpg" width="30px"><span>厚积薄发</span> 👍（0） 💬（2）<div>CUDA out of memory. Tried to allocate 20.00 MiB (GPU 0; 14.75 GiB total capacity; 13.46 GiB 
already allocated; 10.81 MiB free; 13.46 GiB reserved in total by PyTorch) If reserved memory is &gt;&gt; allocated 
memory try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and 
PYTORCH_CUDA_ALLOC_CONF   老师，colab gpu不够了，默认的16g不够，是不是需要购买更大的gpu</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/f2/db90fa96.jpg" width="30px"><span>Oli张帆</span> 👍（0） 💬（2）<div>请教一下老师，结合您之前讲的HuggingFace，我可以通过HuggingFace，免费调用Stable Diffusion的接口，来产生大量的图片。那这整个流程中需要的大量算力，是谁来买单的呢？</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（0） 💬（10）<div>1. 使用 GPU 无疑会加快图像的生成，但实在没有办法使用 GPU 时，就用 CPU，只要将下面代码中的 &quot;cuda&quot; 改成 &quot;cpu&quot; 即可，慢比没有强。

pipeline.to(&quot;cuda&quot;) =&gt; pipeline.to(&quot;cpu&quot;) 
---------------------
from diffusers import DiffusionPipeline
pipeline = DiffusionPipeline.from_pretrained(&quot;runwayml&#47;stable-diffusion-v1-5&quot;)
pipeline.to(&quot;cpu&quot;)

image = pipeline(&quot;Sports car, road, rural areas, blue sky, white clouds, endless grassland in the background&quot;).images[0]
image

--------------
生成上面的图在 cpu 条件下约10分钟。

2. 描述图像的 prompt 如果太长会报错， 比如
Token indices sequence length is longer than the specified maximum sequence length for this model (161 &gt; 77). 

程序会继续运行，但输出结果是黑板。
Potential NSFW content was detected in one or more images. A black image will be returned instead. Try again with a different prompt and&#47;or seed.

prompt 中的 Token 数超过限定时，要停止运行，以节省时间。</div>2023-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/d8/b109ed85.jpg" width="30px"><span>Jack</span> 👍（0） 💬（2）<div>第一次运行“a photograph of an astronaut riding a horse”，只有马，没有宇航员，多运行几次就有了，不过图片没有老师的好看</div>2023-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/ad/6ee2b7cb.jpg" width="30px"><span>Jacob.C</span> 👍（0） 💬（3）<div>老师可以讲一下，colab 上，跑这个太空人骑马要运行耗时多久吗？</div>2023-05-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/270T9KAFd4oCxXXB1giaMDaJuTQVib8gPt77VkM5dbS3hW60kwTNnxMYpVibwWVdnASCrymBbwT7HI77URia0KUylw/132" width="30px"><span>Geek_7ee455</span> 👍（0） 💬（4）<div>老师,在mac上能自己部署一套stable diffusion吗</div>2023-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/c4/40609b81.jpg" width="30px"><span>莹</span> 👍（2） 💬（0）<div>直接新建一个colab notebook后默认不是用的GPU，运行代码出错了&quot;RuntimeError: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http:&#47;&#47;www.nvidia.com&#47;Download&#47;index.aspx&quot;

遇到同样错误的小伙伴记得在Runtime菜单里选择Change runtime type，选择GPU, T4。我遇到了在运行也不成功的情况，这时可以再在Runtime菜单里选择Restart runtime或者Restart and run all。这样，我遇到的错误就解决了。</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（0）<div>李沐的课程太好了</div>2023-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（0） 💬（0）<div>为啥有的图片跟文字不符，文字描述有啥要求吗</div>2024-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（0） 💬（2）<div>大家没遇到huggingface完全访问不了的情况吗？</div>2023-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/13/082013bc.jpg" width="30px"><span>昵称C</span> 👍（0） 💬（0）<div>思考题有做出来的吗？老师有答案吗？
</div>2023-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/5b/d7/d88c1850.jpg" width="30px"><span>和某欢</span> 👍（0） 💬（0）<div>老师，colab如何引入Counterfeit-V3.0 这个模型呢？示例代码没看懂，运行的时候报 NameError: name &#39;pipeline&#39; is not defined.</div>2023-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/80/a0533acb.jpg" width="30px"><span>勇.Max</span> 👍（0） 💬（0）<div>请问下老师colab的在线GPU环境是不是跟本地的macos(m1)也有一定关系？不太理解为啥m1跑colab为啥还要修改成cpu的方式</div>2023-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/80/a0533acb.jpg" width="30px"><span>勇.Max</span> 👍（0） 💬（0）<div>我用老师推荐的示例代码(https:&#47;&#47;huggingface.co&#47;docs&#47;diffusers&#47;optimization&#47;mps)在colab上还是跑不起来，apple m1芯片。RuntimeError: PyTorch is not linked with support for mps devices，在chatgpt搜解决方案推荐!pip install --upgrade torch torchvision，执行完之后依然不行。 这个还有什么解决方案吗？colab如果不花钱也是用的本地资源？那在colab运行代码和在本地jupyter-lab上运行有何区别呢？</div>2023-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/82/5b/df97e03c.jpg" width="30px"><span>Santiago</span> 👍（0） 💬（0）<div>学习打卡
</div>2023-05-05</li><br/>
</ul>