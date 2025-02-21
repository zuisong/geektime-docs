你好，我是黄佳，欢迎来到LangChain实战课！

上节课我给你留了一个思考题：**在提示模板的构建过程中加入了partial\_variables，也就是输出解析器指定的format\_instructions之后，为什么能够让模型生成结构化的输出？**

当你用print语句打印出最终传递给大模型的提示时，一切就变得非常明了。

````plain
您是一位专业的鲜花店文案撰写员。
对于售价为 50 元的 玫瑰 ，您能提供一个吸引人的简短描述吗？
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
        "description": string  // 鲜花的描述文案
        "reason": string  // 问什么要这样写这个文案
}
````

秘密在于，LangChain的输出解析器偷偷的在提示中加了一段话，也就是 {format\_instructions} 中的内容。这段由LangChain自动添加的文字，就清楚地指示着我们希望得到什么样的回答以及回答的具体格式。提示指出，模型需要根据一个schema来格式化输出文本，这个schema从 \`\`\`json 开始，到 \`\`\` 结束。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/bb/7d/26340713.jpg" width="30px"><span>黄振宇</span> 👍（9） 💬（3）<div>我使用prompt遇到的一些问题
    1. 最常见的initial_agent方法直接传入prompt参数，好像无效。只能通过agent_kwargs的PREFIX和SUFFIX等传入。
    2. 先定义个LLMChain传入prompt参数，在定义一个agent（single action或者multi action）
    3. 有时候传值进去，最后打印agent的prompt，发现好像也没有成功。
    4. openAI的模型还好，没怎么管输入输出的prompt的格式。但llama2的模型更难伺候，同样的代码只是换了LLM模型就运行不了，不是报没有input_variables就是输出无法parse，很困惑。
    
    以上希望在老师的课程里都能得到解答。
    
    另外，最近想去解决上述问题，看了langchain的源码，一头雾水，感觉东西太多了，不知从何开始，如果花大量时间在研究langchain上面又担心本末倒置了，毕竟它只是一个工具，还有好多的应用层的东西需要学习和研究，但是不吃透langchain只能做一些简单chatbot的应用。所以也比较迷茫，希望老师也能给出解答，如何做好二者的平衡。</div>2023-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/37/12e4c9c9.jpg" width="30px"><span>高源</span> 👍（2） 💬（1）<div>老师有个问题问下，例如大模型知道你提出问题后，是如何输出满意的答案呢，例如一道算法编程题目，大模型知道你的问题后，是根据自己以前存储类似答案输出的吗，我提个新的特殊问题，他是怎么思考输出的呢</div>2023-10-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YflLdCdbUAkfr9LPzF50EibDrMxBibPicQ5NNAETaPP0ytTmuR3h6QNichDMhDbR2XelSIXpOrPwbiaHgBkMJYOeULA/132" width="30px"><span>抽象派</span> 👍（2） 💬（1）<div>老师，请问“模型思考的时间”这个怎么理解啊？可以举个例子吗？</div>2023-10-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcFhGY0NV4kFzOSXWDHR2lrI2UbUP4Y016GOnpTH7dqSbicqJarX0pHxMsfLopRiacKEPXLx7IHHqg/132" width="30px"><span>一路前行</span> 👍（1） 💬（1）<div>老师，发现你在讲langchain时候基本以openai为主，这没什么问题。可否讲下。比如自己的本地大模型。如何通过langchain实现调用。比如自己的本地大模型，和嵌入模型。langchain之前的调用方法，是否需要修改，如果需要该怎么修改？</div>2024-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（1） 💬（1）<div>我发现有时候不指定 .prompts，直接从 LangChain 包也能导入模板。  会有告警信息：
langchain&#47;__init__.py:34: UserWarning: Importing PromptTemplate from langchain root module is no longer supported. Please use langchain.prompts.PromptTemplate instead. warnings.warn(
所以，建议还是指定 .prompts，即from langchain.prompts.prompt import PromptTemplate</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/b8/0f3bd8ec.jpg" width="30px"><span>曹胖子</span> 👍（0） 💬（1）<div>一路照着内容跑代码  一直到example_selector = SemanticSimilarityExampleSelector.from_examples   就不行了  工具报错 提示 UnicodeEncodeError: &#39;ascii&#39; codec can&#39;t encode characters in position 7-8: ordinal not in range(128)  问了gpt也没解决问题</div>2024-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0d/e9/2f02a383.jpg" width="30px"><span>冬瓜蔡</span> 👍（0） 💬（1）<div>黄老师下午好，我在跑野玫瑰 文案这个case时，并没有输出文案，而是如下信息：“这些看起来像是鲜花分类及其搭配的一些文案。需要帮你做些什么呢？”</div>2024-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bd/48/5d892c11.jpg" width="30px"><span>D.L</span> 👍（0） 💬（1）<div>黄老师，请教一下：
课程中有段代码
```
# 初始化示例选择器
example_selector = SemanticSimilarityExampleSelector.from_examples( samples, 
     OpenAIEmbeddings(), 
     Chroma,
     k=1)
```

将`Chroma`换成`Qdrant`，则会报错，报错信息如下(报错太长，省略部分）
```
Traceback (most recent call last):
  File &quot;&#47;python3.10&#47;site-packages&#47;langchain&#47;vectorstores&#47;qdrant.py&quot;, line 1584, in construct_instance
    collection_info = client.get_collection(collection_name=collection_name)
    ... ...
    ... ...
    ... ...
  File &quot;&#47;python3.10&#47;site-packages&#47;qdrant_client&#47;http&#47;api_client.py&quot;, line 97, in send
    raise UnexpectedResponse.for_response(response)
qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 502 (Bad Gateway)
Raw response content:
b&#39;&#39;

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File &quot;&#47;langchan_learning&#47;05-demo.py&quot;, line 43, in &lt;module&gt;
    example_selector = SemanticSimilarityExampleSelector.from_examples(
  File &quot;&#47;python3.10&#47;site-packages&#47;langchain_core&#47;example_selectors&#47;semantic_similarity.py&quot;, line 97, in from_examples
    vectorstore = vectorstore_cls.from_texts(
  File &quot;&#47;python3.10&#47;site-packages&#47;langchain&#47;vectorstores&#47;qdrant.py&quot;, line 1301, in from_texts
    qdrant = cls.construct_instance(
    ... ...
    ... ...
    ... ... 
  File &quot;&#47;python3.10&#47;site-packages&#47;qdrant_client&#47;http&#47;api_client.py&quot;, line 97, in send
    raise UnexpectedResponse.for_response(response)
qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 502 (Bad Gateway)
Raw response content:
b&#39;&#39;

```

</div>2023-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/01/eb3ba274.jpg" width="30px"><span>一面湖水</span> 👍（0） 💬（1）<div># 初始化示例选择器example_selector = SemanticSimilarityExampleSelector.from_examples(    samples,    OpenAIEmbeddings(),    Chroma,    k=1)
这里改成：Qdrant会报错呢？</div>2023-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/45/adf079ae.jpg" width="30px"><span>杨松</span> 👍（0） 💬（2）<div>老师您好，请教个问题，文中代码：
# 创建一个使用示例选择器的FewShotPromptTemplate对象
prompt = FewShotPromptTemplate(    
example_selector=example_selector,
 example_prompt=prompt_sample, 
 suffix=&quot;鲜花类型: {flower_type}\n场合: {occasion}&quot;, 
 input_variables=[&quot;flower_type&quot;, &quot;occasion&quot;])
print(prompt.format(flower_type=&quot;红玫瑰&quot;, occasion=&quot;爱情&quot;))
的打印结果为：
鲜花类型: 玫瑰
场合: 爱情
文案: 玫瑰，浪漫的象征，是你向心爱的人表达爱意的最佳选择。

鲜花类型: 红玫瑰
场合: 爱情
我的问题是 玫瑰的那个文字是example_selector生成的，还是example_prompt生成的，或者是两者同事生成后去重了？</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/a0/8ea0bfba.jpg" width="30px"><span>Yimmy</span> 👍（0） 💬（1）<div>template=&quot;鲜花类型: {flower_type}\n场合: {occasion}\n文案: {ad_copy}&quot;)--这里多了括号)</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（0） 💬（1）<div>假设做一个垂直领域的对话机器人，是否可以将用户的query通过一定的转换方式，比如embedding去“匹配”一些 Prompt，且增加Few or One example 的参考示例，相当于将query加工后，形成更加“指令化”的请求，便于让模型往更清晰地“理解”用户的说法，并按照更“步骤化”的方式去思考并给出答案。
也就是说，实际上用户与模型的交互，中间还是隐藏了很多“工程师加工”细节～

另外 ExampleSelector 的意义看起来是将 example 的匹配进行高层抽象，屏蔽细节，应该除了 Embbdings 方式，还有其他种种获取 example 的方式。使用Selector还有好处就是可以通过examples的瘦身节省tokens。</div>2023-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（1）<div>langchain 的很多提示都是针对chatgpt的，是不是可以理解为，chatgpt在进行sft的时候，数据集就用上了langchain很多prompt的措辞方式，所以chatgpt对这些prompt的效果也很好。</div>2023-09-13</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（4） 💬（1）<div>用国产模型改写：03_FewShotPrompt.py
用阿里云的通义千问模型 改写  OpenAI 模型。
改写OpenAIEmbeddings，由于使用阿里云embeddings模型代码复杂，采用百川智能的 BaichuanTextEmbeddings 
完整代码如下：
————

# 1. 创建一些示例
&#39;&#39;&#39;  原代码 &#39;&#39;&#39;

# 2. 创建一个提示模板
&#39;&#39;&#39;  原代码 &#39;&#39;&#39;

# 3. 创建一个FewShotPromptTemplate对象
&#39;&#39;&#39;  原代码 &#39;&#39;&#39;

# 4. 把提示传递给大模型
# import os
# os.environ[&quot;OPENAI_API_KEY&quot;] = &#39;你的OpenAI API Key&#39;
# from langchain.llms import OpenAI  #不采用OpenAI
# model = OpenAI(model_name=&#39;text-davinci-003&#39;)  

from langchain_openai import ChatOpenAI # 导入ChatOpenAI类
Model = ChatOpenAI(
    api_key= DASHSCOPE_API_KEY,  # 请在此处用您的阿里云API Key进行替换
    base_url=&quot;https:&#47;&#47;dashscope.aliyuncs.com&#47;compatible-mode&#47;v1&quot;, # DashScope base_url
    model=&quot;qwen-plus&quot; # 阿里云的模型
    )
# result = model(prompt.format(flower_type=&quot;野玫瑰&quot;, occasion=&quot;爱情&quot;))
result = Model(prompt.format(flower_type=&quot;野玫瑰&quot;, occasion=&quot;爱情&quot;))
# print(result) 
print(result.content) # 输出结果 content属性

# 5. 使用示例选择器
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import Qdrant
# from langchain.embeddings import OpenAIEmbeddings # 不采用OpenAI
from langchain_community.embeddings import BaichuanTextEmbeddings # 导入百川智能嵌入模型

# 初始化百川智能嵌入模型
embeddings = BaichuanTextEmbeddings(baichuan_api_key=  BAICHUAN_API_KEY)  # 请在此处用您的百川 API Key进行替换

# 初始化示例选择器
example_selector = SemanticSimilarityExampleSelector.from_examples(
    samples,
#  OpenAIEmbeddings(),  # 不采用OpenAI
    embeddings, # 使用百川智能嵌入模型代替OpenAIEmbeddings
    Qdrant,
    k=1
)

# 创建一个使用示例选择器的FewShotPromptTemplate对象
&#39;&#39;&#39;  原代码 &#39;&#39;&#39;</div>2024-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第4讲打卡~
在LLM应用中，除了准确性和性能，成本也是一个重要的评价指标，SemanticSimilarityExampleSelector可以通过比较余弦相似度，从所有示例中选取出于目标问题语义上最相近的k条示例，在很大程度上可以节省token的消耗，降低成本</div>2024-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/60/4fa1f3bd.jpg" width="30px"><span>rs勿忘初心</span> 👍（0） 💬（0）<div>记住评论区老师的回复：先不用不必苦钻细节，重点先了解LangChain的思想，以及它未来的可能性，知道它能做什么，不能做什么。</div>2024-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/a1/6270eeb7.jpg" width="30px"><span>极客星星</span> 👍（0） 💬（0）<div>咨询下，langchain定义的fewshot模板，把fewshot的格式进行了限制，有几个疑问：
1 这个fewshot模板，对于所有模型都适用吗，实际使用时，需不需要根据不同模型对模板进行调整
2 如果需要调整，能否定义自己的fewshot模板
谢谢</div>2024-09-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（0）<div>最后一段代码需要修改下：
# 5. 使用示例选择器
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
openai_embeddings = OpenAIEmbeddings()  # 实例化 OpenAIEmbeddings 类

example_selector = SemanticSimilarityExampleSelector.from_examples(
    samples,
    #OpenAIEmbeddings,
    openai_embeddings,
    Chroma,
    k = 1
)



# 创建一个使用示例选择器的 FewShotPromptTemplate 对象
prompt = FewShotPromptTemplate(
    example_selector = example_selector,
    example_prompt = prompt_sample,
    suffix = &quot;鲜花类型:{flower_type}\n场合：{occasion}&quot;,
    input_variables = [&quot;flower_type&quot;,&quot;occasion&quot;]
)
print(prompt.format(flower_type=&#39;红玫瑰&#39;, occasion=&#39;爱情&#39;))</div>2024-04-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（0）<div>from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model=&quot;gpt-3.5-turbo&quot;,
  messages=[
    {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;You are a helpful assistant.&quot;},
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;Who won the world series in 2020?&quot;},
    {&quot;role&quot;: &quot;assistant&quot;, &quot;content&quot;: &quot;The Los Angeles Dodgers won the World Series in 2020.&quot;},
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;Where was it played?&quot;}
  ]
)
我的 C:\Users\Admin&gt;openai --version
openai 1.14. 运行这个会报错， 解办法：from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model=&quot;gpt-3.5-turbo&quot;,
  messages=[
    {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;You are a helpful assistant.&quot;},
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;Who won the world series in 2020?&quot;},
    {&quot;role&quot;: &quot;assistant&quot;, &quot;content&quot;: &quot;The Los Angeles Dodgers won the World Series in 2020.&quot;},
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;Where was it played?&quot;}
  ]
)</div>2024-04-17</li><br/>
</ul>