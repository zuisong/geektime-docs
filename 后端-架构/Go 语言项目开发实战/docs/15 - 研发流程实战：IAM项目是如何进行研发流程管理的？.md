你好，我是孔令飞。

在 [**08讲**](https://time.geekbang.org/column/article/383390) 和 [**14讲**](https://time.geekbang.org/column/article/388920) ，我分别介绍了如何设计研发流程，和如何基于 Makefile 高效地管理项目。那么今天，我们就以研发流程为主线，来看下IAM项目是如何通过Makefile来高效管理项目的。学完这一讲，你不仅能更加深刻地理解 **08讲** 和 **14讲** 所介绍的内容，还能得到很多可以直接用在实际操作中的经验、技巧。

研发流程有很多阶段，其中的开发阶段和测试阶段是需要开发者深度参与的。所以在这一讲中，我会重点介绍这两个阶段中的Makefile项目管理功能，并且穿插一些我的Makefile的设计思路。

为了向你演示流程，这里先假设一个场景。我们有一个需求：给IAM客户端工具iamctl增加一个helloworld命令，该命令向终端打印hello world。

接下来，我们就来看下如何具体去执行研发流程中的每一步。首先，我们进入开发阶段。

## 开发阶段

开发阶段是开发者的主战场，完全由开发者来主导，它又可分为代码开发和代码提交两个子阶段。我们先来看下代码开发阶段。

### 代码开发

拿到需求之后，首先需要开发代码。这时，我们就需要选择一个适合团队和项目的Git工作流。因为Git Flow工作流比较适合大型的非开源项目，所以这里我们选择**Git** **Flow工作流**。代码开发的具体步骤如下：
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（4） 💬（2）<div>“如果 review 不通过，feature 开发者可以直接在 feature&#47;helloworld 分支修正代码，并 push 到远端的 feature&#47;helloworld 分支，然后通知 reviewers 再次 review。因为有 push 事件发生，所以会触发 GitHub Actions CI 流水线。”

请问修复后的代码是直接执行gith commit --amend还是重新创建一个commit</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/53/c93b8110.jpg" width="30px"><span>daz2yy</span> 👍（4） 💬（3）<div>老师好，想问下，测试阶段过了之后，这个特性就能直接上线吗？还是说等大家一起开发完这个迭代内容再上线？
另外，后端开发这里经常会设计 SQL 的变动，一种是数据变动，一种是结构变动，老师这块怎么去管理的呢？还有如何集成到特性研发流程里的呢？</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（3） 💬（2）<div>release分支是从develop分支来的，如果测试直接通过，没有做进一步修改，就不用再合并到develop分支了吧，直接合并到master分支就可以了吧，这样理解对不对呢</div>2021-06-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/xfclWEPQ7szTZnKqnX9icSbgDWV0VAib3Cyo8Vg0OG3Usby88ic7ZgO2ho5lj0icOWI4JeJ70zUBiaTW1xh1UCFRPqA/132" width="30px"><span>Geek_6bdb4e</span> 👍（2） 💬（2）<div>我来回答一下第一个问题：make dependencies会执行dependencies.run，进而执行1. dependencies.packages，这个是对代码本身依赖的packages进行管理，2. dependencies.tools，这个是对项目本身依赖的一些工具进行检查和管理，其中又根据重要等级区分为blocker和critical以及trivial，缺失blocker可能导致CI流程失败，缺失critical可能导致make的一些环节失败，tiivial是可选的工具，缺失没有任何影响。我有一个小问题，这个make dependencies的调用时机是什么时候，发现只有通过make dependencies时候才会调用，为什么不把这条放到make all的依赖项里面呢</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ea/11/4f464693.jpg" width="30px"><span>徐蕴</span> 👍（2） 💬（1）<div>测试完成的tag应该打在master上，还是release分支对应的commit上呢？master上应该还有其它没有测试的功能吧？</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/67/17/cbd5c23f.jpg" width="30px"><span>H.xu</span> 👍（1） 💬（2）<div>[going@192 iam]$ make test
===========&gt; Run unit test
found packages example (doc.go) and main (example.go) in &#47;home&#47;going&#47;workspace&#47;golang&#47;src&#47;github.com&#47;marmotedu&#47;iam&#47;pkg&#47;rollinglog&#47;example
found packages example (doc.go) and main (example.go) in &#47;home&#47;going&#47;workspace&#47;golang&#47;src&#47;github.com&#47;marmotedu&#47;iam&#47;pkg&#47;validator&#47;example
no Go files in &#47;home&#47;going&#47;workspace&#47;golang&#47;src&#47;github.com&#47;marmotedu&#47;iam
make[1]: *** [scripts&#47;make-rules&#47;golang.mk:81: go.test] Error 1
make: *** [Makefile:108: test] Error 2
这个错误是什么原因的呀</div>2022-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b4/35/3a96e893.jpg" width="30px"><span>🌿小毒草</span> 👍（1） 💬（1）<div>如何保证“通过make gen 生成的存量代码要具有幂等性”， 如何测试？</div>2022-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a2/94/ae0a60d8.jpg" width="30px"><span>江山未</span> 👍（1） 💬（1）<div>根据符合规范的commit message 生成版本号，这里有个疑问
是一次commit会滚动一次数字吗？因为一个版本可能包含多个feature，feature a有一次commit，feature b有一次commit，但它们都属于这次的版本更新。那会造成 minor version +2 吗</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（1） 💬（1）<div>总结：这些步骤应该是开发者经常遇到的。
开发阶段：执行 make all，本地走一遍CI流程。包括，自动生成部分代码或文档、静态代码检查、代码格式化、构建等。
提交阶段：检查 commit message 是否符合 angular 规范；在 push commit &#47; pull request &#47; merge to develop 点，触发 CI 流程。所以，开发者要有在本地跑CI的方法。
测试阶段：按照 Git Flow 的原则，创建出 release 分支，对代码进行测试。</div>2021-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（2）<div>孔老板，能大致说说：IAM 项目的分支命令规则图怎么解读吗？

主要确认一下和我理解的是否相同。</div>2021-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5f/f8/1d16434b.jpg" width="30px"><span>陈麒文</span> 👍（1） 💬（1）<div>这么多的知识点，从哪开始入手比较能跟上大佬的节奏？</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/17/63887353.jpg" width="30px"><span>王骥</span> 👍（1） 💬（2）<div>执行make 失败，no such linter cyclop

[going@dev iam]$ make
===========&gt; Generating iam error code go source files
===========&gt; Generating error code markdown documentation
===========&gt; Generating missing doc.go for go packages
===========&gt; Formating codes
===========&gt; Run golangci to lint source codes
ERRO Running error: no such linter cyclop, run &#39;golangci-lint linters&#39; to see the list of supported linters
make[1]: *** [scripts&#47;make-rules&#47;golang.mk:76: go.lint] Error 3
make: *** [Makefile:101: lint] Error 2
[going@dev iam]$ go version
go version go1.16.2 linux&#47;amd64
[going@dev iam]$ golangci-lint version
golangci-lint has version v1.28.4-0.20200719134607-6a689074bf17 built from (unknown, mod sum: &quot;h1:LlCfXb0ozr7UL4sgH7UbR2Rt2eSjQE&#47;1zcIeWTu7ypk=&quot;) on (unknown)</div>2021-07-31</li><br/><li><img src="" width="30px"><span>Geek_4c902b</span> 👍（1） 💬（1）<div>老师，您好：
iamctl new helloworld  这个iamctl 命令哪来的呀</div>2021-06-29</li><br/><li><img src="" width="30px"><span>小达</span> 👍（0） 💬（1）<div>iamctl new helloworld -d internal&#47;iamctl&#47;cmd&#47;helloworld这个在哪个目录下执行呢</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/cf/63/23db516f.jpg" width="30px"><span>CSB22</span> 👍（0） 💬（1）<div>Mark一个知识点：Maintainer 处理 pull request 冲突合并。https:&#47;&#47;blog.csdn.net&#47;danchenziDCZ&#47;article&#47;details&#47;81061989</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>孔老师，--tags  和 --always 还是没能理解。能再详细说说看吗？</div>2021-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>孔老板，这里文中创建的release分支的版本1.0.0：git checkout -b release&#47;1.0.0 develop。

是最佳实践吗？ 还是根据需要任意创建一个版本即可。</div>2021-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（0） 💬（3）<div>测试通过后，将功能分支合并到 master 分支和 develop 分支。本地执行完merge步骤还得同步到远端仓库吧？</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（10） 💬（0）<div>这一套流程下来确实能节省很多时间，重复性的操作交给自动化比人手工写更加可靠。
高效，省时省力还不易出错。</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/73/eb/a3bdb006.jpg" width="30px"><span>Fukans</span> 👍（0） 💬（0）<div>.PHONY: copyright.verify    
copyright.verify: tools.verify.addlicense 
  ...
tools.verify.%:          
  @if ! which $* &amp;&gt;&#47;dev&#47;null; then $(MAKE) tools.install.$*; fi
.PHONY: install.addlicense                              
install.addlicense:        
  @$(GO) get -u github.com&#47;marmotedu&#47;addlicense
###

检查如果命令不存在，则执行 tools.install.$*。

但下面的目标写的是 install.addlicense，没有 tools前缀，可以匹配到该目标吗？</div>2024-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/1b/75/0d18b0bc.jpg" width="30px"><span>Lee</span> 👍（0） 💬（1）<div>这里有个疑惑的店：如果基于develop分支checkout的话,假如开发已经完成并且通过测试了功能A，但是develop环境此时还有通过测试但是未打算上线的其他功能B，如果此时把dev分支合并到release分支的话，是不是功能B也一并被上线了？</div>2023-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/26/44095eba.jpg" width="30px"><span>SuperSu</span> 👍（0） 💬（0）<div>慢慢的干活</div>2022-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f0/eb/24a8be29.jpg" width="30px"><span>RunDouble</span> 👍（0） 💬（1）<div>好像没有用 git rebase origin&#47;develop</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（0） 💬（0）<div>私房干活👍</div>2021-10-21</li><br/>
</ul>