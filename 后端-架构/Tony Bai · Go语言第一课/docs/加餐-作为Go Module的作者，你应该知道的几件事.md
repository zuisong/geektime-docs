你好，我是Tony Bai。

我们的专栏在06和07讲对Go Module构建模式的原理，以及如何使用Go Module构建模式做了详细的讲解，在课后留言中，我看到很多同学直呼过瘾，表示终于搞清楚Go Module构建模式了。

不过，之前的讲解更多是从Go Module的使用者角度出发的。在这篇加餐中，我们再从Go Module的作者或维护者的视角，来聊聊在规划、发布和维护Go Module时需要考虑和注意什么事情，包括go项目仓库布局、Go Module的发布、升级module主版本号、作废特定版本的module，等等。

我们先来看看作为Go Module作者在规划module时遇到的第一个问题：一个代码仓库（repo）管理一个module，还是一个仓库管理多个module？

## 仓库布局：是单module还是多module

如果没有单一仓库（monorepo）的强约束，那么在默认情况下，你选择一个仓库管理一个module是不会错的，这是管理Go Module的最简单的方式，也是最常用的标准方式。这种方式下，module维护者维护起来会很方便，module的使用者在引用module下面的包时，也可以很容易地确定包的导入路径。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（1） 💬（3）<div>老师，你好。有没有构建module的项目过程的资料？比如我新建一个项目，想发布出去，整个流程是如何？</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/22/9b/4486d287.jpg" width="30px"><span>黄常凯</span> 👍（0） 💬（1）<div>在代码里import的包，是怎么找到github上的呢？是goproxy的作用吗</div>2022-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/38/4c9cfdf4.jpg" width="30px"><span>谢小路</span> 👍（0） 💬（1）<div>一个隐性规则，tag 永远递增（不会删除，更不会递减），就能避免很多问题。</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（2）<div>有个疑问： 发布版本的时候是 V2.0.0 ， 安装的时候 是不是直接找  v2.0.0 这个 tag就可以了？ 和 go.mod 指定的版本是没有关系？  go.mod 指定的版本 只是依赖模块内部进行区分的</div>2022-02-14</li><br/>
</ul>