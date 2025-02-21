你好，我是李锟。

在前面两节课中，我们花费了不少工夫安装好 AutoGPT，熟悉了 AutoGPT 的工作和开发模式，并且解决了开发 AutoGPT 应用的两个直接挑战。这节课将开启一个非常有意思的部分，开发我们自己的第一个 Autonomous Agent 应用（为了吃这碟醋，我们来包一顿饺子）。我会带着你基于 AutoGPT 实现 [01 课](https://time.geekbang.org/column/article/838710)中讨论过的那个 24 点游戏智能体应用。

## 角色建模和工作流设计

与 [04 课](https://time.geekbang.org/column/article/840305)的设计开发过程相同，我们要做的第一步仍然是角色和工作流设计。因为我们在 04 课中已经基于 MetaGPT 实现过一次这个应用，很熟悉这个应用中的角色和工作流。不需要重复相同的内容，在这节课里我们要做的是把 04 课针对 MetaGPT 的设计和实现移植到 AutoGPT 的环境。

从 [06 课](https://time.geekbang.org/column/article/841091)中学习到的 AutoGPT 基础概念，我们理解了 MetaGPT 的 Action 对应 AutoGPT 的 Block，因此 Action 可以直接移植为 Block。那么 MetaGPT 的 Role 在 AutoGPT 中对应的是什么呢？在 AutoGPT 中，与 Role 对应的概念就是 Agent。MetaGPT 支持多个 Role 的协作，同样的，AutoGPT 新版本也支持多个 Agent 的协作 (老版本仅支持单个 Agent)。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/4c/11/e5af6252.jpg" width="30px"><span>流沙</span> 👍（1） 💬（1）<div>视频怎么看？提示没有权限观看</div>2025-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/69/62/b874af21.jpg" width="30px"><span>颛顼</span> 👍（0） 💬（1）<div>上面提到的临时方案，课程上线也没更新了</div>2025-02-08</li><br/>
</ul>