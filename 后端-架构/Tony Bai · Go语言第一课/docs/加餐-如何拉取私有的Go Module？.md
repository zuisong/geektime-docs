你好，我是Tony Bai。

我们这门课程上线以来收到了同学们的众多留言与热烈反馈，在这些留言和反馈中，有关Go Module的问题占比比较大，其中又以下面这两个问题比较突出：

- 在某module尚未发布到类似GitHub这样的网站前，如何import这个本地的module？
- 如何拉取私有module？

借这次加餐机会，今天我就针对这两个问题和你聊聊我知道的一些解决方案。

首先我们先来看第一个问题：如何导入本地的module。

## 导入本地module

在前面的06和07讲，我们已经系统讲解了Go Module构建模式。Go Module从Go 1.11版本开始引入到Go中，现在它已经成为了Go语言的依赖管理与构建的标准，因此，我也一直建议你彻底抛弃Gopath构建模式，全面拥抱Go Module构建模式。并且，这门课中的所有例子和实战小项目，我使用的都是Go Module构建模式。

当我们的项目依赖已发布在GitHub等代码托管站点的公共Go Module时，Go命令工具可以很好地完成依赖版本选择以及Go Module拉取的工作。

**不过，如果我们的项目依赖的是本地正在开发、尚未发布到公共站点上的Go Module，那么我们应该如何做呢？**我们来看一个例子。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（4） 💬（1）<div>一直使用的都是 replace，还好我们的代码不是太多，人员也少，还没有自己造出比较好用的轮子，所以 replace 的都是本仓库内的代码，仓库内包含公共库和服务。期待 1.18 能尽可能降低开发者的心智负担，replace 我刚开始用的时候，理解起来还是非常费劲的。虽然比 gopath 好了不少，但是 go 在引包的这一块相比简单哲学还是不够友好。</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>大白老师的每篇文章，我都会认真研读几遍。这个专栏下来，自己认为对Go有了全面的认识。有几个小问题，还请解答。

1. 文中：export GOPRIVATE = {private module list}，“private module list” 这里的配置大概是什么样子的呢？

2. 老师，安装goproxy这里，这个地址：http:&#47;&#47;10.10.20.20:8081 是不是相当于自己搭建的内网 服务器地址，每个人的都可能不同？ 我用本地 127.0.0.1地址来安装测试，出现了这个错误：goproxy.io: http: proxy error: dial tcp: lookup goproxy.iogoproxy.io: no such host &#47; goproxy.io: 0.460s 502 &#47;github.com&#47;pkg&#47;errors&#47;@v&#47;list

3. 统一 Goproxy 方案的实现拓扑图中的 gerrit git 服务器（10.10.30.30）这里的 “gerrit” 代表什么意思呢？</div>2022-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/28/22/ebc770dc.jpg" width="30px"><span>哈哈哈哈哈</span> 👍（1） 💬（1）<div>好耶%*%</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/4f/ff04156a.jpg" width="30px"><span>天天向上</span> 👍（0） 💬（1）<div>内部采用了方案二，Gitlab托管的公共库</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/33/b71635c1.jpg" width="30px"><span>锋子</span> 👍（0） 💬（1）<div>好像懂了，又好像没懂。 对于go.mod的module名字有啥意义不？ 是否可以随便取，还是会影响什么？ 比如我要引用的moduleB，那这个moduleB是在哪里定义的？ 是moduleB的go.mod里配的名字还是路径名字？ </div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/b1/54/6d663b95.jpg" width="30px"><span>瓜牛</span> 👍（0） 💬（2）<div>想问一下那种非github的仓库，比如Russ Cox的个人域名（好像是rsc.io？）作为前缀的module是如何实现的，go get的搜索路径是怎样的？</div>2022-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（1）<div>公司里正好用到了私有仓库的搭建，二刷一下，老师的每篇文章都是精品。</div>2022-04-07</li><br/>
</ul>