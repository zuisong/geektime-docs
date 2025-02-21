你好，我是黄佳，欢迎来到LangChain实战课！

大模型的成功，在很大程度上依赖于用户的输入来引导对话生成。如果用户能够详细描述他们的任务和需求，并与ChatGPT建立一个连贯的聊天上下文，那么ChatGPT往往能提供更精确和高质量的答案。但是，为模型提供这种引导是一项既费时又费力的任务。

这就引出了一个有趣的问题：**能否让ChatGPT自己生成这些引导文本呢？**

基于这个想法，KAUST（阿卜杜拉国王大学）的研究团队提出了一个名为CAMEL的框架。CAMEL采用了一种基于“角色扮演”方式的大模型交互策略。在这种策略中，不同的AI代理扮演不同的角色，通过互相交流来完成任务。

## CAMEL 交流式代理框架

下面我们一起来看看CAMEL——这个多AI通过角色扮演进行交互的框架，以及它在LangChain中的具体实现。

![](https://static001.geekbang.org/resource/image/57/c3/578c7a5a91ffe7007c0fe4cea3d20bc3.png?wh=694x290)

CAMEL，字面意思是骆驼。这个框架来自于论文《[CAMEL: Communicative Agents for “Mind” Exploration of Large Scale Language Model Society](https://arxiv.org/pdf/2303.17760.pdf)》（CAMEL：用于大规模语言模型社会的“心智”探索的交流式代理）。这里面所谓的CAMEL，实际上来自**沟通（也就是交流）**、**代理**、**心智**、**探索**以及 **LLM** 这五个单词的英文首字母。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（6） 💬（1）<div>一、感觉可以再增加一个方案评价的角色，每一轮对结果进行挑战和质疑，帮助AI进一步进行优化，这样方案是不是就可以用于实操了。
以鲜花营销方案为例，可以这样调整一下：
1、营销要求进一步具体化，给出期望达到的目标
2、每一轮营销专员给出方案后，花店老板对给出的方案进行评价，并进一步给出优化要求
3、营销专员根据评价和进一步的要求，改进自己的方案
4、当花店老板评价方案达标时，结束循环
最后应该可以形成一个完善、可行的方案。

二、此外，花店老板、营销专员可以交叉使用不同的大模型，相互碰撞，将碰撞结果进行评分，最终由GPT给出评分最高的三个方案，可以得到更好的结果。</div>2023-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4a/ee/fe035424.jpg" width="30px"><span>棟</span> 👍（2） 💬（1）<div>您好，老师，请教一个疑惑，怎么限制这个对话达到某个token数值前停止，防止超出token限制，而且要得出答案。</div>2023-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/e3/c49aa508.jpg" width="30px"><span>鲸鱼</span> 👍（0） 💬（2）<div>老师，我运行您的demo，输出的结果不是很理想。总是花店老板自己就开始给方案了，然后营销专员就简单重复花店老板的方案；对话到后面花店老板开始问营销专员下一个请求了。重复了好几次都是这样

开头的对话==================
AI User (花店老板):

指令：确定目标人群。
输入：夏季玫瑰之夜的目标人群是年龄在25-45岁的城市居民，对浪漫活动和花卉有兴趣的人群。他们可能是情侣、夫妻或单身人士，他们喜欢参加社交活动并寻求独特的体验。他们有一定的消费能力，愿意为特殊的活动支付适当的费用。


AI Assistant (花店营销专员):

解决方案：夏季玫瑰之夜的目标人群是年龄在25-45岁的城市居民，对浪漫活动和花卉有兴趣的人群。他们可能是情侣、夫妻或单身人士，他们喜欢参加社交活动并寻求独特的体验。他们有一定的消费能力，愿意为特殊的活动支付适当的费用。下一个请求。


最后的对话==================

AI User (花店老板):

指令：设计广告和社交媒体推广计划。
输入：设计夏季玫瑰之夜的广告和社交媒体推广计划需要考虑以下方面：
1. 广告渠道：选择适合目标人群的广告渠道，如报纸、杂志、户外广告牌等。
2. 广告内容：设计吸引人的广告内容，包括活动主题、时间、地点和参与方式等信息。
3. 社交媒体平台：选择适合目标人群的社交媒体平台，如Facebook、Instagram、微信等。
4. 社交媒体内容：制作有吸引力的社交媒体内容，包括活动海报、短视频、活动介绍等。
5. 广告预算：确定广告投放的预算，并根据预算选择合适的广告形式和频率。
6. 推广策略：制定推广策略，如合作推广、优惠活动、分享抽奖等，以吸引更多参与者。
请提供下一个请求。


AI Assistant (花店营销专员):

解决方案：设计夏季玫瑰之夜的广告和社交媒体推广计划如下：
1. 广告渠道：选择适合目标人群的广告渠道，如在当地报纸和杂志上发布广告，租用户外广告牌等。
2. 广告内容：xxx字数超限以xxx代替
3. 社交媒体平台：xxx
4. 社交媒体内容：xxx
5. 广告预算：xxx
6. 推广策略：xxx
下一个请求。


AI User (花店老板):

&lt;CAMEL_TASK_DONE&gt;


AI Assistant (花店营销专员):

任务完成。

</div>2023-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/70/f9/352365e3.jpg" width="30px"><span>徐冰</span> 👍（3） 💬（1）<div>貌似这种模式对大模型本身要求还有一点高。实测下来，3.5turbo会逐步变成老板自己给方案，但是格式起码还一直对的。换成通义千问qwen-max测试，结果聊着聊着连格式都不跟随了，两个代理最后 相互加油变成死循环。尝试调整了pompt也效果不大。o(╥﹏╥)o</div>2024-01-31</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>将课程代码的大模型修订为国产通义千问模型qwen-turbo，测试结果理想。

## 新代码1
在from 代码后，增加：
llm = ChatOpenAI(
        model_name=&quot;qwen-turbo&quot;, #用通义模型
        api_key=“API_KEY”, #填写你自己的DASHSCOPE_API_KEY
        base_url=&quot;https:&#47;&#47;dashscope.aliyuncs.com&#47;compatible-mode&#47;v1&quot;
	）

## 旧代码2
model: ChatOpenAI,
task_specify_agent = CAMELAgent(task_specifier_sys_msg, ChatOpenAI(model_name = &#39;gpt-4&#39;, temperature=1.0))
assistant_agent = CAMELAgent(assistant_sys_msg, ChatOpenAI(temperature=0.2))
user_agent = CAMELAgent(user_sys_msg, ChatOpenAI(temperature=0.2))
## 新代码2
model: llm,
task_specify_agent = CAMELAgent(task_specifier_sys_msg, llm)
assistant_agent = CAMELAgent(assistant_sys_msg, llm)
user_agent = CAMELAgent(user_sys_msg, llm)

</div>2024-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fa/b2/d637b234.jpg" width="30px"><span>账号已注销...</span> 👍（1） 💬（0）<div>老师，有可运行的jupyter代码吗？这样看起来比较直观</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第18讲打卡~</div>2024-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/7f/ea/b33596d1.jpg" width="30px"><span>colvin.zhang</span> 👍（0） 💬（1）<div>ask_specifier_prompt = &quot;&quot;&quot;这是一个{assistant_role_name}将帮助{user_role_name}完成的任务：{task}。请使其更具体化。请发挥你的创意和想象力。请用{word_limit}个或更少的词回复具体的任务。不要添加其他任何内容。&quot;&quot;&quot;
task_specifier_template = HumanMessagePromptTemplate.from_template( template=task_specifier_prompt)

老师demo程序本身没啥问题，变量命令建议交换一下

ask_specifier_template= &quot;&quot;&quot;这是一个{assistant_role_name}将帮助{user_role_name}完成的任务：{task}。请使其更具体化。请发挥你的创意和想象力。请用{word_limit}个或更少的词回复具体的任务。不要添加其他任何内容。&quot;&quot;&quot;
task_specifier_prompt = HumanMessagePromptTemplate.from_template( template=task_specifier_prompt)</div>2023-10-31</li><br/>
</ul>