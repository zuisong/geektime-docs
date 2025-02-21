你好，我是孔令飞。

前面我们讲了很多关于应用构建的内容，你一定迫不及待地想看下IAM项目的应用是如何构建的。那么接下来，我就讲解下IAM应用的源码。

在讲解过程中，我不会去讲解具体如何Code，但会讲解一些构建过程中的重点、难点，以及Code背后的设计思路、想法。我相信这是对你更有帮助的。

IAM项目有很多组件，这一讲，我先来介绍下IAM项目的门面服务：iam-apiserver（管理流服务）。我会先给你介绍下iam-apiserver的功能和使用方法，再介绍下iam-apiserver的代码实现。

## iam-apiserver服务介绍

iam-apiserver是一个Web服务，通过一个名为iam-apiserver的进程，对外提供RESTful API接口，完成用户、密钥、策略三种REST资源的增删改查。接下来，我从功能和使用方法两个方面来具体介绍下。

### iam-apiserver功能介绍

这里，我们可以通过iam-apiserver提供的RESTful API接口，来看下iam-apiserver具体提供的功能。iam-apiserver提供的RESTful API接口可以分为四类，具体如下：

**认证相关接口**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（14） 💬（1）<div>总结：
介绍了 internal&#47;pkg&#47;apiserver 内部的组织结构
1. 最外层的Go文件主要完成：
   1. 构建应用框架（app.go）
   2. 提供应用框架执行时，需要的Run函数（run.go）
   3. 创建 apiServer 服务实例（server.go 和 grpc.go）
   4. 创建路由规则，安装中间件等（auth.go, router.go）
2. config 对应**应用配置**
3. options 对应命令行参数和配置文件。
4. controller、service、store 三个层次，controller 负责参数解析、校验；service 层负责业务逻辑；store负责数据库操作。

4层模型，模型层、控制层、业务层、存储层。层级之间如何解耦？
1. 通过 interface 实现解耦；
2. service层和store层的实例，是在请求执行过程中动态创建，它们都依赖一个工厂对象，作为实例化的输入。
3. 工厂对象 store store.Factory 不与具体的表、具体的操作绑定，通过store对象，你可以执行数据库的任何操作。类似的，srv srvv1.Service 工厂也不与具体的业务绑定，通过srv对象，你可以执行任何业务逻辑。

服务启动流程分为三个阶段：配置阶段、PreRun阶段、Run阶段。配置相关的对象有：Options、Config、HTTP&#47;GRPC 相关的配置对象。</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（7） 💬（1）<div>结合前面章节的铺垫，介绍iam-apiserver的使用方法、架构和代码实现，前后连贯，逻辑清晰，简洁易懂。
顺便一提，跟郑晔老师的《软件设计之美》中讲到的：快速了解一个项目时，要了解项目的模型、接口、实现，核心思想如出一辙。软件设计的路上，殊途同归。</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/b9/47377590.jpg" width="30px"><span>Jasper</span> 👍（6） 💬（3）<div>var _ UserSrv = (*userService)(nil)  我是go初学者，这种语法表示没看明白</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（4） 💬（1）<div>练习1：通过component-base共享 REST API 相关代码</div>2021-08-27</li><br/><li><img src="" width="30px"><span>Geek_cede76</span> 👍（2） 💬（1）<div>这里使用到了设计模式中的工厂方法模式。Service是工厂接口，里面包含了一系列创建具体业务层对象的工厂函数：Users()、Secrets()、Policies()。通过工厂方法模式，不仅隐藏了业务层对象的创建细节，而且还可以很方便地在Service工厂接口实现方法中添加新的业务层对象</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/82/ec/99b480e8.jpg" width="30px"><span>hiDaLao</span> 👍（2） 💬（1）<div>老师，请问下context作为参数一直传下去的目的是什么呢</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（2） 💬（2）<div>业务层和仓库层那里都做了两层抽象，比如仓库层有 Factory 和 SecretStore 两类接口，业务层调用的时候要这样写 s.store.Secrets().Create()。我的疑问是 Factory 这层抽象是不是可以省掉，业务层调用直接这样写 store.Secrets(dbIns).Create() 貌似也可以，这样有什么缺点吗？</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/3a/0dd9ea02.jpg" width="30px"><span>Summer  空城</span> 👍（2） 💬（2）<div>老师，您好，在app&#47;app.go 中 func NewApp(name string, basename string, opts ...Option) *App内部执行Option的方法，其实就是给App设置参数。为什么不来个set方法直接设置，现在这种设置方法感觉绕了一圈。。。。。</div>2021-09-02</li><br/><li><img src="" width="30px"><span>Geek_cede76</span> 👍（1） 💬（1）<div>这里使用到了设计模式中的工厂方法模式。Service是工厂接口，里面包含了一系列创建具体业务层对象的工厂函数：Users()、Secrets()、Policies()。通过工厂方法模式，不仅隐藏了业务层对象的创建细节，而且还可以很方便地在Service工厂接口实现方法中添加新的业务层对象

老师，我感觉这里更像是抽象工厂方法模式</div>2022-11-18</li><br/><li><img src="" width="30px"><span>3608375821</span> 👍（1） 💬（1）<div>api接口是在哪里注册到router上面的啊，没找到，比如&#47;v1&#47;secrets&#47;</div>2022-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/09/898d084e.jpg" width="30px"><span>呆呆</span> 👍（1） 💬（1）<div>func initRouter(g *gin.Engine) {
	installMiddleware(g)
	installController(g)
}
如上apiserver&#47;router.go的函数参数都为gin.Engine，是不是不太对？apiserver应该只与genericapiserver有关系，genericapiserver中集成了gin.Engine， genericapiserver中提供路由注册接口会不会更好些。
</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7b/c5/35f92dad.jpg" width="30px"><span>Jone_乔泓恺</span> 👍（1） 💬（1）<div>请教：在仓库层如果不在想使用 mysql ，而是换成 etcd ，应该如何修改代码呢？</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/63/72/a85661ee.jpg" width="30px"><span>船长</span> 👍（1） 💬（2）<div>大佬，在模型层中依赖gorm，这种设计好吗？个人感觉模型层中是尽量不要依赖第三方跟某种实现强相关的东西，不知道大佬这么设计是出于什么样的考虑。
func (u *User) AfterCreate(tx *gorm.DB) error {
	u.InstanceID = idutil.GetInstanceID(u.ID, &quot;user-&quot;)

	return tx.Save(u).Error
}</div>2022-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0c/dd/1b12d77d.jpg" width="30px"><span>Dragon Frog</span> 👍（1） 💬（2）<div>老师好，有个问题，想麻烦老师解惑一下。

在前面的课程谈到 “go 的设计哲学是模块划分而不鼓励 mvc 分层结构”，但是实际上我们这个项目的模型仍然是 MVC 划分的，想问问老师为什么最后决定这么设计。

另外我也大概搜索了一些 Go 的 web 项目，发现大家其实受 MVC 风格影响还是很深的，基本都采用这种设计风格去设计自己的代码架构而不是按功能划分。我目前没有找到一些按功能划分的 Go web 项目，想问问老师有没有知道类似的项目并能推荐一二供大家学习</div>2022-01-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKXjfJWVQGDHmDEI73VQO4dgTzaK5LLz2ax9XUF4FCPy1Oib8aQLibFzpcsiavVVbAQlG4pbrfibdwaYA/132" width="30px"><span>Geek_63505f</span> 👍（1） 💬（2）<div>老师你好！ 我看很多接口都是 &#47;v1&#47;users&#47;:name 这样的用name去定位话会不会不太好，name如果相同的话是不是就有问题了？</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/d8/afd6143f.jpg" width="30px"><span>白羽幽人</span> 👍（1） 💬（1）<div>app.WithRunFunc(run(opts)),

for _, o := range opts {
	o(a)
}

a.buildCommand()

老师这个 run 注册方法，是不是在 buildCommand 之前运行呢。</div>2021-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/2f/26e97ba5.jpg" width="30px"><span>Gary爱学习</span> 👍（1） 💬（1）<div>设计思想很懂，就是不太熟练go，看的吃力，得多摸一摸代码。</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/91/97/a3c8f2e6.jpg" width="30px"><span>印记碾碎回忆！</span> 👍（1） 💬（3）<div>~~~
func (s *SecretController) Create(c *gin.Context) {
    ...
  if err := s.srv.Secrets().Create(c, &amp;r, metav1.CreateOptions{}); err != nil {
    core.WriteResponse(c, err, nil)

    return
  }
  ...
}
~~~

看了下这里是每次都调用`newSecrets`构造一个`secretService`的对象，请问这个是有意设计成的这样吗？</div>2021-11-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLJ86tichGXtZMLLhicb8V0wJE92xdpQmVW1u06ZkT7BkvxyZMfWcVluyUdMrz0cBIkuX9MhXm2PZOQ/132" width="30px"><span>Geek_a15aca</span> 👍（1） 💬（1）<div>不是之前的课程谈到go的设计哲学是模块划分而不鼓励mvc分层结构吗？</div>2021-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/d8/afd6143f.jpg" width="30px"><span>白羽幽人</span> 👍（1） 💬（1）<div>老师： 这个config 下怎么区分不同环境的配置文件呢</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/64/1becc599.jpg" width="30px"><span>drawping</span> 👍（1） 💬（1）<div>这样的模型，是不是贫血模型？ </div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（1） 💬（1）<div>在描述「控制层如何跟业务层进行通信」时，下面的代码贴上 SecretSrv 接口的定义，可能会更好。</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（1） 💬（1）<div>iam-apiserver 代码架构中「控制层能够导入业务层和仓库层的包」，是不是应该修改为：控制层能够导入业务层和模型层的包。</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/e0/1ff26e99.jpg" width="30px"><span>gecko</span> 👍（1） 💬（1）<div>请教老师问题
func WithDefaultValidArgs() Option {
	return func(a *App) {
		a.args = func(cmd *cobra.Command, args []string) error {
			for _, arg := range args {
				if len(arg) &gt; 0 {
					return fmt.Errorf(&quot;%q does not take any arguments, got %q&quot;, cmd.CommandPath(), args)
				}
			}

			return nil
		}
	}
}


上面代码中对App.args 进行赋值，它是一个函数类型  函数签名如下
type PositionalArgs func(cmd *Command, args []string) error

赋值时 其中自定义了其内部实现，其中对于入参的处理 仅用到了 args

没太明白 这个自定义的实现是干啥的 以及什么时候会触发这个return fmt.Errorf(）
请老师指教</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/e0/1ff26e99.jpg" width="30px"><span>gecko</span> 👍（1） 💬（1）<div>app包中的 如下类型 
type Command struct {
	usage    string
	desc     string
	options  CliOptions
	commands []*Command
	runFunc  RunCommandFunc
}


如果 commands 字段 有很多层的话  那么如下实现中

func (c *Command) cobraCommand() *cobra.Command {
	cmd := &amp;cobra.Command{
		Use:   c.usage,
		Short: c.desc,
	}
	cmd.SetOutput(os.Stdout)
	cmd.Flags().SortFlags = false
	if len(c.commands) &gt; 0 { &#47;&#47; c 的类型为 *Command，为c的commands 字段赋值  通过 ddCommand 方法装填
		for _, command := range c.commands {
			cmd.AddCommand(command.cobraCommand()) &#47;&#47; 迭代 直到 commands 切片的 长度为0 
		}
	}
	if c.runFunc != nil {
		cmd.Run = c.runCommand
	}
	if c.options != nil {
		for _, f := range c.options.Flags().FlagSets {
			cmd.Flags().AddFlagSet(f)
		}
		&#47;&#47; c.options.AddFlags(cmd.Flags())
	}
	addHelpCommandFlag(c.usage, cmd.Flags())

	return cmd
}

func (c *Command) AddCommand(cmd *Command) {
	c.commands = append(c.commands, cmd)
}


每层的 *cobra.Command  在调用方那里  cobra.Command.AddCommand 是被绑定到同一个层级的 cobra.Command 吗</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5a/d0/7e58f993.jpg" width="30px"><span>梓荣</span> 👍（1） 💬（3）<div>老师你好。如果出现业务逻辑相互调用，这种情况如何处理较妥？是否有一些业务逻辑的上层不是controller？这部分代码应该放在哪个目录。谢谢。</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（1） 💬（1）<div>“独立于 UI ：在无需改变系统其他部分的情况下，UI 可以轻松地改变。例如，在没有改变业务规则的情况下，Web UI 可以替换为控制台 UI。”, 这里的 Web UI和控制台 UI有什么区别啊, 这俩不是一回事吗</div>2021-08-10</li><br/><li><img src="" width="30px"><span>Geek_b797c1</span> 👍（1） 💬（1）<div>大佬，router.go 里面：
storeIns, _ := mysql.GetMySQLFactoryOr(nil)
userController := user.NewUserController(storeIns)
这个写法感觉好怪呀。感觉没必要，在这边初始化一个nil 的store.Factory。是否可以优化一下

但，我也还没想好如何修改😂</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f7/76/16c52796.jpg" width="30px"><span>逆行*乱世</span> 👍（0） 💬（1）<div>➜  iam git:(f9fd52f) go mod vendor
go: github.com&#47;marmotedu&#47;errors@v1.0.2: stream error: stream ID 1; INTERNAL_ERROR 请问一下这个啥情况？</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/9a/786b1ed8.jpg" width="30px"><span>果粒橙</span> 👍（2） 💬（0）<div>学习学习MVC模式，第一次接触</div>2021-12-31</li><br/>
</ul>