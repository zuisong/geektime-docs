你好，我是郑晔！

前面我们已经了解了大模型的基本特点，知道了如何使用提示词与大模型沟通。你可能已经跃跃欲试，想要开发自己的大模型应用了。但在此之前，我们还是先要了解一下怎么使用大模型的 API 进行编程，这是编写大模型应用的基础。

众所周知，现在的大模型已经进入“百模大战”的阶段，各种大模型层出不穷，如果我们要学习大模型的 API，是不是要一个一个学过去呢？答案显然是否定的。虽然大模型数量众多，但就编程接口这件事来说，基本上都是大差不差的。以编程的术语来说，虽然实现各有差异，但接口基本上是统一的。只要学习了其中一个，相信其它 API 你也能够很快地上手。

既然要学习，我们还是要有一个具体的学习目标，我在这里选择的是 OpenAI API。

之所以选择它，自然是因为 GPT 模型给行业带来的影响，后来者多多少少都会参考它的 API 设计。此外，还有一个很重要的原因，它几乎成了行业的事实标准，现在很多项目选择提供兼容 OpenAI API。有一些中间件性质的项目，不管后台接入的是什么模型，给自己的用户提供的都是 OpenAI 兼容的 API。基于这样的现状，如果只学习一个 API，OpenAI API 是理所当然的选择。

## OpenAI API
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/db/95/daad899f.jpg" width="30px"><span>Seachal</span> 👍（2） 💬（1）<div>GTP 是行业标杆，很多国内大模型都会参考致敬它的 api， 我之前跑一个开源项目，因为没有搞定稳定的 openai key , 直接换成月之暗面 Kimi 的 api 和key, 其他代码都没改，完美运行。</div>2024-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b0/41/2c3ef65a.jpg" width="30px"><span>海洋</span> 👍（1） 💬（1）<div>请问，“为了模型兼容性，使用提示词返回json”能详细说下不</div>2024-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（1） 💬（1）<div>《大模型应用开发极简入门：基于GPT-4和ChatGPT》一书中也介绍了 Api 使用的相关细节，有兴趣的小伙伴可以参考了解 https:&#47;&#47;weread.qq.com&#47;web&#47;reader&#47;3fd32bd0813ab89c6g0150dfkc81322c012c81e728d9d180 。当然，官方文档是最权威的。</div>2024-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/57/1cebae66.jpg" width="30px"><span>YOUNG</span> 👍（0） 💬（1）<div>老师，能不能添加一些代码？看到代码运行的结果可以加深印象。</div>2024-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/dd/a6/4d0c9ee6.jpg" width="30px"><span>程序员一土</span> 👍（5） 💬（0）<div>国内可以用的一个代理平台，https:&#47;&#47;bewildcard.com&#47;i&#47;LIANG89</div>2024-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（3） 💬（0）<div>第5讲打卡~
工具参数（tools）是非常有用的功能，可以使模型生成指定格式的工具调用参数，同时也是实现 AI Agent 的基础~</div>2024-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/45/c8/1ccbb110.jpg" width="30px"><span>淡漠尘花划忧伤</span> 👍（0） 💬（0）<div>速记聊天补全接口的请求参数中，最核心的是模型和消息列表。参数：
核心参数（重要）
工程参数
工具参数（agent 关注）
模型参数</div>2025-02-09</li><br/>
</ul>