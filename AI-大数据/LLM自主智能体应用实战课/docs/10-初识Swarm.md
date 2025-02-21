你好，我是李锟。

在学习了 MetaGPT 和 AutoGPT 两个很不相同的开发框架之后，我们今天开始学习第三个多 Agent 应用开发框架——Swarm。Swarm 是一个非常轻量级、非常精益的开发框架，学习门槛很低，很容易上手，因此这两课学习起来会更加轻松愉快。

学习过 [01 课](https://time.geekbang.org/column/article/838710)之后，相信你已经理解了我特别喜欢这种轻量级的开发框架的原因。Swarm 是所有多 Agent 开发框架中最轻量级的，正是我喜欢的类型。不过，轻量级不代表它只是一个玩具，没有实用性，很快你就会看到它的威力。

Swarm 比 MetaGPT 更轻量级，只依赖 Python。可以使用 Python 3.12 及以上版本，以下所有 Python 代码我都是使用 Python 3.12 开发的。

## Python 项目初始化

为了学习 Swarm，我们首先初始化一个 Python 项目。在 Linux 主机的终端窗口执行以下命令：

```plain
mkdir -p ~/work/learn_swarm
cd ~/work/learn_swarm
touch README.md
# 创建poetry虚拟环境，一路回车即可
poetry init
```

因为众所周知的原因，建议使用国内的 Python 库镜像服务器，例如上海交大的镜像服务器：
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/94/ae6dcfb9.jpg" width="30px"><span>I. Z.</span> 👍（1） 💬（1）<div>请问新版v2 OpenAI assistant api 支持file search, 还有基于thread 的上下文管理， 这个在用swarm 的时候也可以用到吗</div>2025-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/f1/7d21b2b0.jpg" width="30px"><span>方梁</span> 👍（0） 💬（1）<div>安装包是是安装openai-swarm包吧，如何调用别的大模型？</div>2025-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/63/112780b3.jpg" width="30px"><span>晓波</span> 👍（0） 💬（0）<div>建议采用下述方式安装swarm.git ，这样vscode 配置使用虚拟环境后，可以正常调整。方便源码阅读

poetry run pip install git+https:&#47;&#47;github.com&#47;openai&#47;swarm.git </div>2025-02-21</li><br/>
</ul>