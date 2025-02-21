你好，我是黄佳，欢迎来到LangChain实战课！

之前，我们花了两节课的内容讲透了提示工程的原理以及LangChain中的具体使用方式。今天，我们来着重讨论Model I/O中的第二个子模块，LLM。

![](https://static001.geekbang.org/resource/image/cd/81/cd7e1506af5b6a8e382c2c9eab4d7481.jpg?wh=4000x1536)

让我们带着下面的问题来开始这一节课的学习。大语言模型，不止ChatGPT一种。调用OpenAI的API，当然方便且高效，不过，如果我就是想用其他的模型（比如说开源的Llama2或者ChatGLM），该怎么做？再进一步，如果我就是想在本机上从头训练出来一个新模型，然后在LangChain中使用自己的模型，又该怎么做？

关于大模型的微调（或称精调）、预训练、重新训练、乃至从头训练，这是一个相当大的话题，不仅仅需要足够的知识和经验，还需要大量的语料数据、GPU硬件和强大的工程能力。别说一节课了，我想两三个专栏也不一定能讲全讲透。不过，我可以提纲挈领地把大模型的训练流程和使用方法给你缕一缕。这样你就能体验到，在LangChain中使用自己微调的模型是完全没问题的。

## 大语言模型发展史

说到语言模型，我们不妨先从其发展史中去了解一些关键信息。

Google 2018 年的论文名篇Attention is all you need，提出了Transformer架构，也给这一次AI的腾飞点了火。Transformer是几乎所有预训练模型的核心底层架构。基于Transformer预训练所得的大规模语言模型也被叫做“基础模型”（Foundation Model 或Base Model）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/33/d3/30a89b21.jpg" width="30px"><span>nick</span> 👍（5） 💬（1）<div>老师，有个疑问，原来使用像百度AI、腾讯AI做垂直领域的多轮对话，往往需要维护语料意图啥的，那有了大模型后，这些工作还需要做么，如果要那怎么做？跟传统维护语料意图有什么区别。谢谢</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/11/2cbd941d.jpg" width="30px"><span>javanb</span> 👍（3） 💬（1）<div>老师，最近我就在微调垂直行业大模型，但是效果不理想，我这边采用了Lora的训练方式，行业数据和通用数据大约是1:1。行业数据量大约10G。但是出来的结果，通用能力降低了，并且行业能力也并没有那么理想。 所以有几个疑问不知老师能否传授一下SFT的经验、1：我们通常行业数据配比是多少？ 2：哪种训练方式更合适？lora还是freeze  3：哪种类型的数据更合适？目前是大量的公司内部的数据，还需要哪些数据？</div>2024-03-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（3） 💬（1）<div>GITHUB上的类似WeChat chat类项目https:&#47;&#47;github.com&#47;zhayujie&#47;chatgpt-on-wechat，如何结合LangChain和huggingFace结合修改？找不到方向？老师可以加餐讲一讲吗？谢谢。</div>2023-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/18/1a/5f36bb6e.jpg" width="30px"><span>远游</span> 👍（2） 💬（1）<div>老师，macos安装pip install llama-cpp-python报错：
                                      ^
      &#47;private&#47;var&#47;folders&#47;x_&#47;l6wthj_d7mb_gzcx3wvkmcvc0000gn&#47;T&#47;pip-install-ms76ov67&#47;llama-cpp-python_9ce52d9b45d04a73950f2448a45590a0&#47;vendor&#47;llama.cpp&#47;ggml.c:2243:11: note: expanded from macro &#39;GGML_F32x4_REDUCE&#39;
          res = _mm_cvtss_f32(_mm_hadd_ps(t0, t0));                     \
              ~ ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      12 warnings generated.
      [10&#47;13] &#47;Library&#47;Developer&#47;CommandLineTools&#47;usr&#47;bin&#47;c++ -DACCELERATE_LAPACK_ILP64 -DACCELERATE_NEW_LAPACK -DGGML_USE_ACCELERATE -DGGML_USE_K_QUANTS -DGGML_USE_METAL -DLLAMA_BUILD -DLLAMA_SHARED -D_DARWIN_C_SOURCE -D_XOPEN_SOURCE=600 -Dllama_EXPORTS -I&#47;private&#47;var&#47;folders&#47;x_&#47;l6wthj_d7mb_gzcx3wvkmcvc0000gn&#47;T&#47;pip-install-ms76ov67&#47;llama-cpp-python_9ce52d9b45d04a73950f2448a45590a0&#47;vendor&#47;llama.cpp&#47;. -O3 -DNDEBUG -std=gnu++11 -isysroot &#47;Library&#47;Developer&#47;CommandLineTools&#47;SDKs&#47;MacOSX10.15.sdk -fPIC -Wall -Wextra -Wpedantic -Wcast-qual -Wno-unused-function -Wunreachable-code-break -Wunreachable-code-return -Wmissing-declarations -Wmissing-noreturn -Wmissing-prototypes -Wextra-semi -MD -MT vendor&#47;llama.cpp&#47;CMakeFiles&#47;llama.dir&#47;llama.cpp.o -MF vendor&#47;llama.cpp&#47;CMakeFiles&#47;llama.dir&#47;llama.cpp.o.d -o vendor&#47;llama.cpp&#47;CMakeFiles&#47;llama.dir&#47;llama.cpp.o -c &#47;private&#47;var&#47;folders&#47;x_&#47;l6wthj_d7mb_gzcx3wvkmcvc0000gn&#47;T&#47;pip-install-ms76ov67&#47;llama-cpp-python_9ce52d9b45d04a73950f2448a45590a0&#47;vendor&#47;llama.cpp&#47;llama.cpp
      ninja: build stopped: subcommand failed.

      *** CMake build failed
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for llama-cpp-python
Failed to build llama-cpp-python
ERROR: Could not build wheels for llama-cpp-python, which is required to install pyproject.toml-based projects</div>2023-10-26</li><br/><li><img src="" width="30px"><span>Geek_cb5e16</span> 👍（1） 💬（1）<div>老师  要使用HuggingFace 和 Pipeline HuggingFaceHUB 有什么区别 还是不太明白</div>2023-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/fb/37/791d0f5e.jpg" width="30px"><span>Monin</span> 👍（1） 💬（1）<div>老师 垂类模型   当有了相应领域数据后  一般用什么进行微调开源模型？ Loar？ finetune吗</div>2023-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/fb/37/791d0f5e.jpg" width="30px"><span>Monin</span> 👍（1） 💬（2）<div>老师  用LangChain调用自定义语言模型时，在初始化具体模型时如何确定相对应的具体类名。比如目前性能最好的XwinLM模型，在HuggingFace上下载合适的模型后  如何找到对应的初始化类？</div>2023-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/4e/85502e98.jpg" width="30px"><span>balance</span> 👍（1） 💬（1）<div>老师好! 本地电脑运行 Llama-2-7b-chat-hf 模型案例代码，需要什么硬件配置？我运行情况是，输出Loading checkpoint shards: 100%|██████████| 2&#47;2 [00:04&lt;00:00,  2.40s&#47;it] 后一直不动</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/26/35ef9bef.jpg" width="30px"><span>无限可能</span> 👍（1） 💬（5）<div>MabBook M2上面的DEMO都运行不了，提示`AssertionError: Torch not compiled with CUDA enabled`，不知道是不是使用的方式不正确。</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b8/36/2e922a82.jpg" width="30px"><span>Alan</span> 👍（0） 💬（2）<div>黄佳老师好，有没有可能弄一个可运行的镜像环境。每次运行实例程序都有各种环境问题，包括python库的版本兼容等。</div>2024-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/b7/db/dd23d4c3.jpg" width="30px"><span>Charlie</span> 👍（0） 💬（3）<div>llama-cpp-python v0.2.22 加载 llama-2-7b-chat.ggmlv3.q4_K_S.bin 时报错，错误信息如下：
gguf_init_from_file: invalid magic characters &#39;tjgg&#39;
error loading model: llama_model_loader: failed to load model from &#47;Users&#47;xxx&#47;PycharmProjects&#47;hello_langchain&#47;OfflineModel&#47;llama-2-7b-chat.ggmlv3.q4_K_S.bin

准备尝试用gguf model （llama-2-7b-chat.Q4_K_S.gguf）去加载。
https:&#47;&#47;huggingface.co&#47;TheBloke&#47;Llama-2-7B-Chat-GGUF&#47;tree&#47;main
</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/9b/13/47feb437.jpg" width="30px"><span>高浩宇</span> 👍（0） 💬（2）<div>Llama 2和智谱AI的ChatGLM3-6b哪个适合用来做基础模型</div>2023-11-29</li><br/><li><img src="" width="30px"><span>Geek_cb5e16</span> 👍（0） 💬（1）<div>大规模使用语言模型的时候 适合使用开源模型 
量大的时候时候私有化模型会减少一部分成本
</div>2023-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/1b/6444e933.jpg" width="30px"><span>Liberalism</span> 👍（0） 💬（10）<div>我的 Llama 2 已经申请两天了，还在待审核中</div>2023-11-09</li><br/><li><img src="" width="30px"><span>Geek_995b81</span> 👍（0） 💬（2）<div>老师请问一个问题，我是用了其他同学私有化部署的chatGLM模型，他们提供了一个rest api的接口给我去掉，相当于一个chat功能的接口，如果我自己用langchain去接，是应该找他们要chatGLM部署的服务端口吗？我有点弄不清楚</div>2023-10-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YflLdCdbUAkfr9LPzF50EibDrMxBibPicQ5NNAETaPP0ytTmuR3h6QNichDMhDbR2XelSIXpOrPwbiaHgBkMJYOeULA/132" width="30px"><span>抽象派</span> 👍（0） 💬（1）<div>老师，试用了 ‘bigcode&#47;starcoder’，但是生成的内容没有openai的多。设置了max_length也没有用，可以帮我看看是不是我的使用方式不对吗？
def start_coder() -&gt; BaseLanguageModel:
    llm = HuggingFaceHub(
        repo_id=&quot;bigcode&#47;starcoder&quot;, model_kwargs={&quot;max_length&quot;: 16384, &quot;temperature&quot;: 0.5}
    )
    return llm</div>2023-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ad/ff/e7ed1a08.jpg" width="30px"><span>庄楚斌</span> 👍（0） 💬（1）<div>site-packages&#47;langchain&#47;llms&#47;base.py&quot;, line 607, in generate
    self.callbacks,
    ^^^^^^^^^^^^^^ object has no attribute &#39;callbacks&#39;  langchain 版本是多少呢？</div>2023-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ad/ff/e7ed1a08.jpg" width="30px"><span>庄楚斌</span> 👍（0） 💬（1）<div>site-packages&#47;langchain&#47;llms&#47;base.py&quot;, line 607, in generate
    self.callbacks,
    ^^^^^^^^^^^^^^</div>2023-10-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqFqGgBQU7libL1KIov7X5SqNUgIztTOcCX584JcVD8wejgqtbaoBKkFGRBXXkLA1Q57afep1ibBNqw/132" width="30px"><span>Geek_2a4c8d</span> 👍（0） 💬（1）<div>老师请教一个问题，我在MacBook上运行案例 macos 13.6。报：RuntimeError: MPS backend out of memory (MPS allocated: 6.69 GB, other allocations: 8.35 MB, max allowed: 6.77 GB). Tried to allocate 172.00 MB on private pool. Use PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 to disable upper limit for memory allocations (may cause system failure).
。 按照提示将 PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 配置到环境变量了 ，也参考了一些网上办法，都没解决。</div>2023-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4a/ee/fe035424.jpg" width="30px"><span>棟</span> 👍（0） 💬（2）<div>老师，请教一个疑问，通过代码下载模型到对应设备的时候总是网络中断，导致下载失败，有没有网络中断仍然可以恢复下载的方法：
pipeline = transformers.pipeline( &quot;text-generation&quot;,    model=model,    torch_dtype=torch.float16, device_map=&quot;auto&quot;,    max_length = 1000)
llm = HuggingFacePipeline(pipeline = pipeline,   model_kwargs = {&#39;temperature&#39;:0})
有了解的朋友也请指点一下，感谢！
Downloading shards:   0%|                                                                                                           | 0&#47;2 [15:49&lt;?, ?it&#47;s]
Downloading (…)of-00002.safetensors:   7%|████▉                                                                      | 650M&#47;9.98G [15:48&lt;3:46:43, 686kB&#47;s]</div>2023-10-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erXRSYibXVPR8OMP7ZQxFPg6nn9vlcqUH1QeFibdk0HJRRSoYiaZiblHZicgicJ8OEicttqyI70jZl0y8iaPA/132" width="30px"><span>zhhuyi</span> 👍（0） 💬（1）<div>怎么微调模型呢？</div>2023-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/fb/37/791d0f5e.jpg" width="30px"><span>Monin</span> 👍（0） 💬（2）<div>老师 https:&#47;&#47;huggingface.co&#47; 官网经常访问不通，老师有什么稳定访问的办法吗？</div>2023-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>怎么知道电脑上是否有GPU？
我的笔记本是16年年底买的，惠普笔记本，CPU是i7 8核，设备管理器里面好像没有看到GPU。</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（0） 💬（1）<div>预训练、微调、量化，这几个一知半解的概念，在这篇文章中捋清了不少，🙏
这几课都还没来得及跟上实操上机，惭愧惭愧，先mark</div>2023-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/26/6f7b9fd8.jpg" width="30px"><span>AI编程派</span> 👍（0） 💬（5）<div>Llama 申请下载的时候遇到两个问题：
1：Country 选中China, 就提示 Sorry, the download is not available in your region.
2：Country 选项中有Taiwan, zz问题 :)</div>2023-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（3）<div>llama_index 怎么样？ 很多功能 langchain 已经有了， llama_index 这个的价值体现在哪里？</div>2023-09-18</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（3） 💬（0）<div>逐一运行老师的课程代码。
1、&quot;申请使用 Meta 的 Llama2 模型&quot;，填写了香港地址，国内移动号码，通过香港科学上网，很快批准下载模型。

2、“通过 HuggingFace 调用 Llama”的”01_HugggingFace_Llama.py“
（1）因为是手提电脑，没有GPU, 将模型调到CPU上预训练：
旧代码：inputs = tokenizer(prompt, return_tensors=&quot;pt&quot;).to(&quot;cuda&quot;)
新代码： inputs = tokenizer(prompt, return_tensors=&quot;pt&quot;).to(&quot;cpu&quot;)
（2）运行时间很久，加上自动下载模型，有几个小时。运行结果与课程基本一致。也是将“玫瑰”作为女孩名字来编故事的。

3、“通过 HuggingFace Hub”，运行代码结果也是一个词：“flower&quot;

4、“通过 HuggingFace Pipeline”，运行代码结果杂乱。

5、 在”用 LangChain 调用自定义语言模型“的”04_LangChain_CustomizeModel.py“，问题：
（1）安装 llama-cpp-python 时遇到错误，要在VS 中安装编译工具和配置环境；
（2）出现 ValueError: Failed to load model from file 错误。这是课程中采用llama-2-7b-chat.ggmlv3.q4_K_S.bin 模型，但是GGML 格式已经被 GGUF 格式取代，且 llama.cpp 从 2023 年 8 月 21 日起不再支持 GGML 模型文件。 下载改用”TheBloke&#47;Llama-2-7B-Chat-GGUF“模型，修改：
旧代码： MODEL_NAME = &#39;llama-2-7b-chat.ggmlv3.q4_K_S.bin&#39;
新代码： MODEL_NAME = &quot;llama-2-7b-chat.Q4_K_M.gguf&quot;
（3）运行结果与课程基本一致，也是英文，翻译后，发现回答结果很不错：
“感谢您就您最近的购买与我们联系。很抱歉，您收到的鲜花在交货两天后状况不佳。我们理解这对你来说一定是多么令人失望，特别是因为它们是作为送给你女朋友的礼物。
我们想向您保证，我们认真对待这些问题，并正在立即调查此事。我们的团队将调查该问题，并与我们的供应商合作，以确保我们的鲜花具有最高的质量和新鲜度。我们还将根据您的喜好为您提供鲜花的全额退款或更换。
请知道，我们重视您的满意，并感谢您对此事的耐心和理解。如果还有什么我们可以为您提供帮助的，请随时与我们联系。”</div>2024-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/66/4a/a5ecf67a.jpg" width="30px"><span>在路上1619</span> 👍（2） 💬（0）<div>黄老师好，我运行第一个例子前后花了将近8分钟，用的是4090的GPU，体验下来这个速度还是太慢了。如果生产上部署70b的模型，一般选什么样的GPU？</div>2024-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第6讲打卡~
确实就像老师说的，进入大模型领域，仿佛打开了新世界的大门，需要学习和理解的东西非常多，感觉每天都充满了对知识的渴望😂</div>2024-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/f0/fab69114.jpg" width="30px"><span>StopLiu</span> 👍（1） 💬（0）<div>老师好，私有化部署，如何通过 langchain 调用本地模型的 embedding？</div>2024-03-06</li><br/>
</ul>