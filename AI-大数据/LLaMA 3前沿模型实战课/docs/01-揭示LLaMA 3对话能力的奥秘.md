你好，我是Tyler。今天我们正式开始学习LLaMA 3的能力模型。

过去的一年中，大模型技术得到了广泛认可，全行业对大模型的投入也在不断增加。开源社区涌现了许多优秀的模型和框架，推动了大模型技术的普及和应用。在这一年的时间里，LLaMA 系列模型也经历了快速的发展，从 LLaMA 2 到 LLaMA 3，我们看到了性能和应用上的显著提升。

本季专栏中，我将采用“Learn by doing”的方法，通过简洁的示例，深入剖析大模型技术的本质。我们将探讨LLaMA 3的能力模型，详细解析大模型技术的各个方面，并深入到你在使用LLaMA 3过程中会遇到的各种细节。

在第一讲中，我将详细介绍LLaMA 3模型的核心能力——对话生成，并展示它在文本生成方面的强大潜力。

## 基本操作：生成内容

首先，让我们来了解一下LLaMA 3的核心能力。LLaMA 3主要依赖于Next Token Prediction（下一个词预测）机制，通过预测下一个词来生成连贯的对话。这种机制基于海量文本数据的训练，使模型能够捕捉语言的模式和规律，生成符合上下文逻辑的文本内容。

### Next Token Prediction

Next Token Prediction是大语言模型生成文本的基础。模型处理输入文本的步骤如下：
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/fb/4add1a52.jpg" width="30px"><span>兵戈</span> 👍（4） 💬（3）<div>Typler老师的课程代码地址：https:&#47;&#47;github.com&#47;tylerelyt&#47;llama。不过当前工程目录下缺少requirements.txt，可能会让许多跑代码的同学遇到包依赖不一致的问题，我提了一个issue：
https:&#47;&#47;github.com&#47;tylerelyt&#47;llama&#47;issues&#47;1
希望Typer老师有空补充下 :）</div>2024-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/fb/4add1a52.jpg" width="30px"><span>兵戈</span> 👍（3） 💬（2）<div>Tyler老师提供示例很不错，其中第一个示例，最好加上max_length参数，否则可能会一直运行停不下来，如下：
with torch.no_grad():
    outputs = model.generate(**inputs, max_length=100)</div>2024-10-17</li><br/><li><img src="" width="30px"><span>edward</span> 👍（3） 💬（3）<div>请问老师 实验环境需要什么样的机器配置？</div>2024-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/72/2feef236.jpg" width="30px"><span>keep move</span> 👍（1） 💬（1）<div>示例代码如何能运行起来，能否写个简要的步骤呢</div>2024-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/65/35f711a1.jpg" width="30px"><span>J Sun</span> 👍（0） 💬（1）<div>模型怎么下载
</div>2024-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/44/324e3cd6.jpg" width="30px"><span>S！</span> 👍（0） 💬（0）<div>m2系列的mac pro运行demo一直没有输出结果，console输出如下：
import sys; print(&#39;Python %s on %s&#39; % (sys.version, sys.platform))
&#47;usr&#47;local&#47;bin&#47;python3.10 -X pycache_prefix=&#47;Users&#47;salesonlee&#47;Library&#47;Caches&#47;JetBrains&#47;PyCharm2024.1&#47;cpython-cache &#47;Applications&#47;PyCharm.app&#47;Contents&#47;plugins&#47;python&#47;helpers&#47;pydev&#47;pydevd.py --multiprocess --qt-support=auto --client 127.0.0.1 --port 57101 --file &#47;Users&#47;salesonlee&#47;IT&#47;dev_codes&#47;PythonProjects&#47;tylerelyt-llama&#47;chapter1&#47;lesson1&#47;example1.py 
Connected to pydev debugger (build 241.17890.14)
Loading checkpoint shards: 100%|██████████| 4&#47;4 [01:00&lt;00:00, 15.10s&#47;it]
Setting `pad_token_id` to `eos_token_id`:None for open-end generation.
Starting from v4.46, the `logits` model output will have the same type as the model (except at train time, where it will always be FP32)


请问是因为没有使用gpu么，是硬件配置的原因？还是其它原因？ </div>2024-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/44/324e3cd6.jpg" width="30px"><span>S！</span> 👍（0） 💬（0）<div>import sys; print(&#39;Python %s on %s&#39; % (sys.version, sys.platform))
&#47;usr&#47;local&#47;bin&#47;python3.10 -X pycache_prefix=&#47;Users&#47;salesonlee&#47;Library&#47;Caches&#47;JetBrains&#47;PyCharm2024.1&#47;cpython-cache &#47;Applications&#47;PyCharm.app&#47;Contents&#47;plugins&#47;python&#47;helpers&#47;pydev&#47;pydevd.py --multiprocess --qt-support=auto --client 127.0.0.1 --port 57101 --file &#47;Users&#47;salesonlee&#47;IT&#47;dev_codes&#47;PythonProjects&#47;tylerelyt-llama&#47;chapter1&#47;lesson1&#47;example1.py 
Connected to pydev debugger (build 241.17890.14)
Loading checkpoint shards: 100%|██████████| 4&#47;4 [01:00&lt;00:00, 15.10s&#47;it]
Setting `pad_token_id` to `eos_token_id`:None for open-end generation.
Starting from v4.46, the `logits` model output will have the same type as the model (except at train time, where it will always be FP32)
</div>2024-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/44/324e3cd6.jpg" width="30px"><span>S！</span> 👍（0） 💬（0）<div>m2系列mac pro 运行demo一直没有输出结果，console输出如下：</div>2024-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/44/324e3cd6.jpg" width="30px"><span>S！</span> 👍（0） 💬（0）<div>运行课程demo需要什么样的碍硬件资源？</div>2024-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/44/324e3cd6.jpg" width="30px"><span>S！</span> 👍（0） 💬（2）<div>Mac pro可以运行llama3么</div>2024-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/72/2feef236.jpg" width="30px"><span>keep move</span> 👍（0） 💬（0）<div>python学习那个方向 pytorch吗</div>2024-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/9a/cb/53af3dc6.jpg" width="30px"><span>Orson</span> 👍（0） 💬（0）<div># agent_a.py
from common import create_app

app = create_app(&quot;system: 你是一个熟悉人工智能技术的计算机科学家。&quot;)

if __name__ == &#39;__main__&#39;:
    app.run(port=5000)
请问，在用AutoDL这样的云服务的时候，app.run(port=5000）需要怎么修改。或者，agent_a、b、c和common文件需要做哪些修改？</div>2024-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/89/fcf95d32.jpg" width="30px"><span>Allen</span> 👍（0） 💬（0）<div>你好，请问在调用模型时with torch.no_grad():为啥后面几段里没有加？会影响性能吗？谢谢。</div>2024-10-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLCrJQ4AZe8VrDkR6IO03V4Tda9WexVT4zZiahBjLSYOnZb1Y49JvD2f70uQwYSMibUMQvib9NmGxEiag/132" width="30px"><span>Dowen Liu</span> 👍（0） 💬（0）<div>不用python 能不能做同样的调用呢？比如直接调用接口、spring ai </div>2024-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/65/35f711a1.jpg" width="30px"><span>J Sun</span> 👍（0） 💬（1）<div>模型在哪里下载</div>2024-10-18</li><br/>
</ul>