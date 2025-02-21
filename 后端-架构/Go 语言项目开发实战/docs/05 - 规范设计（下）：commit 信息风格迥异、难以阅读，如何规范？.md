你好，我是孔令飞。今天，我们继续学习非编码类规范中的 Commit 规范。

我们在做代码开发时，经常需要提交代码，提交代码时需要填写 Commit Message（提交说明），否则就不允许提交。

而在实际开发中，我发现每个研发人员提交 Commit Message 的格式可以说是五花八门，有用中文的、有用英文的，甚至有的直接填写“11111”。这样的 Commit Message，时间久了可能连提交者自己都看不懂所表述的修改内容，更别说给别人看了。

所以在 Go 项目开发时，一个好的 Commit Message 至关重要：

- 可以使自己或者其他开发人员能够**清晰地知道每个 commit 的变更内容**，方便快速浏览变更历史，比如可以直接略过文档类型或者格式化类型的代码变更。
- 可以基于这些 Commit Message **进行过滤查找**，比如只查找某个版本新增的功能：`git log --oneline --grep "^feat|^fix|^perf"`。
- 可以基于规范化的 Commit Message **生成 Change Log**。
- 可以依据某些类型的 Commit Message **触发构建或者发布流程**，比如当 type 类型为 feat、fix 时我们才触发 CI 流程。
- **确定语义化版本的版本号**。比如 `fix` 类型可以映射为 PATCH 版本，`feat` 类型可以映射为 MINOR 版本。带有 `BREAKING CHANGE` 的 commit，可以映射为 MAJOR 版本。在这门课里，我就是通过这种方式来自动生成版本号。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/84/b4/3ed5adc7.jpg" width="30px"><span>pudu168</span> 👍（25） 💬（1）<div>推荐一个网站： https:&#47;&#47;www.conventionalcommits.org&#47;en&#47;v1.0.0-beta.4&#47;  有中文版，之前一直使用的规范文档</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/f1/ce10759d.jpg" width="30px"><span>wei 丶</span> 👍（7） 💬（1）<div>老师是不是rebase后push会出现 当前分支的最新提交落后于其对应的远程分支 
我每次操作都有这个想要push必须要-f才可以 是我的操作的问题么？？</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4e/bf/0f0754aa.jpg" width="30px"><span>lianyz</span> 👍（4） 💬（2）<div>孔老师，一个commit里允许同时包含一个feat和一个fix吗？如何约束开发的同事？</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/0b/73628618.jpg" width="30px"><span>兔嘟嘟</span> 👍（3） 💬（1）<div>git-chglog只需要安装好后git-chglog -o CHANGELOG.md ，就可以一键生成change log
gsemver没搞懂怎么用</div>2021-12-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oib0a89lqtOhJL1UvfUp4uTsRLrDbhoGk9jLiciazxMu0COibJsFCZDypK1ZFcHEJc9d9qgbjvgR41ImL6FNPoVlWA/132" width="30px"><span>stefen</span> 👍（2） 💬（1）<div>“我们希望将 feature&#47;user 分支的 5 个 commit 合并到一个 commit，在 git rebase 时，需要保证其中最新的一个 commit 是 pick 状态，这样我们才可以将其他 4 个 commit 合并进去”， 我看了好几遍，应该是保持最旧一个commit是pick状态，不是最新一个commit 是 pick 状态.</div>2022-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（2） 💬（1）<div>提交push了之后是不是不能修改了？</div>2022-02-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJyibojtJCnzAE7E8sMqgiaiaAHl3FuzcXcicQnjnT5huUFMxGUMzV5NGuqzzHHr8dBzCs3xfuhwcOnPw/132" width="30px"><span>好家庭</span> 👍（2） 💬（1）<div>请问修改了commit message之后所有的commit id改变，如果修改的是仓库中原有的commit,再提交到仓库会不会产生冲突？</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/74/72ffa6d6.jpg" width="30px"><span>StayLet</span> 👍（2） 💬（2）<div>孔老师，为啥 “subject 的结尾不能加英文句号”？</div>2021-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/5f/32d504bb.jpg" width="30px"><span>🌆🌇🌉🌌</span> 👍（2） 💬（2）<div>老师，这个流程和git-flow哪个更好呢？</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（1） 💬（2）<div>我喜欢用英文提交，避免切换输入法</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>孔老板，项目的第一次提交，type类型应该为feat吧。</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（1） 💬（1）<div>commit-msg工具的github链接缺失了，不知道是不是这个https:&#47;&#47;github.com&#47;JayceChant&#47;commit-msg</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/cd/8d552516.jpg" width="30px"><span>Gojustforfun</span> 👍（1） 💬（1）<div>“在以上规范中，必须用括号 () 括起来......”

哪部份“必须用括号 () 括起来”？</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（1） 💬（1）<div>代码性能上的优化用perf, 如果是代码逻辑或功能上的优化也用perf吗, 如果用perf不合适的话, 用哪个type更合适呢</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/76/36fdddb3.jpg" width="30px"><span>低调</span> 👍（1） 💬（1）<div>有冲突后也需要commit一次，这个是用哪种类型 feat? fix?refactor?</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（1） 💬（1）<div>文章写的不错，但是有些细节问题，修改commit message那部分进入edit界面的commit的id和之前git log看到的都不一致，希望后面越来越好。</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/84/f45c4af9.jpg" width="30px"><span>Vackine</span> 👍（1） 💬（2）<div>孔老师，请问下那个iam git clone 的时候一定要clone到gopath的src的目录下么？还是任意一个目录下都可以？还有本地分支make的时候(变更只是吧安装脚本做了一些注释) 报golint的错，是需要还什么配置么？</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/0a/02ecee7a.jpg" width="30px"><span>女干部</span> 👍（1） 💬（1）<div>孔老板，
对于分支名命，合并这些规范，有没有什么可以参考的资料</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/24/547439f1.jpg" width="30px"><span>ghostwritten</span> 👍（0） 💬（1）<div>6. 我们进行合并
$ git checkout -b feature&#47;user
Switched to a new branch &#39;feature&#47;user&#39;
#这是我们当前的提交历史
$ git log --oneline
cdc05c6 (HEAD -&gt; feature&#47;user, main) append test line &#39;test3&#39; to README.md
053fa91 append test line &#39;test2&#39; to README.md
6a79e97 append test line &#39;test1&#39; to README.md
9927ec0 create README.md
接着，我们在 feature&#47;user分支进行功能的开发和测试，并遵循规范提交 commit，功能开发并测试完成后，Git 仓库的 commit 记录如下：
$ git log --oneline
efa9b1c (HEAD -&gt; feature&#47;user) docs(user): update user&#47;README.md
bec209f docs(user): update user&#47;README.md
9f69521 docs(user): add README.md for user
2fc667e feat(user): add delete user function
c2fda9f feat(user): add create user function
cdc05c6 (main) append test line &#39;test3&#39; to README.md
053fa91 append test line &#39;test22&#39; to README.md
6a79e97 append test line &#39;test1&#39; to README.md
9927ec0 create README.md

合并 5 个 commit
$ git rebase -i cdc05c6
pick c2fda9f feat(user): add create user function
s 2fc667e feat(user): add delete user function  #pick 改成s，squash 操作，保留该commit，但会和上一个commit合并
s 9f69521 docs(user): add README.md for user  #pick 改成s，squash 操作，保留该commit，但会和上一个commit合并
s bec209f docs(user): update user&#47;README.md  #pick 改成s，squash 操作，保留该commit，但会和上一个commit合并
s efa9b1c docs(user): update user&#47;README.md #pick 改成s，squash 操作，保留该commit，但会和上一个commit合并
修改完成后执行:wq 保存，会跳转到一个新的交互页面，在该页面，我们可以编辑 Commit Message

# This is the 1st commit message:

feat(user): add create user module with all function implements

do the following updates:
1. create User go struct
2. (u *User) create() function
3. add (u *User) Delete() function
4. add README.md for user module
wq 保存，就完成了合并提交操作
$ git log --oneline
3650b6c (HEAD -&gt; feature&#47;user) feat(user): add create user module with all function implements
cdc05c6 (main) append test line &#39;test3&#39; to README.md
.....
第一个作业完成</div>2022-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/24/547439f1.jpg" width="30px"><span>ghostwritten</span> 👍（0） 💬（1）<div>5. 我们通过git rebase -i 修改第三次添加的内容，test2写成了test1,注意，这里一定要传入想要变更 Commit Message 的父 commit ID：git rebase -i &lt;父 commit ID&gt;。

pick 6a79e97 append test line &#39;test1&#39; to README.md
r dd07581 append test line &#39;test2&#39; to README.md   # 把pick改成r（意思是保留commit信息，并修改commit信息）
pick ce9b6fb append test line &#39;test3&#39; to README.md

：wq保存，继续弹出

append test line &#39;test2&#39; to README.md  #修改此行,test$ 改为test2
最后:wq保存退出,会自动弹出
[detached HEAD 45a5d2b] append test line &#39;test2&#39; to README.md
 Date: Fri Nov 11 15:59:44 2022 +0800
 1 file changed, 1 insertion(+)
Successfully rebased and updated refs&#47;heads&#47;main.
查看git日志
 git log --oneline
f8300a8 (HEAD -&gt; main) append test line &#39;test3&#39; to README.md
45a5d2b append test line &#39;test2&#39; to README.md   #已经改过来了。
6a79e97 append test line &#39;test1&#39; to README.md
9927ec0 create README.md


</div>2022-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/1e/18/9d1f1439.jpg" width="30px"><span>liaomars</span> 👍（0） 💬（1）<div>老师，想问下，有的时候一次修改可能跨了不同的scope，那scope怎么填写？</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（0） 💬（1）<div>作业1: git rebase -i --root</div>2021-10-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoib6BjEV4KPEaIdlLEfoVFRCxCSlL2XaIVDiaakvjhWEibibym323ZeHXAY46JMO3nSHmjiaWtAY47eww/132" width="30px"><span>dobby</span> 👍（50） 💬（1）<div>这一篇写得就很实用了，在小厂的几乎都不用这些规范。</div>2021-06-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（10） 💬（0）<div>好细致的规范 赞</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（9） 💬（1）<div>每次commit和rebase的时候才发现英语和语文是多么的重要，哎~</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（8） 💬（0）<div>这篇文章是迄今为止见过的最详细的commit规范。
平时只用git commit -m，实在没想到commit还有这么多讲究。
可见精益求精不止会体现在代码上，也可以体现在配套的生态中。
作者这种精益求精的态度值得钦佩。
</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（4） 💬（0）<div>做个笔记
1 git rebase -i &lt;父commit&gt; 一定是父commit id
2 pick 默认不动 s 合并 r 重写</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（4） 💬（0）<div>实战中用起来</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（3） 💬（0）<div>总结：
    1. 介绍 angular 规范，包括，type，scope，subject，body，footer。
    2. 开发手写 angular 规范的 commit message 几乎是不可能的，需要工具来帮助。
    3. commitzen-go 以交互的方式，帮助程序员生成 angular 规范的 commit message
    4. 通过 git hooks, 检查 commit message 规范，不符合时，git commit 执行失败
    5. 压缩 commit message 、修改 commit message ，都可以借助 git rebase -i 命令
    6. 基于 commit message, 使用 git-chglog 自动生成 CHANGELOG
    7. gsemver 自动生成语义化版本号，感觉和 angular message 规范，关系不大。</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/11/d7e08b5b.jpg" width="30px"><span>dll</span> 👍（3） 💬（0）<div>真的干货满满的 一下子看明白rebase 我以前还学的迷迷糊糊的
</div>2021-06-17</li><br/>
</ul>