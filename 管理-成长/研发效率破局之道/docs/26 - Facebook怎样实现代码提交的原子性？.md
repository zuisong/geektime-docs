你好，我是葛俊。今天，我们继续来聊聊如何通过Git提高代码提交的原子性吧。

在上一篇文章中，我给你详细介绍了Git助力提高代码提交原子性的五条基础操作，今天我们再来看看Facebook的开发人员具体是如何使用这些操作来实现提交的原子性的。

为了帮助你更直观地理解、学习，在这篇文章里，我会与你详细描述工作场景，并列出具体命令。同时，我还把这些命令的输出也都放到了文章里，供你参考。所以，这篇文章会比较长、比较细。不过不要担心，这些内容都是日常工作中的自然流程，阅读起来也会比较顺畅。

在Facebook，开发人员最常使用两种Git工作流：

- 使用一个分支，完成所有需求的开发；
- 使用多个分支，每个分支支持一个需求的开发。

两种工作流都利用Git的超强功能来提高代码原子性。这里的“需求”包括功能开发和缺陷修复，用大写字母A、B、C等表示；每个需求都可能包含有多个提交，每个提交用需求名+序号表示。比如，A可能包含A1、A2两个提交，B只包含B1这一个提交，而C包含C1、C2、C3三个提交。

需要强调的是，这两种工作流中的一个分支和多个分支，都是在开发者本地机器上的分支，不是远程代码仓中的功能分支。我在前面[第7篇文章](https://time.geekbang.org/column/article/132499)中提到过，Facebook的主代码仓是不使用功能分支的。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/b1/4d/10c75b34.jpg" width="30px"><span>Johnson</span> 👍（5） 💬（4）<div>第一种太烧脑了，对开发人员的git技能要求太高了，大部分的开发人员都不能正确驾驭，感觉工作中更多的是以第二种为主，然后在某个branch内部结合第一种的情况比较容易驾驭。很头疼的问题是很多老同事没有深入学习git的主动性和激情，稍微复杂点儿的操作就让别人帮忙操作。</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（3） 💬（1）<div>葛老师，请问提交代码的原子性，除了提高git技巧外，在工程上有什么需要注意的点吗？比如软件架构，设计模式。这方面应该随着语言和项目的不同会有较大的差异，有没有什么通用的原则？</div>2019-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/8b/fdb853c4.jpg" width="30px"><span>Weining Cao</span> 👍（2） 💬（1）<div>从来不用rebase, 一直用merge，看来要好好学习下rebase了</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（2）<div>学习了，这两种方式我都会，也经常用。
我比较喜欢线性的提交历史，不喜欢merge。

但有个比较纠结的是。
比如采用第二种方式：
单独开发某个功能，也是采用小步走的方式，这样一个功能分支开发完后，可能有很多小的commit。
如果这些commit都线性的推到远程，感觉也不好。
目前只能先自己用rebase合并一些分支，然后再推。

如果是使用git merge —no-ff的方式，这些小commit就可以保留，在历史中可以看到完整的开发过程。
但是这样分支看上去就临时分叉了。
不知道老师推荐用哪种方法。

课后思考题一
我能想到的笨办法：
1。先备份当前分支，比如git branch temp
2。git reset —hard HEAD^
3。修改并git commit —amend —no-edit
4。git cherry-pick 后面的commit 😄
或者git checkout temp ；git rebase xxx 刚才修改后的commit （不知道可不可行）</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/15/9c/575cca94.jpg" width="30px"><span>LearnAndTry</span> 👍（0） 💬（0）<div>单分支那个是给人用的吗？？？</div>2024-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/58/54/eaf62b2b.jpg" width="30px"><span>浇了汁鸡</span> 👍（0） 💬（0）<div>还有一种合并方式叫做&#39;半线性历史记录&#39;，(https:&#47;&#47;stackoverflow.com&#47;questions&#47;59714347&#47;semi-linear-merge)，先把特性分支基于master做rebase，再merge --no-ff，既可以看到每次合并引入点，又能近似拥有线性历史的定位问题的便捷性</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/25/c4cc1e9f.jpg" width="30px"><span>巫山老妖</span> 👍（0） 💬（0）<div>第一种虽然能够不切换分支完成原子性提交，但感觉复杂性也变高了，要求所有人都能掌握还是比较困难，目前我们团队还是以第二种为主，不过有些同学还是习惯用merge来合并分支</div>2021-04-18</li><br/>
</ul>