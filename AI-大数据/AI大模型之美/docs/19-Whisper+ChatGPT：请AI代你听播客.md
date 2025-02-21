你好，我是徐文浩。

今天，我们的课程开始进入一个新的主题了，那就是语音识别。过去几周我们介绍的ChatGPT虽然很强大，但是只能接受文本的输入。而在现实生活中，很多时候我们并不方便停下来打字。很多内容比如像播客也没有文字版，所以这个时候，我们就需要一个能够将语音内容转换成文本的能力。

作为目前AI界的领导者，OpenAI自然也不会放过这个需求。他们不仅发表了一个通用的语音识别模型 Whisper，还把对应的代码开源了。在今年的1月份，他们也在API里提供了对应的语音识别服务。那么今天，我们就一起来看看Whisper这个语音识别的模型可以怎么用。

## Whisper API 101

我自己经常会在差旅的过程中听播客。不过，筛选听什么播客的时候，有一个问题，就是光看标题和简介其实不是特别好判断里面的内容我是不是真的感兴趣。所以，在看到Whisper和ChatGPT这两个产品之后，我自然就想到了可以通过组合这两个API，让AI来代我听播客。**我想通过Whisper把想要听的播客转录成文字稿，再通过ChatGPT做个小结，看看AI总结的小结内容是不是我想要听的。**

我前一阵刚听过一个[关于 ChatGPT 的播客](https://www.listennotes.com/podcasts/onboard/ep-26-10pmK95wovN/)，我们不妨就从这个开始。我们可以通过 [listennotes](https://www.listennotes.com/) 这个网站来搜索播客，还能够下载到播客的源文件。而且，这个网站还有一个很有用的功能，就是可以直接切出播客中的一段内容，创建出一个切片（clip）。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（32） 💬（1）<div>将长音频分片转录时，如果完全按照精确的时间去切割音频文件，很有可能在结尾处裁出一个不完整的句子，而下一段的开头也可能会是半句话。如何解决，思考题很实用。

下面是一种思路:

1.  从计划切割的位置上取出一小片。比如音频文件长约2小时，初步计划分成四个文件，每份约长30分钟，将30分到30分10秒的音频切出来。实现方法
extract = audio_long[StartTime:EndTime]
extract.export(&quot;cutat30mins.mp3&quot;, format=&quot;mp3&quot;)

2. 找出这个10秒切片中的断句位置，实现方法
from pydub.silence import detect_silence
piece = AudioSegment.from_mp3(&quot;cutat30mins.mp3&quot;)
silent_ranges = detect_silence(piece, min_silence_len=500, silence_thresh=-40)
参数代表静音时长和分贝

3. 选上面断句位置中的第一个的起点作为第一段半小时音频文件的结尾。这样就得到 1. 中的EndTime 准确值，而不是在一句话的中间。

测试: 选 podcast_clip.mp3 作为测试文件，时长3分钟。初选2分钟处分割。

取 2 分钟到 2 分钟10秒 的一个小片段，得出静音数列 [[793, 1803], [4991, 5813]]

file =  = AudioSegment.from_mp3(&quot;podcast_clip.mp3&quot;)
EndTime = 2*60*1000 + 793 = 120793
part_1 = file[:EndTime]
StartTime = 2*60*1000 + 1803 = 121803
part_2 = file[StartTime:]

结果:
part_1 结束句 &#39;证实发布后会有怎样的惊喜,我们都拭目以待。&#39;
part_2 开始句 &#39;AI无疑是未来几年最令人兴奋的变量之一。&#39;

还会有其它的解决方法。</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（12） 💬（3）<div>尝试着将李沐老师视频 &#39;AutoCut--如何用 Whisper 来剪辑视频&#39; 的内容进行了概要信息提取。分三步，1 视频读取和语音识别，2 将大块文件裁成小块，使得输入的 Token 数能满足 OpenAI 的要求，3 分块总结。

1. 从 B 站读取视频 (Bilibili Video)，实现代码如下:

!pip install bilibili-api
from langchain.document_loaders.bilibili import BiliBiliLoader
loader_bi = BiliBiliLoader([&quot;https:&#47;&#47;www.bilibili.com&#47;video&#47;BV1Pe4y1t7de&#47;&quot;])
result_bi = loader_bi.load()

2. 数据分割，实现代码如下:

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter_bi = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=20)
texts_bi = text_splitter_bi.split_documents(result_bi)

调整参数 chunk_size 决定切割的大小，在本例中，裁成了6段，查看代码如下:

len(texts_bi)
6

3. 给出视频内容提要，实现代码如下:

from langchain.prompts import PromptTemplate
llm = OpenAI(temperature=0)
prompt_template = &quot;&quot;&quot;Answer in Chinese. Summarize this conversation {text}. Do NOT write sentences that has no sense.&quot;&quot;&quot;
prompt_template2 = &quot;&quot;&quot;Answer in Chinese. Choose the more relevant phrases of the following text and summarize them {text}.&quot;&quot;&quot;
PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=[&quot;text&quot;]       
)
PROMPT2 = PromptTemplate(
    template=prompt_template2,
    input_variables=[&quot;text&quot;]       
)
overall_bi = load_summarize_chain(llm, chain_type=&quot;map_reduce&quot;, map_prompt=PROMPT, combine_prompt=PROMPT2, return_intermediate_steps=True, verbose=True)

summarize_bi = overall_bi( {&quot;input_documents&quot;: texts_bi},return_only_outputs=True)

输出结果如下:

这段视频介绍了一个叫OpenAI Whisper的剪视频小工具，并附上了一个GitHub链接，...
我们演示了如何使用OpenAI的Whisper模型来识别视频中的字幕，并且可以选择不同的模型，从tiny到large ... 以提高识别精度。
选择Small模型可以满足大部分需求，...可以节省时间。
...
这次讨论的主要内容是Whisper这个模型的使用，它在中文语谅上的表现不是很好，但是在带有英文词汇的视频中，它的识别能力还是很强的， ...

---
上面提供了一种提取视频核心思想的方法，还会有更好的。</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/bb/62/f87ee12f.jpg" width="30px"><span>詹杰</span> 👍（1） 💬（1）<div>老师，whisper开源模型本地部署支持批量推理不？怎么批量推理呢？目前就是需要完成很多很多的语言识别任务，效率跟不上，想请教老师怎么解决呢</div>2023-04-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJiaPZjokKDOAicIIOtJB0Omkw5tXZem8icbDBpxqhqE5iaMicHbEgEicESiaGDZ7icSwqmYfqXc4r8uhKHwQ/132" width="30px"><span>Geek_00eb03</span> 👍（1） 💬（2）<div>老师，运行代码报错， 能帮忙看看什么原因吗？
--&gt; 157     raise ValueError(
    158         &quot;A single term is larger than the allowed chunk size.\n&quot;
    159         f&quot;Term size: {num_cur_tokens}\n&quot;
    160         f&quot;Chunk size: {self._chunk_size}&quot;
    161         f&quot;Effective chunk size: {effective_chunk_size}&quot;
    162     )
    163 # If adding token to current_doc would exceed the chunk size:
    164 # 1. First verify with tokenizer that current_doc
    165 # 1. Update the docs list
    166 if cur_total + num_cur_tokens &gt; effective_chunk_size:
    167     # NOTE: since we use a proxy for counting tokens, we want to
    168     # run tokenizer across all of current_doc first. If
    169     # the chunk is too big, then we will reduce text in pieces

ValueError: A single term is larger than the allowed chunk size.
Term size: 414
Chunk size: 357Effective chunk size: 357</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/7c/12/7b9a2efb.jpg" width="30px"><span>胡萝卜</span> 👍（1） 💬（1）<div>能做成流式的音转文吗？</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cf/b0/5ff252b6.jpg" width="30px"><span>子辰</span> 👍（0） 💬（2）<div>默认就是跑GPU的吗？我用 mac 看活动监视器好像是跑在 CPU 上的。。。</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/bb/62/f87ee12f.jpg" width="30px"><span>詹杰</span> 👍（0） 💬（1）<div>徐老师，我想问一个提高开源whisper模型计算效率的问题，我用多线程去调度解析会报错，请问如何提高效率呢，我只能再买显卡，多部署几台服务嘛？</div>2023-04-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJiaPZjokKDOAicIIOtJB0Omkw5tXZem8icbDBpxqhqE5iaMicHbEgEicESiaGDZ7icSwqmYfqXc4r8uhKHwQ/132" width="30px"><span>Geek_00eb03</span> 👍（0） 💬（1）<div>普通服务器的CPU 能不能跑起来whisper 开源模型？</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/56/75/28a29e7c.jpg" width="30px"><span>安菲尔德</span> 👍（0） 💬（1）<div>老师，请教一个非技术问题，peo.com这个网站是收费的么，如果不收费的话，他们里面chatgpt功能调用的是openai的接口实现的么，如果是的话，那岂不是很费钱，他们怎么赚钱呢？</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/c7/f57dadb9.jpg" width="30px"><span>张弛</span> 👍（0） 💬（2）<div>自己尝试转录了一个播客，成功用Colab进行了语音转文字，一共生成了4个12kb的文本文件，建索引也没问题，但是到最后调模型总结就会出错。用GPT和google查了半天，也尝试自己对比转录的文本和您之前的案例中使用的朝花夕拾的文本，确实没看出差别，最终也没能解决，只好来求助老师了，谢谢！

&#47;usr&#47;local&#47;lib&#47;python3.9&#47;dist-packages&#47;llama_index&#47;langchain_helpers&#47;text_splitter.py in split_text_with_overlaps(self, text, extra_info_str)
    155             num_cur_tokens = max(len(self.tokenizer(cur_token)), 1)
    156             if num_cur_tokens &gt; effective_chunk_size:
--&gt; 157                 raise ValueError(
    158                     &quot;A single term is larger than the allowed chunk size.\n&quot;
    159                     f&quot;Term size: {num_cur_tokens}\n&quot;

ValueError: A single term is larger than the allowed chunk size.
Term size: 683
Chunk size: 358Effective chunk size: 358</div>2023-04-20</li><br/><li><img src="" width="30px"><span>极客用户</span> 👍（0） 💬（0）<div>vad模型可以做分割</div>2024-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/f1/7d21b2b0.jpg" width="30px"><span>方梁</span> 👍（0） 💬（0）<div>很好</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/b0/abb7bfe3.jpg" width="30px"><span>小雨青青</span> 👍（0） 💬（1）<div>老师，我的请求被拒绝了，这种怎么办呢？ openai.RateLimitError: Error code: 429 - {&#39;error&#39;: {&#39;message&#39;: &#39;Your access was terminated due to violation of our policies, please check your email for more information. If you believe this is in error and would like to appeal, please contact us through our help center at help.openai.com.&#39;, &#39;type&#39;: &#39;access_terminated&#39;, &#39;param&#39;: None, &#39;code&#39;: &#39;access_terminated&#39;}}</div>2023-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/60/70/6e816acc.jpg" width="30px"><span>Mr.wu</span> 👍（0） 💬（0）<div>请教一下whisper能读取流式文本输出语音么，接gpt要等待输出完毕后再转文本延迟太久了，实时交互体验不好</div>2023-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c3/94/e89ebc50.jpg" width="30px"><span>神毓逍遥</span> 👍（0） 💬（1）<div>语音转文本，然后本地转录的开源模型有推荐吗</div>2023-06-26</li><br/><li><img src="" width="30px"><span>Geek_083973</span> 👍（0） 💬（0）<div>老师，chatgpt是不是不支持根据文本生成语音
</div>2023-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/71/25/e9bad0b3.jpg" width="30px"><span>树静风止</span> 👍（0） 💬（0）<div>显存大小限制生产力😂</div>2023-04-19</li><br/>
</ul>