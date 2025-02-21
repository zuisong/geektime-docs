专栏上线后，有一些同学对于代码质量有关的问题还不是很清楚，有很多疑问，所以我特意做了一期Q&amp;A，来回答一下这些问题。

## 1. 有没有什么技巧可以不费力地查看源代码？

这是一个好问题。但遗憾的是，我们费力的程度，主要取决于代码的作者，而不是我们自己。我想了好久，也没有找到不费力气查看源代码的技巧。

通常我自己用的办法，有时候就像剥洋葱，从外朝里看；有时候也像挖井，找到地表的一小块地儿，朝下一直挖，直到我理解了代码的逻辑关系。

如果你刚开始接触，我建议你先不要看代码，先去看README，再去看用户指南。先把软件干什么、怎么用搞清楚。然后再去看开发者指南，搞清楚模块之间的关系、功能，理解代码中的示例。最后，再去看代码。

看代码的时候，找一个顺手的IDE。IDE丰富的检索功能，可以帮助我们找到一个方法，在什么地方定义的，有哪些地方使用了。

如果你还不知道要看哪一个源代码，先找一个例子开始。不管这个例子是开发指南里的，还是测试代码里的。先找出一个例子，把它读懂，然后阅读例子中调用的源代码。

比如，你要是看到示例代码调用了Collections.unmodifiableList​()方法，如果想了解它，就查看它的规范文档或者源代码。从例子开始剥每一个你关心的方法，一层一层地深入下去。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（13） 💬（1）<div>第二个问题个人认为目标还是——经济

关于第二个问题，个人认为可能不能算是鱼和熊掌，可能更偏向于鱼和鱼竿。

一面是很多鱼，而另一面是一根鱼竿。二选一。
另外效率这个词，个人认为不恰当。效率是保障质量的前提下更高的产出。个人把这个理念替换为速度。

速度质量二选一。理想化肯定是质量。但是实际上还要参考实际情况。

类似于我们公司的团队，碰到这样的项目，明天就要求能看到效果。都来不及做详细设计，直接把以前的项目拿来改一改调试一下就拿去演示了。然后后续再进行优化调试完善。

这种硬环境下，不是不保障。而是无暇保障。
另一种情况，是有些功能模块，重要性不是很高，甚至根本不会有人用。只是个凑数投标的模块，但是这个模块测试以及优化的话可能很复杂。这时候，去花费大量时间精力在上面明显是不合适的。就假设，这个模块定价1000，但是为了这个模块的测试优化就花了800的成本，公司是不愿意为你的高质量代码买账的。

再举个反例。某模块追求速度开发。两天做完，节约了一天代码优化以及测试的步骤。但是未来的某天，发现这里有个坑。因为代码很久没有看过。导致这个坑难以找到问题所在，最后导致功能模块几乎重写。这里就是不应该因为速度舍弃质量的例子。

综上所述，个人认为，取舍的终极目标。还是老师之前说到的——经济

但是达到这个，并不容易。不仅仅是编写高质量代码的习惯与能力。还有不可或缺的经验，以至于可以灵活取舍。

但是——我们至少要有高质量编码的能力与基础。这样，在你有经验的时候才可以做到灵活的取舍。</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6b/71/e833b14a.jpg" width="30px"><span>李英权</span> 👍（13） 💬（2）<div>最近接手一个质量不高的JAVA工程，读代码过程中 摸索出一个经验——用eclipse的bookmark功能为代码创建索引，现实世界的代码库 大多数像是没有索引的图书馆，运气好的你遇到有文档的项目 也不过是残缺的过期的和错误的引索。
所以需要你去重建准确的索引，eclipse的bookmark用好了  可以达到这个目的。</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/42/28/68eeb317.jpg" width="30px"><span>余山头</span> 👍（6） 💬（1）<div>作为团队负责人，以前推行过upsource作为代码审查工具，这工具和idea结合起来，非常好用。结果怎么样呢，发现工具是次要的，项目各种赶，各种应标废标，各种演示项目。能谈下的项目经过商务的一再拖延最后留给研发的时间少的可怜，结果就是导致低效的加班赶进度，代码都不忍直视，怕小心脏受不了。理想很丰满，现实很骨感，对于主要业务是短期外包的公司来说，只希望用廉价劳动力快速交差。</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/f8/3c0a6854.jpg" width="30px"><span>xavier</span> 👍（5） 💬（1）<div>老师讲得很好，我觉得很多人跟我一样，就因为见识不够，不知道如何去编写高质量的代码。老师可以提供一些实践性的项目或者资源，供大家学习、操作。</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/9a/bbeec5bb.jpg" width="30px"><span>liu</span> 👍（3） 💬（1）<div>广博精深，做好取舍。大处着眼，细处着手；质量从过程抓起，从细节抓起，做好质量把控；同时注重反馈总结。方向对了，过程把握好了，结果不会太坏。</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/6e/126b76bc.jpg" width="30px"><span>hyeebeen</span> 👍（1） 💬（1）<div>是否可以通过调用链路来帮助我们从整体去认识类与类、方法与方法之间的关系，然后再去“剥洋葱”？</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/de/32/67acddcd.jpg" width="30px"><span>若尘</span> 👍（1） 💬（1）<div>从编写，测试，交付，使用的大视角拆解效率，结论是质与量两个变量，质跟效率相关性更高，又一次证明了慢慢做会更快</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（1） 💬（1）<div>打卡</div>2019-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（1） 💬（1）<div>老师您好，质量高的代码是否意味着使用恰当的设计模式？</div>2019-01-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLvRT0Hxy8MLYAw7EVkLtezJSUyibqgCNibZGGqtRvtUano87QPasNNvib2ASB6Yl8BtWxDmHgGCNTCQ/132" width="30px"><span>老吴</span> 👍（0） 💬（1）<div>养肥了  可以开始看了</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（1） 💬（0）<div>非常感谢评论区的哥哥姐姐分享的经验~</div>2021-04-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ooZCPFY1xgC81h0Eu3vuqbWG5MaBp8RNmvXXGQwupo2LpSOLq0rBlTDRAF1yM6wF09WdeG49rA9dJSVKIUBxnQ/132" width="30px"><span>Sisyphus235</span> 👍（1） 💬（1）<div>代码的开发最重要的影响因素之一是经济，有时候为了效率，很多部分我都会写 TODO，因为交付时间总是很急迫，来不及认真的设计架构和实现。有过几次因为这样开发，不长时间就要停下来重构的经历后，我现在往往会在开发新功能的时候，把涉及部分的 TODO 一起做了，局部重构，以解决开发速度和代码质量的问题。</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习了</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>如果一个东西，每个人三秒就可以掌握，那当然是好的。但同时，它就算不上你的优势了。即使有优势，也只是三秒钟的差距。--记下来</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>谢谢分享</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f0/3e/f9f021bf.jpg" width="30px"><span>Geeker</span> 👍（0） 💬（0）<div>感谢老师！</div>2020-03-11</li><br/>
</ul>