你好，我是徐文浩。

在过去的两讲里，我们深入了解了Langchain的第一个核心功能，也就是LLMChain。 LLMChain能够帮助我们链式地调用一系列命令，这里面既包含直接调用OpenAI的API，也包括调用其他外部接口，或者自己实现的Python代码。但是这一连串的调用，还只是完成一个小任务。我们很多时候还是希望用一个互动聊天的过程，来完成整个任务。

所以LangChain并不是只有链式调用这样一个核心功能，它还封装了很多其他能力，来方便我们开发AI应用。比如，让AI能够拥有“记忆力”，也就是记住我们聊天上下文的能力。不知道你还记不记得，我们在[第 6 讲](https://time.geekbang.org/column/article/643915)里做的聊天机器人。在那个里面，为了能够让ChatGPT知道整个聊天的上下文，我们需要把历史的对话记录都传给它。但是，因为能够接收的Token数量有上限，所以我们只能设定一个参数，只保留最后几轮对话。我们最后把这个功能，抽象成了一个Conversation类。

```python
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

class Conversation:
    def __init__(self, prompt, num_of_round):
        self.prompt = prompt
        self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({"role": "system", "content": self.prompt})

    def ask(self, question):
        try:
            self.messages.append({"role": "user", "content": question})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                temperature=0.5,
                max_tokens=2048,
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        message = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": message})

        if len(self.messages) > self.num_of_round*2 + 1:
            del self.messages[1:3] //Remove the first round conversation left.
        return message

```
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/c7/f57dadb9.jpg" width="30px"><span>张弛</span> 👍（4） 💬（1）<div>老师讲的太好了，通过对AI的能力探索，感觉有了跟自己业务结合的空间，但是如果需要身边的朋友使用的话，还是需要封装成网页或者app，而之前例子里面的HuggingFace国内访问还是挺慢的，能否介绍一下如果就是想把实战提高篇里的chatbot做一些定制化，封装为网页给别人在国内使用，推荐使用什么方式部署（例如腾讯云硅谷？），谢谢。</div>2023-04-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKDdkdC6WfWDyETmkUwuhMic8ytESib2fYGSssBjly3vxjdFu9xd24qDehqDKjIlktlhOAuicmHf8YvA/132" width="30px"><span>Geek_429477</span> 👍（2） 💬（3）<div>每天第一个追更. 请问一下大佬:
比如一个客服机器人,卖很多种类的商品,按照大佬之前的文章思路,QA问题集如下
Q:你们卖哪些产品
A:图书,玩具,衣服.......(很多字)

一个用户问,你们卖电子产品吗?
如果先搜索再提示,answer的字数太多,造成token不够,该怎么解决</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/f2/db90fa96.jpg" width="30px"><span>Oli张帆</span> 👍（2） 💬（1）<div>Langchain确实是非常有用的利器，虽然我目前的项目使用NodeJS，但是里面的很多思路非常值得借鉴。</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/aa/33/5e063968.jpg" width="30px"><span>Jelly</span> 👍（1） 💬（2）<div>请问老师，每个用户单独的内存会话怎么做？需要用其他数据库存储起来？</div>2023-04-23</li><br/><li><img src="" width="30px"><span>Geek_053159</span> 👍（1） 💬（1）<div>老师 在chatgpt 界面使用它时 是不是也用到了memory呢 每次我们的问话都会全部发送给它 当超过token数量时 chatGPT会自动总结之前的会话内容吗 还是需要我们提示它来总结 然后再把总结和新的问话结合起来发给它</div>2023-04-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIkqxY5Wm9DNVqtTKwF9kCGsveCoz07n1GgZ0o4vA9Po8qS9J2uBdDGMh5TPRCDU2W9NJbFtQrYuA/132" width="30px"><span>hyetry</span> 👍（1） 💬（1）<div>老师，有文本摘要对应的替换推荐模型吗？</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/56/b3/29c814af.jpg" width="30px"><span>君为</span> 👍（1） 💬（2）<div>老师你好，客服处理用户的问题很多都是一系列任务，有时还需要客服主动给用户发消息。比如用户要退货，需要提供手机号，订单号等信息，用户找不到订单号在哪需要一步步指导用户然后再做一些列操作。

请问老师识别用户意图，提取关键信息后，如何让ChatGPT进入设定的工作流，最终处理好用户的问题？</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（0） 💬（1）<div>使用 LangChain 中的 KnowledgeGraphMemory，检测其处理对话信息的能力。

from langchain.memory import ConversationKGMemory # 知识图谱记忆
llm = OpenAI(temperature=0)
memory=ConversationKGMemory(llm=llm)
template = &quot;&quot;&quot;The following is a conversation between a human and an AI.
The AI provides lots of specific details from its context. 
AI uses all the information contained in &quot;Related Information&quot;, &quot;Current Conversation&quot; and &quot;Context&quot;
If the AI does not know the answer to a question, it truthfully says it does not know，and does not hallucinate.
answer in 20 word.

对话如下
第一轮
Q1 (喂给了AI 这些信息，牵扯到几个方向，试AI 如何提取并处理这些信息)
input=&quot;I am James and I&#39;m helping Will. He&#39;s an engineer working in IBM&#39;s electronics department. He encountered a problem in the &#39;Knowledge Graph Memory&#39; project&quot;
A1
&gt; Finished chain.
&quot; Hi James, I understand that Will is having difficulty with the &#39;Knowledge Graph Memory&#39; project. I&#39;m not familiar with this project, but I can help you find the resources you need to solve the problem.&quot;
(回答中AI 分出了James 和 Will，其它的大差不差。)

第二轮对话
Q2
input=&quot;What do you know about Will?&quot;
A2
&gt; Finished chain.
&quot; Will is an engineer working in IBM&#39;s electronics department. He is currently working on a Knowledge Graph Memory project and has encountered a problem.&quot;
(AI 充分利用了在第一轮对话中得到的有关Will 的信息。)

第三轮对话
A3
input=&quot;What do you know about me?&quot;
Q3
&gt; Finished chain.
&quot; I know that you are talking to me right now and that you asked me a question about Will. I also know that Will is an engineer working in IBM&#39;s electronics department and is working on the Knowledge Graph Memory project.&quot;
(AI 没有捕捉到 me, I, James 之间的关系，尽管它用了Hi James, )

第四轮对话
A4 (继续追问上轮中出现的漏洞)
input=&quot;What is my name?&quot;
Q4
&gt; Finished chain.
&quot;Your name is John Smith.&quot;
(AI 彻底错了)

结果有点意外，是算法有错还是参数设置有待改进? 
共指消解(coreference&#47;entity resolution)在知识图谱记忆中是最基本的方法，整合同一实体的不同称谓。</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/19/0a3fe8c1.jpg" width="30px"><span>Evan</span> 👍（0） 💬（2）<div>from langchain.memory import ConversationSummaryMemory. 
引入这个的时候报错</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/89/da/136cdca6.jpg" width="30px"><span>陈斌</span> 👍（1） 💬（0）<div>这一章节讲了如何利用外部的存储去实现上下文及关键信息的缓存，老师里面提到的一些点都是在应用 gpt 实现过程中对成本和开销需要考虑的问题，非常有实用性。
尤其是关键信息，主要是对场景下问题回答的约束，比如在一个电商网站的客服机器人，问它怎么做饭的，是可以拒绝回答的。这里的模型是否需要重新训练，还是可以利用 gpt 判断问题与场景的相关性，再利用提示语让 gpt 给出一个委婉回答。</div>2023-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/a5/56/b3cf71a9.jpg" width="30px"><span>Penguin Shi</span> 👍（1） 💬（0）<div>原文：Langchain 里面还提供了一个 KnowledgeGraphMemory，你能不能去试着用一下，看看它能在什么样的场景下帮你解决问题？
更新：Conversation Knowledge Graph Memory，https:&#47;&#47;python.langchain.com&#47;docs&#47;modules&#47;memory&#47;types&#47;kg</div>2023-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/81/96f656ef.jpg" width="30px"><span>杨逸林</span> 👍（0） 💬（0）<div>可不可以这样，让一些总结类的活丢给本地 RTX 4090 可以部署的 BlueLM，然后把这一轮的对话和总结的内容丢给 ChatGPT，这样是不是更省 Token。简单的活给本地的部署的完成，复杂的丢给 ChatGPT4。就是不知道能不能做到。</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/d0/7a595383.jpg" width="30px"><span>l_j_dota_1111</span> 👍（0） 💬（0）<div>你好，请问如果既要求有总结，也要求有实体提取，又要求记住上下文，是用哪个chain呢？还有就是还想通过矢量数据库查询出信息就行参考文档，怎么和这些chain结合呢</div>2023-12-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLH5MBWgqEDFiaIpRACgwibh4DGhRgvTRCGpa713rH0c3mI26kj6Ft2jTUCFvxlGdBrtLh96EKmY7yg/132" width="30px"><span>Aurore</span> 👍（0） 💬（0）<div>在最后llm_chain.predict(human_input=&quot;你是谁？&quot;)并没有输入chat_history来替换对应的占位符，不会出错吗</div>2023-11-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLH5MBWgqEDFiaIpRACgwibh4DGhRgvTRCGpa713rH0c3mI26kj6Ft2jTUCFvxlGdBrtLh96EKmY7yg/132" width="30px"><span>Aurore</span> 👍（0） 💬（0）<div>请教一下。滑窗memory中，llm_chain.predict(human_input=&quot;你是谁？&quot;)。没有输入chat_history没有问题吗？</div>2023-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/36/b4a4e6fb.jpg" width="30px"><span>Edon du</span> 👍（0） 💬（0）<div>老师，搭建外部资料索引的QA回答客服，如何使用memory功能呀?
我试了了langchain的相关memory，都不太理想，只能保存历史会话，但是真正询问时，并不能正确回答出「我第一句说的什么」类似的问题</div>2023-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/0d/06/970cc957.jpg" width="30px"><span>Charles</span> 👍（0） 💬（1）<div>使用ConversationEntityMemory的进行redis缓存时报错：redis.exceptions.ResponseError: unknown command `GETEX`, with args beginning with: `memory_store:default:Zhang Laosan`, `EX`, `259200`, 
这个有人遇到过吗，怎么解决？</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d5/14/520e2bc6.jpg" width="30px"><span>王乔</span> 👍（0） 💬（0）<div>请问老师，如果要AI读很长的文档怎么写? 现在文章过长直接就报错了</div>2023-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（0）<div>来了</div>2023-04-13</li><br/>
</ul>