你好，我是黄佳，欢迎来到LangChain实战课！

在默认情况下，无论是LLM还是代理都是无状态的，每次模型的调用都是独立于其他交互的。也就是说，我们每次通过API开始和大语言模型展开一次新的对话，它都不知道你其实昨天或者前天曾经和它聊过天了。

你肯定会说，不可能啊，每次和ChatGPT聊天的时候，ChatGPT明明白白地记得我之前交待过的事情。

![](https://static001.geekbang.org/resource/image/c9/97/c9907bc695521228cdfb5d3f75c13897.png?wh=588x593)

的确如此，ChatGPT之所以能够记得你之前说过的话，正是因为它使用了**记忆（Memory）机制**，记录了之前的对话上下文，并且把这个上下文作为提示的一部分，在最新的调用中传递给了模型。在聊天机器人的构建中，记忆机制非常重要。

![](https://static001.geekbang.org/resource/image/e2/de/e26993dd3957bfd2947424abb9de7cde.png?wh=1965x1363)

## 使用ConversationChain

不过，在开始介绍LangChain中记忆机制的具体实现之前，先重新看一下我们上一节课曾经见过的ConversationChain。

这个Chain最主要的特点是，它提供了包含AI 前缀和人类前缀的对话摘要格式，这个对话格式和记忆机制结合得非常紧密。

让我们看一个简单的示例，并打印出ConversationChain中的内置提示模板，你就会明白这个对话格式的意义了。

```plain
from langchain import OpenAI
from langchain.chains import ConversationChain

# 初始化大语言模型
llm = OpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo-instruct"
)

# 初始化对话链
conv_chain = ConversationChain(llm=llm)

# 打印对话的模板
print(conv_chain.prompt.template)
```
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（13） 💬（3）<div>我们可以通过源码来分析ConversationSummaryBufferMemory是如何实现长短期记忆的。首先要关注ConversationSummaryBufferMemory.save_context()方法，它将每轮对话的inputs和outputs成对加入memory，然后调用self.prune()方法。prune()方法会计算memory的当前token数，如果超过self.max_token_limit，则对超出的messages总结，调用的方法是self.predict_new_summary(pruned_memory, self.moving_summary_buffer)。总结时使用的PromptTemplate来自prompt.py的_DEFAULT_SUMMARIZER_TEMPLATE，_DEFAULT_SUMMARIZER_TEMPLATE的部分内容如下：
EXAMPLE
...
Current summary:
{summary}
New lines of conversation:
{new_lines}
也就是通过示例，让llm学习如何完成长期记忆的总结。

ConversationSummaryBufferMemory是在应用层平衡长短期记忆，我们也可以看看模型层是如何平衡长短期记忆的。RNN模型t时间步的隐藏层参数H_t计算公式为：H_t = phi(X_t*W_xh+H_(t-1)*W_hh+b_h)，X_t*W_xh表示短期记忆，H_(t-1)*W_hh表示长期记忆，平衡长短期记忆，就是给短期记忆和长期记忆加一个权重，来控制对整体记忆（H_t）的影响。现代循环神经网络GRU和LSTM的模型有区别，但是原理上都是为短期记忆和长期记忆加权重。</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（4） 💬（1）<div>github代码是不是没更新呢</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/7c/e91866cf.jpg" width="30px"><span>aloha66</span> 👍（1） 💬（2）<div>为什么我的ConversationSummaryBufferMemory没记住我昨天为什么要来买花。
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from util import base_url


# 创建大语言模型实例
llm = ChatOpenAI(temperature=0.5, base_url=base_url)


# 初始化对话链
conversation = ConversationChain(
    llm=llm, memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=300)
)


# 第一天的对话
# 回合1
result = conversation.invoke(&quot;我姐姐明天要过生日，我需要一束生日花束。&quot;)
print(&quot;回合1&quot;, result)
# 回合2
result = conversation.invoke(&quot;她喜欢粉色玫瑰，颜色是粉色的。&quot;)
# print(&quot;\n第二次对话后的记忆:\n&quot;, conversation.memory.buffer)
print(&quot;回合2&quot;, result)

# 第二天的对话
# 回合3
result = conversation.invoke(&quot;我又来了，还记得我昨天为什么要来买花吗？&quot;)
print(&quot;回合3&quot;, result)
# 回复
回合3 {&#39;input&#39;: &#39;我又来了，还记得我昨天为什么要来买花吗？&#39;, &#39;history&#39;: &#39;Human: 我姐姐明天要过生日，我需要一束生日花束。\nAI:  
哇，生日快乐给您的姐姐！您想要什么样的花束呢？玫瑰、郁金香、百合还是其他花卉？您可以选择她喜欢的颜色和花材，我可以帮您找到最合
适的花束。您知道她喜欢的花吗？\nHuman: 她喜欢粉色玫瑰，颜色是粉色的。\nAI: 粉色玫瑰是一个很浪漫的选择！我会帮您找到一束粉色玫 
瑰花束。您希望花束里还有其他花卉搭配吗？比如一些绿叶或者其他颜色的花朵？您还有其他要求吗？让我知道，我会为您找到完美的生日花束
。&#39;, &#39;response&#39;: &#39;抱歉，我无法记住之前的对话内容。您可以告诉我您昨天为什么要来买花吗？我会尽力帮助您找到合适的花束。&#39;} </div>2024-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/5c/8a/244128ff.jpg" width="30px"><span>Webber</span> 👍（1） 💬（2）<div>老师，ConversationChain中可以加入memory机制，但是agents中怎么加入memory机制中呢。initialize_agent函数中的参数没有Chain类型，只是LLM类型。</div>2023-10-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YflLdCdbUAkfr9LPzF50EibDrMxBibPicQ5NNAETaPP0ytTmuR3h6QNichDMhDbR2XelSIXpOrPwbiaHgBkMJYOeULA/132" width="30px"><span>抽象派</span> 👍（1） 💬（1）<div>如果对话的内容跨度比较广，是不是总结出来的就不太准确了？</div>2023-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（0） 💬（1）<div>老师，问个题外话

说到记忆，我们人类的大脑也不是无穷无尽的。所以说，有的时候事情太多，我们只能把有些遥远的记忆抹掉。毕竟，最新的经历最鲜活，也最重要。

你在文中说人类的记忆不是无穷无尽的，我们只能把遥远的记忆抹掉。但是我觉得人类的记忆可以认为是无穷无尽的，因为我们几乎不可能耗尽我们的记忆空间，大脑还有极强的可塑性，而且我们人类也没办法直接抹去遥远的记忆吧。人类会对于印象深刻的记忆或者经常重复的记忆保留很长时间，并不仅仅与时间有关，如果仅与时间有关的话，我们学习的意义就没了啊，因为我们就只记得刚学过的东西了🤔</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（0） 💬（3）<div>“汇总”的理念跟“摘要”的理念是一致的吗？所以是不是实际应用中，专门的“汇总”模型或许价格比Completions 和 chat  模型更便宜？</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（1）<div>老师，可以认为不同的chain都对应一个prompt，约定了很多 变量，memory 这些机制都预定了自己可以提供哪些变量嘛？
</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（2） 💬（0）<div>第10讲打卡~
对于记忆系统，可以尝试结合ConversationSummaryBufferMemory+RAG的方案，即短期全量记忆+长期摘要记忆+向量数据库辅助记忆，这样的记忆方式可能更好地平衡性能、准确性和Token成本</div>2024-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/38/8e05dac1.jpg" width="30px"><span>王凯</span> 👍（2） 💬（0）<div>langchian里的memory记忆机制面对多用户同时提问，是怎么区分不同的用户的历史记录的？</div>2024-04-17</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>用以下通义千问代码代替OpenAI ，学习课程代码。
旧代码：
# 初始化大语言模型
 llm = OpenAI(
     temperature=0.5,
     model_name=&quot;text-davinci-003&quot;
 )

新代码：
from langchain_openai import ChatOpenAI
# 初始化大语言模型
llm = ChatOpenAI(
    api_key=&quot;ｘｘｘｘ&quot;, 　# 此处用您的DASHSCOPE_API_KEY进行替换
    base_url=&quot;https:&#47;&#47;dashscope.aliyuncs.com&#47;compatible-mode&#47;v1&quot;, # 填写DashScope base_url
    model=&quot;qwen-plus&quot;
    )

但是使用ConversationSummaryBufferMemory 时，出现NotImplementedError: get_num_tokens_from_messages() is not presently implemented for model cl100k_base.  搜索了很多资料，没有找到简单的替代方法。可能是阿里云的某些特定模型不支持某些功能。</div>2024-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/0e/4b/ff4a21de.jpg" width="30px"><span>刘双荣</span> 👍（0） 💬（0）<div>提到了4种会义记忆模式，</div>2024-09-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rURvBicplInVqwb9rX21a4IkcKkITIGIo7GE1Tcp3WWU49QtwV53qY8qCKAIpS6x68UmH4STfEcFDJddffGC7lw/132" width="30px"><span>onemao</span> 👍（0） 💬（0）<div>使用ConversationSummaryMemory, 后面AI的回复姐姐编程妹妹了😄</div>2024-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/59/01/b8709bb9.jpg" width="30px"><span>大师兄</span> 👍（0） 💬（1）<div>请问ConversationSummaryBufferMemory在超过max_token_limit以后是将所有内容进行总结还是将超过max_token_limit的内容进行总结？</div>2024-03-15</li><br/>
</ul>