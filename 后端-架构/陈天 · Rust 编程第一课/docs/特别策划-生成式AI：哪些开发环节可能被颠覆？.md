你好，我是编辑叶芊。

4月份，我们和Tubi 组织了一场坐标北京的线下meetup活动，陈天老师与来自各个领域的工程师交流了三大话题：了解和拥抱 AIGC、AI 2.0 时代下程序员的硬核技能需求描述和架构设计、Serverless Rust。

可能有同学未能参与，这里我简单整理了第一场AIGC分享的要点内容，你也可以看视频：[如何以更有准备的姿态拥抱 AIGC 新时代](https://www.bilibili.com/video/BV1RP411S78r/?share_source=copy_web)。如果你对其他话题更感兴趣，可以看文末的其他资料链接。

* * *

AIGC发展到现在，其实也就是最近三个月被 ChatGPT带火的， ChatGPT你可以理解为是所有AIGC的一个大脑，其他各种各样的model都是四肢，由 ChatGPT指挥，那目前被热议的GPT或者LLM，究竟是个什么东西？我们和它对话的时候到底发生了什么？作为程序员我们如何高效使用ChatGPT？

我们开始今天的交流。

## LLM 或者 GPT究竟是什么?

GPT，generative pretrained transformer，预训练的大语言模型，GPT3.5是一个有1,700亿参数的模型，GPT4的模型大小OpenAI并没有公布，有人说可能是GPT3的100倍甚至更多，所以如果我们把一个参数看成一个神经元，GPT4已经接近人脑神经元的量级，而且按这个趋势看，未来GPT一定会超过人脑神经元的量级。所以如果真的把人类产生的所有知识都拿给GPT训练，能训练出一个什么样的怪物呢？我们谁也不知道。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（6） 💬（0）<div>勘误：
chatGPT →ChatGPT 

instruction，给一些高质量的例子帮助 GPT 进一步理解。
&#47;&#47;应为：example，给一些高质量的例子帮助 GPT 进一步理解。
另外这几点的单词建议首字母大写。</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/3a/60/6ab05338.jpg" width="30px"><span>大汉十三将</span> 👍（0） 💬（0）<div>更新了！</div>2023-06-26</li><br/>
</ul>