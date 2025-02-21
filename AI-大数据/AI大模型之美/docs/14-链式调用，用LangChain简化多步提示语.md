你好，我是徐文浩。

OpenAI的大语言模型，只是提供了简简单单的Completion和Embedding这样两个核心接口。但是你也看到了，在过去的13讲里，通过合理使用这两个接口，我们完成了各种各样复杂的任务。

- 通过提示语（Prompt）里包含历史的聊天记录，我们能够让AI根据上下文正确地回答问题。
- 通过将Embedding提前索引好存起来，我们能够让AI根据外部知识回答问题。
- 而通过多轮对话，将AI返回的答案放在新的问题里，我们能够让AI帮我们给自己的代码撰写单元测试。

这些方法，也是一个实用的自然语言类应用里常见的模式。我之前也都通过代码为你演示过具体的做法。但是，如果我们每次写应用的时候，都需要自己再去OpenAI提供的原始API里做一遍，那就太麻烦了。于是，开源社区就有人将这些常见的需求和模式抽象了出来，开发了一个叫做Langchain的开源库。那么接下来，我们就来看看如何使用LangChain来快速实现之前我们利用大语言模型实现过的功能。以及我们如何进一步地，将Langchain和我们的业务系统整合，完成更复杂、更有实用价值的功能。

## 使用Langchain的链式调用

如果你观察得比较仔细的话，你会发现在[第 11 讲](https://time.geekbang.org/column/article/646363)我们使用llama-index的时候，就已经装好LangChain了。llama-index专注于为大语言模型的应用构建索引，虽然Langchain也有类似的功能，但这一点并不是Langchain的主要卖点。Langchain的第一个卖点其实就在它的名字里，也就是**链式调用**。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/a6/76/b2a1065a.jpg" width="30px"><span>智能</span> 👍（7） 💬（3）<div>这种链式调用是不是很容易让问题超过token限制，有没有什么办法来自动解决这个问题</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/5f/a2c78423.jpg" width="30px"><span>意</span> 👍（5） 💬（1）<div>老师好，看到LangChain获得1000万美元种子轮融资的新闻。
想问下：像LangChain这种开源的产品，商业模式是怎么样的，投资机构是看中了哪点进行投资的。</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（5） 💬（1）<div>老师我的想问下,国内使用Pinecone的效率如何? 会不会受到网络的影响?</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/92/69c2c135.jpg" width="30px"><span>厚积薄发</span> 👍（2） 💬（2）<div>支持多个变量输入的链式调用  这个案例 多运行几次，最后的数据结果，每次都不一样
其中一次是这个‘波尔图更多，他们获得过4次欧冠冠军，而西班牙皇家马德里只获得过3次欧冠冠军。  ’  老师，知道这个是什么原因吗？</div>2023-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（1）<div>autowgpt？</div>2023-04-29</li><br/><li><img src="" width="30px"><span>超超超超人</span> 👍（0） 💬（2）<div>老师你好，AutoGPT 本质上是不是也使用了链式调用呢？</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/c7/f57dadb9.jpg" width="30px"><span>张弛</span> 👍（0） 💬（1）<div>用ChatGPT实测本讲中提到的问题，先翻译英文提问，再翻译回来，好像并未产生更好的结果，跟直接中文提问的结果差不多。我还专门开了新的chat窗口来避免上下文影响。老师能否举个具体的通过这种方式得到更好结果的案例呢？</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/19/0a3fe8c1.jpg" width="30px"><span>Evan</span> 👍（0） 💬（1）<div>input_variables=[&quot;team1&quot;, &quot;team2&quot;],  是怎么传入参数的？</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（2） 💬（2）<div>part 1 (受限于2000字符，将相应的运行代码放在了part 2)

题目:
通过 Langchain 实现自动化撰写 Python 的一个函数(进行时间格式化输出)，并给出对该函数的单元测试，包含对异常输入的测试。

目的: 
1. 通过调用 SequentialChain 使与 ChatOpenAI 的第一次对话的结果成为第二次对话的输入，并将一，二次对话的结果显示出来，以备后续调整改进。(注: 在 ChatOpenAI 的对话窗下，ChatGPT 知道上一次对话的内容，无需重复)。
2. 使用自然语言提编程要求。
3. 通过调制 PromptTemplate 中的参数 template 来实现输出结果的最优化。这其实就是设置合适的 Prompt，以期最有效地使用 ChatGPT。

方法:
尝试着调用了 SequentialChain，使用 ChatOpenAI 的 &quot;gpt-3.5-turbo&quot;，参数设置 temperature=1

结果:

&gt; Entering new SequentialChain chain...

&gt; Finished chain.
def time_format(seconds):
    if seconds &lt; 60:
        return f&quot;{seconds}s&quot;
    elif seconds &lt; 3600:
        minutes = seconds &#47;&#47; 60
        seconds %= 60
        return f&quot;{minutes}min{seconds}s&quot;
    else:
        hours = seconds &#47;&#47; 3600
        seconds %= 3600
        minutes = seconds &#47;&#47; 60
        seconds %= 60
        return f&quot;{hours}h{minutes}min{seconds}s&quot;


&gt; Entering new SequentialChain chain...

&gt; Finished chain.
import pytest

def test_time_format():
    assert time_format(1) == &#39;1s&#39;
    assert time_format(61) == &#39;1min1s&#39;
    assert time_format(3678) == &#39;1h1min18s&#39;
    assert time_format(-1) == &#39;Invalid input&#39;
    assert time_format(&#39;abc&#39;) == &#39;Invalid input&#39;
    assert time_format(None) == &#39;Invalid input&#39;
    assert time_format(999999) == &#39;277h46min39s&#39; # Add a test case for a large input

As an AI language model, I cannot run this code, but I can assure you that the above code functions when used in a Python environment with the necessary dependencies and libraries installed.

结论:
输出基本满足了设计要求。ChatGPT3.5 在编程方面有所表现，尤其是考虑到本例中使用的模型是 gpt-3.5-turbo。</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（1） 💬（0）<div>part 2

在 part 1 中使用的代码如下:

import openai, os
from langchain.chat_models import ChatOpenAI  #from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

openai.api_key = os.environ.get(&quot;OPENAI_API_KEY&quot;)
llm = ChatOpenAI(model_name=&quot;gpt-3.5-turbo&quot;, max_tokens=2048, temperature=1)  #text-davinci-003, 2048, max_tokens: 4096 for gpt-3.5-turbo

Q1_prompt = PromptTemplate(
    template=&quot;用Python写一个函数，进行时间格式化输出，要求仅需要格式化到小时(?h?min?s)。比如：{Q1}&quot;,
    input_variables=[&quot;Q1&quot;]
)
Q2_prompt = PromptTemplate(
#    template=&quot;请为程序{A1}用&#39;pytest&#39; 写一个单元测试&quot;,
    template=&quot;&quot;&quot;请为程序{A1}用&#39;pytest&#39; 写一个单元测试, 
    Besides the test that counts negative numbers, include test cases like the input string &quot;abc&quot;, 
    and any other test cases you can think of, 
    将所有的 Test Cases 写入同一个测试中&quot;&quot;&quot;,
    input_variables=[&quot;A1&quot;]
)

chain1 = LLMChain(llm=llm, prompt=Q1_prompt, output_key=&quot;A1&quot;)
chain2 = LLMChain(llm=llm, prompt=Q2_prompt, output_key=&quot;A2&quot;)

q1=&quot;&quot;&quot;
输入  输出
1  1s
61  1min1s
&quot;&quot;&quot;

sequential_chain_p1 = SequentialChain(chains=[chain1], input_variables=[&quot;Q1&quot;], verbose=True)
answer1 = sequential_chain_p1.run(Q1=q1)
print(answer1)

sequential_chain_p2 = SequentialChain(chains=[chain1, chain2], input_variables=[&quot;Q1&quot;], verbose=True)
answer2 = sequential_chain_p2.run(Q1=q1)
print(answer2)

-----------
-----------

如何将代码封装在一个 App 中呢? 
未来的程序辅助设计是沿这个思路走还是另辟蹊径? 
如果有了用户交互界面，如何控制生成的程序不自己乱跑，亦或 &#39;在正确使用的引导下&#39; 让自动又自动生成的程序跑出了 &#39;天际&#39;，使得让人百思不得其解的事，豁然开朗了起来。

解了一题留下了更多问题。</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/27/1f/42059b0f.jpg" width="30px"><span>HXL</span> 👍（0） 💬（0）<div>遇到给代码问题,翻文档也没找到怎么解决,不知道该如何给plan_chain 传递参数. 现在一直报 &quot;Error: Missing value for input unit_test_package&quot;

&quot;&quot;&quot;
const modal = new ChatOpenAI({
    maxTokens: 2048,
    temperature: 0.5,
    stop: [&#39;\n\n&#39;],
    topP: 1,
});
&#47;&#47;
const explain_prompt = new PromptTemplate({
    &#47;&#47;...
})
const explain_chain = explain_prompt.pipe(modal);
&#47;&#47;
const plan_prompt = new PromptTemplate({
      template: `
      &quot;&quot;&quot;
    A good unit test suite should aim to:
    - Test the function&#39;s behavior for a wide range of possible inputs
    - Test edge cases that the author may not have foreseen
    - Take advantage of the features of &#39;{unit_test_package}&#39; to make the tests easy to write and maintain
    - Be easy to read and understand, with clean code and descriptive names
    - Be deterministic, so that the tests always pass or fail in the same way

    &#39;{unit_test_package}&#39; has many convenient features that make it easy to write and maintain unit tests. We&#39;ll use them to write unit tests for the function above.

    For this particular function, we&#39;ll want our unit tests to handle the following diverse scenarios (and under each scenario, we include a few examples as sub-bullets):
    -&quot;&quot;&quot;
      `,
    inputVariables: [&#39;unit_test_package&#39;],
});
const plan_chain = plan_prompt.pipe(modal);
&#47;&#47;
const write_prompt = new PromptTemplate({
    &#47;&#47;...
});
const write_chain = write_prompt.pipe(modal);
&#47;&#47;
async function main(){
    &#47;&#47;
    const test_code = `
    &#47;&#47;...
    `;
    &#47;&#47; FIXME: 如何给 plain_chain 传递参数？
    const sequence = RunnableSequence.from([explain_chain, plan_chain, write_chain]);
    const resp = await sequence.invoke({
        unit_test_package: &#39;jest&#39;,
        function_to_test: test_code,
    })
    console.log(resp);
};
main()
&quot;&quot;&quot;</div>2024-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/b0/7f/791d0f5e.jpg" width="30px"><span>Esquel-GET IT - gaofeng</span> 👍（0） 💬（0）<div>上下文记忆答复，上文总结，将总结的信息附加到下一次对话中，如果是将中文翻译成英文，答案由英文转换成中文，对于这个过程中，英文的总结和中文的总结是否一致？应该是有差异的吧？对于回复的内容如何提高精准度？</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（0） 💬（0）<div>老师想问一下，langchain增加了PromptTemplete有什么性能的优势吗？</div>2023-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6f/25/791d0f5e.jpg" width="30px"><span>花雨田</span> 👍（0） 💬（0）<div>理解下方代码，如果出现异常，再生成一遍write_unit_test（code）。

是否重生成时，把异常信息也给到语言模型会有帮助？

except SyntaxError as e:
            print(f&quot;Syntax error in generated code: {e}&quot;)
            all_code = code + write_unit_test(code)
            tried += 1</div>2023-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（0）<div>老师前文说过：大语言模型的一个缺点，就是可控性差。那所谓的基于大模型开发，是不是就是先针对每个&#47;多个问题找到比较好的prompt，以便于基于这个prompt 能够比较好的得到某类问题的回答，然后再用LangChain这类工具将prompt串起来，即可这对某一个场景得到相对确定效果的结果。</div>2023-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/59/1689ea0c.jpg" width="30px"><span>金hb.Ryan 冷空氣駕到</span> 👍（0） 💬（0）<div>### 写一个首歌 ，模仿&lt;muisc_copy&gt;
设计一些歌名，模仿&lt;muisc_copy&gt; ，需要给我三个歌名，不用告诉我为什么 -&gt; &lt; music_titles&gt;

如果想模仿&lt;music_copu&gt; 下面哪个标题更好\n&lt;music_titles&gt;\n，不用告诉我为什么，直接告诉{歌名},不需要返回歌名两个字: -&gt; &lt;music_title&gt;

用&lt;music_title&gt;为歌名，模仿&lt;music_copy&gt; 填写歌词

 &gt; Finished chain.
九州风云

Verse 1:
百姓疲惫，战火未息
江湖险恶，英雄无数
风云际会，谁又能料
剑光飞舞，血染长衫

Chorus:
九州风云，谁能掌控
剑指天下，谁能称雄
江山永固，谁又能守
英雄豪杰，谁才是真正的王者

Verse 2:
忠义仁勇，是我们的信仰
江山如画，我们守护
血染长枪，是我们的荣光
天下归心，我们的愿望

Chorus:
九州风云，谁能掌控
剑指天下，谁能称雄
江山永固，谁又能守
英雄豪杰，谁才是真正的王者

Bridge:
岁月如梭，英雄逝去
但江山永在，我们的信仰
九州风云，永远不会消逝
我们就是那些，历史长河中的传奇

Chorus:
九州风云，谁能掌控
剑指天下，谁能称雄
江山永固，谁又能守
英雄豪杰，谁才是真正的王者

Outro:
九州风云，我们的传奇
永远铭刻在历史长河之中
我们是那些，燃烧生命的英雄
九州风云，我们的荣光永不磨灭
</div>2023-05-23</li><br/><li><img src="" width="30px"><span>Geek_7ef8fe</span> 👍（0） 💬（0）<div>只有 SimpleSequentialChain, verbose=True ，可以打印不出过程日志。
SequantialChain, verbose=True ，仍然打印不出过程日志。有人知道 怎么解决嘛？</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/68/ec442a70.jpg" width="30px"><span>王jojo</span> 👍（0） 💬（0）<div>这个思路确实可以，写简单代码可以这样搞，实际中需要能把代码运行起来，再把结果吐给ai。</div>2023-04-13</li><br/>
</ul>