你好，我是Chrono。

在上次课里，我们一起研究了Kubernetes的内部架构和组成，知道它分为控制面和数据面。控制面管理集群，数据面跑业务应用，节点内部又有apiserver、etcd、scheduler、kubelet、kube-proxy等组件，它们互相协作来维护整个集群的稳定运行。

这套独特的Master/Node架构是Kubernetes得以安身立命的根本，但仅依靠这套“内功心法”是不是就能够随意仗剑走天涯了呢？

显然不行。就像许多武侠、玄幻作品里的人物一样，Kubernetes也需要一份“招式秘籍”才能把自己的“内功”完全发挥出来，只有内外兼修才能够达到笑傲江湖的境界。

而这份“招式秘籍”，就是Kubernetes世界里的标准工作语言YAML，所以今天，我就来讲讲为什么要有YAML、它是个什么样子、该怎么使用。

## 声明式与命令式是怎么回事

Kubernetes使用的YAML语言有一个非常关键的特性，叫“声明式”（Declarative），对应的有另外一个词：“命令式”（Imperative）。

所以在详细了解YAML之前，我们得先来看看“**声明式**”与“**命令式**”这两种工作方式，它们在计算机世界里的关系有点像小说里的“剑宗”与“气宗”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/8a/fc767da7.jpg" width="30px"><span>nada</span> 👍（29） 💬（4）<div>1. 因为空调的使用是我们设置温度，然后空调尽量去达成设置的温度，即我们设置的是我们想要达成的效果，而不像电视遥控器，每次操作都发送一个指令，声明式还有一个特点是容易 patch，拿空调举例，当前气温 30 度，我们先设置了 24 度，然后升高到 26 度，空调并不会先降低到 24 度，再升高到 26 度，而是将两次传递的意图 patch，直接降低到 26 度，k8s 也是这样
2. yaml 转换 json 的过程基本上字段一一对应，除了最后会把当前的 json 再序列化为字符串，存储到 &quot;kubectl.kubernetes.io&#47;last-applied-configuration&quot; 这个 annotations 中</div>2022-07-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2xoGmvlQ9qfSibVpPJyyaEriavuWzXnuECrJITmGGHnGVuTibUuBho43Uib3Y5qgORHeSTxnOOSicxs0FV3HGvTpF0A/132" width="30px"><span>psoracle</span> 👍（13） 💬（1）<div>回答一下作业
1. 你是如何理解“命令式”和“声明式”的？为什么说空调是“声明式”的？
我现在从kubernetes相关知识点中学习并理解到的“声明式”一个最直白的地方是新增与修改两个命令式操作写成apply，如果创建对象不存在则创建、对象已存在就比较spec进行相应变更，当然k8s的修改实际上是先delete再create。至于kubectl create、kubectl edit、kubectl delete等都是&quot;命令式&quot;操作，告诉k8s应该怎么做。
空调是“声明式”的原因是我不知道当前温度是多少，只需要我知道应该开成多少度即可，即我们在操作遥控器之前就知道我们要将空调调成多少度，这是预期值。

2. 使用 --v=9 参数，试着解释一下 YAML 是如何被 kubectl 转换成 HTTP 请求的。
虽然yaml格式是json的超集，但在k8s中的yaml文件最终都是被转换为json格式字符串放在request body中提交到apiserver的，从`kubectl -v=9`对各种操作的调试中可以看到。
除此之外，还发现一些有规律的地方，如下：
可见简单对象（如pod, configmap, secret, serviceaccount等）调用的接口形式如 `&#47;api&#47;&lt;apiVersion&gt;&#47;namespaces&#47;&lt;namespace&gt;&#47;&lt;kinds&gt;[&#47;&lt;name&gt;]`，其中对象类型为复数形式即`kubectl api-resources`中的name字段，修改、删除与查询具体对象时在URL中有`&#47;&lt;name&gt;`部分，其它如创建、查询所有就没有。对于复合对象（简单对象的包装对象，如replicaset, deployment, statefulset, cronjob等）的URL不同的是以`&#47;apis`开头，说明是属于复合型的接口（组合服务）。
</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/ed/3a/ab8faba0.jpg" width="30px"><span>陶乐思</span> 👍（9） 💬（2）<div>请问一下老师, —dry-run=client -o yaml生成的YAML默认情况下会将文件保存在哪里啊？没有找到呢…环境：windows+minikube</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（8） 💬（1）<div>终于对一头雾水的yaml文件有了一个正确的了解，感谢老师</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（5） 💬（1）<div>这门课太棒了，以前接触的杂乱的知识点在学完这一章之后逐渐变得脉络清晰！</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/a8/d5bf5445.jpg" width="30px"><span>郑海成</span> 👍（3） 💬（2）<div>有了刚才 YAML 语言知识“打底”，相信你基本上能够把它看明白，知道它是一个 Pod，要使用 nginx:alpine 镜像创建一个容器，开放端口 80，而其他的部分，就是 Kubernetes 对 API 对象强制的格式要求了。
————
查了一下官方文档，其实不是“开放”，好像是是“说明”容器中暴露的端口是80</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c4/51/5bca1604.jpg" width="30px"><span>aLong</span> 👍（2） 💬（1）<div>首先感谢老师三个技巧。这块配置的内容我确实很头大啊。初学时看书都想跳过去看看后面内容。今天看完老师讲的有点意思啊。尤其是我喜欢那种比喻生动的多。

两种方式进行比较：
命令：简单、直观、快捷，上手快。 适合临时测试或实验。
yaml文件：文件描述了What，即应用最终要达到的状态。配置文件提供了创建资源的模板，能够重复部署。可以像管理代码一样管理部署。适合正式的、跨环境的、规模化部署。这种方式要求熟悉配置文件的语法，有一定难度。
另外 kubectl apply不但能够创建Kubernetes资源，也能对资源进行更新，非常方便。


空调这种有些需求没办法直接达到预期工作，比如制冷、制热、温度调整。 反观：电视，你想换台就换了，声音控制多少按+ -就行了。 所以空调很多功能更像是声明式。</div>2023-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/7e/26/162e8e57.jpg" width="30px"><span>bruce</span> 👍（2） 💬（2）<div>
apiVersion: v1
kind: Pod
metadata:
  name: ngx-pod
  labels:
    env: demo
    owner: chrono

spec:
  containers:
  - image: nginx:alpine
    name: ngx
    ports:
    - containerPort: 80

metadata里的name和spec里的name有啥区别？</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/4a/9d/2aa87437.jpg" width="30px"><span>沃德天·泥维森陌·拉莫帅</span> 👍（2） 💬（1）<div>1. “命令式”是指采用命令式语言编写的程序，这种语言通常会指定程序执行的每一个步骤，并指定具体的操作来完成每一个步骤。

“声明式”是指采用声明式语言编写的程序。这种语言通常会指定程序的输出，而不是具体的操作。

例如，如果要编写一个程序来控制空调，那么“命令式”的方法可能是指定每一个步骤，例如打开空调、调整温度、打开风扇等，而“声明式”的方法可能是指定空调最终的状态，例如“调节到25摄氏度”。

因此，空调可以被认为是“声明式”的，因为它通过声明最终的状态来控制空调的工作方式，而不是通过指定具体的操作。


2. 当 kubectl 读取 YAML 文件时，它会将 YAML 文件转换成对应的 Kubernetes API 对象。比如，一个 YAML 文件可能会声明一个 pod 对象，而 kubectl 可以将这个 pod对象转换成 Kubernetes API 所需的 JSON 格式。

接下来，kubectl 会将这个转换后的 JSON 对象转换成一个 HTTP 请求，并发送到 Kubernetes API 服务器。Kubernetes API 服务器会根据这个 HTTP 请求来执行相应的操作。

具体过程：
kubectl 会使用一个 HTTP 客户端库（比如 http.Client）来将这个 JSON 对象转换成一个 HTTP 请求。这个 HTTP 请求会包含一些基本信息，比如请求方法（比如 POST）、请求路径（比如 &#47;apis&#47;apps&#47;v1&#47;namespaces&#47;default&#47;deployments）和请求内容（比如转换后的 JSON 对象）。

一旦这个 HTTP 请求被创建，kubectl 就可以使用这个 HTTP 客户端库来发送这个请求到 Kubernetes API 服务器。Kubernetes API 服务器会根据这个 HTTP 请求来执行相应的操作。</div>2022-12-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（2） 💬（2）<div>有两个问题想请教老师，

1. 通过 `kubectl api-resources` 看到的资源名称中其实没有 pod 而是 pods，但是我们依旧可以通过 pod 来访问对应的资源，这里是否可以理解为 k8s 自动帮忙做了单复数转换？

2. 没有看到 images 相关的资源，k8s 是如何管理 image 的呢？还是说对应的镜像管理被细分到 pod 的字段中？

3. 文章中（在 “什么是 YAML” 的结尾处）给的最后一个复杂的 YAML 例子，我试着在 https:&#47;&#47;www.bejson.com&#47;json&#47;json2yaml&#47; 上面转换成 JSON，但是平台会报如下错误：

yaml错误:
TypeError: Cannot read properties of undefined (reading &#39;split&#39;)

感觉像是缩进的问题</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/bd/e7ff842c.jpg" width="30px"><span>赤色闪电</span> 👍（2） 💬（1）<div>“声明式”：空调遥控器操控空调设定想要的温度和模式即可。“命令式”：电视遥控器操控电视，按一个钮换一个台。</div>2022-07-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuj7Wx21ecNlPHCfBsQIchmFxVSlPepwUiaKh0RMGgDB0aibTM50ibQN06dDmbqjuQZUIdH4qiaRJkgQ/132" width="30px"><span>Geek_adb513</span> 👍（1） 💬（1）<div>yaml 以前都是直接抄现成的用法，只知道必须这么用，这里把为什么讲解的很到位，的确让思绪一下明朗了，三要素 和 自定义</div>2023-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/86/cc/eecffb35.jpg" width="30px"><span>Liang Li</span> 👍（1） 💬（1）<div>一个好的老师能在一堆复杂的网状知识中，找到非常清晰的线性脉络，并把这些知识给串联表达起来，难得的好文章。</div>2022-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/56/abb7bfe3.jpg" width="30px"><span>云韵</span> 👍（1） 💬（6）<div>老师 我执行了这些命令  （环境是 mac m1 直接在本机上运行的 docker minikube）
export out=&quot;--dry-run=client -o yaml&quot;
kubectl run ngx --image=nginx:alpine $out
但是报这个错 error: Invalid dry-run value (client -o yaml). Must be &quot;none&quot;, &quot;server&quot;, or &quot;client&quot;.
请老师帮忙解答一下，谢谢
</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（1） 💬（1）<div>很棒，讲的很清楚</div>2022-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（1） 💬（1）<div>Yaml 在 Json 的基础上又把双引号，大括号各种非必要的字符都给干掉了，信息的有效性更高了，还能表示多个文档。

Xml —&gt; Json —&gt; Yaml，一路走来，贯穿它们的主线是什么？

信息的密度越来越高。</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/b9/6f/b40d1acf.jpg" width="30px"><span>mkcaptain</span> 👍（1） 💬（2）<div>问个问题，这个例子里，为什么master和nod前面没有减号（不用数组），而他们的下一级就用呢？谢谢

# 复杂的例子，组合数组和对象
Kubernetes:
  master:
    - apiserver: running
    - etcd: running
  node:
    - kubelet: running
    - kube-proxy: down
    - container-runtime: [docker, containerd, cri-o]</div>2022-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/0b/a943bcb3.jpg" width="30px"><span>zhou</span> 👍（1） 💬（1）<div>

1.声明式：只关注结果不关注过程
命令式：过程结果都关注
我只要告诉空调你给我把温度调到26度，我根本不用管他的过程是怎么样的

2.其实就是根据yaml的属性中的版本，类型拼接请求地址，然后将对应的属性当做请求体和参数传递</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（1） 💬（1）<div>老师有几个疑问，想问一下
1,我用yaml的方式创建了一个pod,这个文件我执行了2次， 名字改了一下，其他都没改， 端口是一样的，我在想 这样端口不会冲突吗？还有就是我这两个yaml都执行成功了，端口都是8888，为啥去访问虚拟机的端口访问不了呢？
2，我用minikube ssh 登进去这个k8s系统里面看，执行了一下docker ps 命令，里面有好多容器在运行，我记得我当时只在宿主机ubuntu里面装了docker,没有在这个minikube 里面装docker,我想请问一下，k8s系统里面的docker 是绑定的吗？就是前面几讲讲的，容器可以不绑定docker 还可以绑定其他其他容器， 是这个时候 k8s系统里面才有docker的吗？
3,用yaml方式创建pod成功之后， 使用kubectl get pod命令，可以查看到这里增加一个pod， 然后在登进去 k8s 这个系统里面，执行docker ps ，这里应该也会增加一个容器把，他们有啥关系吗？</div>2022-08-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mfZN0Rvvg3fhxtX3vglEreFhY8aAgUBfuWLN6UC02XTR5fIoUFEvQ5QmYtk2YkPQdSSUqfyuu8rxQZDicfYRTMA/132" width="30px"><span>Geek_eb20c9</span> 👍（1） 💬（1）<div>你是如何理解“命令式”和“声明式”的？为什么说空调是“声明式”的？  
命令式是它不知道怎么去完成你给它的目标，你需要指导它才能完成。声明式，我只需要给它一个目标，它就知道怎么完成！
因为我给空调一个目标，空调通过自己的办法可以完成这个目标！所以是声明式！
使用 --v=9 参数，试着解释一下 YAML 是如何被 kubectl 转换成 HTTP 请求的
YAML被转换成两部分，一部份是apiversion  metedata，kind作为head，剩余的转换为body！</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（1） 💬（1）<div>对于&quot;命令式&quot;和&quot;声明式&quot;，我觉得最本质的区别就是，命令式是通过实际的shell命令来执行完成某项功能，而声明式是仅仅定义一个配置文件，来描述预期的对象状态，再通过特定的命令去加载渲染这个配置文件，去完成对应的功能。</div>2022-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（1） 💬（1）<div>有了那个三个技巧，终于可以方便地写YAML 文件了</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（1） 💬（4）<div>1. 声明式： 我要结果。命令式：过程要符合要求，有一个不合适的比喻那就是面向对象和面向过程。要结果和要过程。
2. 会变成这样一条curl命令，curl -v -XGET  -H &quot;Accept: application&#47;com.github.proto-openapi.spec.v2@v1.0+protobuf&quot; -H &quot;User-Agent: kubectl&#47;v1.23.3 (linux&#47;amd64) kubernetes&#47;816c97a&quot; &#39;https:&#47;&#47;192.168.49.2:8443&#47;openapi&#47;v2?timeout=32s&#39; 不确定是不是要的答案</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>这一讲非常好，其他的教程都没有专门章节去讲解配置文件的，只有这门课才有，并切教了大家怎么看api对象信息， 怎么生成对象基础模板，都是能用上的高价值经验。</div>2024-03-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/sm5IXHKibVUAloJG9EIp7x49f5BttGhsibzgpo1ILyH1VA3cRVib2ewKE7evcZ98cExKLDD4aXNJvqlmVoh5FdYAg/132" width="30px"><span>Geek_c53032</span> 👍（0） 💬（1）<div>以前写yaml只是死搬硬套，今天终于理解理解了</div>2023-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（1）<div>总有一种强迫症，想把
```
spec:
  containers:
  - image: nginx:alpine
    name: ngx
    ports:
    - containerPort: 80
```

中的 - 往里缩进两个字符 😂

```
spec:
  containers:
    - image: nginx:alpine
       name: ngx
       ports:
         - containerPort: 80
```</div>2022-11-08</li><br/><li><img src="" width="30px"><span>Geek_cb910c</span> 👍（0） 💬（1）<div>containerPort: 80， 开发端口是80
这个pod资源对象，containerPort字段写出来有什么意义呢？</div>2022-10-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oib0a89lqtOhJL1UvfUp4uTsRLrDbhoGk9jLiciazxMu0COibJsFCZDypK1ZFcHEJc9d9qgbjvgR41ImL6FNPoVlWA/132" width="30px"><span>stefen</span> 👍（0） 💬（2）<div>报错了呢, 不知道为啥，麻烦指点一下，谢谢
export out=&quot;--dry-run=client -o yaml&quot;
kubectl run ngx2 --image=nginx:alpine $out

error: Invalid dry-run value (client -o yaml). Must be &quot;none&quot;, &quot;server&quot;, or &quot;client&quot;.</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f5/8a/e0fa8730.jpg" width="30px"><span>学渣要每日进步</span> 👍（0） 💬（1）<div>我倒是觉得申明是和命令式是只是多了一个概念，申明式其实就是一个配置文件</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（0） 💬（1）<div>好多client和server的交互，其实本质上还是http&#47;socket&#47;等底层的东西，例如mysql client&#47;server的交互，redis cli的交互，kafka交互等，选择RESTful的http的接口形式，代表着最通用，最宽泛和最自由的形势，外面加上软件自身的编码解码翻译过程</div>2022-07-26</li><br/>
</ul>