你好，我是孔令飞。今天我们来聊聊如何编写高质量的Makefile。

我们在 [第10讲](https://time.geekbang.org/column/article/384648) 学习过，要写出一个优雅的Go项目，不仅仅是要开发一个优秀的Go应用，而且还要能够高效地管理项目。有效手段之一，就是通过Makefile来管理我们的项目，这就要求我们要为项目编写Makefile文件。

在和其他开发同学交流时，我发现大家都认可Makefile强大的项目管理能力，也会自己编写Makefile。但是其中的一些人项目管理做得并不好，我和他们进一步交流后发现，这些同学在用Makefile简单的语法重复编写一些低质量Makefile文件，根本没有把Makefile的功能充分发挥出来。

下面给你举个例子，你就会理解低质量的Makefile文件是什么样的了。

```
build: clean vet
	@mkdir -p ./Role
	@export GOOS=linux && go build -v .

vet:
	go vet ./...

fmt:
	go fmt ./...

clean:
	rm -rf dashboard
```

上面这个Makefile存在不少问题。例如：功能简单，只能完成最基本的编译、格式化等操作，像构建镜像、自动生成代码等一些高阶的功能都没有；扩展性差，没法编译出可在Mac下运行的二进制文件；没有Help功能，使用难度高；单Makefile文件，结构单一，不适合添加一些复杂的管理功能。

所以，我们不光要编写Makefile，还要编写高质量的Makefile。那么如何编写一个高质量的Makefile呢？我觉得，可以通过以下4个方法来实现：
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（16） 💬（4）<div>格式化代码、静态代码检查，这种ide或vim都会配置保存时格式化和代码检查，还有必要写在makefile中吗</div>2021-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（4） 💬（2）<div>总结：Makefile 是高效项目管理的重要工具，编写高质量的 Makefile，方便你做CI的检查，不至于自己的代码提交上以后，被提示各种不通过（静态代码检查、格式错误、单元测试等）。

要做好 Makefile 的管理，可按照下面的步骤：1. 学习 Makefile 语法；2. 规划 Makefile 要实现的功能；3. 规划 Makefile 结构；4. 善用 Makefile 技巧。

直接拷贝IAM项目的Makefile，也很香。</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/84/f45c4af9.jpg" width="30px"><span>Vackine</span> 👍（4） 💬（1）<div>写好一个功能齐全的项目的makefile，然后只对makefile 的各个功能做编排，是不是就可以做到基本的持续发布了？</div>2021-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/5d/a7/1a6b74df.jpg" width="30px"><span>青苔入镜</span> 👍（2） 💬（1）<div>我有些困惑，iam项目将控制流和数据流放在了一个仓库中，然后使用makefile进行管理，方便我们学习部署，这个我倒是可以理解。
实际企业中是将所有组件也放在一个大仓库中的吗？我所在公司是将项目各个组件分为各个小仓库，开发后进行持续交付和持续部署。我感觉这样也比较合理一些啊，适合现在微服务这样，单个人就维护几个组件。而且控制面和数据面如果部署在一台机器上不会影响数据面的性能吗？
什么场景需要用makefile来管理项目呢？私有化部署的项目吗？我没有想的太明白</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/0b/73628618.jpg" width="30px"><span>兔嘟嘟</span> 👍（1） 💬（2）<div>请问老师如何看待Makefile已过时的言论？
在知乎上查找相关资料时，发现很多人认为Makefile过时了，只需要学习cmake、bazel之类的，各种说法都有，现在有点晕</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/60/4f/db0e62b3.jpg" width="30px"><span>Daiver</span> 👍（1） 💬（2）<div>老师，看到iam项目下面的license 文件中添加了其他库的说明，这个是手动加上去的吗</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/6b/af7c7745.jpg" width="30px"><span>tiny🌾</span> 👍（0） 💬（1）<div>make lint执行完为什么会报这个错误
make[1]: *** [go.lint] Error 1
make: *** [lint] Error 2</div>2022-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/6b/af7c7745.jpg" width="30px"><span>tiny🌾</span> 👍（0） 💬（1）<div>运行make lint报错 ，这个怎么排查
make[1]: *** [go.lint] Error 1
make: *** [lint] Error 2
</div>2022-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（0） 💬（2）<div>.PHONY: format
format: tools.verify.golines
.PHONY: tools.verify.%
tools.verify.%:
	@if ! which $* &amp;&gt;&#47;dev&#47;null; then $(MAKE) tools.install.$*; fi
这里的 $* 是指 ‘golines’ 还是 ‘tools.verify.golines’ 呢？</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（1）<div>对 Windows 系统不友好，实际 CRUD 业务中，更多人是在 Windows 下开发吧（IDE 选 VSCode 或 GoLand）。</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e6/74/8b8097c1.jpg" width="30px"><span>牛2特工</span> 👍（0） 💬（1）<div>go为什么不设计专用的构建工具 
把常见通用的任务都集成了</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/cf/63/23db516f.jpg" width="30px"><span>CSB22</span> 👍（0） 💬（1）<div>您有没有比较好的makefile editor推荐么？</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/66/04/1919d4b4.jpg" width="30px"><span>夏心C.J</span> 👍（0） 💬（1）<div>$*是指示目标模式中 % 及其之前的部分，不是指代被匹配的值swagger、mockgen吧？</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>win上没有make命令 老师你的开发环境是linux或者mac么 win上怎么搞make</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ad/e6/bf43ee14.jpg" width="30px"><span>ggchangan</span> 👍（0） 💬（1）<div>老师的课程真是超值，特别感谢！有个问题请教下，怎么自动生成基于suite的测试代码呢？</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/01/8c/41adb537.jpg" width="30px"><span>Tiandh</span> 👍（0） 💬（1）<div>[going@dev iam]$ make install
make[1]: *** No rule to make target &#39;install.install&#39;.  Stop.
make: *** [Makefile:154: install] Error 2
[going@dev iam]$ </div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/72/2a/c4042a20.jpg" width="30px"><span>骑蜗牛的勇士</span> 👍（0） 💬（1）<div>看iam源码，各功能的service和store都是每次调用的时候，返回一个新的实例，这样对性能有影响吗，或者是有别的考虑吗？</div>2021-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/0a/18201290.jpg" width="30px"><span>Juniper</span> 👍（10） 💬（2）<div>这部分以前没接触过，先战略性放弃，后面再回来好好啃</div>2021-09-29</li><br/><li><img src="" width="30px"><span>Geek_23bbd5</span> 👍（2） 💬（0）<div>内容满满的...感觉都是作者的亲身体验</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（1） 💬（0）<div>Makefile 是只有go语言项目才会使用到的吗,小白问问</div>2023-06-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Pr5AAcOgyGosnjeNibbWp31xlqJJaThWwh5ZGuK1k2SbHSrq3vlIibAvhqcpibbp6Km75Y5rOrTwgVCnlbgV9hnwQ/132" width="30px"><span>Geek_d5b59b</span> 👍（0） 💬（0）<div>root@fusion:~&#47;go&#47;src&#47;marmotedu&#47;iam# codegen -type int .&#47;internal&#47;pkg&#47;code
codegen: internal error: package &quot;net&#47;http&quot; without types was imported from &quot;github.com&#47;marmotedu&#47;iam&#47;internal&#47;pkg&#47;code&quot;
tools&#47;codegen&#47;codegen.go代码有问题呀</div>2023-10-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLCrJQ4AZe8VrDkR6IO03V4Tda9WexVT4zZiahBjLSYOnZb1Y49JvD2f70uQwYSMibUMQvib9NmGxEiag/132" width="30px"><span>Dowen Liu</span> 👍（0） 💬（0）<div>编写简单，低耦合，可复用的代码。</div>2023-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/93/2a/08675e68.jpg" width="30px"><span>__PlasticMan</span> 👍（0） 💬（2）<div>建议通读项目的Makefile，看看项目是如何管理和构建的，有助于大幅提高项目的自动化水平。</div>2023-08-10</li><br/><li><img src="" width="30px"><span>Geek_6b7b96</span> 👍（0） 💬（0）<div>这就是和大佬的差距， 完成啃不动这一节</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（0）<div>用win开发的表示 亚历山大</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/8e/62/5cb377fd.jpg" width="30px"><span>yangchnet</span> 👍（0） 💬（0）<div>第二遍了，越读越觉得总结的到位精辟。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（0） 💬（0）<div>使用Makefile可以高效管理go项目。</div>2021-08-10</li><br/>
</ul>