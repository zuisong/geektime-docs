你好，我是Tony Bai。

现在是2021年12月，万众期盼的潜力网红版本Go 1.18的开发已经冻结，Go核心开发团队正在紧锣密鼓地修bug。我们已经可以开始期待2022年的2月份，Go 1.18将携带包括泛型语法的大批新特性赶来。不过当下我们不能“舍近求远”，今年8月中旬Go核心团队发布的 [Go 1.17版本](https://go.dev/blog/go1.17)才是当下最具统治力的Go社区网红，它的影响力依旧处于巅峰。

根据我们在[第3讲](https://time.geekbang.org/column/article/427489)中提到的Go版本选择策略，我估计很多Go开发者都还没切换到Go 1.17版本，没有亲自体验过Go 1.17新特性带来的变化；还有一些Go开发者虽然已经升级到Go 1.17版本，但也仅限于对Go 1.17版本的基本使用，可能还不是很清楚Go 1.17版本中究竟有哪些新特性，以及这些新特性会带给他们哪些好处。

所以今天这讲，我们就来聊聊Go 1.17版本中的新特性，目的是让那些没用过Go 1.17版本，或者用过Go 1.17版本但还不知道它新特性变化的Go开发者，对Go 1.17有一个全面的了解。

Go 1.17版本中的新特性很多，在这里我就不一一列举了，我仅挑几个有代表性的、重要的新特性和你好好聊聊。这里会包括新的语法特性、Go Module机制变化，以及Go编译器与运行时方面的变化。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/44/b5/7eba5a0e.jpg" width="30px"><span>木木</span> 👍（3） 💬（2）<div>老师您好，我也想跑一下您的这个benchmark测试代码，请问文中的代码是完整代码么？以及go test -bench . 中的“-bench .”是什么意思？</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/b9/c8/4c0cc367.jpg" width="30px"><span>言己</span> 👍（3） 💬（1）<div>性能测试示例代码，golang 的字符串拼接原来有这么多方式。</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（2）<div>看了大白老师的这节课后，马上升级到了1.17版本。

1. 我是直接下载macOS的pkg安装包覆盖原来安装的，之前的版本也是这么安装的，请问老师，这么操作在Mac上面，属于比较通用的升级方式吗？

2. 另外文中这这句话：“并指定一些寄存器为调用保存寄存器，允许函数在不同的调用中保持状态。” 能展开说一下不，没太明白这句话？

2. “或者依赖一些像比较函数代码指针的未公开的行为。” 能详细说一下什么是未公开的行为呢？

3. 我是直接修改go.mod中的go 版本为：go 1.15，然后执行本课程之前讲的在本地安装多个go版本的go 1.15.13 版本的测试命令： go1.15.13 test -bench .  发现比1.17版本耗时增加很多。  请问老师，我的这个测试方式是正确的么？

ps: go module 的变更那里，需要先 执行go install golang.org&#47;x&#47;exp&#47;cmd&#47;txtar@latest  安装txtar工具。
</div>2021-12-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（2） 💬（1）<div>与时俱进的一个语言。</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（2） 💬（1）<div>老师，java是基于堆栈的还是基于寄存器的？我的理解好像是基于堆栈的😂，但不知道是否正确</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b0/6e/921cb700.jpg" width="30px"><span>在下宝龙、</span> 👍（2） 💬（1）<div>老师您好，我最近使用go mod tidy 发现并不能很好的生效，使用之后 go mod文件并没有增加出自己想要的包信息，给我的提示是这个，我尝试去理解并没有找到答案- =，我的go版本是1.17
To upgrade to the versions selected by go 1.16:
        go mod tidy -go=1.16 &amp;&amp; go mod tidy -go=1.17
If reproducibility with go 1.16 is not needed:
        go mod tidy -compat=1.17</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/39/72d81605.jpg" width="30px"><span>大尾巴老猫</span> 👍（1） 💬（1）<div>后续是否会讲解如何搭建一套私有的开发环境？企业级应用开发，通常有一些安全合规相关的要求，使用go mod，不太可能直接从github或者gitee上引用，私有代码库通常也是需要身份验证的，这种情况下如何使用go get？</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（1） 💬（2）<div>go 1.18版本的泛型还是比较让人期待的</div>2021-12-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（1） 💬（2）<div>按第7讲的第一段代码，能go run代码，但是logrus.Println 一直显示红色报错，尝试很多办法，解决
go构建约束问题，Build constraints exclude all Go files in c：src下代码目录文件夹？
尝试以下办法解决不了
1、searcheverything 搜索后删除所有包,
$GOPATH目录下，把对应的包删除，重新go get,还是不行.
2、go get -u -v github.com&#47;karalabe&#47;xgo
3、Right click -&gt; Mark folder as not excluded.
4、引用包报错，重启电脑，查看goproxy配置，还不行重装goland，还是IDE，引用的github.com&#47;sirupsen&#47;logrus红色下画波浪线，和logrus.Println红色报错
怎么解决，寻求老师帮助，谢谢。</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（1） 💬（1）<div>我已经被go mod的本地包的引入方式难受死了，为了能引入本地包，我不得不把我的代码提前上传到码云。</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（1） 💬（1）<div>老师后面可以加餐说下 go 1.18 的新“工作区模式”特性吗？感觉和泛型一样，它也会是一个重要的新特性。</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（0）<div>修剪的 go mod 依赖终于符合我的直觉了，刚开始使用 go mod 的时候，这种简接依赖真的让我很不理解，现在终于被修复了。</div>2021-12-18</li><br/>
</ul>