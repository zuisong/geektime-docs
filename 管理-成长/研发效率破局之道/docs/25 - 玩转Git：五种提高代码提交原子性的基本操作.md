你好，我是葛俊。今天，我们来聊一聊Git吧。

毫无疑问，Git是当前最流行的代码仓管理系统，可以说是开发者的必备技能。它非常强大，使用得当的话可以大幅助力个人效能的提升。一个最直接的应用就是，可以帮助我们提升代码提交的原子性。如果一个团队的成员都能熟练使用Git的话，可以大大提高团队代码的模块化、可读性、可维护性，从而提高团队的研发效能。但可惜的是，现实情况中，由于Git比较复杂，用得好的人并不多。

所以接下来，我会通过两篇文章，与你详细讲述如何使用Git助力实现代码原子性。今天这篇文章，我先与你分享Git支持原子性的5种基础操作；下一篇文章，则会给你介绍Facebook开发人员是怎样具体应用这些基础操作去实现代码原子性的。

通过这两篇文章，我希望你能够：

1. 了解在分布式代码仓管理系统中，如何通过对代码提交的灵活处理，实现提交的原子性；
2. 帮你学习到Git的实用技巧，提高开发效率。

我在[第21篇文章](https://time.geekbang.org/column/article/148170)中提到，代码提交的原子性指的是，一个提交包含一个不可分割的特性、修复或者优化。如果用一个提交完成一个功能，这个提交还是会比较大的话，我们需要把这个功能再拆分为子功能。

为什么要强调代码提交的原子性呢？这是因为它有以下3大好处：
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（8） 💬（3）<div>git rebase -i 确实很好很强大，哈哈！

课后思考题
1.git cherry-pick 应该可以间接实现
2.git push -f &#47; git rebase 已提交的代码后再git push -f 是危险操作。
人少时，吼一嗓子，再使用。人多时还是放弃吧。哈哈！
可是我经常这么干。🤦‍♂️

git push -f 后，轻则已拉取代码回本地的人需要手动修复下环境，重则之后推送的分支会被丢失。
（别人以为已经提交了，哪知还有人敢强推代码）
如果时间久了，别人本地分支也没留记录，可能代码就需要手敲了。（概率很小，但也可找回历史提交）
</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（5） 💬（2）<div>思考题留言区有同学已经答得很帅了，想了下就是做不到答得更好，只对第二个问题大概做一下补充，其实这个本体本质上还是git rebase和远端库共享的潜在冲突的问题，所以从这一点上讲，远端是fork的私库，任何共享都是基于TBD的CI基础上完成就非常重要了，对发布出去的东西，还是得注意品质，后悔药在git世界里不是没有，只是可能会让大家都很痛苦，发出去的东西就当泼出去的水，一路向前，不要回头

其实进来这里就是纯赞的，我本来以为我经常PR之前用git rebase -i仔细梳理就算是会了git了，但是看第一个场景git add -p我就直接跪了，也许以前见过，但是真没印象，一点也没有，我甚至没想过还可以这么干，虽然我不太认同这么部分的管理更新吧，要做这种部分提交，我觉得很大程度上是设计上没太想好，自己本地库这里还在debug的感觉；但是git的强大真的可见一斑</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（2） 💬（3）<div>1.很棒，历史提交操作这块以前没概念，一直都是手动来，导致增加很多提交，学习了，练习下应用到工作去。
2.现在工作主要用idea，用git的拉推提交回滚啥的简单操作都是直接在idea上。涉及到拆分提交这类操作就要切命令行敲git  指令。感觉操作不连贯。老师工作中是纯命令的吗？这些操作跟idea是否有对应？如果有应该怎么做？
3.git-history，小工具，但看历史变更更直观，推荐使用。</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>思考题
可以通过强制push: git push -f 覆盖掉在远程的分支，不过这样做确实很危险。</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/80/21d67b9b.jpg" width="30px"><span>二狗</span> 👍（0） 💬（1）<div>没用过 没看懂(╥╯^╰╥)  看来还得拿栗子实践一下</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（0）<div>老师操作四说交换AB后，重新有选择地放到 origin&#47;master 上面。但结果是放到master，并不是origin&#47;master，是不是表述的不够严谨？</div>2023-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/47/e4/17cb3df1.jpg" width="30px"><span>BBQ</span> 👍（0） 💬（0）<div>老师，不知道是不是我的理解有问题
&gt;同时，在没有接–hard 或者–soft 参数时，git reset 会把目标提交的内容同时复制到暂存区，但不会复制到工作区。
我看了您的控制台输出 ，我自己也试了一下，reset 之后，之前Commit 的修改会全部复制到工作区，不是复制到暂存区，reset 之后暂存区并没有内容。

多谢！</div>2021-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/25/c4cc1e9f.jpg" width="30px"><span>巫山老妖</span> 👍（0） 💬（0）<div>git rebase的操作，我们大多是在合并分支的时候用到，用于原子性提交确实日常没怎么用，因为要让大部人做到原子性提交还是件不容易的事情</div>2021-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a0/a7/db7a7c50.jpg" width="30px"><span>送普选</span> 👍（0） 💬（2）<div>简单用过git，有个问题，若只提交到本地分支，不推送到远程分支，若本地电脑硬盘故障代码就丢失了，每日多次推送会减少损失，但从远程还是没有最近没推送的代码。请问葛老师我理解对吗？这种情况如何解决？谢谢！</div>2021-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/71/c92efb11.jpg" width="30px"><span>scguo</span> 👍（0） 💬（0）<div>给推荐一个git的学习工具，https:&#47;&#47;github.com&#47;Gazler&#47;githug</div>2020-12-21</li><br/>
</ul>