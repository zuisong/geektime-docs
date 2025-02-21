你好，我是姚琪琳。

上节课，我们讲了任务分解、小步提交、质量门禁、分级构建、制品晋级等DevOps实践，它们都可以看做是持续集成的基础。只有做好任务分解和小步提交，才能放心大胆地PUSH代码，触发持续构建；只有通过质量门禁，才能得到一个有信心的制品；分级构建可以让我们更加快速地得到反馈；而制品晋级才真正地让持续集成流水线流动起来。

不过，有了一个初始版本的DevOps持续集成流水线还不够，今天我们就继续聊聊DevOps现代化的高阶话题，即如何从持续集成演进到持续部署和持续交付。

开始学习之前，我想给你提个醒。这节课内容相当长（特别是分支策略这里），本可以拆成两篇甚至三篇。但为了让你一次看个够，我还是决定不拆分。如果你耐心看完，一定可以从根本上理解从持续集成到持续部署的关键知识点。毕竟只有筑牢基础，未来DevOps实践里才可能大展身手。

## 持续集成

要想做到真正的持续集成，需要一个与之匹配的代码分支策略。这方面的话题历来就十分有争议，我来说说我的观点。

### 分支策略：特性分支or基于主干开发？

要说现在国内最流行的分支策略，非**特性分支（Feature Branch）**莫属，它还有一个更响亮的名字—— [GitFlow](https://nvie.com/posts/a-successful-git-branching-model)。不过，虽然名字叫GitFlow，但它并不是Git官方推荐的做法，而只是Vincent Driessen的发明创造而已。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkOBhbBYIlfyo8oibrrJPjz4BJIdR2DPVxfXSOlfcg8icAKRwtibj0W1gJ1C3HT2GLs7zWQjLBdhz3A/132" width="30px"><span>hzecool</span> 👍（0） 💬（1）<div>基于主干开发，发布前还是要拉一个分支出来进行测试吧，测试通过后再把该分支合并到一个线上发版分支进行部署。感觉是否至少需要三个分支？</div>2022-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/3e/cdc36608.jpg" width="30px"><span>子夜枯灯</span> 👍（0） 💬（1）<div>老师,文中说到&quot;因为采用了基于业务场景的任务分解和小步提交，理论上每个 commit 都能提供业务价值，也是可以部署和交付的。&quot;这里能使用一个复杂的场景做个拆解举例么?这里没有理解上去,如何实际操作,谢谢</div>2022-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：“用细粒度的用户故事替代落后的需求文档。”，这句话怎么理解？
    是不要需求文档吗？
Q2：每天提交代码和code review，是不是太频繁？这样做的话，写代码的时间只有半天，
    时间不够啊。我自己感觉做一个功能都需要好几天，至少两三天吧。
Q3：Jenkins除了持续集成功能外，还有部署功能吗？</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/97/23/9c9bd0d4.jpg" width="30px"><span>苜蓿°</span> 👍（0） 💬（0）<div>老师这里的QA负责测试。是统一了QC在里面的意思？</div>2025-02-06</li><br/>
</ul>