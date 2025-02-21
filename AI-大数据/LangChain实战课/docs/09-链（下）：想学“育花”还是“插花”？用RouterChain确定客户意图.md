你好，我是黄佳。欢迎来到LangChain实战课！

上一节课中，我带着你学习了Chain的基本概念，还使用了LLMChain和SequencialChain，这一节课，我们再来看看其他类型的一些Chain的用法。

## 任务设定

首先，还是先看一下今天要完成一个什么样的任务。

这里假设咱们的鲜花运营智能客服ChatBot通常会接到两大类问题。

1. **鲜花养护**（保持花的健康、如何浇水、施肥等）
2. **鲜花装饰**（如何搭配花、如何装饰场地等）

你的需求是，**如果接到的是第一类问题，你要给ChatBot A指示；如果接到第二类的问题，你要给ChatBot B指示**。

![](https://static001.geekbang.org/resource/image/d8/59/d8491e696c03f49a331c94e31d20e559.jpg?wh=1490x1077)

我们可以根据这两个场景来构建两个不同的目标链。遇到不同类型的问题，LangChain会通过RouterChain来自动引导大语言模型选择不同的模板。

当然我们的运营过程会遇到更多种类的问题，你只需要通过同样的方法扩充逻辑即可。

## 整体框架

RouterChain，也叫路由链，能动态选择用于给定输入的下一个链。我们会根据用户的问题内容，首先使用路由器链确定问题更适合哪个处理模板，然后将问题发送到该处理模板进行回答。如果问题不适合任何已定义的处理模板，它会被发送到默认链。

在这里，我们会用LLMRouterChain和MultiPromptChain（也是一种路由链）组合实现路由功能，该MultiPromptChain会调用LLMRouterChain选择与给定问题最相关的提示，然后使用该提示回答问题。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（19） 💬（1）<div>ConversationChain和LLMChain的区别在于，ConversationChain有memory成员变量，能保留对话上下文，而LLMChain不行。在源码上，跟踪ConversationBufferMemory.load_memory_variables()可知，对话上下文会作为inputs的一部分传入PromptTemplate，成为llm的提示词。</div>2023-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/03/660c8a3c.jpg" width="30px"><span>阶前梧叶</span> 👍（5） 💬（1）<div>在这种路由链中，返回的数据也想做结构化json解析，那最终llm返回的结果，如何去确定是哪个chain返回的？继而选择对应的parser处理</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/e3/c49aa508.jpg" width="30px"><span>鲸鱼</span> 👍（4） 💬（1）<div>我发现使用MultiPromptChain.from_prompts方法会更简洁，其内部实现就是老师上面列出的内容类似
flower_care_template = &quot;&quot;&quot;
你是一个经验丰富的园丁，擅长解答关于养花育花的问题。
下面是需要你来回答的问题:
{input}&quot;&quot;&quot;
flower_deco_template = &quot;&quot;&quot;
你是一位网红插花大师，擅长解答关于鲜花装饰的问题。
下面是需要你来回答的问题:
{input}&quot;&quot;&quot;
prompt_infos = [
    {
        &#39;name&#39;: &#39;flower_care&#39;,
        &#39;description&#39;: &#39;适合回答关于鲜花护理的问题&#39;,
        &#39;prompt_template&#39;: flower_care_template,
    },
    {
        &#39;name&#39;: &#39;flower_decoration&#39;,
        &#39;description&#39;: &#39;适合回答关于鲜花装饰的问题&#39;,
        &#39;prompt_template&#39;: flower_care_template,
    },
]

llm = OpenAI()
chain = MultiPromptChain.from_prompts(llm=llm, prompt_infos=prompt_infos, verbose=True)
print(chain.run(&quot;如何为玫瑰浇水？&quot;))</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/bb/7d/26340713.jpg" width="30px"><span>黄振宇</span> 👍（3） 💬（1）<div>感觉router_chain是一个agent了，只不过agent调用的是不同的tool，router_chain调用的是其他的大模型LLM</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（2） 💬（1）<div>打卡 mark！课跟上了，代码还没跟上。chains 的理念算不算就是利用LLM来驱动LLM？</div>2023-09-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/hllDt1dmuR6iciaahutPe9NjOic5OPMc7fbTysLTn8wgCSPW3zjYvd5rYDWBwQkSmqfsFntK12fLmam63FWpMklfg/132" width="30px"><span>dydcm</span> 👍（0） 💬（1）<div>老师您好，我跑样例的时候一直报一个错，能麻烦帮忙看下原因吗？报错如下：

The above exception was the direct cause of the following exception:
。。。

 File &quot;&#47;Library&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.12&#47;lib&#47;python3.12&#47;site-packages&#47;langchain&#47;utils&#47;__init__.py&quot;, line 15, in &lt;module&gt;
    from langchain.utils.math import cosine_similarity, cosine_similarity_top_k
  File &quot;&#47;Library&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.12&#47;lib&#47;python3.12&#47;site-packages&#47;langchain&#47;utils&#47;math.py&quot;, line 5, in &lt;module&gt;
    import numpy as np
  File &quot;&#47;Library&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.12&#47;lib&#47;python3.12&#47;site-packages&#47;numpy&#47;__init__.py&quot;, line 135, in &lt;module&gt;
    raise ImportError(msg) from e
ImportError: Error importing numpy: you should not try to import numpy from
        its source directory; please exit the numpy source tree, and relaunch
        your python interpreter from there.

  </div>2023-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/8c/791d0f5e.jpg" width="30px"><span>SH</span> 👍（0） 💬（1）<div>这节里面的问题，如果使用 当前的 ChatGPT 我们如果直接向他提问的时候，他的内部是否已经帮助我调整好了相关的提示模版，通过相关的链 来回答相关的问题呢？  

实际测试了一下，没有提示模板问，与加了提示模板（告诉他是个专门），两种方式输出的确会有些差异；</div>2023-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b4/3a/02ea71fa.jpg" width="30px"><span>sunny</span> 👍（0） 💬（4）<div>文章中的这一段话：
（RouterChain，也叫路由链，能动态选择用于给定输入的下一个链。我们会根据用户的问题内容，首先使用路由器链确定问题更适合哪个处理模板，然后将问题发送到该处理模板进行回答。如果问题不适合任何已定义的处理模板，它会被发送到默认链。）
我的疑问是：这里指路由链是能自动推理出用户意图，进而选择对应意图所要走的任务处理目标链吗；不需要通过写prompt+用户输入送入到大模型让大模型进行自动推理做选择题输出意图吗？
（比如写个prompt:
请理解这一段话{变量=用户输入},判断这段话是想进行[鲜花养护]还是[鲜花培育];
##若是鲜花养护请输出&quot;A&quot;,若是鲜花培育输出”B“）
这样得到到了A或B判断出了用户意图走哪个目标链</div>2023-10-16</li><br/><li><img src="" width="30px"><span>Geek_19a2eb</span> 👍（0） 💬（2）<div>就是当输入的内容匹配不上其他的链的时候到默认路由这报错  其他的链都是正常的  报错信息如下，麻烦老师帮忙看下 刚入门的小白，多多理解：OutputParserException: Parsing text
```json
{
    &quot;destination&quot;: &quot;DEFAULT&quot;,
    &quot;next_inputs&quot;: &quot;如何考入哈佛大学?&quot;
}
 raised following error:
Got invalid JSON object. Error: Expecting value: line 1 column 1 (char 0)</div>2023-10-16</li><br/><li><img src="" width="30px"><span>Geek_19a2eb</span> 👍（0） 💬（1）<div>老师您好 我运行到print(chain.run(“如何考入哈佛大学？”))的时候报错  能给看下是啥原因吗  报错如下：
OutputParserException: Parsing text
```json
{
    &quot;destination&quot;: &quot;DEFAULT&quot;,
    &quot;next_inputs&quot;: &quot;如何考入哈佛大学?&quot;
}
 raised following error:
Got invalid JSON object. Error: Expecting value: line 1 column 1 (char 0)</div>2023-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/aa/a2/c7a3758d.jpg" width="30px"><span>漏网之渔</span> 👍（0） 💬（1）<div>RouterChain中每个分支chain的输入参数要求是相同的么，可以使用不同数量的参数么</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/9f/0c/8484f8b1.jpg" width="30px"><span>夏落de烦恼</span> 👍（0） 💬（1）<div>langchain有集成文心一言么？这个案例能用在文心一言上么？</div>2023-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/5b/caacc46f.jpg" width="30px"><span>zhouqin</span> 👍（0） 💬（1）<div>建议有开发经验的同学，先通过gpt把作者文章核心点精炼出来。然后用作者通过LangChain模板跑出的提示词，通过gpt或者claude做验证。多跑几遍就能感觉到大模型的思维方式。最后再去看代码。事半功倍、、：》</div>2023-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/8d/9a/6c9a252e.jpg" width="30px"><span>Geek_7ca963</span> 👍（0） 💬（1）<div>老师，Agent 和 Chain 到底有啥区别 ？ chain 似乎也可以做 act，甚至判断用途</div>2023-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/5c/8a/244128ff.jpg" width="30px"><span>Webber</span> 👍（0） 💬（2）<div>老师啥时候更新agent的内容啊，我在用langchain做一个agent。遇到一个问题，就是在最开始输入的是一个query，比如：帮我从上海中心大厦导航到上海虹桥火车站，agent此时决定去调用高德导航这个tool，高德导航tool接收的输入是出发地和目的地，那么这个出发地和目的地是怎么解析出来传给高德导航tool的呢，是在自定义tool的description中写prompt让模型提取出发地和目的地两个实体吗，不懂怎么才能给想要调用的tool传递tool需要的参数。如果有10个tool，每个tool接收的输入参数都不一样，不知道怎么才能实现给指定tool传递特定参数的目标。</div>2023-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0e/1f/d0472177.jpg" width="30px"><span>厉害了我的国</span> 👍（2） 💬（0）<div>langchain迭代太快，在最新的0.1.12版本中，可以通过MultiPromptChain直接实现 router 能力，全部代码如下：

from langchain.chains.router import MultiPromptChain
from langchain_openai import ChatOpenAI

flower_care_template = &quot;&quot;&quot;
你是一位经验丰富的园丁，擅长解答关于养花育花的问题，下面是需要你来回答的问题：{input}
&quot;&quot;&quot;

flower_deco_template = &quot;&quot;&quot;
你是一位网红插花大师，擅长解答关于鲜花装饰的问题，下面是需要你来回答的问题：{input}
&quot;&quot;&quot;

prompt_infos = [
    {
        &quot;name&quot;: &quot;flower_care&quot;,
        &quot;prompt_template&quot;: flower_care_template,
        &quot;description&quot;: &quot;适合回答关于鲜花护理的问题&quot;
    },
    {
        &quot;name&quot;: &quot;flower_deco&quot;,
        &quot;prompt_template&quot;: flower_deco_template,
        &quot;description&quot;: &quot;适合回答关于鲜花装饰的问题&quot;
    }
]

llm = ChatOpenAI()
router_chain = MultiPromptChain.from_prompts(llm=llm, prompt_infos=prompt_infos, verbose=True)
print(router_chain.invoke({&quot;input&quot;: &quot;如何为玫瑰花浇水?&quot;}))

</div>2024-03-17</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>用阿里云的通义大模型代替OpenAI ,也顺利完成RouterChain确定客户意图的代码练习。
——
# 旧代码：
# 初始化语言模型
from langchain.llms import OpenAI
llm = OpenAI()
——
# 新代码：
# 用阿里云的大语言模型
from langchain_community.llms import Tongyi
DASHSCOPE_API_KEY = &quot; API_KEY&quot;  # # 设置API密钥，用你的 DASHSCOPE_API_KEY 代替
llm = Tongyi(dashscope_api_key=DASHSCOPE_API_KEY)</div>2024-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第9讲打卡~
LangChain内置了很多功能丰富的Chain，是个宝藏集合~</div>2024-07-16</li><br/><li><img src="" width="30px"><span>Geek_e74222</span> 👍（1） 💬（0）<div>老师你好，我通过本地部署chatglm3-6b来实现了本次课程中的例子，但是很奇怪，无论我的输入是否跟我们的提示模板相关，它总是会选择目标链中的一个去调用，而不是调用default_chain,这跟我的prompt内容相关吗？还是说跟大模型的能力相关呢？希望您能解答，感谢！</div>2024-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/0e/4b/ff4a21de.jpg" width="30px"><span>刘双荣</span> 👍（0） 💬（0）<div>routerChain </div>2024-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/03/06/791d0f5e.jpg" width="30px"><span>Jason Lee</span> 👍（0） 💬（0）<div>ConversationChain和LLMChain都有memory成员变量，都能保持上下文。
源码上ConversationChain extends LLMChain。
区别是 ConversationChain在LLMChain基础上扩展了一个lc_name静态属性。</div>2024-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/56/50/f54bd646.jpg" width="30px"><span>子飞鱼</span> 👍（0） 💬（0）<div>老师你好，我想问一下上面的示例，如果直接把input丢给llm，上述三种input应该也能给出不同的回答吧。请问路由链的最佳使用场景是什么呢</div>2024-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/10/28d5a686.jpg" width="30px"><span>Longerian</span> 👍（0） 💬（0）<div>思考题2:
# 用LLMChain代替 ConversationChain
from langchain.prompts import PromptTemplate
# 原始字符串模板
template = &quot;&quot;&quot;
The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:

Human: {input}
AI:
&quot;&quot;&quot;
# 创建LangChain模板
prompt_temp = PromptTemplate.from_template(template)
default_chain = LLMChain(
    llm=llm,
    prompt=prompt_temp)</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0a/61/ff5549d1.jpg" width="30px"><span>洋</span> 👍（0） 💬（0）<div>最新版还用这样写吗，怎么用LCEL实现</div>2024-02-22</li><br/><li><img src="" width="30px"><span>Geek_1b01a0</span> 👍（0） 💬（1）<div>SequentialChain和RouterChain可以结合使用吗</div>2024-01-24</li><br/>
</ul>