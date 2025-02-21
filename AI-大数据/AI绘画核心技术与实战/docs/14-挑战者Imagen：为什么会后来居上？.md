你好，我是南柯。

上一讲我们一起探索了OpenAI推出的DALL-E 2背后的技术原理。仅仅过去一个月，在2022年5月，**Google便发布了自己的AI绘画模型Imagen。Imagen在效果上显著优于DALL-E 2**，并且通过实验证明，只要文本模型足够大，就不再需要扩散先验模型。

一年之后，2023年的4月28日，后来者StabilityAI，也就是搞出来Stable Diffusion这个模型的公司，发布了DeepFloyd模型。这个模型完美地解决了DALL-E 2不能在生成图像中指定文字内容的问题，是当下公认的效果最好的AI绘画模型之一。并且，**DeepFloyd模型的技术方案，恰恰就是我们今天要讲的主角Imagen**。

今天这一讲我们来探讨Imagen背后的技术，主要搞清楚以下几个问题。

第一，相比DALL-E 2，Imagen在能力上有哪些优势？

第二，Imagen的工作原理是怎样的？

第三，DeepFloyd又在Imagen的基础上做了哪些改进？

明白了这些，你会对AI绘画技术的发展趋势理解更深刻，在选择AI绘画模型时也会更加得心应手。让我们开始吧！

## 初识Imagen

我们先来看看Imagen模型在AI绘画这个任务上的表现，建立一个直观感受。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（1） 💬（3）<div>在Colab A100 下跑 DeepFloyd IF 的代码会出现下列报错:

ModuleNotFoundError                       Traceback (most recent call last)
&lt;ipython-input-8-1bb975dcc2d2&gt; in &lt;cell line: 7&gt;()
      5 # stage 1
      6 stage_1 = DiffusionPipeline.from_pretrained(&quot;DeepFloyd&#47;IF-I-M-v1.0&quot;, variant=&quot;fp16&quot;, torch_dtype=torch.float16)
----&gt; 7 stage_1.enable_xformers_memory_efficient_attention()  # remove line if torch.__version__ &gt;= 2.0.0
      8 stage_1.enable_model_cpu_offload()
      9 

8 frames
&#47;usr&#47;local&#47;lib&#47;python3.10&#47;dist-packages&#47;diffusers&#47;models&#47;attention_processor.py in set_use_memory_efficient_attention_xformers(self, use_memory_efficient_attention_xformers, attention_op)
    191                 )
    192             if not is_xformers_available():
--&gt; 193                 raise ModuleNotFoundError(
    194                     (
    195                         &quot;Refer to https:&#47;&#47;github.com&#47;facebookresearch&#47;xformers for more information on how to install&quot;

ModuleNotFoundError: Refer to https:&#47;&#47;github.com&#47;facebookresearch&#47;xformers for more information on how to install xformers

--------------------

再装 xformers 后报错依旧，什么原因?
pip install -U xformers</div>2023-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/99/17/e25c3884.jpg" width="30px"><span>Eric.Sui</span> 👍（0） 💬（1）<div>边缘重绘用什么方案？算是变体吗？</div>2023-08-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKuaZauv0hcyH9e51azzYTt2rFQPia1ryfupuAVYYeDaicp1ictV7dciarbAXUb2bz2x0qu9x6tL4VVhA/132" width="30px"><span>Geek_7401d2</span> 👍（0） 💬（1）<div>老师您好，DeepFloyd IF模型和stable diffusion 1.5、stable diffusion 2.0等是什么关系呢，他们是两类扩散模型吗？生成效果哪个更好呢</div>2023-08-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLhs7ykGEy46a8ljg3LPvXTRxpgMLEhvZoAYIQL6I46OEqbNV4U1mXryhJt1bE3mhf7ey6jfl3IyQ/132" width="30px"><span>cmsgoogle</span> 👍（0） 💬（1）<div>运行上面这段代码，需要至少 20G 以上的显存。如果需要降低显存占用，可以用 xFormer 优化 Transformer 的计算效率，或者释放已经完成推理的模型资源等。
- TextinImage的示例代码没有给出。</div>2023-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（0） 💬（1）<div>在哪里可以体验下imagen绘画呢？</div>2023-08-18</li><br/>
</ul>