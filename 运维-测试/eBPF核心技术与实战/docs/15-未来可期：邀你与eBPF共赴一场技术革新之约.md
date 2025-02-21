你好，我是倪朋飞。

不知不觉间，这门课程已经上线一个月了，第一阶段的正文更新到今天就暂告一段落了。在这里，首先恭喜你完成了这一阶段的学习，掌握了关于 eBPF 的基本知识，也获得了理解 eBPF 机制、把握 eBPF 进化方向的抓手。接下来的动态更新阶段，我会带着你持续跟进 eBPF 技术的最新进展、发展趋势，相信之后四年持续学习的你，在结课时会有更多的收获。

在准备这门课的过程中，我有了很多感想和收获，接下来就把它们分享给你。

## 我为什么要做这门动态更新的eBPF课程？

去年10月的时候，极客时间团队就联系到了我，商量要一起筹备平台上的第一个动态专栏。我第一时间就想到了 eBPF 这个主题。一方面，是因为我觉得 eBPF 会是我的第一季专栏中涉及的动态追踪技术的完美补充；另一方面，动态更新的形式也很适合 eBPF 这样还在快速发展、变更频繁的技术。

早在几年前开设[《Linux 性能优化实战》](https://time.geekbang.org/column/intro/100020901?tab=catalog)专栏的时候，我就发现了一个问题：在讨论相对简单的单指标性能时，同学们都很热情；但在综合多个指标之后，有些同学就掉队了。特别是在涉及系统底层知识时，很多同学虽然也可以利用课程中的工具解决一些性能问题，但由于对内核原理的潜在恐惧，在分析多性能指标之间的相互关系时，还是不能利用底层知识把它们全部贯穿起来。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/59/d3/696b1702.jpg" width="30px"><span>校歌</span> 👍（6） 💬（2）<div>留个言，4年后，看看自己水平咋样，💪</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（5） 💬（1）<div>感谢倪老师，很赞的课程，推荐大家学习。</div>2022-02-18</li><br/><li><img src="" width="30px"><span>Geek9635</span> 👍（2） 💬（2）<div>ebp的sockmap相比unix domain socket的优势在那呢？从测试情况（TCP_RR）看，unix domain socket比sockmap方式还高12%左右；功能上看，两者都不能很方便的抓包，无抓包功能，就很难无法落地；有点优势是能对业务透明，但在同一个host上，并不是非常强的需求，感觉有点鸡肋，还请老师指教</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/63/d5909105.jpg" width="30px"><span>小李同学</span> 👍（2） 💬（1）<div>感谢倪老师，赞赞赞</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/c5/f8/97d4508e.jpg" width="30px"><span>Tok1c</span> 👍（1） 💬（1）<div>留个言，4年后，看看自己水平咋样，💪</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e6/ee/8fdbd5db.jpg" width="30px"><span>Damoncui</span> 👍（1） 💬（0）<div>感谢老师～
四月加油！</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/19/fe/d31344db.jpg" width="30px"><span>lJ</span> 👍（0） 💬（0）<div>打了卡 两年后检查下自己</div>2024-02-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJRicibrZZK2F5zgOzTeGQHBKXELdqhiaabAPJMRVsfHHRmmu1W69Cqo6P9At3DvWdBoznfYIuXA1tFw/132" width="30px"><span>kong62</span> 👍（0） 💬（0）<div>概念理念很好，实际复杂，难以落地。</div>2023-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/18/e4382a8e.jpg" width="30px"><span>有识之士</span> 👍（0） 💬（0）<div>留个言，4年后，看看自己技术能力有哪些提升！！！</div>2023-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/92/7c/12c571b6.jpg" width="30px"><span>Slience-0°C</span> 👍（0） 💬（0）<div>eBPF可以下钩子，进行某些行为的阻断么？比如阻断文件打开？谢谢</div>2022-09-14</li><br/>
</ul>