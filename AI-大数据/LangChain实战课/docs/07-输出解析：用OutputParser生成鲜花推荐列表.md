你好，我是黄佳，欢迎来到LangChain实战课！

首先请你回忆一下[第4课](https://time.geekbang.org/column/article/700699)中我们学了什么: 为一些花和价格生成吸引人的描述，并将这些描述和原因存储到一个CSV文件中。为了实现这个目标，程序调用了OpenAI模型，并利用了结构化输出解析器，以及一些数据处理和存储的工具。

今天我要带着你深入研究一下LangChain中的输出解析器，并用一个新的解析器——Pydantic 解析器来重构第4课中的程序。这节课也是模型I/O框架的最后一讲。

![](https://static001.geekbang.org/resource/image/62/2d/6215fdd31373523a46bb02f86283522d.jpg?wh=4000x1536 "模型 I/O Pipeline")

下面先来看看LangChain中的输出解析器究竟是什么，有哪些种类。

## LangChain 中的输出解析器

语言模型输出的是文本，这是给人类阅读的。但很多时候，你可能想要获得的是程序能够处理的结构化信息。这就是输出解析器发挥作用的地方。

输出解析器是**一种专用于处理和构建语言模型响应的类**。一个基本的输出解析器类通常需要实现两个核心方法。

- get\_format\_instructions：这个方法需要返回一个字符串，用于指导如何格式化语言模型的输出，告诉它应该如何组织并构建它的回答。
- parse：这个方法接收一个字符串（也就是语言模型的输出）并将其解析为特定的数据结构或格式。这一步通常用于确保模型的输出符合我们的预期，并且能够以我们需要的形式进行后续处理。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（23） 💬（1）<div>从源码上看，OutputFixingParser和RetryWithErrorOutputParser的本质是相同的，都是当PydanticOutputParser.parse(input)解析失败，通过语言模型分析抛出的异常，修正input。
不同之处在于，OutputFixingParser利用input schema、input、exception来修正input，RetryWithErrorOutputParser除了利用input schema、input、exception，还利用一个额外的prompt来修正input，有了额外的prompt，自然就能够既修正input格式，又补全input内容。</div>2023-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/37/12e4c9c9.jpg" width="30px"><span>高源</span> 👍（10） 💬（2）<div>老师有个问题请教，例如目前大模型比较多，我的理解如果满足企业内部自己使用，是需要对大模型微调吧才能完全满足定制，例如输出企业自己相关数据，文档，代码等，而不是简单把提示写好弄个差不多开源大模型上去。我的理解是需要微调吧，针对自己企业数据进行训练对模型，但这块听老师课我理解需要对模型层次熟悉才能下手进行微调吧，我自己理解目前从效果上还是gpt其它模型还是比较弱，百度说他的2.0已经超过gpt3.5，比gpt4差点，我觉得没那么快吧，另外训练模型机器硬件人员等各种因素叠加，不是说都能做好了吧，企业自己落地自己模型这块现实吗，自己做需要那些条件，例如人员要求等，谢谢</div>2023-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4a/ee/fe035424.jpg" width="30px"><span>棟</span> 👍（1） 💬（4）<div>老师，请教一个问题，
fix_parser或retry_parser中，如果错误的输出是json格式会报如下错误：
action_input
  Field required [type=missing, input_value={&#39;action&#39;: &#39;search&#39;}, input_type=dict]
    For further information visit https:&#47;&#47;errors.pydantic.dev&#47;2.3&#47;v&#47;missing

我是将错误bad_response = &#39;{&quot;action&quot;: &quot;search&quot;}&#39;  --&gt; 更改为bad_response = &quot;{&#39;action&#39;: &#39;search&#39;}&quot;才能正常调用模型，这个要怎么修复。
知道的朋友也请指点，感谢！</div>2023-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/b8/0f3bd8ec.jpg" width="30px"><span>曹胖子</span> 👍（0） 💬（1）<div>parsed_output = output_parser.parse(output.content)   会报异常， 目前我尝试打印了 output的数据类型和结构，感觉是返回的数据结构出现的变动，最终我调整为 parsed_output = output_parser.parse(output.content) 后代码可执行。</div>2024-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/dc/39fa0a55.jpg" width="30px"><span>风隼[咖啡]</span> 👍（0） 💬（1）<div>    # parsed_output_dict = parsed_output.dict()  # 将Pydantic格式转化位字典
    # Pydantic 格式转化为字典,Pydantic V2dict 方法已经被废弃，推荐使用 model_dump 方法来代替
    parsed_output_dict = parsed_output.model_dump()</div>2023-12-15</li><br/><li><img src="" width="30px"><span>rick009</span> 👍（0） 💬（1）<div>老师您好，有个问题请教一下，我想要从给定的一段文本中抽离一些FAQ，然后想返回JSON数组的格式，以下是prompt：
template = &quot;&quot;&quot;你是一名知识库管理员，需将以下内容拆分成 {nums} 个问答对，确保准确无误且只从文献中获取，不得扩散。你的算法或流程应该能够准确抽取关键信息，并生成准确的问答对，以充分利用文献。
    {doc_content}
    {format_instructions}  
    &quot;&quot;&quot;
想要返回的格式为
The output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {&quot;properties&quot;: {&quot;foo&quot;: {&quot;title&quot;: &quot;Foo&quot;, &quot;description&quot;: &quot;a list of strings&quot;, &quot;type&quot;: &quot;array&quot;, &quot;items&quot;: {&quot;type&quot;: &quot;string&quot;}}}, &quot;required&quot;: [&quot;foo&quot;]}\nthe object {&quot;foo&quot;: [&quot;bar&quot;, &quot;baz&quot;]} is a well-formatted instance of the schema. The object {&quot;properties&quot;: {&quot;foo&quot;: [&quot;bar&quot;, &quot;baz&quot;]}} is not well-formatted.\n\nHere is the output schema:\n```\n{&quot;$defs&quot;: {&quot;QA&quot;: {&quot;properties&quot;: {&quot;Q&quot;: {&quot;description&quot;: &quot;\\u95ee\\u9898&quot;, &quot;title&quot;: &quot;Q&quot;, &quot;type&quot;: &quot;string&quot;}, &quot;A&quot;: {&quot;description&quot;: &quot;\\u7b54\\u6848&quot;, &quot;title&quot;: &quot;A&quot;, &quot;type&quot;: &quot;string&quot;}}, &quot;required&quot;: [&quot;Q&quot;, &quot;A&quot;], &quot;title&quot;: &quot;QA&quot;, &quot;type&quot;: &quot;object&quot;}}, &quot;items&quot;: {&quot;$ref&quot;: &quot;#&#47;$defs&#47;QA&quot;}}\n```
class QA(BaseModel):
    Q: str = Field(description=&quot;问题&quot;)
    A: str = Field(description=&quot;答案&quot;)

class QAList(RootModel):
    root: List[QA] = Field(description=&quot;FAQ问答对列表&quot;)
但是返回的格式总是不停的在变，都无法返回希望的数据结构</div>2023-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/e3/c49aa508.jpg" width="30px"><span>鲸鱼</span> 👍（0） 💬（1）<div>我遇到一个问题，目前的langchain必须使用v1版本的pydantic，如果使用了v2版本抛出的异常类型不对，会导致PydanticOutputParser无法捕获正常的ValidationError异常，从而不会去请求openAI修复response。
PydanticOutputParser的具体捕获代码是这里

class PydanticOutputParser(BaseOutputParser[T]):
    &quot;&quot;&quot;Parse an output using a pydantic model.&quot;&quot;&quot;

    pydantic_object: Type[T]
    &quot;&quot;&quot;The pydantic model to parse.&quot;&quot;&quot;

    def parse(self, text: str) -&gt; T:
        try:
            # Greedy search for 1st json candidate.
            match = re.search(
                r&quot;\{.*\}&quot;, text.strip(), re.MULTILINE | re.IGNORECASE | re.DOTALL
            )
            json_str = &quot;&quot;
            if match:
                json_str = match.group()
            json_object = json.loads(json_str, strict=False)
            return self.pydantic_object.parse_obj(json_object)

        except (json.JSONDecodeError, ValidationError) as e: # 这里只能捕获v1版本的ValidationError
            name = self.pydantic_object.__name__
            msg = f&quot;Failed to parse {name} from completion {text}. Got: {e}&quot;
            raise OutputParserException(msg, llm_output=text)
</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（1）<div>佳哥好，我发现在OutputFixingParser示例中，如果做如下修改：
new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI(temperature=0))
或者
new_parser = OutputFixingParser.from_llm(parser=parser, llm=OpenAI(temperature=0))
可以得到稳定的输出：
name=&#39;康乃馨&#39; colors=[&#39;粉红色&#39;, &#39;白色&#39;, &#39;红色&#39;, &#39;紫色&#39;, &#39;黄色&#39;]
而不是：
name=&#39;Rose&#39; colors=[&#39;red&#39;, &#39;pink&#39;, &#39;white&#39;]</div>2023-09-20</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>重试解析器（RetryWithErrorOutputParser）实战学习，修改代码如下。注意：要设置max_retries=3，增加重试次数，解析成功率会极大提高
（1）原代码：
fix_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())
新代码：
os.environ[&quot;BAICHUAN_API_KEY&quot;] =&quot;xxx&quot; # 请替换为你的百川模型 BAICHUAN API Key
from langchain_community.llms import BaichuanLLM
# 加载百川模型
llm = BaichuanLLM()
fix_parser = OutputFixingParser.from_llm(parser=parser, llm=llm, max_retries=3) # 使用百川模型，增加重试次数:3
（2）
原代码：
from langchain.llms import OpenAI
retry_parser = RetryWithErrorOutputParser.from_llm(
    parser=parser, llm=OpenAI(temperature=0)
)
新代码：
from langchain_community.llms import BaichuanLLM
# 初始化百川智能模型
baichuan_llm = BaichuanLLM()
# 初始化RetryWithErrorOutputParser，使用百川智能模型
retry_parser = RetryWithErrorOutputParser.from_llm(
    parser=parser, llm=baichuan_llm  , max_retries=3     # 使用百川模型
)</div>2024-07-27</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>继续使用国产大模型替代OpenAI进行代码学习。
在自动修复解析器（OutputFixingParser）实战中发现，使用通义千问模型调用时出错，无法解析。但是用百川智能模型能够正确解析。
使用百川模型修正代码如下：
原代码：
new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())
新代码：
os.environ[&quot;BAICHUAN_API_KEY&quot;] =&quot;xxx&quot; # 请替换为你的百川模型 BAICHUAN API Key
from langchain_community.llms import BaichuanLLM
llm = BaichuanLLM()  # 加载百川模型
new_parser = OutputFixingParser.from_llm(parser=parser, llm=llm, max_retries=3) # 增加重试次数:3</div>2024-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第7讲打卡~
再补充一个最简单的StrOutputParser字符串解析器，它将LLM的输出结果直接解析成字符串，在客服系统、聊天机器人等场景中使用得比较多。</div>2024-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/42/ac/179015d9.jpg" width="30px"><span>LVEli</span> 👍（0） 💬（0）<div>老师，请问这里提到的List Parser。在实际使用中：list_parser = ListOutputParser()时，会提示类似这样的报错：这是一个静态类。。。如果不能使用这个输出解析器，是否还有其他方法能使agent执行后输出的string类型结果，转换成列表呢，谢谢~~</div>2025-01-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKr3ZPRg8ECLpOkfpN1ny8HGV8DIkQ0fo4blKFSQgK0x76C5WiaxFXQpoIqTHWEV3bia603bBmtwZcg/132" width="30px"><span>勤小码</span> 👍（0） 💬（0）<div>2024&#47;8 目前使 langchain==0.2.12，运行文中示例代码会抛异常。参考官方文档发现需要修改两处导入：

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import RetryOutputParser

具体内容见官方How-to文档
https:&#47;&#47;python.langchain.com&#47;v0.2&#47;docs&#47;how_to&#47;output_parser_retry&#47;

langchain 目前更新比较快，各种API也不稳定，容易出现各种意想不到的问题。本示例异常原因后续再debug详细看看。
</div>2024-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5d/3c/2253daa8.jpg" width="30px"><span>核桃爸爸</span> 👍（0） 💬（0）<div>2024年7月24日，最新版本的 langchain 库无法运行成功</div>2024-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/58/c0/d1d488b0.jpg" width="30px"><span>chenyang</span> 👍（0） 💬（0）<div>老师你好，
02_OutputFixParser.py 和 03_RetryParser.py 运行时，都会报
KeyError: &quot;Input to PromptTemplate is missing variables {&#39;completion&#39;}.  Expected: [&#39;completion&#39;, &#39;error&#39;, &#39;instructions&#39;] Received: [&#39;instructions&#39;, &#39;input&#39;, &#39;error&#39;]&quot;
请问是什么原因呀</div>2024-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/a0/8b9d5aca.jpg" width="30px"><span>eagle</span> 👍（0） 💬（0）<div>对于RetryWithErrorOutputParser，template 变量的目的是什么？ 似乎没有被引用啊？

template = &quot;&quot;&quot;Based on the user question, provide an Action and Action Input for what step should be taken.{format_instructions}Question: {query}Response:&quot;&quot;&quot;</div>2024-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/25/f7/4cc60573.jpg" width="30px"><span>zhang</span> 👍（0） 💬（0）<div>老师你好，我是一个从事了几年的C语言开发者。计划在机器学习领域拓展拓展。可是我看了LangChain的一些基本理念之后，使用提示模板在性能方面比直接用代码处理异常开销要差很多吧。

比如作为一个server对外提供服务的时候，它的延迟、并发数等又该如何考量呢？</div>2024-03-06</li><br/><li><img src="" width="30px"><span>Geek_a23cc7</span> 👍（0） 💬（1）<div>Traceback (most recent call last):
  File &quot;E:\Code-python\langchain-main\langchain-main\07_解析输出\01_Pydantic_Parser.py&quot;, line 71, in &lt;module&gt;
    parsed_output = output_parser.parse(output)
  File &quot;D:\Anaconda\envs\python3.10\lib\site-packages\langchain\output_parsers\pydantic.py&quot;, line 34, in parse
    return self.pydantic_object.parse_obj(json_object)
  File &quot;D:\Anaconda\envs\python3.10\lib\site-packages\typing_extensions.py&quot;, line 2499, in wrapper
    return arg(*args, **kwargs)
  File &quot;D:\Anaconda\envs\python3.10\lib\site-packages\pydantic\main.py&quot;, line 1027, in parse_obj
    return cls.model_validate(obj)
  File &quot;D:\Anaconda\envs\python3.10\lib\site-packages\pydantic\main.py&quot;, line 503, in model_validate
    return cls.__pydantic_validator__.validate_python(
pydantic_core._pydantic_core.ValidationError: 4 validation errors for FlowerDescription
flower_type
  Field required [type=missing, input_value={&#39;properties&#39;: {&#39;flower_t...description&#39;, &#39;reason&#39;]}, input_type=dict]
    For further information visit https:&#47;&#47;errors.pydantic.dev&#47;2.5&#47;v&#47;missing
price
  Field required [type=missing, input_value={&#39;properties&#39;: {&#39;flower_t...description&#39;, &#39;reason&#39;]}, input_type=dict]
    For further information visit https:&#47;&#47;errors.pydantic.dev&#47;2.5&#47;v&#47;missing
description
  Field required [type=missing, input_value={&#39;properties&#39;: {&#39;flower_t...description&#39;, &#39;reason&#39;]}, input_type=dict]
    For further information visit https:&#47;&#47;errors.pydantic.dev&#47;2.5&#47;v&#47;missing
reason
  Field required [type=missing, input_value={&#39;properties&#39;: {&#39;flower_t...description&#39;, &#39;reason&#39;]}, input_type=dict]
    For further information visit https:&#47;&#47;errors.pydantic.dev&#47;2.5&#47;v&#47;missing
黄老师您看一下我这个问题</div>2024-01-30</li><br/>
</ul>