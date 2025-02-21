你好，我是南柯。

上一讲我们已经学习了LoRA的算法原理，搞懂了引入LoRA技术减少可学习参数的技巧。

如今LoRA几乎家喻户晓，我们在Civitai或者Hugging Face上，也能找到各种各样的LoRA模型。这些LoRA模型既可以代表人物形象、动物形象或者某个特定物体，也可以代表水彩风、油画风这种特定的风格。

这一讲我们不妨自己动手，从零开始训练自己的LoRA模型。我们会以宝可梦生成和彩铅风格生成为例，完成两个模型的训练，借此探索LoRA模型表达内容和表达风格的能力如何实现。

## 如何训练一个LoRA

在我们动手训练LoRA前，我先为你预告一下整个流程。

对于LoRA的训练，我们首先需要考虑两个问题：数据集获取和基础模型选择。幸运的是，我们已经熟悉了 [Hugging Face](https://huggingface.co/models) 和 [Civitai](https://civitai.com/) 这两个强大的开源社区，可以免费获取到海量数据集和基础模型。

### 数据准备

我们可以使用 [Hugging Face](https://huggingface.co/datasets/lambdalabs/pokemon-blip-captions) 上现有的数据集，完成宝可梦的生成任务。这个数据集中包含800多张训练图片。从后面的数据集说明中你可以看到，每一张图，我们都可以获取到它对应的prompt。

![](https://static001.geekbang.org/resource/image/85/f3/857851382cf9e59969c4dd85a8ab55f3.png?wh=1568x774)

首先，我们可以通过后面这两行代码下载并加载数据集。

```python
from datasets import load_dataset

dataset = load_dataset("lambdalabs/pokemon-blip-captions", split="train")
```
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKuaZauv0hcyH9e51azzYTt2rFQPia1ryfupuAVYYeDaicp1ictV7dciarbAXUb2bz2x0qu9x6tL4VVhA/132" width="30px"><span>Geek_7401d2</span> 👍（5） 💬（1）<div>老师你好，看完后还是不知道如何入手训练，有几个问题
1、选择素材图片时要用多少张，什么样的图片合适，比方说训练某个人物的Lora时，选择该人的图片时要选择什么样的，全身照、半身照、面部特写等各占多少合适
2、Lora 模型训练多少轮（num_epochs）合适
3、训练完会有多个Lora模型，选择哪一个呢，选最后一轮训练的吗
4、我理解训练lora模型的原理是一样的，为什么同样的素材、用同样的基础模型，用不同的代码会出现不同的训练效果，文中用到的这两个代码库差异在哪呢</div>2023-08-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLhs7ykGEy46a8ljg3LPvXTRxpgMLEhvZoAYIQL6I46OEqbNV4U1mXryhJt1bE3mhf7ey6jfl3IyQ/132" width="30px"><span>cmsgoogle</span> 👍（1） 💬（1）<div>使用diffusers库训练Lora，文中提到：耐心等待 20 分钟，我们就完成了 LoRA 模型的训练。
需要说明下是什么环境，如果再colab上使用T4服务器，大约要1个小时10多分钟。</div>2023-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/95/71/20b96bc8.jpg" width="30px"><span>王大叶</span> 👍（1） 💬（1）<div>老师好，请教两个问题：
1. 对于人像 LoRA 的训练，精细化的打标是否有必要，对 LoRA 质量的影响会很大吗？
2. 实验发现用 deepbooru 给写实人像打标不是很准确，比如经常会把男性图片标注成 1girl，用 BLIP 打标信息又比较少，无法完全涵盖画面的内容。请教人像 LoRA 训练有什么推荐的打标方法吗？</div>2023-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c2/5c/791d0f5e.jpg" width="30px"><span>易企秀-郭彦超</span> 👍（1） 💬（2）<div>Y=（W+weight1​∗A1​⋅B1​+weight2​∗A2​⋅B2​）⋅X
老师你好，按照上面公式权重融合的过程是加权融合，W的值在相同维度上会同时受到A和B的影响，最终导致结果既不像A也不像B, 有没有一种累计方式 避免A和B的互相影响？ 比如多lora融合前先merge， 根据CNN的思想， 取d&#47;2的A模型参数量 与d&#47;2的B模型参数量 合并成新的d*d lora模型，新的模型保留了原始的A 和 B的部分参数 并没有累加A和B
</div>2023-08-31</li><br/><li><img src="" width="30px"><span>Geek_ca0b19</span> 👍（0） 💬（1）<div>老师好我有一个问题
如果采用五六张类似风格画风的图，可以通过这几张图训练出一个代表类似风格的lora吗？</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/4e/1e/137ad3cf.jpg" width="30px"><span>石沉溪洞</span> 👍（0） 💬（1）<div>老师您好，请问这个能支持将基本模型改为SDXL吗？谢谢您</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6a/f2/8829a0b8.jpg" width="30px"><span>@二十一大叔</span> 👍（0） 💬（1）<div>老师，lora训练可以写一个本地运行的python版本吗，colab上看的不是很明白</div>2023-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/38/b6/234a17a7.jpg" width="30px"><span>陈问渔</span> 👍（0） 💬（2）<div>请问 make_captions.py 的代码在哪看呀？</div>2023-09-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8qibAw4lRCic1pbnA6yzQU3UqtQm3NqV1bUJ5EiaUnJ24V1yf4rtY7n2Wx7ZVvTemqq5a61ERWrrHA/132" width="30px"><span>Alex</span> 👍（0） 💬（1）<div>最新的sd 的bweui 的additional networks 是已经集成了么？我不太确定 我安装了一下 没有显示这个选项  请老师指教下 </div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>是否有安卓手机上可以使用绘画AI?</div>2023-08-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI64XUGp3cKv99kb0dB3TQgod7yeCDEKe94QVP5rSv4yzR24CcE6UqD6wxjMo2z9CRn06S7fvrqMQ/132" width="30px"><span>zec123</span> 👍（0） 💬（2）<div>老师，24年1月11日运行colab彩铅代码，在def train代码块会发成报错导致运行不了报错如下：RuntimeError: 
        CUDA Setup failed despite GPU being available. Please run the following command to get more 
information:

        python -m bitsandbytes

        Inspect the output of the command and see if you can locate CUDA libraries. You might need 
to add them
        to your LD_LIBRARY_PATH. If you suspect a bug, please take the information from python -m 
bitsandbytes
        and open an issue at: https:&#47;&#47;github.com&#47;TimDettmers&#47;bitsandbytes&#47;issues
CalledProcessError: Command &#39;[&#39;&#47;usr&#47;bin&#47;python3&#39;, &#39;train_network.py&#39;, 
&#39;--sample_prompts=&#47;content&#47;LoRA&#47;config&#47;sample_prompt.txt&#39;, 
&#39;--dataset_config=&#47;content&#47;LoRA&#47;config&#47;dataset_config.toml&#39;, 
&#39;--config_file=&#47;content&#47;LoRA&#47;config&#47;config_file.toml&#39;]&#39; returned non-zero exit status 1.</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/64/7403c694.jpg" width="30px"><span>ALAN</span> 👍（0） 💬（0）<div>还有这块代码在哪个文件里，好像也没找到。
 for epoch in range(num_train_epochs):
     for step, batch in enumerate(train_dataloader):
     
         # VAE模块将图像编码到潜在空间
         latents = vae.encode(batch[&quot;pixel_values&quot;].to(weight_dtype)).latent_dist.sample()
         
         # 随机噪声 &amp; 加噪到第t步
         noise = torch.randn_like(latents)
         timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps)
         noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)
         
         # 使用CLIP将文本描述作为输入
         encoder_hidden_states = text_encoder(batch[&quot;input_ids&quot;])[0]
         target = noise
         
         # 预测噪声并计算loss
         model_pred = unet(noisy_latents, timesteps, encoder_hidden_states).sample
         loss = F.mse_loss(model_pred.float(), target.float(), reduction=&quot;mean&quot;)
         optimizer.step()</div>2023-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/91/51/3da9420d.jpg" width="30px"><span>糖糖丸</span> 👍（0） 💬（0）<div>文章里的make_captions.py文件，在哪里可以看？</div>2023-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（0） 💬（2）<div>在LoRA 模型训练时，采用变化的学习率(learning rate)，从较大的学习率开始，逐渐将其减小到较小值，帮助优化器(optimizer)能够较快较好地达到全局或局部最优，以期训练出的模型有更高的质量。

为了比较，采用同样的基础模型，训练集，优化器，但将学习率调度器(Learning Rate Scheduler)改成了Cosine，lr_scheduler = &quot;cosine_with_restarts&quot;，出图质量有明显改进。

还有其它优化模型的方法，大家可以分享。</div>2023-08-30</li><br/>
</ul>