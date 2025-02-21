你好，我是徐昊，今天我们来继续学习AI时代的软件工程。

上节课，我们通过将LLM看作一个迁移学习平台，理解了在提示词中上下文和任务的不同作用，并利用这个特性，构造了基于LLM的知识提取与应用的流程：通过聚焦在上下文，使用不同的问题反馈以提取知识，再将提取的知识与具体的任务结合，完成知识的应用过程。

这样的流程对于显式知识，或是隐式知识都有极高的提取和传递效率。但是对于知识过程中的核心——不可言说知识要怎么处理呢？这就是我们今天要讨论的问题。

在前面的课程中，我们已经知道，不可言说知识的应用会产生清晰（Clear）和庞杂（Complicated）认知模式，而不可言说知识的学习会产生复杂（Complex）认知模式。不同的认知行为模式具有不同的认知行为，因而与LLM交互的模式也就不尽相同。不同的交互模式，是我们处理不可言说知识应用和学习的关键。

## 与LLM交互的模式

由于LLM的回答具有不确定性，我们与LLM的默认交互模式是**复杂认知模式**，它的表现是：

- **探测（Probe）**：我们向LLM提出问题或者任务，LLM帮助我们执行这个任务，并产生了初始结果；
- **感知（Sense）**：我们依照LLM返回的结果，思考哪些地方是我们不满意的，或者需要进一步了解的。然后我们提出新的问题，或者是重新调整初始问题；
- **响应（Respond）**：通过不同的问题调整，最终拿到满意的结果。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/56/29877cb9.jpg" width="30px"><span>临风</span> 👍（48） 💬（9）<div>    分清楚行为模式真的很重要，过去在使用LLM时，完全是凭直觉的，结果就是有的时候符合预期，有的时候就完全没用。当然我也知道，如果回答的不够好，就需要补充背景知识。这又产生了新的问题，就是补充背景知识也是凭直觉的，所以有时后写了半天提示词，最后发现还不如自己写算了。而在行为模式的思考框架下，你可以清楚的根据自己当下的问题和自己所掌握的知识来决定采用什么行为模式，再根据不同的行为模式才有不同的提示词方法。
    好，那回到开发场景。什么时候应该采用清晰模式，比如为一段代码补充注释、编写UT、重构、写一个方法&#47;函数等，基本上描写清楚prompt并给LLM源代码就足够了，这也是我使用LLM最常用的方式。然后是庞杂模式和复杂模式，这也是之前用不好LLM的场景。我们一定要先弄清楚自己掌握的知识是否能覆盖问题（不可言说的知识是否充分学习），如果不能，那就是复杂模式，你只能先进行探测。借助LLM已经掌握的海量知识，给自己思考和启发，不断迭代。当充分掌握知识后，再进入庞杂模式，拆分TODO LIST，每个TODO项其实就是一个清晰模式的行为。
    突然想到一句话，“我们不生产水，我们只是大自然的搬运工”，但你仔细想想就知道，他真的只是做了搬运吗？他做的是对搬运水的知识工程管理，否则怎么能做到人人都可以用2元的价格就获取到一瓶水呢？背后凝结的供应链知识、营销网络、物流管理才是他的核心竞争力。LLM是很厉害，拥有一个人一生都无法学完的知识，但知识本身是没有用的，知识的应用才能产生价值。在LLM时代的我们同样可以说，“我们不生产知识，我们只是知识的搬运工”，或许这也是这个时代给予我们的机会。</div>2024-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（2） 💬（1）<div>🤔☕️🤔☕️🤔
【R】 默认的LLM交互模式 = 复杂认知模式（PSR=Probe&#47;Sense&#47;Respond）
区分：LLM的交互模式 vs 我们的认知行为
清晰时，指导性提示词（Instruction Prompting）；
庞杂时，知识生成（Generated Knowledge），用思维链生成任务列表，即不可言说知识的提取，达到思路对齐；
复杂时，获取思路是重点；
【.I.】LLM在我面前，跟白纸在我面前，都会给我带来大脑空白感，不知道敲入点啥，不知道写上点啥。
差别在于，前者，稍微敲入点东西后，我会被输出的内容带着走，琢磨起我想要啥，对照着LLM给我点啥；后者，顺意写出几个字、几个词、几句话后，我会有种流出来的感觉，我不要去审视流出的是啥，降低流出的任何阻力，让它们自然流一会儿。
【.I.】清晰时，照我说的干；庞杂时，给我说清楚，到底想咋干；复杂时，先跟我说说，有哪些思路，让我琢磨一下；
【Q】到底是LLM提取我的不可言说知识，还是我提取LLM自己的不可言说知识，还是我们互相在提取？ 怎么判断已成功提取出不可言说知识？
— by 术子米德@2024年3月18日</div>2024-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（2） 💬（0）<div>LangChain LCEL 代码如下：

llm = Tongyi()

# Define the API design and implementation prompt templates
api_design_prompt = ChatPromptTemplate.from_template(
    &quot;&quot;&quot;\
    需求背景
    =======
    {requirements}
    
    API要求
    =====
    API返回的结果是json格式；
    当查找的SKU不存在时，返回404；
    按关键搜索功能使用POST而不是GET；
    
    任务
    ===
    按照API要求为需求设计RESTful API接口。使用RAML描述。
    &quot;&quot;&quot;
)

api_implementation_prompt = ChatPromptTemplate.from_template(
    &quot;&quot;&quot;\
    需求背景
    =======
    {requirements}
    
    API
    ===
    {API}
    
    要求
    ===
    使用Java实现
    
    任务
    ===
    按照要求，根据需求实现API中提及的RESTful API
    &quot;&quot;&quot;
)

# Output parser remains the same as it just converts model output to string
output_parser = StrOutputParser()

requirements = &quot;&quot;&quot;\
目前我们在编写一个产品目录服务，通过API提供所有可售商品的详细信息。
商品详细信息包括：SKU，商品名字，不同的产品选项，以Markdown形式保存的商品详情；
此API包含列出所有商品，按SKU查看某个商品，按照分类列出商品以及按关键词搜索的功能；
使用Java编写。
&quot;&quot;&quot;

# Designing API
api_design_result = (api_design_prompt | llm | output_parser).invoke({&quot;requirements&quot;: requirements})
print(&quot;================================API设计结果:\n&quot;, api_design_result)

# Implementing API
api_implementation_result = (api_implementation_prompt | llm | output_parser).invoke({
    &quot;requirements&quot;: requirements,
    &quot;API&quot;: api_design_result
})
print(&quot;================================API实现结果:\n&quot;, api_implementation_result)
</div>2024-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/f9/69/106f4ff9.jpg" width="30px"><span>hakunamatata</span> 👍（2） 💬（0）<div>https:&#47;&#47;www.youtube.com&#47;watch?v=ug8XX2MpzEw&amp;t=11s
Dave Thomas在演讲里面讲到(37:50)过一点,通过潜意识传递的信息效率最高。因为这些“信息”的“传递”几乎是“自动”完成的(另外一种“认知模式”)。

比如不要读下面的一段话



“I TOLD YOU NOT TO READ IT!”
</div>2024-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/e3/44/791d0f5e.jpg" width="30px"><span>大卫</span> 👍（2） 💬（0）<div>清晰的问题，清晰的期望答案 =&gt; 正确的文档代码测试等
清晰的问题，模糊的解决方案 =&gt; 达成一致的TODO
模糊的问题，未知的思路 =&gt; 获取启发来让问题定义的更准确
所谓不可言知识的提取可以认为是将requirements不断具象化为TODO的整个思维过程</div>2024-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（1） 💬（0）<div>🤔☕️🤔☕️🤔
【Q】对于提取的知识，怎么样的传递是最有效率的？
【A】文生图，时序图和状态图，前者时间上的可视化，后者空间上的可视化。
— by 术子米德@2024年3月18日</div>2024-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（0）<div>🤔☕️🤔☕️🤔
【.I.】知识我已经掌握，面对问题，直接分类时我清晰（Clear），要做分析时我庞杂（Complicated），这都能解决问题到预期的结果。
若是问题的结果不符合预期，调头回来看问题，大意了，被问题的表象遮蔽，顺着老思路去解决，实际问题要揭开一层再看、或要换个角度再看，问题不再是那个问题，问题变成个新问题。
这样错中求解的经历，这样打破旧思路的经验，正是学到新知识的过程，所谓我在复杂（Complex）中探测（Probe）— 感知（Sense）— 响应（Respond）。即：所谓的Probe是在自以为正确的路上，掉进坑里的时刻，在那个知道自己原来已经被困住的时刻，明白发现，自己已不再Clear或Complicted的Respond，瞬间切换到Complex的Probe。这时候我要的思路，如何才能爬出坑。
— by 术子米德@2024年5月30日</div>2024-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>1. 介绍背景：尽量缩小背景范围，突出重点
2. 描述问题：尽量拆分成多个小问题，一个问题只有一个关注点

例如：
介绍背景：使用 DDD 设计一个图片管理系统的领域模型
问题描述：
1. 有哪些领域对象？
2. 每个领域对象都有哪些关键属性？
3. 领域对象之间的关系是什么？
4. 对接不同云服务商的图片存储服务时，如何通过领域模型实现开闭原则？</div>2024-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/f6/eca921d9.jpg" width="30px"><span>赫伯伯</span> 👍（0） 💬（0）<div>最近看过一些 TW 组织的 AI 赋能软件研发的专场分享，涉及业务分析，编码，产品设计，交互设计和测试。每个嘉宾都很优秀，不过分享这种形式，内容上总是支离破碎的，希望徐老师的课程能给我带来体系化的思考和认识</div>2024-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（0） 💬（0）<div>根据在工作遇到的问题,有意识的根据老师教的问题分类方法,把问题分类后,与GPT进行问答练习,多练才能找到与GPT配合的感觉,和形成自己的模板.</div>2024-03-18</li><br/>
</ul>