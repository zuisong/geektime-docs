你好，我是徐文浩。

在[第 11 讲](https://time.geekbang.org/column/article/646363)里，我为你讲解了如何把各种资料的内容向量化，然后通过llama-index建立对应的索引，实现对我们自己的文本资料的问答。而在过去的3讲里面，我们又深入了解了如何使用Langchain。Langchain能够便于我们把AI对语言的理解和组织能力、外部各种资料或者SaaS的API，以及你自己撰写的代码整合到一起来。通过对这些能力的整合，我们就可以通过自然语言完成更加复杂的任务了，而不仅仅只是能闲聊。

不过，到目前为止。我们所有基于ChatGPT的应用，基本都是“单项技能”，比如前面关于“藤野先生”的问题，或者[上一讲](https://time.geekbang.org/column/article/648167)里查询最新的天气或者通过Python算算术。本质上都是限制AI只针对我们预先索引的数据，或者实时搜索的数据进行回答。

## 支持多种单项能力，让AI做个选择题

但是，如果我们真的想要做一个能跑在生产环境上的AI聊天机器人，我们需要的不只一个单项技能。它应该针对你自己的数据有很多个不同的“单项技能”，就拿我比较熟悉的电商领域来说，我们至少需要这样三个技能。

1. 我们需要一个“导购咨询”的单项技能，能够查询自己商品库里的商品信息为用户做导购和推荐。
2. 然后需要一个“售中咨询”的单项技能，能够查询订单的物流轨迹，对买了东西还没有收到货的用户给出安抚和回复。
3. 最后还需要一个“FAQ”的单项技能，能够把整个电商网站的FAQ索引起来，当用户问到退货政策、运费、支付方式等问题的时候，我们可以从FAQ里面拿到对应的答案，回复给用户。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/99/5bf198e3.jpg" width="30px"><span>孟健</span> 👍（8） 💬（3）<div>最近的autogpt，agentgpt是不是都是这个思路</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（5） 💬（1）<div>老师,这是我让让用中文回答的代码,你看下这样对不对? 或是说还有更加简单的方法?


```python
from langchain import LLMChain
from langchain.agents import Tool, AgentExecutor, ZeroShotAgent
import os


from langchain.chat_models import ChatOpenAI


def search_order(input: str) -&gt; str:
    return &quot;订单状态：已发货；发货日期：2023-01-01；预计送达时间：2023-01-10&quot;


def recommend_product(input: str) -&gt; str:
    return &quot;红色连衣裙&quot;


def faq(intput: str) -&gt; str:
    return &quot;7天无理由退货&quot;


tools = [
    Tool(
        name=&quot;Search Order&quot;, func=search_order,
        description=&quot;useful for when you need to answer questions about customers orders&quot;  # 当您需要回答有关客户订单的问题时很有用
    ),
    Tool(name=&quot;Recommend Product&quot;, func=recommend_product,
         description=&quot;useful for when you need to answer questions about product recommendations&quot;  # 你需要回答关于产品推荐的问题时很有用
         ),
    Tool(name=&quot;FAQ&quot;, func=faq,
         description=&quot;useful for when you need to answer questions about shopping policies, like return policy, shipping policy, etc.&quot;
         # 当您需要回答关于购物政策的问题时，例如退货政策、运输政策等，这将非常有用。
         )
]

PREFIX = &quot;&quot;&quot;Answer the following questions as best you can. You have access to the following tools: (所有的回答都用中文返回)&quot;&quot;&quot;

prompt_ = ZeroShotAgent.create_prompt(
    tools,
    prefix=PREFIX,
    input_variables=[&quot;input&quot;, &quot;agent_scratchpad&quot;]
)

llm_chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=prompt_)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)

agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
result = agent_chain.run(&quot;我有一张订单，订单号是 2022ABCDE，一直没有收到，能麻烦帮我查一下吗？&quot;)
print(result)
```
</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/84/1c56c8a5.jpg" width="30px"><span>Leo</span> 👍（3） 💬（2）<div>老师，我想基于这个做一个对人的检索，用户输入姓名、年龄、性别等能找到相关的人，这个用embedding index能实现吗？或者有其他思路可以实现吗？求解答</div>2023-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/2a/b3/81b09345.jpg" width="30px"><span>李蕾</span> 👍（3） 💬（1）<div>关于老师思考题的第一个问题，经过自己的尝试，比较简单的方式是在Template中明确要求必须用中文返回即可。
answer_order_info = PromptTemplate(    template=&quot;请把下面的订单信息用中文回复给用户： \n\n {order}?&quot;, input_variables=[&quot;order&quot;])
我的第一想法和Geek_4ec46c一样，也是尝试着在Prompt中规定返回必须是中文，但是没有生效，可能是自己当前的功力不够导致的bug，哈哈</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/71/25/e9bad0b3.jpg" width="30px"><span>树静风止</span> 👍（3） 💬（1）<div>这么强大超期的课程，人怎么这么少呢</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a6/76/b2a1065a.jpg" width="30px"><span>智能</span> 👍（3） 💬（1）<div>所以这里chatGPT其实相当于一个调度者？识别用户意图然后调用其他应用</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/ad/6ee2b7cb.jpg" width="30px"><span>Jacob.C</span> 👍（2） 💬（1）<div>老师，请问 agent 的 一个 tool如果需要 llm 做两件事再回来，应该怎么玩呢？</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e3/81/25bb6ba7.jpg" width="30px"><span>～鹏～</span> 👍（1） 💬（1）<div>请问下我用chatglm我试了下上面写的agent例子，发现不支持，这个只能openai可以用吗</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/ad/6ee2b7cb.jpg" width="30px"><span>Jacob.C</span> 👍（1） 💬（1）<div>解决的方法也不复杂，我们只需要调整一下 search_order 这个 Tool 的提示语。通过这个提示语，Agent 会知道，这个工具就应该在找不到订单的时候，告诉用户找不到订单或者请它再次确认。这个时候，它就会根据这个答案去回复用户。下面是对应修改运行后的结果。

老师这里两段代码实在看不出来修改了啥，麻烦看出来的人说明一下！</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/34/3f/4b6cd370.jpg" width="30px"><span>Viktor</span> 👍（1） 💬（1）<div>如果按照这个思路，我们还可以添加更多的功能，比如更细致的订单查询，商品咨询，修改收货地址等。只是这些功能如果每个都独立开发还是需要花费很多时间，所以这个时候就需要开发一个框架的工作流，在这个框架下面更方便做功能集成。点赞👍。</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/f2/db90fa96.jpg" width="30px"><span>Oli张帆</span> 👍（1） 💬（1）<div>请教老师，第一步的Intent Detection，是不是算是zero shot的？在这种情况下，如果我给出几个输出的例子，强化一下它的输出形式，会不会效果更好？</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/de/6f2ab154.jpg" width="30px"><span>风</span> 👍（0） 💬（2）<div>你好，我尝试使用ChatGLM实现这一节的内容，但是效果很差，经常没办法像OpenAI那样进行“思考”，最后返回正常的结果。有什么好的办法吗？或者，有什么其他可用的中文LLM模型可以使用agent和tool实现类似的功能。</div>2023-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/20/07/80337e76.jpg" width="30px"><span>江湖中人</span> 👍（0） 💬（2）<div>老师，请教一下，如果想做一个特定行业的客服机器人，有一些私有的数据需要喂给AI，是有现成的东西可以用，还是利用我们课程学的东西去开发训练，可以大致梳理一下流程吗？很多有这种需求的但是对技术并不了解的人，他们要怎么做呢？</div>2023-04-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTISHN4HwTsOicDUzB1jyzlxzriaI3S7tAfoPzicSfuTbxLxRjkCic2eBwRWxJTrwTpiaYP8Hg8vqWgNE2w/132" width="30px"><span>Geek_3d7708</span> 👍（0） 💬（1）<div>1、 LLM 换成了 ChatOpenAI，不知道怎么 回答过程都是英文了；
2、converstional-react-description  采用这个，回答就不是从知识库了。 比如我用藤野显示，问鲁迅老师是谁？zero-shot-react-description 的时候，是藤野先生，但是换成converstional-react-description 就变成 陈寅格，不知道哪来的。</div>2023-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/d4/97/2f01be06.jpg" width="30px"><span>xianbin.yang</span> 👍（0） 💬（1）<div>老师，很喜欢您这个专栏，您除了这个专栏，还有其他的博客、社群或者知识星球吗？</div>2023-04-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTISHN4HwTsOicDUzB1jyzlxzriaI3S7tAfoPzicSfuTbxLxRjkCic2eBwRWxJTrwTpiaYP8Hg8vqWgNE2w/132" width="30px"><span>Geek_3d7708</span> 👍（0） 💬（1）<div>EntityMemory  每个不同的客户，保存的数据会不会冲突？ 比如A的数据，B也访问到了？</div>2023-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（1）<div>解决的方法也不复杂，我们只需要调整一下 search_order 这个 Tool 的提示语。

在这个位置的代码和上面的代码都是一样的,好像没有任何调整....... ( 老师是你没改好? ) 
</div>2023-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/c7/f57dadb9.jpg" width="30px"><span>张弛</span> 👍（0） 💬（1）<div>question3 = &quot;你们的退货政策是怎么样的？
&quot;answer3 = conversation_agent.run(question3)
print(answer2)
这段代码的第三行，print的参数错了，应该是answer3</div>2023-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/c7/f57dadb9.jpg" width="30px"><span>张弛</span> 👍（0） 💬（1）<div>question1 = &quot;我有一张订单，一直没有收到，能麻烦帮我查一下吗？&quot;
answer1 = conversation_agent.run(question)
print(answer1)
这段代码的第二行的参数填错了，应该是question1</div>2023-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/c7/f57dadb9.jpg" width="30px"><span>张弛</span> 👍（0） 💬（1）<div>老师您好！本次案例中的ecommerce_products.csv文件好像并未上传到github，麻烦补充，谢谢！</div>2023-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（1）<div>老师,你里面提到的faq的txt可以下载,或是给我们看下是什么格式吗?这样方便我们手动去跑一下代码</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/19/0a3fe8c1.jpg" width="30px"><span>Evan</span> 👍（0） 💬（1）<div>最简单的办法是：再调用一次ChatGPT 就可以翻译一下如何？ 
但是老师肯定不是这样想得，
是否能自定义回复内容</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（1）<div>老师，改成中文是不是要在每个tool的描述下说明要用中文回答？还是说要直接改他的原始内置指令？</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/f2/db90fa96.jpg" width="30px"><span>Oli张帆</span> 👍（0） 💬（1）<div>在第一步检测用户的意图的时候，是否也可以直接提供一些“捷径”，让用户明确自己的目的，能省去让AI去检测意图这一步。比如，客户点击我要查询订单，就直接问他订单号，然后完成查询。客户点击“我要查询新闻”，就帮助他&#47;她创建query，完成查询。客户点击“用苏格拉底式诘问帮我理解这篇文章”，就直接调用相关的Agent和Context来完成多轮对话。</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/0d/06/970cc957.jpg" width="30px"><span>Charles</span> 👍（2） 💬（5）<div>当 llm使用ChatOpenAI和agent=&quot;conversational-react-description&quot;，会报错。
File &quot;&#47;Users&#47;XXX&#47;opt&#47;anaconda3&#47;envs&#47;openai&#47;lib&#47;python3.10&#47;site-packages&#47;langchain&#47;agents&#47;conversational&#47;output_parser.py&quot;, line 23, in parse
    raise OutputParserException(f&quot;Could not parse LLM output: `{text}`&quot;)
langchain.schema.OutputParserException: Could not parse LLM output: `Do I need to use a tool? No`

使用agent=&quot;zero-shot-react-description&quot; 时，不会报错

为什么呢？</div>2023-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/65/22a37a8e.jpg" width="30px"><span>Yezhiwei</span> 👍（2） 💬（0）<div>谢谢老师哈，这篇文章牛皮plus</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/89/da/136cdca6.jpg" width="30px"><span>陈斌</span> 👍（1） 💬（0）<div>Gpt 只是一个模型，在应用过程中关键的是去体会跟 gpt 交互时思考应该让 gpt采用什么样的策略回答问题，就是什么样的情况下用什么套话或者话术来回答。鉴别的工具和套话的模板就需要我们去自己开发。因为开放式问答的场景跟实际情况很不一样，虽然 gpt 可以节省人工，但毕竟跟人与人的交流不一样，对气氛的把握也没有那么精准。所以 gpt 的回答也不是万能，在接收客户提问的时候，要时刻注意对客户的情绪进行分析，如果发现客户负面情绪极度飙升，那么应该尽快切换回人工模式，而不能等待关键词的触发。</div>2023-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/c6/441acafd.jpg" width="30px"><span>海边停车</span> 👍（0） 💬（0）<div>设置了return_direct = True，怎么流式返回Tool的observation？</div>2023-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/24/f2dfbbec.jpg" width="30px"><span>liuy1226</span> 👍（0） 💬（0）<div>question3 = &quot;你们的退货政策是怎么样的？&quot;
answer3 = conversation_agent.run(question3)
print(answer3)执行后出错，这个是什么原因OutputParserException: Could not parse LLM output: `Do I need to use a tool? No`</div>2023-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/24/f2dfbbec.jpg" width="30px"><span>liuy1226</span> 👍（0） 💬（1）<div>这个agent和把多个文档放到一个向量库中问答有什么区别</div>2023-09-20</li><br/>
</ul>