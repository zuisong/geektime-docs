你好，我是孔令飞。这一讲我们来聊聊构建应用时常用的Go包。

因为IAM项目使用了Pflag、Viper和Cobra包来构建IAM的应用框架，为了让你后面学习更加容易，这里简单介绍下这3个包的核心功能和使用方式。其实如果单独讲每个包的话，还是有很多功能可讲的，但我们这一讲的目的是减小你后面学习IAM源码的难度，所以我会主要介绍跟IAM相关的功能。

在正式介绍这三个包之前，我们先来看下如何构建应用的框架。

## 如何构建应用框架

想知道如何构建应用框架，首先你要明白，一个应用框架包含哪些部分。在我看来，一个应用框架需要包含以下3个部分：

- 命令行参数解析：主要用来解析命令行参数，这些命令行参数可以影响命令的运行效果。
- 配置文件解析：一个大型应用，通常具有很多参数，为了便于管理和配置这些参数，通常会将这些参数放在一个配置文件中，供程序读取并解析。
- 应用的命令行框架：应用最终是通过命令来启动的。这里有3个需求点，一是命令需要具备Help功能，这样才能告诉使用者如何去使用；二是命令需要能够解析命令行参数和配置文件；三是命令需要能够初始化业务代码，并最终启动业务进程。也就是说，我们的命令需要具备框架的能力，来纳管这3个部分。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（14） 💬（1）<div>使用Pflag解析命令行参数，使用Viper解析配置文件，使用Cobra实现命令行框架。
复用优秀轮子省时省力。</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（7） 💬（1）<div>总结一下：
1：cobra = flag+启动流程管理
2： viper读取配置文件+flag参数 最后 反序列化出来一个配置struct实例
ps 最终代码里没有pflag包的事</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（7） 💬（2）<div>有个疑问：flag和非选项参数数什么关系呢？</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6f/01/7b82dd50.jpg" width="30px"><span>龍捲風</span> 👍（5） 💬（1）<div>想问下，关于golang的项目怎么实现优雅下线？注册中心可以将服务节点剔除，但关闭服务时怎么让已接收到请求可以做完呢？</div>2021-07-16</li><br/><li><img src="" width="30px"><span>Geek_8efe79</span> 👍（3） 💬（1）<div>全是文字看着好心累，没有视频？</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（2） 💬（3）<div>开发环境，测试环境，生产环境的配置文件是不同的，关于不同环境下读取配置文件，这块有什么好的最佳实践吗，是通过命令行参数指定不同环境的配置文件的方式好呢，还是通过系统环境变量来区分环境并读取对应配置文件好呢</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/f5/ed/d23daf19.jpg" width="30px"><span>Neroldy</span> 👍（2） 💬（1）<div>标志可以是“持久的”，这意味着该标志可用于它所分配的命令以及该命令下的每个子命令。
老师能再具体讲讲这个标志的持久化是什么意思吗？</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/66/35/c3fa51c0.jpg" width="30px"><span>我要去卖冰淇淋</span> 👍（1） 💬（2）<div>老师我有个疑问.例如 我现在要在别的方法中引用yaml中配置的变量，但在代码中我没有发现global存配置文件的信息，难道只能 1。自己声明一个全局了存储，2 直接用 viper.GetString(&quot;xxx.xxx&quot;) 方式。
我在观察代码的时候 发现所有的初始化信息基本上都是在 启动之初处理好了。</div>2022-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/9a/6f/c4490cf2.jpg" width="30px"><span>czy</span> 👍（0） 💬（1）<div>Viper读取配置部分第2种方法反序列化两个示例解释的很不清楚，过于晦涩了，不如用一个简单的例子，这两个例子是官方上的，就直接翻译搬过来了吧？也没有加一些解析。</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/01/53/eafa07ae.jpg" width="30px"><span>雪峰</span> 👍（0） 💬（1）<div>viper在容器中无法watch</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4f/66/88acb1cc.jpg" width="30px"><span>scorpio</span> 👍（0） 💬（1）<div>这段代码最后一行，应该加上 VIPER_ 前缀，否则获取不到变量。

&#47;&#47; 使用环境变量
os.Setenv(&quot;VIPER_USER_SECRET_ID&quot;, &quot;QLdywI2MrmDVjSSv6e95weNRvmteRjfKAuNV&quot;)
os.Setenv(&quot;VIPER_USER_SECRET_KEY&quot;, &quot;bVix2WBv0VPfrDrvlLWrhEdzjLpPCNYb&quot;)

viper.AutomaticEnv()                                             &#47;&#47; 读取环境变量
viper.SetEnvPrefix(&quot;VIPER&quot;)                                      &#47;&#47; 设置环境变量前缀：VIPER_，如果是viper，将自动转变为大写。
viper.SetEnvKeyReplacer(strings.NewReplacer(&quot;.&quot;, &quot;_&quot;, &quot;-&quot;, &quot;_&quot;)) &#47;&#47; 将viper.Get(key) key字符串中&#39;.&#39;和&#39;-&#39;替换为&#39;_&#39;
viper.BindEnv(&quot;user.secret-key&quot;)
viper.BindEnv(&quot;user.secret-id&quot;, &quot;USER_SECRET_ID&quot;) &#47;&#47; 绑定环境变量名到key</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（1）<div>孔老师，有几个问题想请求下：
1、viper 有没有办法配置让它能区分大小写的配置 Key？
2、如果有一长串的配置文件，例如以下 yml 配置，viper 有没有办法只反序列化我要关心的内层的那一部分配置（这样我不用定义其他配置项结构体和它的外层结构体）？
aaa:
  foo:
    bar: 123
    hhh: &quot;$%^&quot;
bbb:
  bar: foo
  hello:
  - world
  - hihihi
只反序列化 aaa.foo 配置子项为以下结构体：
type AFoo struct {
    bar  int
    hhh string
}</div>2022-06-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/rSzzqGwHcvhwPejiaPsCY9XBX7ib7zTxJ6cUDORdhGIakX8dTPVsz6ibud5ec1FeWQGTseF2TPRECCjky5JMlHvDg/132" width="30px"><span>Struggle~honor</span> 👍（0） 💬（1）<div>老师，大厂里面应用构建，一般都是用自己内部造的轮子，更符合业务要求对吗？ 之前在腾讯实习用rainbow配置中心来存放配置，用他的sdk来拉取配置</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/d4/c9b5d3f9.jpg" width="30px"><span>💎A</span> 👍（9） 💬（0）<div>Pflag + Cobra 不如直接用github.com&#47;urfave&#47;cli</div>2022-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/d6/a2/bff28e13.jpg" width="30px"><span>Geek_d9ada3</span> 👍（6） 💬（0）<div>感觉cobra学的有点没有头绪，要么概念上没发理解到位，要么找不到实际例子可以看看效果。 建议这块可以完善丰富一下，把概念和例子都整详细点。谢谢大佬</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/24/547439f1.jpg" width="30px"><span>ghostwritten</span> 👍（1） 💬（0）<div>good，这一篇很干货，当然，更像是个引子，很多玩法需要自己去扩展探索。</div>2022-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/50/8d/b1d352f1.jpg" width="30px"><span>NGTNL</span> 👍（0） 💬（0）<div>请问下在实际使用中，使用 viper.unmarshal 将配置文件反序列化成 config struct 然后直接使用这个 struct 对象，还是在代码中到处使用 viper.Get？感觉在代码中显式使用 viper.Get 有些不太解耦，但是如果直接反序列化成 struct 如果是比较复杂的 struct，默认值又没有方便的配置方式。</div>2024-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/93/2a/08675e68.jpg" width="30px"><span>__PlasticMan</span> 👍（0） 💬（0）<div>看到有同学想看到具体的例子，那么可以在作者说的几个开源项目上看看，比如docker、k8s。前面课程中生成错误码代码和文档的工具codegen比较简单，所以用了内置的Flag包，生成代码用`codegen -type=&lt;type&gt; [args]`，生成文档用`codegen -doc -type=&lt;type&gt; -output=&lt;output&gt; [args]`。在学习了本节课介绍的工具后，就可以做一些修改，生成代码用`codegen code -type=&lt;type&gt; [args]`， 生成文档用`codegen doc -type=&lt;type&gt; -output=&lt;output&gt; [args]`，其中code、doc作为子命令，type作为持久化标志所有命令通用，而output作为本地标志，只在生成文档时使用。这样设计之后命令行清晰易懂，更别说还有配置文件、环境变量、远程存储、校验、兼容性处理等等非常友好的封装。</div>2023-08-20</li><br/>
</ul>