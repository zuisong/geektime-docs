你好，我是吴咏炜。

今天这一讲，我会介绍 Python 程序员定制 Vim 工作环境的完整方法。

Python 的流行程度越来越高，Python 程序员们对此一定是很高兴的。在 Stack Overflow 的 2020 年开发者调查里，Python 在最受爱戴（most loved）的语言里排名第三，而在最想要（most wanted）的语言里则已经连续四年排名第一！因此，它在 Vim 的生态系统里受到了良好的支持，也不会是件令人吃惊的事。有开发者已经把 Python 开发所需要的若干插件揉到了一起，组成了一套开箱即用的工具，python-mode。

今天我们就以它为基础，讨论一下 Vim 对开发 Python 提供的支持。

## 功能简介

[Python-mode](https://github.com/python-mode/python-mode) 实际上是以 Vim 插件形式出现的一套工具，它包含了多个用于 Python 开发的工具。根据官网的介绍，它的主要功能点是：

- 支持 Python 3.6+
- 语法加亮
- 虚拟环境支持
- 运行 Python 代码（`<leader>r`）
- 添加/删除断点（`<leader>b`）
- 改善了的 Python 缩进
- Python 的移动命令和操作符（`]]`, `3[[`, `]]M`, `vaC`, `viM`, `daC`, `ciM`, …）
- 改善了的 Python 折叠
- 同时运行多个代码检查器（`:PymodeLint`）
- 自动修正 PEP 8 错误（`:PymodeLintAuto`）
- 自动在 Python 文档里搜索（`K`）
- 代码重构
- 智能感知的代码完成
- 跳转到定义（`<C-c>g`）
- ……
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（2）<div>学习了。

平常工作中，python用的不多，我就用coc.nvim应付一下算了。
有基本的语法高亮、补全、跳转就行了。
</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cf/db/9693d08f.jpg" width="30px"><span>YouCompleteMe</span> 👍（1） 💬（1）<div>测了下--startuptime，IsGitRepo在我的电脑上带来140ms的耗时，换成 let g:pymode_rope = !empty(finddir(&#39;.git&#39;, &#39;.;&#39;)) ,耗时较少。同时看到colorscheme 设置语句，会带来30ms的加载时间，这个有办法优化吗～</div>2020-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2b/ca/71ff1fd7.jpg" width="30px"><span>谁家内存泄露了</span> 👍（0） 💬（1）<div>吴老师好，我用python都是小工程，不是大工程，因此我有个疑问：
我遇到的python工程中没有使用过cmake组织代码（或者说python这种解释类语言不需要？），
所以也不会生成ycm中提到的数据库json文件。
那在这种情况下，vim如何在全工程范围内进行find reference等跳转呢？</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（0） 💬（2）<div>老师, 断点的功能怎么用呢, 我设置了断点后, 使用&lt;leader&gt;r运行python程序后, 状态栏提示:[Pymode] Code running ..., 就这样卡住了, 不知道接下来该怎么操作</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9b/35/79e42357.jpg" width="30px"><span>铁匠</span> 👍（0） 💬（3）<div>使用pyenv和portry来管理依赖，怎么为不同项目配置不同虚拟目录</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cf/db/9693d08f.jpg" width="30px"><span>YouCompleteMe</span> 👍（0） 💬（2）<div>又到了纠结用ale 还是 pymode 和 YouCompleteMe提供的诊断功能了-_-</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/cd/2c513481.jpg" width="30px"><span>瀚海星尘</span> 👍（0） 💬（0）<div>最近正好在用 python 开发，配置好马上就用上了，真香！</div>2020-10-22</li><br/>
</ul>