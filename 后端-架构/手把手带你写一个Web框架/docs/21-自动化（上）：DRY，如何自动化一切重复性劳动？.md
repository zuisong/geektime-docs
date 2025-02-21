你好，我是轩脉刃。

不知道你有没有听过这种说法，优秀程序员应该有三大美德：懒惰、急躁和傲慢，这句话是Perl语言的发明者Larry Wall说的。其中懒惰这一点指的就是，程序员为了懒惰，不重复做同样的事情，会思考是否能把一切重复性的劳动自动化（don’t repeat yourself）。

而框架开发到这里，我们也需要思考，有哪些重复性劳动可以自动化么？

从第十章到现在我们一直在说，框架核心是服务提供者，在开发具体应用时，一定会有很多需求要创建各种各样的服务，毕竟“一切皆服务”；而每次创建服务的时候，我们都需要至少编写三个文件，服务接口、服务提供者、服务实例。**如果能自动生成三个文件，提供一个“自动化创建服务的工具”，应该能节省不少的操作**。

说到创建工具，我们经常需要为了一个事情而创建一个命令行工具，而每次创建命令行工具，也都需要创建固定的Command.go文件，其中有固定的Command结构，这些代码我们能不能偷个懒，“**自动化创建命令行工具**”呢？

另外之前我们做过几次中间件的迁移，先将源码拷贝复制，再修改对应的Gin路径，这个操作也是颇为繁琐的。那么，我们是否可以写一个“**自动化中间件迁移工具**”，一个命令自动复制和替换呢？
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/98/e2d8f2a9.jpg" width="30px"><span>zzq</span> 👍（0） 💬（1）<div>大佬， 在 framework&#47;command&#47;middleware.go 文件中缺少了    默认: 同中间件名称。 if folder == &quot;&quot; {folder = name}   </div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（3） 💬（0）<div>课程设计的好棒</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（1） 💬（1）<div>中间件也要拷贝代码吗...是否可以安装以后在go.mod里replace呢？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（0）<div>go-git 配置http代理：
		res_url := &quot;https:&#47;&#47;github.com&#47;gin-contrib&#47;&quot; + repo + &quot;.git&quot;
		fmt.Println(&quot;下载中间件 gin-contrib:&quot;, res_url)
	
		&#47;&#47;自定义 http proxy
		proxy_url, _ := url.Parse(&quot;http:&#47;&#47;127.0.0.1:7890&quot;)
		customHttp := &amp;http.Client{
			Transport: &amp;http.Transport{
				Proxy: http.ProxyURL(proxy_url),
			},
		}
		client.InstallProtocol(&quot;https&quot;, githttp.NewClient(customHttp))
		_, err := git.PlainClone(path.Join(middlewarePath, repo), false, &amp;git.CloneOptions{
			URL:      res_url,
			Progress: os.Stdout,
		})</div>2024-01-20</li><br/>
</ul>