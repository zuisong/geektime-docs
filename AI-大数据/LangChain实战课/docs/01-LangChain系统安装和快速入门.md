你好，我是黄佳，欢迎来到LangChain实战课！

在我们开始正式的学习之前，先做一些基本知识储备。虽然大语言模型的使用非常简单，但是如果我们通过API来进行应用开发，那么还是有些基础知识应该先了解了解，比如什么是大模型，怎么安装LangChain，OpenAI的API有哪些类型，以及常用的开源大模型从哪里下载等等。

## 什么是大语言模型

大语言模型是一种人工智能模型，通常使用深度学习技术，比如神经网络，来理解和生成人类语言。这些模型的“大”在于它们的参数数量非常多，可以达到数十亿甚至更多，这使得它们能够理解和生成高度复杂的语言模式。

你可以**将大语言模型想象成一个巨大的预测机器，其训练过程主要基于“猜词”**：给定一段文本的开头，它的任务就是预测下一个词是什么。模型会根据大量的训练数据（例如在互联网上爬取的文本），试图理解词语和词组在语言中的用法和含义，以及它们如何组合形成意义。它会通过不断地学习和调整参数，使得自己的预测越来越准确。

![](https://static001.geekbang.org/resource/image/57/e5/5730e6debb8c1a0876f79814c0fb78e5.png?wh=744x478 "语言模型帮我们预测下一个词")

比如我们给模型一个句子：“今天的天气真”，模型可能会预测出“好”作为下一个词，因为在它看过的大量训练数据中，“今天的天气真好”是一个常见的句子。这种预测并不只基于词语的统计关系，还包括对上下文的理解，甚至有时能体现出对世界常识的认知，比如它会理解到，人们通常会在天气好的时候进行户外活动。因此也就能够继续生成或者说推理出相关的内容。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/9d/a9/4602808f.jpg" width="30px"><span>黄佳</span> 👍（9） 💬（4）<div>OpenAI，最近戏比较多，旧代码是0.28版本，任何以上的版本，都需要比较大的改动，记录如下。

旧代码
# import openai

新代码
from openai import OpenAI
client = OpenAI()

旧代码
# response = openai.Completion.create(
#   model=&quot;text-davinci-003&quot;,
#   temperature=0.5,
#   max_tokens=100,
#   prompt=&quot;请给我的花店起个名&quot;)

新代码
response = client.completions.create(
  model=&quot;gpt-3.5-turbo-instruct&quot;,
  temperature=0.5,
  max_tokens=100,
  prompt=&quot;请给我的花店起个名&quot;)

旧代码
# response = openai.ChatCompletion.create(
#   model=&quot;gpt-4&quot;,
#   messages=[
#         {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;You are a creative AI.&quot;},
#         {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;请给我的花店起个名&quot;},
#     ],
#   temperature=0.8,
#   max_tokens=60
# )

# print(response[&#39;choices&#39;][0][&#39;message&#39;][&#39;content&#39;])

新代码
response = client.completions.create(  model=&quot;gpt-4&quot;,
  messages=[
        {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;You are a creative AI.&quot;},
        {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;请给我的花店起个名&quot;},
    ],
  temperature=0.8,
  max_tokens=60
)

print(response.choices[0].message.content)</div>2024-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/a9/846e2e85.jpg" width="30px"><span>吴曦</span> 👍（12） 💬（1）<div>搭建了基础的langchain问答机器人，怎样评估回答质量？有适合的指标吗？</div>2023-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/bb/7d/26340713.jpg" width="30px"><span>黄振宇</span> 👍（11） 💬（1）<div>最近在死磕langchain 终于有中文的详细课程啦</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（6） 💬（5）<div>1.我认为LangChain的核心价值在于功能模块化和模块链接化，这意味着AI应用开发被提炼成了很多个标准步骤，每个步骤有标准的参数和接口，便于灵活的替换和组合。这就像Java中Spring，封装了各种组件，并通过控制反转将它们组合在一起。

2.HuggingFace模型：
import os
# 设置网络代理
os.environ[&quot;http_proxy&quot;] = &quot;http:&#47;&#47;127.0.0.1:7890&quot;
os.environ[&quot;https_proxy&quot;] = &quot;http:&#47;&#47;127.0.0.1:7890&quot;

# 通过.env管理huggingfacehub_api_token
from dotenv import load_dotenv
load_dotenv()

from langchain import HuggingFaceHub
llm = HuggingFaceHub(repo_id=&quot;bigscience&#47;bloom-1b7&quot;)
resp = llm.predict(&quot;请给我的花店起个名&quot;)
print(resp)

#输出：,叫&quot;花之恋&quot;。&quot;花之恋&quot;</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/9f/8a7cd83d.jpg" width="30px"><span>Crazy</span> 👍（5） 💬（1）<div>使用LangChain编程，是一个编程思维的转化，你定义工具，流程，让大模型的能力去提供逻辑判断，流程组建，我写的过程中感觉其对传统编程思维挑战最大。同时，调试的复杂度更高，更要语义化的编程，导致你要获取确定的答案或者拿到预期的结果挑战很大。希望课程后续能分享到系统化地讲解调试输出，目前个人调试方法是各种参数、提示词，工具描述一顿改，花费比之前更长的时间调试一个功能，能解决这个效率问题对之后的产品化或者应用至关重要。</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/73/93e09e89.jpg" width="30px"><span>dengyu</span> 👍（5） 💬（3）<div>windows中使用把openai API key保存在.env 文件中，读取文件，能否给出具体代码？</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（3） 💬（1）<div>对于开发人员来说，LangChain是一个工具箱，可以方便的组合各类AI和非AI的能力，并通过抽象实现各相似组件的快速替代，有点儿类似于java生态下的spring。
对于AI来说，会有两个门槛，一个是AI学会使用和组合这些工具，二是可以自行创造新的工具并予以使用。一旦走到第二步，硅基生物的时代可能就到来了。</div>2023-09-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YflLdCdbUAkfr9LPzF50EibDrMxBibPicQ5NNAETaPP0ytTmuR3h6QNichDMhDbR2XelSIXpOrPwbiaHgBkMJYOeULA/132" width="30px"><span>抽象派</span> 👍（3） 💬（1）<div>请问Python用什么版本？</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c4/51/5bca1604.jpg" width="30px"><span>aLong</span> 👍（1） 💬（1）<div>磕磕绊绊，跑到openai看API文档，跑到langchain去看文档。然后按照课程内容写下了新版本的东西。

#我让他给我返回三个店名供我挑选，格式是list。
Sure! Here are three name suggestions for your flower shop:
1. Blossom Boutique
2. Petal Paradise
3. Floral Haven
</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/1f/7551f182.jpg" width="30px"><span>卓丁</span> 👍（1） 💬（1）<div>老师好，请教一下关于assistant的讲解：

assistant：助手消息是模型的回复。例如，在你使用 API 发送多轮对话中新的对话请求时，可以通过助手消息提供先前对话的上下文。然而，请注意在对话的最后一条消息应始终为用户消息，因为模型总是要回应最后这条用户消息。

这里的assistant的用途，我还是比较模糊，意思就是说：比如在多轮对话的场景中，可以将 跟模型的历史对话 通过 assistant 字段 再次传递给llm，是吗？
额外，“然而，请注意在对话的最后一条消息应始终为用户消息，因为模型总是要回应最后这条用户消息。”中你所说的 “最后一条” 是什么含义？没理解；

是否可以理解为：每次对话中user字段就是传递的用户最新的一次提问， 然后assistant 字段传递的是历史消息，但是需要记着：assistant字段的最后一条为历史消息中的用户消息？ 是这个意思否？ </div>2023-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（1） 💬（2）<div>LangChain 作为LLM模型的应用开发框架，个人理解是致力于为模型落地提供技术层面的“一站式”解决方案。或者说是把大模型相关的技术集成和最佳流程实践，通过模块化、链式的方式，为应用开发者提供易用的脚手架。</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4b/63/e97ef435.jpg" width="30px"><span>DOOM</span> 👍（1） 💬（1）<div>LangChain提供一个抽象层，这样后期更换其他语言模型的话，就不用修改已经写好的应用代码逻辑</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（0） 💬（1）<div>import os
os.environ[&quot;OPENAI_API_KEY&quot;] = &#39;你的Open API Key&#39;
from langchain.llms import OpenAI
llm = OpenAI(  
    model=&quot;gpt-3.5-turbo-instruct&quot;,
    temperature=0.8,
    max_tokens=60,)
response = llm.predict(&quot;请给我的花店起个名&quot;)
print(response)  这个代码 在目前这个时间段已经运行不了啦，老师</div>2024-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/27/93/ade2062d.jpg" width="30px"><span>Coding</span> 👍（0） 💬（1）<div>老师，调用聊天模型，我理解应该是client.chat.completions.create，代码示例是不是少了个chat</div>2024-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/b2/91/cf0de36e.jpg" width="30px"><span>saltedfish</span> 👍（0） 💬（1）<div>gpt-3.5-turbo-instruct是chat模型不是text模型（可能是后来改的）</div>2024-04-19</li><br/><li><img src="" width="30px"><span>Geek_27bb04</span> 👍（0） 💬（1）<div>老师您好&#xff0c;我们想用langchain&#43;开源模型微调的方式&#xff0c;实现公司内私有数据的简单知识问答&#xff0c;请问langchain架构支持对接私有部署的模型吗&#xff0c;不是通过调用外部大模型API的方式</div>2024-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/88/b1/5718003f.jpg" width="30px"><span>神话</span> 👍（0） 💬（5）<div>现在openapi的账号不好申请，而且对ip有限制，可有其他替代方案？</div>2024-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/26/e0bd8d24.jpg" width="30px"><span>Crystal</span> 👍（0） 💬（2）<div>老师，有什么办法搞定openai充值</div>2024-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/28/cf/6fd2e10e.jpg" width="30px"><span>潮舀</span> 👍（0） 💬（1）<div>老师，刚学，有很多疑惑的地方没途径交流，您的微信加不了了，麻烦您加我一下拉我进一下交流群，我的微信是：15871350247</div>2024-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/60/4fa1f3bd.jpg" width="30px"><span>rs勿忘初心</span> 👍（0） 💬（1）<div>已经主动加不了老师微信了，显示被加次数太多，呜呜，老师方便的拉我进入下交流群：rs894568618，感谢</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/e9/f43781b3.jpg" width="30px"><span>Sandy</span> 👍（0） 💬（2）<div>老师你好 我是Azure Databricks中开发gpt的功能 怎么时候环境变量呢 十分感谢

#from langchain.chat_models import AzureChatOpenAI
# from langchain.llms import AzureOpenAI

# export OPENAI_API_TYPE=azure
# export OPENAI_API_VERSION=2023-05-15
# export OPENAI_API_BASE=https:&#47;&#47;vpa-openai-dev.openai.azure.com
# export OPENAI_API_KEY=mykey


# llm = AzureOpenAI(temperature=0, verbose=True)</div>2023-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/49/80/791d0f5e.jpg" width="30px"><span>不吃苦瓜</span> 👍（0） 💬（2）<div>老师，咱们这个课程主要是用哪个大模型来做的，我想我自己封装了星火大模型的接口，能放在咱们这个课程用吗，我之前照着官方文档学过一下langchain发现，他对于OpenAI的生态做的很好，但是其他的就不知道了</div>2023-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/1f/7551f182.jpg" width="30px"><span>卓丁</span> 👍（0） 💬（2）<div>response = openai.Completion.create(model=&quot;text-davinci-003&quot;, temperature=0.5, max_tokens=100, prompt=&quot;请给我的花店起个名&quot;)

print(response)

老师好，我运行了上面相同的例子，直接报：

{
  &quot;error&quot;: {
    &quot;code&quot;: &quot;DeploymentNotFound&quot;,
    &quot;message&quot;: &quot;The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.&quot;
  }
}

请问下，如何替换 ，才可以正常的run ？ </div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/47/3f/51708649.jpg" width="30px"><span>Blow</span> 👍（0） 💬（2）<div>有人入群了？哪位大哥能拉我入群</div>2023-11-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/270T9KAFd4oCxXXB1giaMDaJuTQVib8gPt77VkM5dbS3hW60kwTNnxMYpVibwWVdnASCrymBbwT7HI77URia0KUylw/132" width="30px"><span>Geek_7ee455</span> 👍（0） 💬（1）<div>1 langchain本身不仅仅对openai家族的支持,支持多种语言模型和数据源,封装了一些工具,能够减少我们的开发成本,但是感觉它的文档写的不是那么清晰,读起来有点费劲
顺便,老师, langchain能做对用户问题中的专有名词进行规范化处理吗</div>2023-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/47/3f/51708649.jpg" width="30px"><span>Blow</span> 👍（0） 💬（1）<div>老师，如何知道llm中OpenAI类剩下的方法，我想要获得模型返回的时间戳</div>2023-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/42/58/2286eca6.jpg" width="30px"><span>HdUIprince</span> 👍（0） 💬（2）<div>本地测试，基于Text的模型都会先输出一个 &quot;字&quot;，一个 &quot;\n&quot;，然后才是具体内容，请问下老师，前面的 &quot;字&quot; 的输出是模型对于问题的补全么

```plain
字

美花坊、芳草园、花舞香草、小花园、芬芳花店、花艺汇、花艺家、花艺坊、花艺汇、花艺园、花之恋
```</div>2023-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/22/559c2fdb.jpg" width="30px"><span>Mr.S</span> 👍（0） 💬（1）<div>问题1:
从解决问题的角度看，一个模型通常只能解决一个特定场景的问题，要解决复杂的业务问题，需要多模型协作，有LangChain这么一个开发工具，可以更方便的对接多模型，提升解决问题效率
从工程化角度看，LangChain这样的统一框架工具能提升开发效率</div>2023-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/7b/2d/6ba4a75a.jpg" width="30px"><span>🦅⃒⃘⃤ Shean</span> 👍（0） 💬（1）<div>老师，咱们用langchain哪个版本的？</div>2023-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/86/fb564a19.jpg" width="30px"><span>bluuus</span> 👍（0） 💬（2）<div>chat模型只能使用gpt-4吗？</div>2023-09-24</li><br/>
</ul>