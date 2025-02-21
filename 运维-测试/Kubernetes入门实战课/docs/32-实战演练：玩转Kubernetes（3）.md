你好，我是Chrono。

到今天，我们的“高级篇”课程也要结束了。比起前面的“初级篇”“中级篇”来说，这里的知识点比较多，难度也要高一些。如果你能够一篇不漏地学习下来，相信一定对Kubernetes有更深层次的认识和理解。

今天的这节课还是来对前面的知识做回顾与总结，提炼出文章里的学习要点和重点，你也可以顺便检验一下自己的掌握程度，试试在不回看课程的情况下，自己能不能流畅说出关联的操作细节。

复习之后，我们就来进行最后一次实战演练了。首先会继续改进贯穿课程始终的WordPress网站，把MariaDB改成StatefulSet，加上NFS持久化存储；然后我们会在Kubernetes集群里安装Dashboard，综合实践Ingress、namespace的用法。

## 要点回顾一：API对象

“高级篇”可以分成三个部分，第一部分讲的是PersistentVolume、StatefulSet等API对象。

（[24讲](https://time.geekbang.org/column/article/542376)）**PersistentVolume简称PV，是Kubernetes对持久化存储的抽象**，代表了LocalDisk、NFS、Ceph等存储设备，和CPU、内存一样，属于集群的公共资源。

因为不同存储设备之间的差异很大，为了更好地描述PV特征，就出现了StorageClass，它的作用是分类存储设备，让我们更容易去选择PV对象。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oib0a89lqtOhJL1UvfUp4uTsRLrDbhoGk9jLiciazxMu0COibJsFCZDypK1ZFcHEJc9d9qgbjvgR41ImL6FNPoVlWA/132" width="30px"><span>stefen</span> 👍（4） 💬（1）<div>如果能带主从的mariadb去部署wordpress就比较完美一些.</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/85/6f/1654f4b9.jpg" width="30px"><span>nc_ops</span> 👍（2） 💬（1）<div>老师。“还是拿现成的模板修改”，模板在哪里？没找到。是在你发的dashboard项目网站里吗？模板名字是啥？</div>2022-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（1） 💬（2）<div>在部署statefulset管理的maria pod时，不要忘了创建service对象，不然`maria-sts-0.maria-svc`是无效的，有可能报Error establishing a database connection

maria-svc.yml内容如下：
apiVersion: v1
kind: Service
metadata:
  name: maria-svc

spec:
  selector:
    app: maria-sts

  ports:
  - port: 3306
    protocol: TCP
    targetPort: 3306</div>2023-03-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/oqsRehqvt95V3jUACiaS9FhVunlWr8j3vY6VSartRU1TFQPxS106My9ySfYgOymwM2EF6SNNho3DIIJHtAjo6uw/132" width="30px"><span>Geek_515a78</span> 👍（0） 💬（1）<div>老师，kubectl apply -f dashboard.yaml拉镜像，科学上网后pod一直加载失败到不了runing状态，是什么原因啊</div>2024-06-11</li><br/><li><img src="" width="30px"><span>Geek_1d8cd9</span> 👍（0） 💬（1）<div>老师，我成功部署Wordpress后却发现伴随着每次虚拟机的重启，我之前在博客上上传的图片都会消失或者被破坏，但我写的文章却可以保存，所以我猜可能图片保存到了Wordpress这个Pod里，因为博客图片的保存路径为 &#47;var&#47;www&#47;html&#47;wp-content&#47;uploads，所以我就想在wp-dep.yaml里再加一个PVC动态存储，把Pod里的&#47;var&#47;www&#47;html&#47;wp-content&#47;uploads 挂载到 我创建的nfs 挂载目录 &#47;app&#47;nfs下，但这样做并没有成功，是我哪部分的方向有问题吗？</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（0） 💬（1）<div>1. 部署 dashboard 过程中被科学搞了一下，顺便删了 &#47;etc&#47;cni&#47;net.d 下的 10-flannel.conflist 后发现成功了
2. 通过 dashboard 发现了两个 pod 在 terminating，一个 worker 挂掉了，处理后全绿了，666</div>2023-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（0） 💬（2）<div>k8s.test需要再kubetcl里配置吗？
这个点很困惑</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（0） 💬（1）<div>老师，按照流程，最后通过Ingress是可以访问到（https）的dashboard页面，但是页面是为空，看title以及页面源码确实有dashboard字样，但是没有具体内容，显示为空白页面。

会是什么原因导致的呢？</div>2023-02-26</li><br/><li><img src="" width="30px"><span>Geek_674ea8</span> 👍（0） 💬（1）<div>老师，为dashboard配置ingress时，配置好后还是无法通过浏览器使用域名访问（已在hosts添加），浏览器报503：gateway time-out，查看ingress-controller日志显示如下：
Host is unreachable) while connecting to upstream, client: 10.10.1.1, server: k8s.test, request: &quot;GET &#47; HTTP&#47;2.0&quot;, upstream: &quot;https:&#47;&#47;10.10.0.19:8443&#47;&quot;
其中upstream的地址 10.10.0.19为kubernetes-dashbord的pod地址。
请问这种问题是什么原因造成的啊？</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/85/6f/1654f4b9.jpg" width="30px"><span>nc_ops</span> 👍（0） 💬（1）<div>为什么kubernetes-dashboard的那些对象要处于2个不同的名字空间呢？有什么用吗</div>2022-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（1）<div>分享我遇到的问题：
1. 搭建 dashboard ，访问时一直有这个错误 “Client sent an HTTP request to an HTTPS server”，原因是 ingress 没有加上 nginx.org&#47;ssl-services annotation（老师已经提醒了）
参考文档 https:&#47;&#47;docs.nginx.com&#47;nginx-ingress-controller&#47;configuration&#47;ingress-resources&#47;advanced-configuration-with-annotations&#47;#backend-services-upstreams

2. 搭建 wordpress 时，ingress 有端口号，浏览器打开页面无法正常显示，比如主页 https:&#47;&#47;wp.test:30443&#47; ，加载页面资源时会变成 https:&#47;&#47;wp.test&#47;xxxx ，丢失了端口号。这个问题不知道该如何解，请老师&#47;同学帮忙解答，谢谢！
（为了验证自己的想法，手动去改了 ingress controller pod 里 nginx 配置，强制设置“ proxy_set_header Host $host:430443; ”，可以凑效。）</div>2022-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（0） 💬（4）<div>请教老师一个问题：
文章后面的给Dashboard绑定Ingrss的时候，IngressClass的名字空间是kubernetes-dashboard，IngressController的名字空间是nginx-ingress。IngressClass和IngressConroller绑定的时候是不是忽略名字空间的？那是不是意味着IngressClass的name必须全局唯一？</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/27/e5a74107.jpg" width="30px"><span>Da Vinci</span> 👍（0） 💬（2）<div>按照老师的课程步骤去部署dashboard，但是最后访问的时候返回404，不知道为啥</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：Prometheus和Skywalking是一类产品吗？
Q2：对于常见的CI&#47;CD(持续集成、部署)，k8s等同于CD吗？
Q3：用openssl”生成的自签名证书，可以应用于生成环境吗？</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/98/ad/f9d755f2.jpg" width="30px"><span>邓嘉文</span> 👍（0） 💬（0）<div>第一</div>2022-09-05</li><br/>
</ul>