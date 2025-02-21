你好，我是孔令飞。

上一讲，我们一起安装和配置了一个基本的 Go 开发环境。这一讲，我就来教你怎么在它的基础上，快速部署好 IAM 系统。

因为我们要通过一个 IAM 项目来讲解怎么开发企业级 Go 项目，所以你要对 IAM 项目有比较好的了解，了解 IAM 项目一个最直接有效的方式就是去部署和使用它。

这不仅能让你了解到 IAM 系统中各个组件功能之间的联系，加深你对 IAM 系统的理解，还可以协助你排障，尤其是跟部署相关的故障。此外，部署好 IAM 系统也能给你后面的学习准备好实验环境，边学、边练，从而提高你的学习效率。

所以，今天我们专门花一讲的时间来说说怎么部署和使用 IAM 系统。同时，因为 IAM 系统是一个企业级的项目，有一定的复杂度，我建议你严格按照我说的步骤去操作，否则可能会安装失败。

总的来说，我把部署过程分成 2 大步。

1. 安装和配置数据库：我们需要安装和配置 MariaDB、Redis和MongoDB。
2. 安装和配置 IAM 服务：我们需要安装和配置 iam-apiserver、iam-authz-server、iam-pump、iamctl和man 文件。

当然啦，如果你实在不想这么麻烦地去安装，我也在这一讲的最后给出了一键部署 IAM 系统的方法，但我还是希望你能按照我今天讲的详细步骤来操作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/7f/746a6f5e.jpg" width="30px"><span>Q</span> 👍（5） 💬（5）<div>---用户名和密码有错---
$ curl -s -XPOST -H&#39;Content-Type: application&#47;json&#39; -d &#39;{&quot;username&quot;:&quot;admin&quot;,&quot;password&quot;:&quot;Admin@2021&quot;}&#39; http:&#47;&#47;127.0.0.1:8080&#47;login
{&quot;message&quot;:&quot;incorrect Username or Password&quot;}
----
2021-05-27 15:36:32.340	INFO	gorm@v1.21.4&#47;callbacks.go:124	mysql&#47;user.go:69 ReadMapCB: expect { or n, but found , error found in #0 byte of ...||..., bigger context ...||...[1.701ms] [rows:1] SELECT * FROM `user` WHERE name = &#39;admin&#39; ORDER BY `user`.`id` LIMIT 1
2021-05-27 15:36:32.340	ERROR	apiserver&#47;auth.go:146	get user information failed: ReadMapCB: expect { or n, but found , error found in #0 byte of ...||..., bigger context ...||...
2021-05-27 15:36:32.341	INFO	middleware&#47;logger.go:135	401 - [127.0.0.1] &quot;2.055136ms POST &#47;login&quot; 	{&quot;requestID&quot;: &quot;c4bdae71-6fb4-4a74-9730-06102f5e4e0e&quot;, &quot;username&quot;: &quot;&quot;}</div>2021-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/4b/bbb48b22.jpg" width="30px"><span>越努力丨越幸运</span> 👍（22） 💬（6）<div>老师讲的真的很细致，按照老师的教程基本没什么问题，我自己是在 docker 容器中部署的，我把项目部署好的容器打包上传了，有需要的同学可以直接拉下来用（docker pull mjcjm&#47;centos-go-project），启动参数一定要用：docker run -tid --name 容器名称 -v &#47;sys&#47;fs&#47;cgroup:&#47;sys&#47;fs&#47;cgroup  --privileged=true 镜像id &#47;usr&#47;sbin&#47;init。 最后继续加油💪🏻，冲冲冲！</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/ef/81/b411e863.jpg" width="30px"><span>真想</span> 👍（18） 💬（2）<div>配置环境劝退   折腾了很久 最终放弃了  希望能简化配置流程   把重心放在开发实战 而不是环境实战 </div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/f1/8b06801a.jpg" width="30px"><span>哇哈哈</span> 👍（8） 💬（5）<div>在执行“make build BINS=iam-apiserver” 的时候报错了，麻烦老师看一下
===========&gt; Building binary iam-apiserver 132d18e for linux amd64
no required module provides package github.com&#47;marmotedu&#47;iam&#47;cmd&#47;iam-apiserver: go.mod file not found in current directory or any parent directory; see &#39;go help modules&#39;
make[1]: *** [scripts&#47;make-rules&#47;golang.mk:60: go.build.linux_amd64.iam-apiserver] Error 1
make: *** [Makefile:62: build] Error 2</div>2022-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（8） 💬（2）<div>不容易啊，经过了三天，期间换了一次操作系统（从centos7 到 centos8），换了一次电脑（从低配云主机到本地虚拟机），踩了无数次坑，遇到了 n 多问题，终于按照本节步骤实打实的跑出来了，期间还为了 ReadMapCB 的问题翻了半天的源代码，虽然没有找到问题所在，但是也大致读懂了项目结构和作用，一把辛酸泪，终究得到了如下收获：
```
iamctl version -o yaml
clientVersion:
  buildDate: &quot;2021-05-28T11:57:56Z&quot;
  compiler: gc
  gitCommit: fb0a7b4ee5d497e7b1707fb5251d844d8538c5d8
  gitTreeState: dirty
  gitVersion: fb0a7b4
  goVersion: go1.16.2
  platform: linux&#47;amd64
serverVersion:
  buildDate: &quot;2021-05-28T11:12:56Z&quot;
  compiler: gc
  gitCommit: fb0a7b4ee5d497e7b1707fb5251d844d8538c5d8
  gitTreeState: dirty
  gitVersion: fb0a7b4
  goVersion: go1.16.2
  platform: linux&#47;amd64
```</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/d7/5d2bfaa7.jpg" width="30px"><span>Aliliin</span> 👍（7） 💬（1）<div>经过一上午的奋战总算是搭建完了，我在想就这样子的项目，入职一家新公司，如果没有文档，大佬级别的人物能在本地运行起来进行开发吗？

iamctl version -o yaml
clientVersion:
  buildDate: &quot;2021-06-02T03:23:02Z&quot;
  compiler: gc
  gitCommit: c01dd7bc7ee8aa2c06b9b70e565dff9f5e13e5ce
  gitTreeState: dirty
  gitVersion: c01dd7b
  goVersion: go1.16.2
  platform: linux&#47;amd64
serverVersion:
  buildDate: &quot;2021-06-02T03:13:04Z&quot;
  compiler: gc
  gitCommit: c01dd7bc7ee8aa2c06b9b70e565dff9f5e13e5ce
  gitTreeState: dirty
  gitVersion: c01dd7b
  goVersion: go1.16.2
  platform: linux&#47;amd64</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/7a/6f/db08c945.jpg" width="30px"><span>单推dd</span> 👍（6） 💬（5）<div>在启动iam-authz-server服务的时候一直启动不起来，然后我通过日志发现他用的端口是9090，正好和我阿里云服务器的web界面管理工具cockpit用的一样，所以用了sudo systemctl stop cockpit.socket命令，让9090端口空出来，成功启动iam-authz-server服务。</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/f1/bd61dbb1.jpg" width="30px"><span>Ransang</span> 👍（6） 💬（1）<div>好家伙，就这个项目安装就够我喝几壶里</div>2021-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c4/45/88287ede.jpg" width="30px"><span>chinandy</span> 👍（5） 💬（5）<div>安装 iamctl。第二步生成并安装 iamctl 的配置文件（config）：$ .&#47;scripts&#47;genconfig.sh scripts&#47;install&#47;environment.sh configs&#47;config &gt; config
在configs下面没有config文件，这个文件是怎么来的，我自己touch了一个显然不对的，我打开看.iam目录下看他是空的。</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/54/b9cd3674.jpg" width="30px"><span>小可爱(`へ´*)ノ</span> 👍（5） 💬（1）<div>老师，你mariadb安装脚本中的出现类似iam::mariadb::uninstall的命名，使用::有什么目的吗</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/19/77/3ca9f42d.jpg" width="30px"><span>呵呵哒</span> 👍（4） 💬（19）<div>最后的鉴权验证一直这样{&quot;code&quot;:100202,&quot;message&quot;:&quot;Signature is invalid&quot;}
换了token 新加的用户  策略 和秘钥 都不行</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（4） 💬（7）<div>老师的脚本玩的真的非常溜，我几乎无阻碍的到了 iam-apiserver 安装这个地方了，但是遇到了两个问题，第一个文中关于 git clone --depth 的命令有错误，depth 没有指定参数，导致 clone 失败；第二个问题很棘手，google 尝试了几个办法都没有解决，在运行：
```sh
make build BINS=iam-apiserver
```
脚本的时候，会报错：
```sh
===========&gt; Building binary iam-apiserver f96a5c8 for linux amd64
verifying github.com&#47;marmotedu&#47;marmotedu-sdk-go@v1.0.0&#47;go.mod: checksum mismatch
	downloaded: h1:QAuHe4YwnwlHYcktAFodwYyzxp2lqRDIi0yh1WbLtOM=
	go.sum:     h1:314QsW&#47;6+tVtngSxPzipgFJNCQMPFtDQQiXC7O66BwM=

SECURITY ERROR
This download does NOT match an earlier download recorded in go.sum.
The bits may have been replaced on the origin server, or an attacker may
have intercepted the download attempt.
```
我尝试用 go clean --modcache 和 go mod tidy 都没有解决，还是报校验错误，可能 sdk-go 这个包本身就有问题，这个包又是老师维护的，麻烦老师答疑解惑，多谢了～</div>2021-05-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqHKnvztWJLQBCFibpEZYA8HXqMz3SibTiajj8JXBAMjmXYHCD1rqG5aw6ghIWc5I9gP2I4DmGktSuWg/132" width="30px"><span>Geek_9b9ea5</span> 👍（3） 💬（6）<div>第 3 步，测试 iam-authz-server 是否成功安装中，测试资源授权是否通过，执行
$ curl -s -XPOST -H&#39;Content-Type: application&#47;json&#39; -H&#39;Authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Ilp1eHZYTmZHMDhCZEVNcWtUYVA0MUwyRExBcmxFNkpwcW9veCIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJpYW0uYXV0aHoubWFybW90ZWR1LmNvbSIsImV4cCI6MTYxNzg0NTE5NSwiaWF0IjoxNjE3ODM3OTk1LCJpc3MiOiJpYW1jdGwiLCJuYmYiOjE2MTc4Mzc5OTV9.za9yLM7lHVabPAlVQLCqXEaf8sTU6sodAsMXnmpXjMQ&#39; -d&#39;{&quot;subject&quot;:&quot;users:maria&quot;,&quot;action&quot;:&quot;delete&quot;,&quot;resource&quot;:&quot;resources:articles:ladon-introduction&quot;,&quot;context&quot;:{&quot;remoteIP&quot;:&quot;192.168.0.5&quot;}}&#39; http:&#47;&#47;127.0.0.1:9090&#47;v1&#47;authz
{&quot;allowed&quot;:true}报错，在问题区发现有人提出问题并且未有正确的解决方案，望老师解惑。
{&quot;code&quot;:100202,&quot;message&quot;:&quot;Signature is invalid&quot;}</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/96/58/b91503e7.jpg" width="30px"><span>forever_ele</span> 👍（3） 💬（2）<div>创建授权策略时如果报 {&quot;code&quot;:100101,&quot;message&quot;:&quot;Database error&quot;} ，说明策略已经存在了，可执行
curl -s -XDELETE -H&#39;Authorization: Bearer {Token}&#39; http:&#47;&#47;127.0.0.1:8080&#47;v1&#47;policies&#47;{策略名} 删除后重试</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/67/f3/db05d1b8.jpg" width="30px"><span>morris</span> 👍（3） 💬（2）<div>执行：   iamctl user list 
error: {&quot;code&quot;:100207,&quot;message&quot;:&quot;Permission denied&quot;}

这是为啥呢</div>2021-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/07/7711d239.jpg" width="30px"><span>ling.zeng</span> 👍（3） 💬（2）<div>老师 后边能加入云原生的功能吗？ 目前云原生化挺火的，能加上就好了。</div>2021-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/67/4e381da5.jpg" width="30px"><span>Derek</span> 👍（3） 💬（3）<div> cd $IAM_ROOT 这个路径是哪个啊？我咋没看到，我的环境变量里没这个值啊</div>2021-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（2） 💬（2）<div>api server如果起不来，可以去看日志：
1. 先从配置文件目录中找到日志目录
cd ${IAM_CONFIG_DIR}
vim iam-apiserver.yaml

2. 查看日志
vim &#47;var&#47;log&#47;iam&#47;iam-apiserver.log

2022-05-13 19:05:16.486 ^[[34mINFO^[[0m apiserver       gorm@v1.22.4&#47;gorm.go:202        mysql&#47;mysql.go:79[error] failed to initialize database, got error Error 1045: Access denied for user &#39;iam&#39;@&#39;172.18.0.1&#39; (using password: YES)
2022-05-13 19:05:16.486 ^[[31mFATAL^[[0m        apiserver       apiserver&#47;server.go:139 Failed to get cache instance: got nil cache server

我遇到的问题是，MariaDB数据库连接的密码和老师的不一样，改了就好了。</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cf/cd/32b1c1a7.jpg" width="30px"><span>pmpleader</span> 👍（2） 💬（2）<div>安装cfssl时报错误；

 .&#47;scripts&#47;install&#47;install.sh:293. &#39;((i&lt;3-1))&#39; exited with status 4

麻烦看看啥原因呢？</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（2） 💬（1）<div>如果是 Mac 的同学，尽量在 VirtualBox 中虚拟 CentOS。如果模拟处的 CentOS 有一些复制&#47;粘贴，以及界面预览受限的问题，可以考虑在 Mac 端 SSH 连接到本地虚拟机上。</div>2021-10-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKor4hwrdAK8E6XBLAUdznRLRUn29vdw7mBYRRN3TDhWz9KgGSicDibxiarlNjIf4yd2JeiafUVb0sE2A/132" width="30px"><span>Geek_3650cc</span> 👍（2） 💬（2）<div>systemctl启动iam-apiserver失败，确认文件存在
systemctl list-unit-files --type=service
iam-apiserver.service                      bad 

systemctl enable iam-apiserver.service 
Failed to enable unit: Unit file iam-apiserver.service does not exist
</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f4/77/dbb2aad8.jpg" width="30px"><span>今天也要加油鸭！</span> 👍（2） 💬（1）<div>老师 这个错误怎么解决呢
[parallels@dev iam]$iamctl user list
error: {&quot;code&quot;:100207,&quot;message&quot;:&quot;Permission denied&quot;}

[parallels@dev iam]$cat $HOME&#47;.iam&#47;config
apiVersion: v1
user:
  #token: # JWT Token
  username: admin # iam 用户名
  password: Admin@2021 # iam 密码
  #secret-id: # 密钥 ID
  #secret-key: # 密钥 Key
  client-certificate: &#47;home&#47;parallels&#47;.iam&#47;cert&#47;admin.pem # 用于 TLS 的客户端证书文件路径
  client-key: &#47;home&#47;parallels&#47;.iam&#47;cert&#47;admin-key.pem # 用于 TLS 的客户端 key 文件路径
  #client-certificate-data:
  #client-key-data:

server:
  address: 127.0.0.1:8443 # iam api-server 地址
  timeout: 10s # 请求 api-server 超时时间
  #max-retries: # 最大重试次数，默认为 0
  #retry-interval: # 重试间隔，默认为 1s
  #tls-server-name: # TLS 服务器名称
  #insecure-skip-tls-verify: # 设置为 true 表示跳过 TLS 安全验证模式，将使得 HTTPS 连接不安全
  certificate-authority: &#47;etc&#47;iam&#47;cert&#47;ca.pem # 用于 CA 授权的 cert 文件路径
  #certificate-authority-data:
</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ec/97/58e7bc9a.jpg" width="30px"><span>噼里啪啦啪啦噼里噼里啪啦</span> 👍（2） 💬（2）<div>老师，在获取用户列表错误：
 curl -s -XGET -H&#39;Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJpYW0uYXBpLm1hcm1vdGVkdS5jb20iLCJleHAiOjE2Mjc0NDI5NzUsImlkZW50aXR5IjoiYWRtaW4iLCJpc3MiOiJpYW0tYXBpc2VydmVyIiwib3JpZ19pYXQiOjE2MjczNTY1NzUsInN1YiI6ImFkbWluIn0.95HBXRxC0IYUH-mfmImZ4dxe1E_DcwXhfQyBJSB-UgQ&#39; &#39;http:&#47;&#47;127.0.0.1:8070&#47;v1&#47;users?offset=0&amp;limit=10&#39;
{&quot;code&quot;:100207,&quot;message&quot;:&quot;Permission denied&quot;}

我查看了其他同学也有同样的问题，我根据回答都修改了，并重新生成了token，但还是不行。
查看日志文件后显示：

2021-07-27 11:30:08.763 INFO    apiserver       middleware&#47;logger.go:135        200 - [127.0.0.1] &quot;146.40118ms POST &#47;v1&#47;users&quot;  {&quot;requestID&quot;: &quot;73bcefbe-4abf-45d0-bd7d-961b10046a6d&quot;, &quot;username&quot;: &quot;&quot;}
2021-07-27 11:31:37.397 INFO    apiserver       gorm@v1.21.12&#47;callbacks.go:133  mysql&#47;user.go:76 record not found[0.729ms] [rows:0] SELECT * FROM `user` WHERE name = &#39;&#39; ORDER BY `user`.`id` LIMIT 1
2021-07-27 11:31:37.398 INFO    apiserver       middleware&#47;logger.go:135        403 - [127.0.0.1] &quot;1.125017ms GET &#47;v1&#47;users?offset=0&amp;limit=10&quot;  {&quot;requestID&quot;: &quot;b3d3e22b-1528-41a8-94f9-313c5d5c3d2a&quot;, &quot;username&quot;: &quot;&quot;}

请问怎么解决呀
</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/2a/ce7c487d.jpg" width="30px"><span>Terence孫</span> 👍（2） 💬（1）<div>老师，想请问下man这部分的安装，想知道man这个是用来做什么的？？不是很懂，希望能有一点资料可以了解一下</div>2021-07-24</li><br/><li><img src="" width="30px"><span>Geek_399957</span> 👍（2） 💬（1）<div>
$ cd $IAM_ROOT
$ source scripts&#47;install&#47;environment.sh
$ make build BINS=iam-apiserver
$ sudo cp _output&#47;platforms&#47;linux&#47;amd64&#47;iam-apiserver ${IAM_INSTALL_DIR}&#47;bin


新手求解，make build BINS=iam-apiserver 这句命令是啥意思？</div>2021-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4e/bf/0f0754aa.jpg" width="30px"><span>lianyz</span> 👍（2） 💬（3）<div>老师好，在生成证书的环节，运行cfssl gencert...，报了没有hosts的警告，是不是不太对啊，如下。
cfssl gencert -ca=${IAM_CONFIG_DIR}&#47;cert&#47;ca.pem \
  -ca-key=${IAM_CONFIG_DIR}&#47;cert&#47;ca-key.pem \
  -config=${IAM_CONFIG_DIR}&#47;cert&#47;ca-config.json \
  -profile=iam iam-apiserver-csr.json | cfssljson -bare iam-apiserver。


[WARNING] This certificate lacks a &quot;hosts&quot; field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA&#47;Browser Forum (https:&#47;&#47;cabforum.org);
specifically, section 10.2.3 (&quot;Information Requirements&quot;).</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/49/8d/1a588fb4.jpg" width="30px"><span>默契</span> 👍（2） 💬（1）<div>老师为什么我的环境变量 $IAM_ROOT不能执行
[lin@dev iam]$ pwd
&#47;home&#47;lin&#47;workspace&#47;golang&#47;src&#47;github.com&#47;marmotedu&#47;iam
[lin@dev iam]$ cd $IAM_ROOT
bash: cd: GOWORK&#47;github.com&#47;marmotedu&#47;iam: No such file or directory</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/01/8c/41adb537.jpg" width="30px"><span>Tiandh</span> 👍（2） 💬（1）<div>项目部署完成。
环境：centos8.2 （内存 1G）
按照文章的部署顺序，在部署到 iam-pump 时遇到一个问题，
解决方法：kill 掉占用内存较多的进程
错误如下：
[going@dev iam]$ make build BINS=iam-pump
===========&gt; Building binary iam-pump c01dd7b for linux amd64
# github.com&#47;olivere&#47;elastic&#47;v7
fatal error: runtime: out of memory
...</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/fc/0e887697.jpg" width="30px"><span>kkgo</span> 👍（2） 💬（2）<div>已看完，坐等更新</div>2021-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/61/93b4ce97.jpg" width="30px"><span>赵新星</span> 👍（2） 💬（3）<div>为什么不云原生化呢</div>2021-05-26</li><br/>
</ul>