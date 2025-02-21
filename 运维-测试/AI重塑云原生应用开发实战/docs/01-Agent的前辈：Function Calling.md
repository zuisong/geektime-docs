你好，我是邢云阳。

自2023年3月 ChatGPT 在中国爆火以来，大模型已经悄然改变了许多人的提问方式，尤其是在互联网圈子里。从以前的“有问题，Google 一下”，到现在的“先问问大模型”，这种转变反映了技术对日常生活的深远影响，比如图中这位女士就将 ChatGPT 使用的淋漓尽致。

![](https://static001.geekbang.org/resource/image/d6/23/d608212c2ebb73c43ee94353f6021923.jpg?wh=968x961)

但是在使用过程中，我们会发现，有时大模型并不是万能的，它会一本正经的给出错误答案，业界把这种现象称之为“幻觉”。比如我问 ChatGPT-4o 一个它肯定不会的问题。

![图片](https://static001.geekbang.org/resource/image/12/ce/126d324784yy8bfb4d2ff9fc66475fce.png?wh=1221x505)

我们会发现，大模型给出了看似正确实则“废话”的答案。

再比如，我问一道小学一二年级的数学题：

![图片](https://static001.geekbang.org/resource/image/34/6e/342d4b45a41122d6868b5686d546586e.png?wh=1183x264)

我们很容易知道1+2+3+4-5-6=-1，但大模型给我们的答案是0。

“幻觉”出现的原因其实很简单。我们知道作为人类来说，即使是才高八斗，学富五车，也不可能什么都懂，于是就有这样一种人，为了面子，在遇到不会的问题时，也要强行给出一个模模糊糊的答案，我们称之为不懂装懂。

同样，作为大模型，训练数据是有限的，特别是对于一些垂直领域以及实时性的问题，例如附近哪有加油站？今天的茅台股票多少钱一股？大模型是无法给出正确的回答的。那大模型为什么也处理不了小学数学题呢？这是因为大模型的训练方法是通过学习语言的结构和模式，使得其能够生成与人类语言相似的文本，而不是针对数学问题这种精确逻辑做的训练，因此它的数学能力很弱。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/fd/dc/8c394a51.jpg" width="30px"><span>刘蕾</span> 👍（4） 💬（1）<div>没看懂，Tool里面没有定义加法实现。还是用大语言模型给出结果，这样用function call有什么好处?</div>2024-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/33/1b7eb2cd.jpg" width="30px"><span>日月星辰</span> 👍（0） 💬（1）<div>下面是我这边执行结果的输出，想请教老师，为什么这里会多次调用函数
2025&#47;02&#47;10 13:22:45 message_store.go:44: {ID:0194f006b99eab2c83e6d4ebde00af4f Object:chat.completion Created:1739193760 Model:deepseek-ai&#47;DeepSeek-V3 Choices:[{Index:0 Message:{Role:assistant Content: Refusal: MultiContent:[] Name: FunctionCall:&lt;nil&gt; ToolCalls:[{Index:&lt;nil&gt; ID:0194f006cc4a3475b18692239a8c0e41 Type:function Function:{Name:AddTool Arguments:{&quot;numbers&quot;:[1,2,3,4]}}}] ToolCallID:} F。。。]}
2025&#47;02&#47;10 13:22:45 chat.go:49: 大模型回复的内容:
2025&#47;02&#47;10 13:22:45 chat.go:50: 大模型选择的工具是: [{&lt;nil&gt; 0194f006cc4a3475b18692239a8c0e41 function {AddTool {&quot;numbers&quot;:[1,2,3,4]}}}]
函数计算结果:  10
2025&#47;02&#47;10 13:22:47 message_store.go:44: {ID:0194f006cd150a0。。。。:47 GMT]]}
2025&#47;02&#47;10 13:22:47 chat.go:49: 大模型回复的内容:
2025&#47;02&#47;10 13:22:47 chat.go:50: 大模型选择的工具是: [{&lt;nil&gt; 0194f006d51bf7375ffe69a9b6fcbb08 function {AddTool {&quot;numbers&quot;:[1,2,3,4]}}}]
函数计算结果:  10
2025&#47;02&#47;10 13:22:49 message_store.go:44: {ID:0194f006d59cff7a0964。。。。}
2025&#47;02&#47;10 13:22:49 chat.go:49: 大模型回复的内容:
2025&#47;02&#47;10 13:22:49 chat.go:50: 大模型选择的工具是: [{&lt;nil&gt; 0194f006de23c39d1001e9c67f5b829e function {AddTool {&quot;numbers&quot;:[1,2,3,4]}}}]
函数计算结果:  10
2025&#47;02&#47;10 13:22:53 message_store.go:44: {ID:0194f006de9。。。。]}
2025&#47;02&#47;10 13:22:53 chat.go:49: 大模型回复的内容:
2025&#47;02&#47;10 13:22:53 chat.go:50: 大模型选择的工具是: [{&lt;nil&gt; 0194f006ecb585e948c052459e301020 function {AddTool {&quot;numbers&quot;:[1,2,3,4]}}}]
函数计算结果:  10
2025&#47;02&#47;10 13:22:57 message_store.go:44: {ID:0194f006e。。。]]}
大模型的最终回复:  &lt;｜tool▁calls▁begin｜&gt;&lt;｜tool▁calls▁begin｜&gt;&lt;｜tool▁call▁begin｜&gt;function&lt;｜tool▁sep｜&gt;AddTool
```json
{&quot;numbers&quot;:[1,2,3,4]}
```&lt;｜tool▁call▁end｜&gt;&lt;｜tool▁calls▁end｜&gt;</div>2025-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/e5/6b/17de4410.jpg" width="30px"><span>🤡</span> 👍（0） 💬（1）<div>遇到一个奇怪的问题
代码中需要去计算 prompt := &quot;1+2-3+4-5+6=? Just give me a number result&quot; 

按照老师给的代码跑，会在循环中有好几轮计算，每次将计算结果附加到 messageStore 后面
我修改代码将计算过程打印在命令行，每一轮计算使用 ----- 符号分隔
第一轮计算调用  addTool 计算出 1 2 4 6 之和为13 
第二轮计算调用 subTool 计算出 3 5 只差 为 -2 （这里有问题）
第三轮得出结论 最终计算结果为 5 
这里我的问题是为什么 在 第二轮计算出的结果是 -2 ，添加到messageStore中，居然最后能得出正确的答案，本质上第二轮计算应该是 -3 -5 = -8 才是合理的
后面又使用 go run main.go 多次实验都有同样的问题，请问下这个是什么原因呢？？

附加某次实验的输出：
大模型选择的工具是:  [{0xc0004c9bc0 call_81af19d5cf3247a99b0d45 function {AddTool {&quot;numbers&quot;: [1, 2, 4, 6]}}}]
函数计算结果:  13
--------------
大模型选择的工具是:  [{0xc000014a50 call_d7719388d48d42e5994cb0 function {SubTool {&quot;numbers&quot;: [3, 5]}}}]
函数计算结果:  -2
--------
大模型的最终回复:  The result of the calculation \( 1 + 2 - 3 + 4 - 5 + 6 \) is \( 5 \).</div>2025-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/33/b4bb0b9c.jpg" width="30px"><span>仲玄</span> 👍（0） 💬（1）<div>AddTool和SubTool的函数是需要用户自己实现吗? </div>2024-12-27</li><br/>
</ul>