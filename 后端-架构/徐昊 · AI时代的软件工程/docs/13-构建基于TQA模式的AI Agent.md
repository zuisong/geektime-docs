你好，我是徐昊，今天我们来继续学习AI时代的软件工程。

上节课我们介绍了三种通过大语言模型（Large Language Model，LLM）辅助用户故事编写的形式：通过LLM提取不可言说的业务知识，修改用户故事以及补充完善验收条件。

这三种方式都需要使用到一种特殊的LLM交互模式TQA（Thought-Question-Answer），TQA的主要用途是收集人的反馈，用以提高生成内容的质量。TQA是从推理行动（Reason-Act，ReACT）演化出来的交互模式。那么今天我们就来学习如何构造一个TQA的AI Agent。

## 推理行动（Reason-Act）

ReAct是一种专门为了LLM能执行某些操作任务而设计的模式。举个例子，当LLM收到一个问题时，它可以选择执行一个动作来检索相关信息，然后利用检索到的信息来回答问题。通过ReAct，LLM可以超越其常规功能，利用自然语言推理解决复杂任务。

ReAct也是目前最热门的一个LLM模式。前一阵子（2023年底）大火的ChatGPT Plugin，还有Microsoft开源的Semantic Kernel都是基于ReAct模式。

一个典型的ReAct Prompting通常包含四个部分：
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（3）<div>🤔☕️🤔☕️🤔
【R】TQA = &lt;想&gt;Thought-&lt;问&gt;Question-&lt;答&gt;Answer
（an evolution of ReACT&lt;Thought&#47;Action&#47;Action Input&#47;Observation&gt;）
用于：提取不可言说的业务知识、修改用户故事、补充完善验收条件。
【Q】告诉LLM从哪方面想&lt;Thought&gt;，然后LLM根据上下文、进行推理后会向我发问&lt;Question&gt;，由我来回答&lt;Answer&gt;，再继续来几轮TQA，如此这般嘛？
如果每轮的Answer由我来回答，那下一轮的Thought是我每次新给出，还是预定义要进行哪几方面的Thought？
— by 术子米德@2024年4月7日</div>2024-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（4） 💬（0）<div>实践出真知，直接用我的代码在本地跑起来～

我把老师的方法和 Prompt 做了微调，不需要处理 history 和 Stop Sequence，也不需要手写OutputParser，感觉自己实现还是比较优雅的哈哈~

代码在文章最后~：https:&#47;&#47;mp.weixin.qq.com&#47;s?__biz=Mzg3MDg5MzYyMA==&amp;mid=2247483961&amp;idx=1&amp;sn=792be3eb1c598edd8e256e86359aa398&amp;chksm=ce879362f9f01a74ead04c804e77f9a93e802f51c506cdb6520d641137c4db82576cdccfe255&amp;token=1482009703&amp;lang=zh_CN#rd</div>2024-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（0）<div>原文：模板中 {context} 表示了业务整体的解决方案。

这里不准确，根据上一讲[1]， context 不仅包含了整体解决方案，还包含了用户旅程。


[1] 12讲的原文：“ 为 LLM 提供整体解决方案和用户旅程作为业务背景说明；”</div>2024-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（0）<div>思考题：请根据不同的用户故事场景（前台，API），改写 TQA 模板，增加 LLM 反馈的内容。

首先，这个思考题我就没太搞懂，我是这么理解的：改写TQA模板，使 LLM 返回 API 文档。
（不知道这样理解对嘛？）

那么，对于这个思考题，我的想法是，修改Prompt的第一句和最后一句就可以了？

比如，
把“You are a business analyst who is familiar with specification by example. ” ，
改成 “You are a software engineer expert who is familar with REST and other best practices in API design.”

再把“Scenarios: List all possible scenarios with concrete example in Given&#47;When&#47;Then style”，
改成“Final Answers: Output the API document using RAML format.”</div>2024-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>TQA1 TQA2 包装成 bot 在 coze.com 上发布了「搜索路径 Bot Store -&gt; Learning -&gt; TQA」，效果没有直接使用 workflows 好「TQA2 的 bot 只有一轮就结束了， workflows 经过多轮才得出解决方案」

TQA1 开始数据
context
作为学校的教职员工，我希望学生可以根据录取通知将学籍注册到教学计划上，从而我可以跟踪他们的获取学位的进度
整个学籍管理系统是一个 Web 应用； 当教职员工发放录取通知时，会同步建立学生的账号；学生可以根据身份信息，查询自己的账号；在报道注册时，学生登录账号，按照录取通知书完成学年的注册；

story
1. 我希望学生可以根据录取通知将学籍注册到教学计划上
2. 作为学生，我希望登录之后接收到注册的通知，从而我可以不会错过学期注册的期限

TQA2 拼接 history 数据
context
作为学校的教职员工，我希望学生可以根据录取通知将学籍注册到教学计划上，从而我可以跟踪他们的获取学位的进度
整个学籍管理系统是一个 Web 应用； 当教职员工发放录取通知时，会同步建立学生的账号；学生可以根据身份信息，查询自己的账号；在报道注册时，学生登录账号，按照录取通知书完成学年的注册；

story
1. 我希望学生可以根据录取通知将学籍注册到教学计划上
2. 作为学生，我希望登录之后接收到注册的通知，从而我可以不会错过学期注册的期限

history
学生如何根据录取通知将学籍注册到教学计划上？登录教学系统后完成注册
学生何时可以注册学籍？收到注册手机短信后
学生如何登录账号来完成学年注册？使用手机号码登录注册
学生如何查询自己的账号？使用手机号码查询或注册成功后分配到的学号
学生注册学籍后，是否会收到通知？会收到手机短信通知
学生如何知道学期注册的期限？30天内完成注册</div>2024-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>coze 使用 2 个 workflows 半自动实现丐版 TQA

1. TQA_1：根据 context、story 进行提问
2. TQA_2：回答 TQA_1 的问题，并将回答手动录入 history，下一轮提问会知道上一轮的问题与答案
3. 重复多次 TQA_2，直到得出解决方案

测试数据

context
作为学校的教职员工，我希望学生可以根据录取通知将学籍注册到教学计划上，从而我可以跟踪他们的获取学位的进度
整个学籍管理系统是一个 Web 应用； 当教职员工发放录取通知时，会同步建立学生的账号；学生可以根据身份信息，查询自己的账号；在报道注册时，学生登录账号，按照录取通知书完成学年的注册；

story
1. 我希望学生可以根据录取通知将学籍注册到教学计划上
2. 作为学生，我希望登录之后接收到注册的通知，从而我可以不会错过学期注册的期限

TQA_2 中经过多轮循环得到了解决方案</div>2024-04-06</li><br/>
</ul>