你好，我是轩脉刃。

在前面的课程中，我们基本上已经完成了一个能同时生成前端和后端的框架hade，也能很方便对框架进行管理控制。下面两节课，我们来考虑框架的一些周边功能，比如部署自动化。

部署自动化其实不是一个框架的刚需，有很多方式可以将一个服务进行自动化部署，比如现在比较流行的Docker化或者CI/CD流程。

但是一些比较个人比较小的项目，比如一个博客、一个官网网站，**这些部署流程往往都太庞大了，更需要一个服务，能快速将在开发机器上写好、调试好的程序上传到目标服务器，并且更新应用程序**。这就是我们今天要实现的框架发布自动化。

所有的部署自动化工具，基本都依赖本地与远端服务器的连接，这个连接可以是FTP，可以是HTTP，但是更经常的连接是SSH连接。因为一旦我们购买了一个Web服务器，服务器提供商就会提供一个有SSH登录账号的服务器，我们可以通过这个账号登录到服务器上，来进行各种软件的安装，比如FTP、HTTP服务等。

基本上，SSH账号是我们拿到Web服务器的首要凭证，所以要设计的自动化发布系统也是依赖SSH的。

## SSH服务

那么在Golang中如何SSH连接远端的服务器呢？有一个[ssh](https://golang.org/x/crypto/ssh)库能完成SSH的远端连接。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/ed/4e249c6b.jpg" width="30px"><span>Vincent</span> 👍（0） 💬（2）<div>之前用到的makefile较多，想问老师如何选择呢，是集成到hade中还是在makefile中呢</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（0）<div>如果在Windows下运行部署到Linux平台，uploadFolderToSFTP函数里远端路径的filepath.Join需要用filepath.ToSlash包一下转换成Unix路径格式。</div>2024-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5a/76/3f8dcda6.jpg" width="30px"><span>陈亦凡</span> 👍（0） 💬（1）<div>Mac cc
https:&#47;&#47;github.com&#47;messense&#47;homebrew-macos-cross-toolchains</div>2022-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5a/76/3f8dcda6.jpg" width="30px"><span>陈亦凡</span> 👍（0） 💬（0）<div>这里交叉编时，gspt库使用了c，需要交叉编译，网上看了一下，如果使用musl的话，运行环境也要安装，请教下除了docker、musl还有别的方案吗？</div>2022-09-05</li><br/>
</ul>