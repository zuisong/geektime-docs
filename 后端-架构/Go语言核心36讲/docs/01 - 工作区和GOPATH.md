> 这门课中Go语言的代码比较多，建议你配合文章收听音频。

你好，我是郝林。从今天开始，我将和你一起梳理Go语言的整个知识体系。

在过去的几年里，我与广大爱好者一起见证了Go语言的崛起。

从Go 1.5版本的自举（即用Go语言编写程序来实现Go语言自身），到Go 1.7版本的极速GC（也称垃圾回收器），再到2018年2月发布的Go 1.10版本对其自带工具的全面升级，以及可预见的后续版本关键特性（比如用来做程序依赖管理的`go mod`命令），这一切都令我们欢欣鼓舞。Go语言在一步步走向辉煌的同时，显然已经成为软件工程师们最喜爱的编程语言之一。

我开办这个专栏的主要目的，是要与你一起探索Go语言的奥秘，并帮助你在学习和实践的过程中获取更多。

我假设本专栏的读者已经具备了一定的计算机基础，比如，你要知道操作系统是什么、环境变量怎么设置、怎样正确使用命令行，等等。

当然了，如果你已经有了编程经验，尤其是一点点Go语言编程经验，那就更好了，毕竟我想教给你的，都是Go语言中非常核心的技术。

如果你对Go语言中最基本的概念和语法还不够了解，那么可能需要在学习本专栏的过程中去查阅[Go语言规范文档](https://golang.google.cn/ref/spec)，也可以把预习篇的基础知识图拿出来好好研究一下。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erNhKGpqicibpQO3tYvl9vwiatvBzn27ut9y5lZ8hPgofPCFC24HX3ko7LW5mNWJficgJncBCGKpGL2jw/132" width="30px"><span>Geek_1ed70f</span> 👍（54） 💬（0）<div>下午上班时间随便读了一下,感觉有点讲的太散,只吸收了20%,晚上专门花了时间精读几遍 吸收了100%后真的干货满满,以前不懂得原理都能知道了 这是网上博客不会有的工匠级解说</div>2019-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（13） 💬（1）<div>对于初学者第一次看确实有些难懂，但是多看几遍后就会发现其实干货满满，我读了好几遍，接触golang也快一年了，但是很多知识点是第一次接触到，感谢郝林老师！</div>2018-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/7c/8ef14715.jpg" width="30px"><span>NIXUS</span> 👍（4） 💬（1）<div>归档文件，可以理解为程序的动态链接库文件吗？</div>2018-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/54/cd487e91.jpg" width="30px"><span>有风的林子</span> 👍（4） 💬（2）<div>目前还没用到GOPATH包含多个工作区，不知多个目录间的分隔符是什么？空格、冒号、还是分号？如果作者顺便说一下就好了，至少增加一个知识点。😁</div>2018-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/5c/f34849ac.jpg" width="30px"><span>白宇</span> 👍（5） 💬（2）<div>请教一下，如何解决下载第三方包失败情况</div>2018-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/81/fe2797cf.jpg" width="30px"><span>xyang</span> 👍（10） 💬（1）<div>go语言适合做什么业务，能概述性的罗列讲述下吗</div>2018-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/3b/c5ae689a.jpg" width="30px"><span>许明</span> 👍（18） 💬（3）<div>ide 我觉得vscode就很好用了，我现在是vscode + glide</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/9f/36ea3be4.jpg" width="30px"><span>千年孤独</span> 👍（21） 💬（2）<div>如果在面试中让老师来回答“设置&#39;GOPATH有什么意义？”这个问题，除去典型回答

老师会如何简要明了回答这个问题？</div>2018-08-10</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK1iadgQFxhYdu7wIUf7n5XYZlchNicdGBsafY9GPX3hNq0313DfE7ia6CeRm7VZAmwGPsLI8icTJUqXg/132" width="30px"><span>jians</span> 👍（6） 💬（2）<div>看完再结合测试后的疑问：
在不同项目src中有同名包时，go build, install只会执行gopath中最早发现包的工作区，哪如何编译后面其他工作区中的同名包呢？</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/53/62b5c104.jpg" width="30px"><span>郝林</span> 👍（191） 💬（5）<div>有很多读写问归档文件是什么意思。归档文件在Linux下就是扩展名是.a的文件，也就是archive文件。写过C程序的朋友都知道，这是程序编译后生成的静态库文件。</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/53/2d/8bc7a3a6.jpg" width="30px"><span>第五季节</span> 👍（17） 💬（2）<div>工作区是指： 放go的源码目录。
gopath是指：指向工作区的路径。

归档文件： 相当于java的jar包。下载到本地私服


不知道对不对。纯属个人观点。</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/53/2d/8bc7a3a6.jpg" width="30px"><span>第五季节</span> 👍（4） 💬（1）<div>gopath 的设计类似java  。
具体的用途是执行命令要用 例如：go run、go install、go get等。
允许设置多个路径。
在idea里面的多个project或工具组建都并列放在gopath的src下面。
例如：go install myProject1
            go install myProject2 
所以老师说的这个归档文件。可以理解成工作空间吗？
至于老师说的两个问题。
1:按照代码的执行顺序 从上往下 每个引入的初始化。
2:引入一下试试就知道了。</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（8） 💬（2）<div>一脸懵逼，并不知道归档文件是啥😄</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5f/bb/cd23de6c.jpg" width="30px"><span>全干工程师</span> 👍（23） 💬（1）<div>什么是归档文件，归档文件里都是什么？有什么作用。</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/e7/226025f7.jpg" width="30px"><span>Arno Fan</span> 👍（12） 💬（2）<div>$ go env |grep -E &quot;GOPATH|GOROOT&quot;
GOPATH=&quot;&#47;Users&#47;arno&#47;go&quot;
GOROOT=&quot;&#47;usr&#47;local&#47;Cellar&#47;go&#47;1.12.9&#47;libexec&quot;

$ tree &#47;Users&#47;arno&#47;go
&#47;Users&#47;arno&#47;go
├── bin
│   ├── hello
│   └── hello_v2
├── pkg
└── src
    ├── github.com
    │   └── opsarno
    │       └── hello
    │           └── hello.go
    └── hello_v2
        └── hello.go

单纯的去读文字，确实不易理解，实际操作下就比较容易理解了。</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/31/b26b56bf.jpg" width="30px"><span>Lever</span> 👍（10） 💬（1）<div>go v1.11 之后已经很不一样了，所有依赖包都放到 $GOPATH&#47;pkg&#47;mod 下了</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/5e/2d1c63b4.jpg" width="30px"><span>Eric</span> 👍（7） 💬（1）<div>归档文件是不是类似Java的class文件啊</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/80/61107e24.jpg" width="30px"><span>快乐就好</span> 👍（4） 💬（2）<div>请教一个问题，我这边设置了GOPATH，然后在GOPATH路径下下了一段代码，代码调用了自定义模块，然后go run执行的时间报我的自定义模块不在GOROOT中（package voile is not in GOROOT），详细细节是：GOPATH=&#47;home&#47;godev&#47;go，&#47;home&#47;godev&#47;go下的目录路径是$ ls
bin  pkg  src；
src下目录路径是：
$ ls
main.go  voile
voile是作为自定义模块的，voile下有一个voile.go文件，内容如下：
$ cat voile&#47;voile.go 
package voile

import &quot;fmt&quot;

func init(){
  fmt.Println(&quot;Is file Init.&quot;)
}

func Simple(){
  fmt.Println(&quot;Hello world!&quot;)
}
原src目录下main.go文件内容如下：
package main

import (
&quot;fmt&quot;
&quot;log&quot;
&quot;os&quot;
&quot;voile&quot;
)

func init(){
  log.SetOutput(os.Stdout) 
}

func main(){
  voile.Simple()
}
在src下执行go run main.go就是有问题（说我自定义模块voile找不到），请问这里是什么问题呢？</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/81/c7/cf36f3cc.jpg" width="30px"><span>Krysta</span> 👍（4） 💬（1）<div>你好，我的理解是。gopath之下的第一个目录是用来存放go get下载的一些第三方库，类似于Node的node_module ，可以新建其他的目录用来存放我们写的代码，通过Import就可以引入哪些库。不知道这样的理解是不是对的</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/55/2a465781.jpg" width="30px"><span>Hurray</span> 👍（4） 💬（1）<div>问题2，会冲突，可以用别名来解决。</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/e3/39dcfb11.jpg" width="30px"><span>来碗绿豆汤</span> 👍（4） 💬（2）<div>老师，我用的是windows系统。我将我的一个工作目录配置到了GOPATH。然后在该目录的src目录下面创建了一个package。执行go install.的时候报错，提示找不到这个包。然后错误信息显示，它只去go的安装目录小面找了，并没有去我新配置的GOPATH下面找。</div>2018-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（3） 💬（1）<div>老师，请教一下：
您在补充阅读中说“在运行go build命令的时候，默认不会编译目标代码包所依赖的那些代码包。”而在回答同学问题中说“Go语言对可执行程序进行安装的时候，会把相关的静态链接库与之打包在一起。所以生成的可执行文件才可以独立运行的。这也是很明显的优势。“
有点不理解，这两个说法矛盾么？依赖的代码包和相关的静态链接库是什么区别？我每次在本地 build 完了就可以扔到服务器上执行了，Go 这个特性非常方便实用。</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（3） 💬（1）<div>我有编码经验但从没接触过Go，这一篇更像是给学习过Go的人总结知识点一样，是不是入门选这个专栏有点不太合适？</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（3） 💬（2）<div>自定义代码包远程导入路径没有搞懂是如何使用的，烦请郝老师给个具体的示例，谢谢啦~</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/58/95/c1d937f6.jpg" width="30px"><span>庄忠惠</span> 👍（3） 💬（1）<div>老师，go语言有没有虚拟机这样概念，runtime算吗，如果没有，他怎么做到内存自动回收</div>2018-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/0b/810875aa.jpg" width="30px"><span>阿尔特纳晨风</span> 👍（3） 💬（1）<div>老师您好，近日golang 1.11 正式发版了，有着两个重要的特性：modules 和 WebAssembly，请问modules是要取代GOPATH吗？专栏会涉及这些新特性吗？谢谢</div>2018-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/61/abb7bfe3.jpg" width="30px"><span>招耳</span> 👍（3） 💬（1）<div>推荐一个比较好用的go包管理工具呗</div>2018-08-25</li><br/><li><img src="" width="30px"><span>Geek_c227aa</span> 👍（2） 💬（1）<div>说实话，讲的有点抽象，刚到新公司，已经用了三个月go开发业务。现在想系统的学习下go，但是三个环境变量还是看的模模糊糊的。

比如下面的：
在工作区中，一个代码包的导入路径实际上就是从 src 子目录，到该包的实际存储位置的相对路径。
这个为啥是src目录就没有说明白。建议郝老师说到类似这方面知识点到时候可以附上链接让人了解其原因
</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9b/d0/86aee34c.jpg" width="30px"><span>刘凯</span> 👍（2） 💬（1）<div>.a文件什么情况会用到，构建的exe文件我感觉直接包含了依赖，直接没有pkg文件夹就能运行啊
我的理解是.a文件相当于其它语言的.dll，了事实是没有.a文件，构建的.exe同样可以运行，有点慒
求解答</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/cf/d5382404.jpg" width="30px"><span>RRR</span> 👍（2） 💬（2）<div>go mod 出来之后，GOPATH 的意义就小了很多</div>2019-02-21</li><br/>
</ul>