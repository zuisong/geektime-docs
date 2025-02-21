你好，我是张磊。今天我和你分享的主题是：深入解析声明式API之API对象的奥秘。

在上一篇文章中，我为你详细讲解了Kubernetes声明式API的设计、特点，以及使用方式。

而在今天这篇文章中，我就来为你讲解一下Kubernetes声明式API的工作原理，以及如何利用这套API机制，在Kubernetes里添加自定义的API对象。

你可能一直就很好奇：当我把一个YAML文件提交给Kubernetes之后，它究竟是如何创建出一个API对象的呢？

这得从声明式API的设计谈起了。

在Kubernetes项目中，一个API对象在Etcd里的完整资源路径，是由：Group（API组）、Version（API版本）和Resource（API资源类型）三个部分组成的。

通过这样的结构，整个Kubernetes里的所有API对象，实际上就可以用如下的树形结构表示出来：

![](https://static001.geekbang.org/resource/image/70/da/709700eea03075bed35c25b5b6cdefda.png?wh=1820%2A783)  
在这幅图中，你可以很清楚地看到**Kubernetes里API对象的组织方式，其实是层层递进的。**

比如，现在我要声明要创建一个CronJob对象，那么我的YAML文件的开始部分会这么写：

```
apiVersion: batch/v2alpha1
kind: CronJob
...
```

在这个YAML文件中，“CronJob”就是这个API对象的资源类型（Resource），“batch”就是它的组（Group），v2alpha1就是它的版本（Version）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（73） 💬（3）<div>运维人员会心碎?
我是运维人员，此刻看完我感到很兴奋。</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/4b/170654bb.jpg" width="30px"><span>千寻</span> 👍（31） 💬（7）<div>我从代码开始，就按着步骤走，最后创建network的CRD和example-network都成功了，
但是我直接将cdr&#47;network.yml和example&#47;example-network.yml文件单独拿出来，并没有执行代码生成那些步骤，发现也创建成功了，搞得有点懵。
老师可以说一下这大概是什么回事吗？</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（16） 💬（3）<div>好好好。之前学习过这些内容，但是很不系统，只是大概知道怎么回事，很多细节没有穿起来。跟老师比起来，我太不善于总结了。
磊哥大神，等我把你的课都学会了，能跟着你干吗？

另外我看到有人问需要把代码重新编译进k8s中么？不需要。作为插件应该是可以热插拔的。比如service catalog，flannel，都不要求你重启k8s。
在k8s里定义了你的CR后，controller可以作为一个container跑在k8s集群里，来响应CR的增删改。

</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（12） 💬（1）<div>自定义resource的Controller 单独运行，只是通过client-go 与api 交互？ 是否可以认为，k8s内建的Resource 对应的Controller，由Controller-manager 统一管理呢？</div>2019-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（11） 💬（1）<div>有一个问题张老师，一直不是特别清楚… 通过 crd 创建的自定义资源我还并没有定义他的结构，为什么就可以通过 kubectl get 拿到这个资源的详情呢？</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（8） 💬（4）<div>register.go会将自定义Type注册到APIServer，那register.go本身是怎么交给APIServer，然后被APIServer调用注册过程的？

$ kubectl apply -f crd&#47;network.yaml
$ kubectl apply -f example&#47;example-network.yaml 

执行完这两步，自定义的Newwork对象被创建出来，怎么感觉register.go并没有被用到</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/57/a84d633e.jpg" width="30px"><span>圣诞使者</span> 👍（4） 💬（1）<div>老师，我照着你的代码敲了一遍，这个pkg&#47;signals目录是自己创建的吗？我这个生成完代码也没有这个目录。</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（3） 💬（2）<div>这章会让运维人员心碎的...幸好俺会Go语言! 
请教下这个生成的代码，还得合并到apiserver的代码树中吧？还是得重新编译apiserver吧？毕竟Go目前还没有动态加载机制。</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（1） 💬（1）<div>怎么感觉register.go没有用到，它是什么时机把自定义Type注册到APIServer的？</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（1） 💬（1）<div>请问老师 通过那个CustomResourceDefinition相关的ymal文件已经可以正常定义查看crd了 为什么还需要写相关的go代码呢？生成的clients又是给谁用的呢？</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/91/fba79b87.jpg" width="30px"><span>小伟</span> 👍（0） 💬（1）<div>老师好，作为一个运维，觉得你讲的内容好深，学得好吃力，不知能否分享一些实际生产环境的troubleshooting 的案例和思路？</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（58） 💬（0）<div>一般来说，扩展api server (或者说添加自定义 resource )有两种方式：
1. 通过创建CRDs, 主API server可以处理 CRDs 的 REST 请求（CRUD）和持久性存储。简单，不需要其他的编程。更适用于声明式的API，和kubernetes高度集成统一。
2. API Aggregation, 一个独立的API server。主API server委托此独立的API server处理自定义resource。 需要编程，但能够更加灵活的控制API的行为，更加灵活的自定义存储，以及与API不同版本之间的转换。一般更适用于命令模式，或者复用已经存在REST API代码，不直接支持kubectl 和 k8s UI, 不支持scope resource in a cluster&#47;namespace.

自定义 resource 可以使你方便的存取结构化的resource 数据。但是只有和controller组合在一起才是声明式API。声明式API允许你定义一个期望的状态。controller通过解读结构化的resource数据，获得期望状态，从而不断的调协期望状态和实际状态。

综上，今天文档中的types.go 应该是给controller来理解CRDs的schema用的。只有掌握了resource的schema，才能解释并得到用户创建的resource API object。
而 kubectl create -f resourcedefinition.yaml 或者 自定义API server， 则定义了RESTful API endpoint. 用于接受 REST 请求，改变 resource 的期望状态。
</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/c9/9f783069.jpg" width="30px"><span>小金刚</span> 👍（45） 💬（0）<div>可以用 kubebuild 自动生成项目框架，添加自己的 CRD 并实现 controller 即可。</div>2018-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ca/d5/a2cd57c9.jpg" width="30px"><span>小明root</span> 👍（37） 💬（11）<div>我是运维人员，我很心碎.....我不会go语言</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（17） 💬（2）<div>我是开发人员，会go,也会C++，也自己设计过业务协议，看到这篇异常兴奋</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/44/b8/d5fe40fb.jpg" width="30px"><span>Vndi</span> 👍（16） 💬（1）<div>CRD就像你去数据库定义一张表，CR就像表里的记录</div>2021-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/11/e8506a04.jpg" width="30px"><span>小宇宙</span> 👍（11） 💬（0）<div>用CRD来开发定义自主化的operator ，将有状态的应用自动化</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/81/8dd164fb.jpg" width="30px"><span>丶海口</span> 👍（9） 💬（0）<div>使用最新版本 cd 到 code-generator 目录去执行会报错，改成这样就好了：
# 代码生成的工作目录，也就是我们的项目路径
ROOT_PACKAGE=&quot;github.com&#47;resouer&#47;k8s-controller-custom-resource&quot;
# API Group
CUSTOM_RESOURCE_NAME=&quot;samplecrd&quot;
# API Version
CUSTOM_RESOURCE_VERSION=&quot;v1&quot;
# Code-Generator Directory
EXEC_DIR=$GOPATH&#47;src&#47;k8s.io&#47;code-generator

# 安装 k8s.io&#47;code-generator
go get -u k8s.io&#47;code-generator&#47;...

# 执行代码自动生成，其中pkg&#47;client是生成目标目录，pkg&#47;apis是类型定义目录
&quot;${EXEC_DIR}&quot;&#47;generate-groups.sh all &quot;$ROOT_PACKAGE&#47;pkg&#47;client&quot; &quot;$ROOT_PACKAGE&#47;pkg&#47;apis&quot; &quot;$CUSTOM_RESOURCE_NAME:$CUSTOM_RESOURCE_VERSION&quot; --go-header-file &quot;${EXEC_DIR}&quot;&#47;hack&#47;boilerplate.go.txt -v 10</div>2021-11-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/nhLS152kEs5J65bBpM2fzMn4agfoow8xibFzNSDcmo9Oiby2lNB4hWRcetRWFyY2y05IJu8GbkZer9BUiahtadU0w/132" width="30px"><span>yuanlinios</span> 👍（8） 💬（0）<div>.&#47;generate-groups.sh all &quot;$ROOT_PACKAGE&#47;pkg&#47;client&quot; &quot;$ROOT_PACKAGE&#47;pkg&#47;apis&quot; &quot;$CUSTOM_RESOURCE_NAME:$CUSTOM_RESOURCE_VERSION&quot;
Generating deepcopy funcs
F1228 01:11:20.543446    2908 deepcopy.go:866] Hit an unsupported type invalid type.
</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/93/38/71615300.jpg" width="30px"><span>DayDayUp</span> 👍（7） 💬（1）<div>看了好兴奋，真的感觉自己能够从一个旁观者慢慢变成一个开发贡献者</div>2020-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/89/9312b3a2.jpg" width="30px"><span>Vincen</span> 👍（7） 💬（0）<div>从kubernetes用户到kubernetes玩家成长中...</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/ca/c3949f49.jpg" width="30px"><span>疯狂的小企鹅</span> 👍（6） 💬（0）<div>提示 Hit an unsupported type invalid type的同学，可以先安装下k8s.io&#47;apimachinery包。应该是deepcopy找不到metav1.ObjectMeta和metav1.TypeMeta
go get -u k8s.io&#47;apimachinery</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/4a/c02c597b.jpg" width="30px"><span>Joe</span> 👍（5） 💬（1）<div>Generating deepcopy funcs
F0110 15:05:38.168635   11946 deepcopy.go:866] Hit an unsupported type invalid type.

按文档走了一半，报错~ 这个是什么问题呀？</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/95/aad51e9b.jpg" width="30px"><span>waterjiao</span> 👍（4） 💬（0）<div>deepcopy的作用是什么？runtime.Object是什么呢？是Network这个资源在k8s客户端的形态呢？</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/55/d7/67c517c0.jpg" width="30px"><span>刘小鹏</span> 👍（3） 💬（1）<div>老师，容器是单进程模型的，那在一个容器中能运行多个不同进程么？多个相同进程又可以么？</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/d9/bf/897f4f93.jpg" width="30px"><span>打小就会敲代码</span> 👍（2） 💬（0）<div>我的 k8s server 版本是v1.24.0，文中关于 Network 的 CRD 已经失败了，我将更改后的放到了 github。https:&#47;&#47;github.com&#47;mayooot&#47;k8s-controller-custom-resource</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/76/0f/c7c8021d.jpg" width="30px"><span>豆豆</span> 👍（2） 💬（1）<div>之前死磕这一块，啃不下去。跳槽后，同事跟我说，直接上kubebuilder，我不想，我就想搞懂，回过头来，一行一行的看这几节关于operator的开发章节，就想搞清楚内部原理，终于看懂了，终于搞明白了。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/e5/ab/cece3199.jpg" width="30px"><span>jason</span> 👍（2） 💬（0）<div>v1.22.2执行create -f network.yaml报错，error validating &quot;network.yaml&quot;: error validating data: [ValidationError(CustomResourceDefinition.spec): unknown field &quot;version&quot;</div>2021-11-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoxRRRXqZ3FjR7kaeTmj73C6zjeX8SWDX70Tg0OOBG44vQ4Xtr7xphVeHhdtp6RwbwrTMfaOFTkRQ/132" width="30px"><span>Geek_260c9a</span> 👍（2） 💬（3）<div>没有弄明白生成这些代码和CRD可以被k8s 识别的必然联系。</div>2019-10-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BIRpwViaN51yynIeFonD7QRlwDCVtKibrG956NTxzEqibOZZVjhMMgibOPmd3VicfYxpknZsic1oJq8KicZvXkmmiajuQg/132" width="30px"><span>tuyu</span> 👍（2） 💬（1）<div>老师你好, 问一下这个metav1是啥意思</div>2019-09-26</li><br/>
</ul>