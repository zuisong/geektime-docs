你好，我是徐文浩。

过去几讲里，我们一起为AI加上了语音能力。而且相对于大语言模型，语音识别和语音合成都有完全可以用于商业应用的开源模型。事实上，Huggingface的火爆离不开他们开源的这个Transformers库。这个开源库里有数万个我们可以直接调用的模型。很多场景下，这个开源模型已经足够我们使用了。

不过，在使用这些开源模型的过程中，你会发现大部分模型都需要一块不错的显卡。而如果回到我们更早使用过的开源大语言模型，就更是这样了。

在课程里面，我们是通过用Colab免费的GPU资源来搞定的。但是如果我们想要投入生产环境使用，免费的Colab就远远不够用了。而且，Colab的GPU资源对于大语言模型来说还是太小了。我们在前面不得不使用小尺寸的T5-base和裁剪过的ChatGLM-6B-INT4，而不是FLAN-UL2或者ChatGLM-130B这样真正的大模型。

那么，这一讲我们就来看看，Transformers可以给我们提供哪些模型，以及如何在云端使用真正的大模型。而想要解决这两个问题啊，都少不了要使用HuggingFace这个目前最大的开源模型社区。

## Transformers Pipeline
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（0） 💬（1）<div>从下面这段代码看在 Endpoint 上部署自己需用的模型后，得到一个&quot;个人&quot;的 API_URL 接口，每次任务还是从用户端发起请求，结果再从云端返回。单次请求任务也就完成了，但如果涉及大量的运算，一来一往会消耗大量时间在&quot;路&quot;上。可以将数据打包放在离&quot;计算中心&quot;近处，完成计算后再一次性将结果打包返回吗? 还是有其它的解决方法? 请老师指点迷津。

API_URL = &quot;https:&#47;&#47;abmlvcliaa98k9ct.us-east-1.aws.endpoints.huggingface.cloud&quot;

text = &quot;My name is Lewis and I like to&quot;
data = query({&quot;inputs&quot; : text}, api_url=API_URL)

print(data)</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/a7/e9/fe14835f.jpg" width="30px"><span>芋头</span> 👍（0） 💬（1）<div>想复现graph-gpt https:&#47;&#47;graphgpt.vercel.app&#47;, 即用纯文本，通过模型生成知识图谱。想问问大大能教一下吗
</div>2023-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8e/27/d90028c3.jpg" width="30px"><span>Meadery</span> 👍（0） 💬（1）<div>DLL load failed while importing _imaging: 找不到指定的模块。是什么问题啊
</div>2023-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/f2/db90fa96.jpg" width="30px"><span>Oli张帆</span> 👍（5） 💬（0）<div>HuggingFace是个好东西！</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/cc/9f90b797.jpg" width="30px"><span>77</span> 👍（0） 💬（0）<div>看晚了 这课程着实有用</div>2024-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3f/9d/c59c12ad.jpg" width="30px"><span>实数</span> 👍（0） 💬（1）<div>咨询下老师，公司想用大模型，但是又不想贡献出来数据给外部模型怎么破？
私有化部署向量化数据库和模型吗</div>2023-08-24</li><br/><li><img src="" width="30px"><span>Geek_8a8c75</span> 👍（0） 💬（0）<div>老师您好，我想请教一下，如果我想更改 huggingface 上下载下来的模型结构，比如我想在模型中间添加一层全连接层。如果这样的话，我该怎么做呢，因为 huggingface 把api包装的太好了，如果是平时自己写的模型的话都是继承了 nn.Module 模块的，可是 huggingface 下载下来的模型我不知道这些代码在哪里，这个代码也都是存在于 transformers 包里的吗？如果我想这么做的话，老师可不可以给我一个方向，让我去查阅什么资料或者从哪里入手呀。</div>2023-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/a8/adf7e4d1.jpg" width="30px"><span>sanpang228</span> 👍（0） 💬（0）<div>Endpoint 页面要绑定一个信用卡，请问是需要绑卡才能用吗？是外国信用卡吗？</div>2023-07-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epmAicDUiaUdtLhVwSs6fT0yx69ibWy6ia46ZD4vblGtyee8QFz71icKZJkzccAFG3zHnMngSz7WeGBtKw/132" width="30px"><span>小神david</span> 👍（0） 💬（0）<div>希望huggingface越办越好</div>2023-05-01</li><br/>
</ul>