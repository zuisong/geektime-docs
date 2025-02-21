你好，我是徐文浩。

过去的两讲，我带着你通过OpenAI提供的Embedding接口，完成了文本分类的功能。那么，这一讲里，我们重新回到Completion接口。而且这一讲里，我们还会快速搭建出一个有界面的聊天机器人来给你用。在这个过程里，你也会第一次使用 HuggingFace 这个平台。

HuggingFace 是现在最流行的深度模型的社区，你可以在里面下载到最新开源的模型，以及看到别人提供的示例代码。

## ChatGPT来了，更快的速度更低的价格

我在[第03讲](https://time.geekbang.org/column/article/642197)里，已经给你看了如何通过Completion的接口，实现一个聊天机器人的功能。在那个时候，我们采用的是自己将整个对话拼接起来，将整个上下文都发送给OpenAI的Completion API的方式。不过，在3月2日，因为ChatGPT的火热，OpenAI放出了一个直接可以进行对话聊天的接口。这个接口叫做 **ChatCompletion**，对应的模型叫做gpt-3.5-turbo，不但用起来更容易了，速度还快，而且价格也是我们之前使用的 text-davinci-003 的十分之一，可谓是物美价廉了。

```python
import openai
openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLAD2YLZnuaicxibvPo6SEC3VoZ9Yra2g7HXDeqkWodb4nUvfRkhaOJxechJjUHBib4Ih1ryymCOW7AkQ/132" width="30px"><span>Geek_19eca2</span> 👍（6） 💬（0）<div>最新代码： 
import os

from openai import OpenAI
client = OpenAI()

class Conversation:
    def __init__(self, prompt, num_of_round):
        self.prompt = prompt
        self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: self.prompt})

    def ask(self, question):
        try:
            self.messages.append({&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: question})
            response = client.chat.completions.create(
                model=&quot;gpt-3.5-turbo&quot;,
                messages=self.messages,
                temperature=0.5,
                max_tokens=2048,
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        message = response.choices[0].message.content
        self.messages.append({&quot;role&quot;: &quot;assistant&quot;, &quot;content&quot;: message})

        if len(self.messages) &gt; self.num_of_round*2 + 1:
            del self.messages[1:3] # Remove the first round conversation left.
        return message


不然跑不过去。。openai改了。。。
</div>2024-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/81/d1/c06ba7a2.jpg" width="30px"><span>我自己带盐</span> 👍（30） 💬（2）<div>可以认模型总结一下，全部的对话，再发过去</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a0/aa/a4c1fa31.jpg" width="30px"><span>黄琨</span> 👍（16） 💬（1）<div>问题1: 为了防止超标，可能需要在对话开始前设置一个允许最大的token阈值，比如 MAX_TOKEN_LIMIT = 2000，再设置一个小于某个数量就需要提醒的警告值，比如 MIN_TOKEN_LIMIT = 200，对话前初始化一个最大值，对话过程中减去每轮所消耗的token数量，当结果少于最小值的时候，再调用删减对话数组的代码。

问题2: 限制文本长度。或许可以把对话中的大段文本缩减为精简摘要，以减少token数量，比如把“鱼香肉丝的做法是......”这种精简后的文本带入到上下文中去。别的暂时想不到 =_=!</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/98/883c42b4.jpg" width="30px"><span>LiuHu</span> 👍（9） 💬（2）<div>用向量数据库把历史回话保存到本地，新的问题先转向量，从向量库中搜出相关内容，再把搜出的内容作为上下文+新问题一起带过去</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（7） 💬（4）<div>目前chatGPT的上下文功能也是这么实现的吗？每次都要发之前的问题和答案，感觉很蠢</div>2023-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/7c/12/7b9a2efb.jpg" width="30px"><span>胡萝卜</span> 👍（6） 💬（1）<div>输入文本超长时需要不能直接截断，不然可能不听指令直接续写。截断后把最后一个句子去掉，并以句号结尾防止出现奇怪的回复。</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fe/b4/295338e7.jpg" width="30px"><span>Allan</span> 👍（3） 💬（1）<div>老师可以把每节课的项目都放到一个工程里面吗？然后我们可以下载这样是不是方便一些。</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/a8/be/e98383cc.jpg" width="30px"><span>new one</span> 👍（1） 💬（1）<div> 出现SSL握手失败的问题，请教一下应该怎么解决，问了chatgpt，使用了：
import ssl
context = ssl.create_default_context()
context.load_verify_locations(&quot;D:\Anaconda\Library\ssl\cert.pem&quot;)
并没有得到解决

具体报错如下：
Error communicating with OpenAI: HTTPSConnectionPool(host=&#39;api.openai.com&#39;, port=443): Max retries exceeded with url: &#47;v1&#47;chat&#47;completions (Caused by SSLError(SSLError(1, &#39;[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1129)&#39;)))
Assistant : Error communicating with OpenAI: HTTPSConnectionPool(host=&#39;api.openai.com&#39;, port=443): Max retries exceeded with url: &#47;v1&#47;chat&#47;completions (Caused by SSLError(SSLError(1, &#39;[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1129)&#39;)))</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/9e/2e/e46ab171.jpg" width="30px"><span>川月</span> 👍（1） 💬（6）<div>    del self.messages[1:3] &#47;&#47;Remove the first round conversation left.
        ^
SyntaxError: cannot delete operator 为什么这个报错啊</div>2023-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1a/b5/9635696d.jpg" width="30px"><span>Bonnenult丶凉煜</span> 👍（1） 💬（1）<div>安装gradio需要使用这个命令conda install -c conda-forge gradio</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/5c/2b75c836.jpg" width="30px"><span>陈鹏</span> 👍（0） 💬（1）<div>成功运行，开心。
请教老师一个问题：用hugging face 自己搭建的app，会一直运行吗？平台是否有策略到一定时间后停止我的app？</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/14/91/794687ef.jpg" width="30px"><span>王石磊</span> 👍（0） 💬（3）<div>我的示例报错现象是这样的，程序代码中设置了 API_KEY 和 网路代理，运行其他前面的代码正常，本节课的代码出现了。下面的问题。不存在API_KEY 费用不足或谷歌不能访问的情况。
openai.api_key = os.environ[&quot;OPENAI_API_KEY&quot;]
os.environ[&quot;http_proxy&quot;] = &quot;socks5:&#47;&#47;127.0.0.1:xxx&quot;
os.environ[&quot;https_proxy&quot;] = &quot;socks5:&#47;&#47;127.0.0.1:xxx&quot;
Traceback (most recent call last):
  File &quot;D:\Python3810\lib\site-packages\urllib3\connectionpool.py&quot;, line 703, in urlopen
    httplib_response = self._make_request(
  File &quot;D:\Python3810\lib\site-packages\urllib3\connectionpool.py&quot;, line 449, in _make_request
    six.raise_from(e, None)
  File &quot;&lt;string&gt;&quot;, line 3, in raise_from
  File &quot;D:\Python3810\lib\site-packages\urllib3\connectionpool.py&quot;, line 444, in _make_request
    httplib_response = conn.getresponse()
  File &quot;D:\Python3810\lib\http\client.py&quot;, line 1344, in getresponse
    response.begin()
  File &quot;D:\Python3810\lib\http\client.py&quot;, line 307, in begin
    version, status, reason = self._read_status()
  File &quot;D:\Python3810\lib\http\client.py&quot;, line 276, in _read_status
    raise RemoteDisconnected(&quot;Remote end closed connection without&quot;
http.client.RemoteDisconnected: Remote end closed connection without response

During handling of the above exception, another exception occurred:</div>2023-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/5c/2b75c836.jpg" width="30px"><span>陈鹏</span> 👍（0） 💬（2）<div>老师，第一段代码示例中的num_of_round=2，是不是要改为3？  感觉 前后内容对应不上，前面num_of_round设为2，虽然第三轮对话能练习上下文，但是问了问题3后，第一个问题和回答已经删除了</div>2023-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/80/a0533acb.jpg" width="30px"><span>勇.Max</span> 👍（0） 💬（1）<div>gradio应用代码，我在jupyter-lab上运行，左下角一直显示Busy，卡着不动。
我电脑配置并不低（macbook pro m1），网络也没问题。请问老师这种问题如何解决呢？</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ea/5d/ccb4c205.jpg" width="30px"><span>绘世浮夸 つ</span> 👍（0） 💬（1）<div>对于现在api做了限制每分钟只能提问三次怎么解决老师</div>2023-04-21</li><br/><li><img src="" width="30px"><span>Geek_053159</span> 👍（0） 💬（1）<div>老师 chatGPT 理解上下文都是需要把每次的会话全部传递给它 那如果是下面这种场景有没有处理办法呢 即我在和它的前面四次会话中我需要它记住上下文 在第五次会话中 为了节约token消耗和不影响回答的效果 我需要它忘记前面四次的会话 这种场景有没有特殊的指令可以实现 比如直接让告诉chatgpt ：忘记前面的对话</div>2023-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/3d/cd/65e6b3d3.jpg" width="30px"><span>独立思考</span> 👍（0） 💬（2）<div>报错：module &#39;openai&#39; has no attribute &#39;ChatCompletion&#39;，如何解决？</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（0） 💬（1）<div>del self.messages[1: 3] 为什么是3呢？理解应该是 del self.messages[1: self.num_of_round + 1]？</div>2023-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f1/65/b6508936.jpg" width="30px"><span>徐连振</span> 👍（0） 💬（1）<div>老师您好！计算gpt-3.5-turbo模型的token数有对应的Java库吗？因为我们的应用是Java写的，写的也比较复杂和成熟了，不想再部署一个Python服务，有计算token数Java对应的库吗？求推荐</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/29/c3/791d0f5e.jpg" width="30px"><span>渣渣辉</span> 👍（0） 💬（1）<div>我这里有个疑问，如果老师已经讲过了的话十分抱歉。在老师给的代码里提示词prompt不会因为达到最大token被删除掉。因此我得出在实际的使用上prompt是要求不可以被删掉的参数。我的结论对吗？</div>2023-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/85/d6/0221579f.jpg" width="30px"><span>王昊翔Harry</span> 👍（0） 💬（2）<div>没有编程的新手，在跑代码的时候常常出现 NameError                                 Traceback (most recent call last)
&lt;ipython-input-12-a8673c85e21c&gt; in &lt;cell line: 4&gt;()
      2 1. 你的回答必须是中文
      3 2. 回答限制在100个字以内&quot;&quot;&quot;
----&gt; 4 conv1 = Conversation(prompt, 2)
      5 question1 = &quot;你是谁？&quot;
      6 print(&quot;User : %s&quot; % question1)

NameError: name &#39;Conversation&#39; is not defined
这一类问题。但是没有具体的解释。Pandas一些下载的方式也有些迷茫。无法推进</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ba/8c/c57520b3.jpg" width="30px"><span>Zhang.Q.W</span> 👍（0） 💬（1）<div>请教一下：
运行时
import gradio as gr

报错
ModuleNotFoundError: No module named &#39;gradio&#39;

在运行 pip install gradio 和pip list 也可以查看到gradio，在运行时 依然报错ModuleNotFoundError</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/7d/adf4f7c3.jpg" width="30px"><span>智勇双全</span> 👍（0） 💬（3）<div>想部署到自己的腾讯云上该如何操作呢</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（0） 💬（10）<div>老师好，https:&#47;&#47;huggingface.co&#47;spaces&#47;xuwenhao83&#47;simple_chatbot这个链接我试了下，好像输入问题后按回车没有反应，是什么原因啊？</div>2023-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/49/c5/80c33529.jpg" width="30px"><span>代码五花肉</span> 👍（4） 💬（0）<div>设置一个阈值，如果超过阈值的话，就让AI总结一下，限定字数，然后清空对话记录，假如总结的这段话作为过往聊天记录再一起发送，缺点是要多调用API，多消耗token。</div>2023-03-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJaaRiaBo5xtYPib3az6lBtSG8ibebDUVGgSMRPD3nGn9hr0Iz8dDZXxMzsUV2M7uiaicBg9HdBxcSFic7g/132" width="30px"><span>Geek_b83fff</span> 👍（2） 💬（2）<div>成功运行，app.py 和require.txt； 老师没有展开说明，不是开发人员可能这一步会卡主</div>2023-05-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKuAaicIfRL8yyG4MZ64DoBhFrJS2TXAYs4hS8ibicoAHlSt3wx7xKMEloncnjgWbwzGqCq3IENvOvWw/132" width="30px"><span>林晨晨</span> 👍（1） 💬（0）<div>我能不能让ai帮忙把所有的对话概括写一下，然后再重新喂到提示中去？</div>2024-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/af/01/44fb3104.jpg" width="30px"><span>小掌柜</span> 👍（1） 💬（0）<div>没有视频吗？</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（0） 💬（0）<div>如何访问huggingface</div>2025-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/e9/d131dd81.jpg" width="30px"><span>Mamba</span> 👍（0） 💬（0）<div>你能根据这一讲学到的内容，修改一下代码，让这个聊天机器人不限制轮数，只在 Token 数量要超标的时候再删减最开始的对话么？除了“忘记”开始的几轮，你还能想到什么办法让 AI 尽可能多地记住上下文吗？
把两个需求一起解决，限制tokens数量，当要超标了的时候，将前文对话总结并替换掉之前的对话，然后就可以使得AI“记住”更多的上下文信息
class Conversation:
    def __init__(self, prompt, tokens):
        self.prompt = prompt
        self.instruct = &#39;请用简短的话总结目前对话的所有内容。&#39;
        self.tokens = tokens
        # self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: self.prompt})

    def ask(self, question):
        try:
            self.messages.append({&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: question})
            response = client.chat.completions.create(
                model=&quot;gpt-4o-mini&quot;,
                messages=self.messages,
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        message = response.choices[0].message.content
        self.messages.append({&quot;role&quot;: &quot;assistant&quot;, &quot;content&quot;: message})
        # 统计tokens
        num_of_tokens = response.usage.total_tokens

        # 如果超过一定tokens额度就把前面的对话总结并替换
        if num_of_tokens &gt; self.tokens:
            self.messages.append({&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: self.instruct})
            summary = response.choices[0].message.content
            del self.messages[1:]
            # print(summary)
            self.messages.append({&quot;role&quot;: &quot;assistant&quot;, &quot;content&quot;: summary})
            
        # if len(self.messages) &gt; self.num_of_round*2 + 1:  # sytem+n*(user+assistant)
        #     del self.messages[1:3] #Remove the first round conversation left.
        return message,num_of_tokens</div>2024-09-29</li><br/>
</ul>