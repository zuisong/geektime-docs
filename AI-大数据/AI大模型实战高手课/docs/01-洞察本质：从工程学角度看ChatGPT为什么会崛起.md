你好，我是独行。

2022年11月底，OpenAI发布了ChatGPT，2023年1月注册用户超过一亿，成为历史上增长最快的应用，上一个纪录保持者是TikTok，注册用户超过一亿用时9个月。2023年3月开始，ChatGPT燃爆中国互联网界。

实际上国内外同一时期搞大模型的团队很多，为什么ChatGPT会突然火起来？还有在ChatGPT发布后，为什么各个大厂在短时间内相继发布大模型产品？比如3月百度发布文心一言，4月阿里云发布通义千问，5月科大讯飞发布星火认知大模型等等。

![](https://static001.geekbang.org/resource/image/67/f6/67b5bdf53481e6ba693f042yy76a80f6.png?wh=2558x558)

我们最容易想到的原因是，OpenAI在自然语言处理（NLP）方面取得了突破性的进展，这是技术层面看到的。实际上，ChatGPT背后包含了一系列的资源整合，包括技术、资金、大厂背书等等，以及多个国际巨头的通力合作，比如OpenAI、微软、NVIDIA、GitHub等。所以说，**ChatGPT不仅仅是技术上的突破，更是工程和产品的伟大胜利！**

那么ChatGPT具体是如何赢得这场胜利的呢？我们一一来看。

## NLP技术突破：强势整合技术资源

基于Transformer架构的语言模型大体上分为两类，一类是以BERT为代表的**掩码语言模型**（Masked Language Model，MLM），一类以GPT为代表的**自回归语言模型**（Autoregressive Language Model，ALM）。OpenAI的创建宗旨是：创建造福全人类的安全通用人工智能（AGI），所以创立之初就摒弃了传统AI模型标注式的训练方式，因为可用来标注的数据总是有限的，很难做得非常通用。那么为了实现AGI，OpenAI在技术上到底做对了什么呢？
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/bJjBw4nJOV2VFDibH86RicG3tA92ngUH7R0PRx5yZqhGmcWv5QPjWNFPafOIpDlHZ5BMnQH9a7r0S3Xhqa9w36NA/132" width="30px"><span>wlih45</span> 👍（0） 💬（1）<div>我认为从目前的技术来看还不可能代替，人类会根据所经历的事情去就行自我的一个反馈更改，但大模型用的啥数据训练出来就只知道啥，还无法不过的通过对话去就行回归训练</div>2024-08-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwL1khHEqadibhMpibdC6bQ875qUOUVzWUzOSGwJmwSvF7icIicnJQbAsMqkvuC6YIVNVJLrGU3xk6Tg/132" width="30px"><span>干就完了</span> 👍（6） 💬（1）<div>老师你好，问个问题：
有编程基础，没有深度学习和机器学习的基础，能看懂这门课吗？学完之后能达到什么程度？</div>2024-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/48/7dbd183b.jpg" width="30px"><span>zMansi</span> 👍（4） 💬（1）<div>看了chatgpt 4o发布会演示，感觉真的具备初步的人脑思维了，场景对话以及语气等等都让人觉得未来将至

在我身边目前感觉还是偏向提效类工具，没有代替到真实工作

老师身边有工作被替代了吗？</div>2024-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（2） 💬（1）<div>第1讲打卡~ AI已经可以代替很多人类的日常工作了，我自己比较常用的包括代码生成、代码翻译、文章摘要、搜索等。并且未来的应用场景应该会越来越广泛！</div>2024-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（2） 💬（1）<div>1、虽然不太想承认。但是AI现在确实已经具备了一定的人类思维，不过还不多。随着训练数据规模的不断加大，技术的持续迭代，我觉着AI会越来越具备人类的思维，像人类一样思考问题。

2、简单重复的场景，已经能替代人类了。复杂的场景，AI还需要学习，但只是时间问题。这给平时只会CRUD的同学已经敲响了警钟</div>2024-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（1） 💬（1）<div>老师，请问代码训练是什么意思</div>2024-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/35/16861bf8.jpg" width="30px"><span>蒋波</span> 👍（1） 💬（1）<div>个人理解目前大模型的确很强大了，而且还在多模态方向上发力提升学习能力，但我认为还不具备人类思维。个人理解人类思维很大的一个特点是具备自我反思能力，人类知道在有输出的每个节点自我完成了什么，知道下一步需要做什么，下一步可以做什么，还能根据自身的能力评估自我在可以做的里面能做什么，在发现不对时，还具备回退能力，总之具备在广泛意义上的大型网络上反馈（不仅仅是前馈）和各个节点列举、选择和评估路径的能力，更为重要的是在列举、选择和评估能力下，在顶层全局维度下，对当前局势、关系和情感的观察和评判，受情绪左右程度的把握。</div>2024-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/ab/7ba4218a.jpg" width="30px"><span>JACOB</span> 👍（1） 💬（1）<div>多久更新一次？</div>2024-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（1）<div>Ai不是代替人，而是赋能人更高效的完成任务。</div>2024-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/a9/3135d4b1.jpg" width="30px"><span>aiorosxu</span> 👍（0） 💬（1）<div>Emergent，在复杂科学领域，好像一般会翻译为“涌现”，而不是“突现”。个人感觉涌现这个词更能体现Emergent的精髓。</div>2024-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/ab/66/6f23e2e7.jpg" width="30px"><span>绿月亮</span> 👍（0） 💬（1）<div>1. 我觉得已经具备了简单基本的思维。
一方面：人说话时是根据前面的信息想下一个字词要说什么，这跟大模型大量的训练让机器学习语言的规律，上文预测下个token的概率是一致的。
另一方面：我感觉婴儿学习也是类似的过程，他接收一般的语言规律（通过大量的观察并模仿，类似于无监督训练），在使用时经常犯错，这时候大人会纠正他（类似于有监督训练）。

2. 我觉得AI可以替代某些一成不变的工作，这些是标准化的，有规律的（这些正是大模型通过训练容易学习到的）；有些创新性的倒是不容易被替代，也就是想象力不够（目前我们觉得大模型很强是因为我们人的记忆学习能力有限，但是机器是无限的，它学习了人类知识的大部分内容）
以上纯属个人见解，还请老师和前辈们批评指正。

另外有个疑问：大模型的有监督微调会不会就是让大模型记住了微调的内容？</div>2024-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/dd/f2/3513c633.jpg" width="30px"><span>张 ·万岁！</span> 👍（0） 💬（1）<div>我觉得chatgpt还是没有具备真正的人类大脑思维，他本质上还是对于已知资源的整合，直至信息准确率更高，记忆更长，在一个绘画中，如果有很多的聊天，他还是会忘掉一些记忆。</div>2024-07-12</li><br/><li><img src="" width="30px"><span>Geek_e9e5f5</span> 👍（0） 💬（1）<div>一直对大模型的训练没法理解</div>2024-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（1）<div>现在做的项目，甲方想用大模型去做一些科学研究，创新性的东西，我觉得不现实，可能用大模型发现规律，汇总信息是可行的，但是它从来没见过的，新的理论怎么可能直接被发现呢？我该怎么说服甲方呢？🤣</div>2024-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/eb/ad/20b60d15.jpg" width="30px"><span>hudy_coco</span> 👍（5） 💬（1）<div>1.是否已经具备了人类大脑的思维，这个问题无法被验伪，那我们就姑且认为是真实的。从目前的测试表现来看，只能说明和人类大脑思维有差距，但这不一定是它全部的实力。

2.AI已经能够部分替代我们的工作，以后还会越来越多的，但个人认为最终无法完全替代，一是输出取决于输入，二是情感和想象是人类最后的高原。除非快进到智械时代，社会运转都由它来调控，那么人类就要找准自己新定位了。</div>2024-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/95/56/f19c95ae.jpg" width="30px"><span>Geek_baby</span> 👍（0） 💬（0）<div>。这要放在国内，还不得让你下载个 App，甚至拉几个朋友才可以用.
deepseek豹:人内心的成见，是一座难以逾越的大山😄</div>2025-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/89/681d9b13.jpg" width="30px"><span>小一</span> 👍（0） 💬（0）<div>1. 不具备人类大脑思维，chatgpt基于的是自回归语言训练模型，没有真正的理解力和意识；
2. 可替代一部分工作，例如UED部分基础工作、基础编码工作、测试层面、性能优化检测层面；</div>2024-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/0c/66/51161385.jpg" width="30px"><span>like life</span> 👍（0） 💬（0）<div>我认为ChatGPT已经初步具备了人类大脑的思维，可以和人进行简单的交流对话。同时大多数场景下他的表现都是比较优秀的。但是现实世界是很复杂的。目前还有很多地方不能完全替代我们的工作，毕竟GPT只是我们人类创造的工具。由此可见 AI 不可能完成代替我们人类完成目前所有的工作，但确实有助于提高咱搬砖人的工作效率。</div>2024-11-07</li><br/>
</ul>