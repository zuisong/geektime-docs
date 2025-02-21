你好，我是Tony Bai。

通过上一节课的讲解，我们掌握了Go Module构建模式的基本概念和工作原理，也初步学会了如何通过go mod命令，将一个Go项目转变为一个Go Module，并通过Go Module构建模式进行构建。

但是，围绕一个Go Module，Go开发人员每天要执行很多Go命令对其进行维护。这些维护又是怎么进行的呢？

具体来说，维护Go Module 无非就是对Go Module 依赖包的管理。但在具体工作中还有很多情况，我们接下来会拆分成六个场景，层层深入给你分析。可以说，学好这些是每个Go开发人员成长的必经之路。

我们首先来看一下日常进行Go应用开发时遇到的最为频繁的一个场景：**为当前项目添加一个依赖包**。

## 为当前module添加一个依赖

在一个项目的初始阶段，我们会经常为项目引入第三方包，并借助这些包完成特定功能。即便是项目进入了稳定阶段，随着项目的演进，我们偶尔还需要在代码中引入新的第三方包。

那么我们如何为一个Go Module添加一个新的依赖包呢？

我们还是以上一节课中讲过的module-mode项目为例。如果我们要为这个项目增加一个新依赖：github.com/google/uuid，那需要怎么做呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（40） 💬（8）<div>Tony Bai 老师这一讲的内容很实用，可以说有很多Go教程都没有涉及到这块知识的归纳总结。
麻烦老师抽空回答一下我以下的疑问：

1. 空导入的方式的作用吗？我看很多源码中有使用这种包导入的方式。

2. 在go module构建模式下，怎么对vendor目录的有无进行取舍呢？老师有什么实战建议呢？</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/ed/bb32e906.jpg" width="30px"><span>blur</span> 👍（28） 💬（2）<div>go mod edit -require=github.com&#47;sirupsen&#47;logrus@v1.7.0这个指令在win 上的golangd好像会因github 后面的那个 . 识别不出来path,加引号变成 go mod edit -require=&quot;github.com&#47;sirupsen&#47;logrus@v1.7.0&quot;就可以了</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/1e/4a93ebb5.jpg" width="30px"><span>Aaron Liu</span> 👍（17） 💬（7）<div>如果之前引用的包是v1，之后升级v2，go get可以替换引用的包，但源码里的import要怎么改，如果很多go文件都引用了呢</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（14） 💬（2）<div>老师讲太好了， 有主线 有关键细节，
请教老师， 关于vendor， 存好副本后， 一般在其他地方怎么用呢，
手动传输过去 还是 上传到代码库再下载呢</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/0a/02ecee7a.jpg" width="30px"><span>女干部</span> 👍（13） 💬（1）<div>老师你好，
有一个疑问困扰我很久了，这样一个例子:
安装 go get -u github.com&#47;cweill&#47;gotests&#47;...
然后就可以在命令行里执行 gotests了，
我想知道&#47;...这是个什么写法，
还有gotests.exe，是怎么构建并被放到我的%USERPROFILE%\go\bin目录下的
辛苦</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/16/5c/d0476f9f.jpg" width="30px"><span>运维夜谈</span> 👍（11） 💬（3）<div>老师这个专栏绝了，真的收获很大！
老师，想请教个问题，在一些无法连接外网的环境下，Go Module有没有类似maven和Nexus一样可以搭建自己的私库，然后私库去连接外部代理去下载依赖？</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（6） 💬（2）<div>大白老师，如果我想升级go.mod中定义的Go版本的话，最佳实践是不是这么操作：

go mod edit -go=1.17
</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（6） 💬（5）<div>我是一名前端，初“卷”到go，对比 go module 对比 npm （node 的包管理）：
1. vendor 类似于 node 项目中的 node_modules,
2. 默认条件下用 go get xxx 相当于 npm i -g xxx，
总之，我的方法就是结合新学的内容，和我熟悉的其他语言体系做对比；这样一是方便记忆，二可以更好的理解新知识。
老师的课条理清晰，深入浅出，点赞</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/1e/8ed4a7cf.jpg" width="30px"><span>Paradise</span> 👍（5） 💬（1）<div>Tony 的专栏不适合跳着看，因为细节干货太多啦哈哈，感谢老师</div>2022-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/13/2f/24420ab6.jpg" width="30px"><span>jacky</span> 👍（5） 💬（1）<div>讲得挺好，就是更新有点慢啊，这得更到啥时候</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/57/a3/09efc7cb.jpg" width="30px"><span>阿星</span> 👍（4） 💬（1）<div>两个问题请教 Tony Bai 老师,
1. go mod edit -require=github.com&#47;sirupsen&#47;logrus@v1.7.0 这种方式和直接改go.mod中对应的依赖效果是一样的吗？如果依赖更新多了，go get 肯定没有go mod tidy 方便

2. 如果go mod vendor 建立了当前依赖库的副本的话，默认go build 会用vendor来构建，那样依赖更新后，就必须再执行下go mod vendor 了，除非手动指定 -mod=mod 是这样吗？ </div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/86/d689f77e.jpg" width="30px"><span>Hank_Yan</span> 👍（3） 💬（1）<div>解决了我的疑问，之前还在想，如果是内网部署的服务，go 里面的依赖怎么处理呢？  原来还是可以继续使用 vendor 的，绝了！</div>2022-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/36/c5d1a120.jpg" width="30px"><span>CLMOOK🐾</span> 👍（3） 💬（1）<div>老师好，如果用go get给一个依赖包降为低一个次版本的，再跑go mod tidy是否会自动把这个依赖包升级成之前的新版本？</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/10/5173922c.jpg" width="30px"><span>泽韦德</span> 👍（3） 💬（1）<div>老师，当前Go Module自身的版本号怎么设置的，是不是没讲？</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3a/8d/f5e7a20d.jpg" width="30px"><span>何以解忧</span> 👍（3） 💬（2）<div>vendor 模式和 module 模式，互相有影响么，比如顶级目录下面，有go.mod 同时有vendor 目录。 vendor 下的modules.txt 和go.mod 可以理解为两种模式的类似的定位么，记录版本</div>2022-06-23</li><br/><li><img src="" width="30px"><span>woJA1wCgAApKZLcyM5n8DSoPyMkMZk5A</span> 👍（3） 💬（4）<div>老师，请问下replace和go vendor应该如何选择呢？比如引用一个第三方依赖包，但需要对其部分内容进行自定义修改，那么是使用vendor机制将其下载下来后修改还是使用replace替换那个官方的依赖包呢</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/f2/5edd20e1.jpg" width="30px"><span>E</span> 👍（2） 💬（1）<div>老师请教两个问题
1. 如果我想让logrus从v1.7.0恢复到默认最高版本，如何操作？只能手动执行go mod edit去指定一个特定版本么？有没有其他“复原”的方式。

2. 老师引用的包，都是发布于GO库的场景，如果A、B两个本地团队，A要引用B团队开发的一个工具，两方要如何操作呢？</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ec/08/68cf2f1b.jpg" width="30px"><span>116153</span> 👍（2） 💬（3）<div>老师好，作为一名现在的java coder跟随老师教程学习go,总是有意比较这两种语言。
在本节中，依赖包管理，java项目常用工具如maven,通常先在pom.xml中添加要依赖的包，maven自动下载，然后在代码里ide就自动提示并导入了；
而经过本节学习，go项目是先在代码里导入，然后执行命令下载，所依赖的包路径再自动写入go.mod中。
有点疑问，为什么go设计者们不采用maven那样，在go.mod中手动添加依赖，然后自动下载呢？</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bb/e0/c7cd5170.jpg" width="30px"><span>Bynow</span> 👍（2） 💬（1）<div>公共go包的作者应该比较关注 包的tag 和 go mod init 后面的v(版本)吧。</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（2）<div>go 的命令好多，老师来讲讲 使用 Makefile 来管理的方法</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（2） 💬（1）<div>虽然已用 Go 开发三年了，老师把所有的坑点都说了，还顺便讲了一些我不知道🤷‍♂️的知识点，受益匪浅！</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/29/50/2b2e6875.jpg" width="30px"><span>慕士塔格</span> 👍（1） 💬（1）<div>是不是直接修改go.mod版本号，然后go mod tidy一下更方便</div>2023-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/57/a3/09efc7cb.jpg" width="30px"><span>阿星</span> 👍（1） 💬（1）<div>老师，还有个不明白的地方，为什么我删除了依赖包后，GOMODCACHE中 pkg&#47;mod 中还存在这个包，这个里面是只能手动去删除的吗?</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/43/1aa8708a.jpg" width="30px"><span>子杨</span> 👍（1） 💬（1）<div>请问下老师，如果是不同的项目，需要依赖不同的包版本，那么是使用 vendor 来解决这种情况吗？</div>2022-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ea/5d/ccb4c205.jpg" width="30px"><span>绘世浮夸 つ</span> 👍（1） 💬（1）<div>老师，go里面有类似Java中的Maven和gradle这种版本依赖管理的工具吗，这样每次都要手动引入有点麻烦啊</div>2022-10-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eptSDsykxSicnicBibUOOmC9FOuuFWRaDkJqK69LOe10yQpIibYURwBgDrdqOTSlWPiaNbQ9Y8cMAhaENA/132" width="30px"><span>唐家岭大盗</span> 👍（1） 💬（1）<div>从远程仓库下载一个项目之后，要安装所有依赖，用什么命令啊？</div>2022-10-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eptSDsykxSicnicBibUOOmC9FOuuFWRaDkJqK69LOe10yQpIibYURwBgDrdqOTSlWPiaNbQ9Y8cMAhaENA/132" width="30px"><span>唐家岭大盗</span> 👍（1） 💬（1）<div>老师您好，使用go get依赖降级时发现一个问题，就是indirect依赖并不会降级。一开始依赖如下：
module github.com&#47;bigwhite&#47;hellomodule

go 1.18

require github.com&#47;valyala&#47;fasthttp v1.40.0

require (
	github.com&#47;andybalholm&#47;brotli v1.0.4 &#47;&#47; indirect
	github.com&#47;klauspost&#47;compress v1.15.0 &#47;&#47; indirect
	github.com&#47;valyala&#47;bytebufferpool v1.0.0 &#47;&#47; indirect
)
将fasthttp降级到v.12.0之后，并且go mod tidy之后依赖如下：
module github.com&#47;bigwhite&#47;hellomodule

go 1.18

require github.com&#47;valyala&#47;fasthttp v1.12.0

require (
	github.com&#47;klauspost&#47;compress v1.15.0 &#47;&#47; indirect
	github.com&#47;valyala&#47;bytebufferpool v1.0.0 &#47;&#47; indirect
)
然而fasthttp@v1.12.0实际上依赖compress v1.10.4，但是go mod中是compress v1.15.0。为什么不会展示实际的dependency</div>2022-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/8e/8fc00a53.jpg" width="30px"><span>🐎</span> 👍（1） 💬（1）<div>总结就是 go mod tidy 最好使</div>2022-08-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/uqaRIfRCAhL5pZIYib6S4nMSZcpCemic6YaVOpWWbiaDbYIRlXcyjtWJPuiciadr70ict63JEjkX4TzFvzYnSSU6jtMgQrdbVfmz6W/132" width="30px"><span>正在旅程</span> 👍（1） 💬（2）<div>go mod tidy 会自动分析依赖项这看起来很好，假设我现在项目里需要引入一个依赖，我在代码里手动添加了这个包，执行go mod tidy,默认是拉取该包的最新版本，灾难来了，我项目里的很多依赖也因为拉取这个包的缘故被升级，对于我来说简直就是个灾难，整个项目直接大量报错！这是我初学go时遇到的一个糟糕场景，不知道是不是我的“姿势”不到位。</div>2022-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（1） 💬（2）<div>老师请教一个版本号问题
我看我们的go 工程中以来内部的一个库比如  xxx&#47;CQRS&#47;consumer-mysql v0.0.0-20211213083836-9bbdf7237216
但我进入内部git这个工程下，从tag目录下，什么版本都没有，那这里引用的版本号，怎么来的呢，一直没有想明白</div>2022-07-07</li><br/>
</ul>