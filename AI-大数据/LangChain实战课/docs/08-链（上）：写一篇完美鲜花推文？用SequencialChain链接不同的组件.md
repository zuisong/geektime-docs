你好，我是黄佳。欢迎来到LangChain实战课！

到这节课，我们已经学到了不少LangChain的应用，也体会到了LangChain功能的强大。但也许你心里开始出现了一个疑问：LangChain，其中的 **Chain** 肯定是关键组件，为什么我们还没有讲到呢？

这的确是个好问题。对于简单的应用程序来说，直接调用LLM就已经足够了。因此，在前几节课的示例中，我们主要通过LangChain中提供的提示模板、模型接口以及输出解析器就实现了想要的功能。

## 什么是 Chain

但是，如果你想开发更复杂的应用程序，那么就需要通过 “Chain” 来链接LangChain的各个组件和功能——模型之间彼此链接，或模型与其他组件链接。

![](https://static001.geekbang.org/resource/image/e2/de/e26993dd3957bfd2947424abb9de7cde.png?wh=1965x1363)

这种将多个组件相互链接，组合成一个链的想法简单但很强大。它简化了复杂应用程序的实现，并使之更加模块化，能够创建出单一的、连贯的应用程序，从而使调试、维护和改进应用程序变得容易。

**说到链的实现和使用，也简单。**

- 首先LangChain通过设计好的接口，实现一个具体的链的功能。例如，LLM链（LLMChain）能够接受用户输入，使用 PromptTemplate 对其进行格式化，然后将格式化的响应传递给 LLM。这就相当于把整个Model I/O的流程封装到链里面。
- 实现了链的具体功能之后，我们可以通过将多个链组合在一起，或者将链与其他组件组合来构建更复杂的链。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（9） 💬（1）<div>Chain有三个能力，有状态，可观测，可组合。
有状态：Chain类定义了memory: Optional[BaseMemory]成员变量，记录了chain执行过程的状态。调用chain._call(inputs)可得到输出对象outputs，之后会调用chain.prep_outputs(inputs, outputs)加输入和输出对象成对放入memory对象。
可观测：Chain类定义了callbacks: Callbacks成员变量，在chain执行过程中回调on_xxx()方法。
可组合：比如SequentialChain类定义了chains: List[Chain]成员变量，会遍历chains列表调用，将初始输入inputs和已调用的chain的outputs合并到一个字典，作为当前chain的inputs，具体可阅读SequentialChain._call()。</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/73/4c/f743ac7c.jpg" width="30px"><span>Nikola</span> 👍（2） 💬（1）<div>上面的例子是不是也可以用思维链来实现？这样可以只调用一次模型。
思维链和langChain的chain组件的使用场景上有区别？</div>2023-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（2） 💬（2）<div># -*- coding: utf-8 -*-
import os

# 设置网络代理
os.environ[&quot;http_proxy&quot;] = &quot;http:&#47;&#47;127.0.0.1:7890&quot;
os.environ[&quot;https_proxy&quot;] = &quot;http:&#47;&#47;127.0.0.1:7890&quot;

# 通过.env管理api_token
from dotenv import load_dotenv
load_dotenv()

from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=.7, verbose=True)

# 导入结构化输出解析器和ResponseSchema
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
# 定义我们想要接收的响应模式
response_schemas = [
    ResponseSchema(name=&quot;description&quot;, description=&quot;鲜花的描述文案&quot;),
    ResponseSchema(name=&quot;reason&quot;, description=&quot;问什么要这样写这个文案&quot;)
]
# 创建输出解析器
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
print(output_parser.get_format_instructions())

# 创建原始提示模板
prompt_template = &quot;&quot;&quot;
您是一位专业的鲜花店文案撰写员。
对于售价为 {price} 元的 {flower} ，您能提供一个吸引人的简短描述吗？
输出格式：
{format_instructions}
&quot;&quot;&quot;
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=[&quot;flower&quot;, &quot;price&quot;],
    partial_variables={&quot;format_instructions&quot;: output_parser.get_format_instructions()},
    output_parser=output_parser)

chain = LLMChain(llm=llm, prompt=prompt)

# 数据准备
flowers = [&quot;玫瑰&quot;, &quot;百合&quot;, &quot;康乃馨&quot;]
prices = [&quot;50&quot;, &quot;30&quot;, &quot;20&quot;]

for flower, price in zip(flowers, prices):
    result = chain.run({
        &quot;flower&quot;: flower,
        &quot;price&quot;: price
    })
    print(result)
</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（2）<div>from langchain import PromptTemplate, OpenAI, LLMChain 
这行代码，为什么会有warning呢？
换成下面的import后，就没有告警了
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/01/eb3ba274.jpg" width="30px"><span>一面湖水</span> 👍（0） 💬（1）<div>为什么生成的文案不完整呢？看起来是被截断了。</div>2023-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/bd/e7ff842c.jpg" width="30px"><span>赤色闪电</span> 👍（0） 💬（2）<div>老师，您好！在文中构造顺序链的过程中，chains=[introduction_chain, review_chain, social_post_chain]中的social_post_chain是从哪里定义的？</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7a/84/fe247aff.jpg" width="30px"><span>.。。。</span> 👍（0） 💬（1）<div>老师，您好！学习了langchain后，实现了咱们课程中讲的case,但是有个疑问请假下，通过langchain框架调用的模型，如何对正在运行的模型进行停止呢？</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b0/ee/7409a0d3.jpg" width="30px"><span>冬青</span> 👍（2） 💬（0）<div>今日加更，快冲快冲！！！</div>2023-09-21</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div># 导入LangChain
from langchain import LLMChain 
# 导入LangChain中的提示模板
from langchain import PromptTemplate
# 创建原始模板
template = &quot;&quot;&quot;您是一位专业的鲜花店文案撰写员。\n
对于售价为 {price} 元的 {flower} ，您能提供一个吸引人的简短描述吗？\n
            
请以JSON格式返回，包含以下字段：\n
- flower_type: 鲜花的种类
- price: 鲜花的价格
- description: 鲜花的描述文案
- reason: 为什么要这样写这个文案
&quot;&quot;&quot;
# 根据原始模板创建LangChain提示模板
prompt = PromptTemplate.from_template(template)

# 定义我们想要接收的数据格式
from pydantic import BaseModel, Field
class FlowerDescription(BaseModel):    
    flower_type: str = Field(description=&quot;鲜花的种类&quot;)    
    price: int = Field(description=&quot;鲜花的价格&quot;)    
    description: str = Field(description=&quot;鲜花的描述文案&quot;)    
    reason: str = Field(description=&quot;为什么要这样写这个文案&quot;)


# 创建输出解析器
from langchain.output_parsers import PydanticOutputParser
output_parser = PydanticOutputParser(pydantic_object=FlowerDescription)


# 用阿里云的大语言模型
from langchain_community.llms import Tongyi
# 直接在代码中设置API密钥
DASHSCOPE_API_KEY = &quot;XXX&quot; # 请替换为您的阿里云通义千问模型API密钥
llm = Tongyi(dashscope_api_key=DASHSCOPE_API_KEY)

# apply允许您针对输入列表运行链
input_list = [
    {&quot;flower&quot;: &quot;玫瑰&quot;,&#39;price&#39;: &quot;50&quot;},
    {&quot;flower&quot;: &quot;百合&quot;,&#39;price&#39;: &quot;30&quot;},
    {&quot;flower&quot;: &quot;郁金香&quot;,&#39;price&#39;: &quot;20&quot;}
]
llm_chain = LLMChain( # 创建链
    llm=llm, 
    prompt=prompt,
    output_parser=output_parser) 
result = llm_chain.apply(input_list)      # 运行链
print(result)</div>2024-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/a0/8b9d5aca.jpg" width="30px"><span>eagle</span> 👍（1） 💬（1）<div>LangChainDeprecationWarning: The class `LLMChain` was deprecated in LangChain 0.1.17 and will be removed in 0.3.0. Use RunnableSequence, e.g., `prompt | llm` instead.</div>2024-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/0e/4b/ff4a21de.jpg" width="30px"><span>刘双荣</span> 👍（0） 💬（0）<div>多个提示链完成完整的业务生成</div>2024-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第8讲打卡~</div>2024-07-13</li><br/><li><img src="" width="30px"><span>黎楚萱</span> 👍（0） 💬（0）<div>为什么我的result会把所有的prompt都拼接在一起？有谁遇到同样的情况吗
我的输出是这样的：
introduction：\n你是一个植物学家，给定花的名称和类型，你需要为这种花写一个100字左右的介绍。\n花名：玫瑰\n颜色：red\n植物学家：这是关于上述花的介绍：\n玫瑰是一种美丽的花卉，通常被种植在花园或庭院中。它们通常有红色的花朵，通常有五到六片花瓣。玫瑰花的花瓣通常有五到六片，它们通常有红色的花粉，这使得它们成为一种非常受欢迎的花卉。玫瑰花通常需要充足的阳光和水分，以保持其健康和美丽。
review:\n你是一个鲜花评论家，给定一种花的介绍，你需要为这种花写一个200字左右的评论。\n鲜花介绍：\n\n你是一个植物学家，给定花的名称和类型，你需要为这种花写一个100字左右的介绍。\n花名：玫瑰\n颜色：red\n植物学家：这是关于上述花的介绍：\n玫瑰是一种美丽的花卉，通常被种植在花园或庭院中。它们通常有红色的花朵，通常有五到六片花瓣。玫瑰花的花瓣通常有五到六片，它们通常有红色的花粉，这使得它们成为一种非常受欢迎的花卉。玫瑰花通常需要充足的阳光和水分，以保持其健康和美丽。\n花评人对上述花的评论：\n玫瑰是一种非常美丽的花卉，它们通常有红色的花朵，通常有五到六片花瓣。玫瑰花的花瓣通常有五到六片，它们通常有红色的花粉，这使得它们成为一种非常受欢迎的花卉。玫瑰花通常需要充足的阳光和水分，以保持其健康和美丽。
...
</div>2024-03-07</li><br/>
</ul>