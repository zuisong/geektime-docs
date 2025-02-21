你好，我是黄佳，欢迎来到LangChain实战课！

在上节课中，我们深入探讨了如何利用CAMEL框架制定出一个高效的鲜花营销方案。然而，LangChain目前是将基于CAMEL框架的代理定义为Simulation Agents（模拟代理）。这种代理在模拟环境中进行角色扮演，试图模拟特定场景或行为，而不是在真实世界中完成具体的任务。

随着ChatGPT的崭露头角，我们迎来了一种新型的代理——Autonomous Agents（自治代理或自主代理）。这些代理的设计初衷就是能够独立地执行任务，并持续地追求长期目标。在LangChain的代理、工具和记忆这些组件的支持下，**它们能够在无需外部干预的情况下自主运行，这在真实世界的应用中具有巨大的价值。**

目前，GitHub上已有好几个备受关注的“网红”项目，如AutoGPT、BabyAGI和HuggingGPT，它们都代表了自治代理的初步尝试。尽管这些代理仍处于实验阶段，但潜力十分巨大。它们都是基于LangChain框架构建的。通过LangChain，你可以在这些开源项目中轻松地切换和测试多种LLM、使用多种向量存储作为记忆，以及充分利用LangChain的丰富工具集。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/37/49/80/791d0f5e.jpg" width="30px"><span>不吃苦瓜</span> 👍（4） 💬（1）<div>单从这babyAGI的DEMO就决定了这个课值不值，太赞了，写的太好了</div>2023-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/1c/9255261b.jpg" width="30px"><span>AAT天宇</span> 👍（2） 💬（1）<div>如果将自主代理和Camel结合呢？

通过自主代理的方式，解决长期记忆的问题，将自主代理的示例编程领域专家；
通过Camel代理的方式，完成多校色，多领域认知和复杂任务的解决问题；</div>2024-01-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（2） 💬（1）<div>hugging和大模型在老师的企业工作实践产生的什么作用？和大家分享吗？学习了还找不到技术点的抓手。</div>2023-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/1b/6444e933.jpg" width="30px"><span>Liberalism</span> 👍（1） 💬（1）<div>老师您好，在结尾处您有提到 AI 在未来项目管理领域有很大的想象空间，方便细讲一下吗？</div>2023-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/e3/c49aa508.jpg" width="30px"><span>鲸鱼</span> 👍（1） 💬（2）<div>老师，vectorstore可以换成其他的吗？比如Chroma？faiss这个库安装遇到问题了，上网搜了一圈，运行时总是遇到各种问题，一直跑不起来</div>2023-11-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（1） 💬（1）<div>练习以上代码自己部署本地，还是使用云平台合适，老师平时生产时使用什么设备生产，我想练习到生产一起使用，请老师可以推荐吗？谢谢。</div>2023-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/b5/c7/ed1dcbed.jpg" width="30px"><span>曙光</span> 👍（0） 💬（8）<div>老师，运行代码的时候报这个错误，Chain, BaseModel他们共同基类是哪个呀？
Traceback (most recent call last):
  File &quot;D:\py_dev\langchain19\BabyAGI_CN.py&quot;, line 160, in &lt;module&gt;
    class BabyAGI(Chain, BaseModel):
TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
</div>2023-10-24</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（2） 💬（0）<div>用国产大模型代替 OpenAI ，调试很久，才终于成功！太难啦。

###1  出现Chain, BaseModel 共同基类错误。按留言安装 pydantic 1.10.12 

###2  替换模型：
# 旧代码1： 
embeddings_model = OpenAIEmbeddings()
# 新代码1：（用百川模型）
from langchain_community.embeddings import BaichuanTextEmbeddings 
embeddings_model = BaichuanTextEmbeddings(baichuan_api_key=&quot; sk-KEY&quot;)  #此用你的百川智能API KEY 代替
# 旧代码2：
llm = OpenAI(temperature=0)
# 新代码2：（用阿里模型）
llm = ChatOpenAI(
        api_key=&quot;sk-KYE&quot;,   # 此用您的阿里 DASHSCOPE_API_KEY替换
        base_url=&quot;https:&#47;&#47;dashscope.aliyuncs.com&#47;compatible-mode&#47;v1&quot;, 
        model_name=&quot;qwen-turbo&quot;)

###3  更新导入路径
# 旧代码3：
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM, OpenAI
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
# 新代码3：
from langchain_community.embeddings import OpenAIEmbeddings  
from langchain_community.llms import BaseLLM, OpenAI  
from langchain_community.vectorstores import FAISS  
from langchain_community.docstore.in_memory import InMemoryDocstore  

###4  发生异常: AssertionError 。
exception: no description：  results = vectorstore.similarity_search_with_score(query, k=k)
查找 FAISS 文档，并采用其代码类似例子调试，发现 vectorstore 调用 FAISS 时，index 是不能随意设置的，修改如下：
# 旧代码4：
embedding_size = 1536
# 新代码4：
embedding_size = 1024

###5  出现不定期的代码错误，在  # Step 2: Execute the task  中 发生异常: ValueError
invalid literal for int() with base 10: &#39;#&#39; ， this_task_id = int(task[&quot;task_id&quot;]) 
这个错误在代码前2轮循环中是不会产生的，但在第3轮循环产生。检查代码，task字典中的 task_id  值是‘#’ 号，不是数字，但是这是模型自动生成。而模型的生成是很魔幻的，如何是好？
检查任务优先级模块，核查提示词，发现要求的生成的例子是：#. First task   ，  #. Second task  格式的。将 # 改为数字，一举成功！
# 旧代码5
&quot; #. First task&quot;
&quot; #. Second task&quot;
# 新代码5
&quot; 1. First task&quot;
&quot; 2. Second task&quot;</div>2024-09-07</li><br/><li><img src="" width="30px"><span>张帅</span> 👍（0） 💬（0）<div>学完这个篇章，LLM给出的成果相比开发所需的代码量来说，真是令人惊讶。也许以后更重要的能力，是发现需求，以及能将需求拆分成合适的颗粒度并写出合适的提示词。这个感觉是一个可以努力达成的目标。</div>2024-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/58/c0/d1d488b0.jpg" width="30px"><span>chenyang</span> 👍（0） 💬（0）<div>老师，请问task1执行时，怎么获得北京当前的天气状况的呀？ 这里没看到用到search相关的tools呀</div>2024-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第19讲打卡~</div>2024-07-22</li><br/>
</ul>