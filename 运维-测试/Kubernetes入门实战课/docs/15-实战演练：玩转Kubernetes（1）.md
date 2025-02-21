你好，我是Chrono。

经过两个星期的学习，到今天我们的“初级篇”也快要结束了。

和之前的“入门篇”一样，在这次课里，我也会对前面学过的知识做一个比较全面的回顾，毕竟Kubernetes领域里有很多新名词、新术语、新架构，知识点多且杂，这样的总结复习就更有必要。

接下来我还是先简要列举一下“初级篇”里讲到的Kubernetes要点，然后再综合运用这些知识，演示一个实战项目——还是搭建WordPress网站，不过这次不是在Docker里，而是在Kubernetes集群里。

## Kubernetes技术要点回顾

容器技术开启了云原生的大潮，但成熟的容器技术，到生产环境的应用部署的时候，却显得“步履维艰”。因为容器只是针对单个进程的隔离和封装，而实际的应用场景却是要求许多的应用进程互相协同工作，其中的各种关系和需求非常复杂，在容器这个技术层次很难掌控。

为了解决这个问题，**容器编排**（Container Orchestration）就出现了，它可以说是以前的运维工作在云原生世界的落地实践，本质上还是在集群里调度管理应用程序，只不过管理的主体由人变成了计算机，管理的目标由原生进程变成了容器和镜像。

而现在，容器编排领域的王者就是——Kubernetes。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（18） 💬（7）<div>Mac上或者Window上，可能出现访问不到问题，这里写了一篇排查问题的思路，期望能帮到各位老板

https:&#47;&#47;juejin.cn&#47;post&#47;7127679053242302477</div>2022-08-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（18） 💬（3）<div>思考题 2，

试着写出了 Pod 的 YAML 文件

apiVersion: v1
kind: ConfigMap
metadata:
  name: ngx-cm

data:
  default.conf: |-
    server {
      listen 80;
      default_type text&#47;html;

      location &#47; {
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_pass http:&#47;&#47;127.0.0.1:8080;
      }
    }

---

apiVersion: v1
kind: Pod
metadata:
  name: ngx-pod
  labels:
    app: nginx-alpine
    role: website

spec:
  volumes:
    - name: conf
      configMap:
        name: ngx-cm

  containers:
  - volumeMounts:
    - mountPath: &#47;etc&#47;nginx&#47;conf.d&#47;
      name: conf

    image: nginx:alpine
    name: ngx-pod
    imagePullPolicy: IfNotPresent
    ports:
    - containerPort: 80

可以成功创建 Pod，nginx 的配置文件也被挂载到指定的位置，但是浏览器还是无法访问 wordpress，不知道是不是我的 YAML 文件中少了什么🤔，还望老师指点</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（11） 💬（1）<div>学了这一节，没感觉到容器编排的好用，反而遇到了一个问题，在配置中，我把wordpress链接数据库的host给小写了，结果一直告诉我链接数据库失败，我也没有排查手段，一直失败，我想的是，这个k8s的部署步骤实在是太复杂了，复杂到配置需要一个yaml，容器需要一个yaml，port-forward也需要一个yaml，我想如果是docker直接部署，其实就需要两条命令，所有参数都放到env中，或者放到配置文件中，也比检查yaml文件强，在入门篇中没感受到k8s的好用，只感觉到琐碎，是因为服务太小，还是因为没用好的原因呢
</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（9） 💬（7）<div>写一下第2题吧解题步骤：
首先如果我们把docker 形式改成pod形式这里存在两个问题（1）网络问题，（2）nginx配置文件加载问题，
第一个问题k8s的插件会处理节点内以及节点间网络通信问题，这个我们这里暂时不需要考虑，
那么需要我们处理的就是配置文件问题：这里我们可以用多个方法处理
   a: pod挂载宿主机目录，把配置文件放到宿主机目录下，容器启动挂载
   b: 使用我们学过的configMap
   c：使用pv、pvc 这个后面老师应该会讲到
这里我门就使用第二种方法，也是评论里使用最多的方法：
yml文件如下：
    ngx-cm.yml

apiVersion: v1
kind: ConfigMap
metadata:
  name: ngx-cm
data:
  nginx.conf: |
    server {
      listen 8080;
      #default_type text&#47;html;

      location &#47; {
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_pass http:&#47;&#47;172.17.0.9:80;
      }
    }

nginx.yml:

apiVersion: v1
kind: Pod
metadata:
  name: ngx-pod
  labels:
    env: demo
    owner: ant

spec:
  volumes:
    - name: nginx-conf
      configMap:
        name: ngx-cm
        items:
        - key: nginx.conf
          path: default.conf
  containers:
  - image: nginx:alpine
    name: ngx
    volumeMounts:
      - name: nginx-conf
        mountPath: &#47;etc&#47;nginx&#47;conf.d
    ports:
    - containerPort: 8080

然后使用 kubectl apply -f nginx.yml 创建pod，但是这个时候由于k8s节点还是一个隔离环境，所以我们还是无法访问，
所以我们要在网页观察到具体的网页内容，还是要再用docker创建一层nginx代理，server 内容如下：
server {
  listen 80;
  default_type text&#47;html;

  location &#47; {
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_pass http:&#47;&#47;127.0.0.1:8888;
  }
}

使用 docker run -d --rm --net=host -v &#47;home&#47;ant&#47;kubernetes&#47;pod&#47;nginx-conf&#47;nginx.conf:&#47;etc&#47;nginx&#47;conf.d&#47;default.conf nginx:alpine
启动，
然后使用 kubectl port-forward ngx-pod 8888:8080 &amp; 做转发

访问 http:&#47;&#47;192.168.56.208&#47; 正常访问</div>2022-08-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKQuaDVYz2jWN9vrmgbB785SNkmYmxf1xzEG8m8ku3ZvzYSkiaanTjqt7O47ficOQUpGmEy7eImplDw/132" width="30px"><span>椰子</span> 👍（7） 💬（1）<div>老师，目前Pod配置中使用了固定IP。如果pod被重启了，ip 是否会变化？如果有变化，这样配置是否有点不合理？</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/e7/c534fab3.jpg" width="30px"><span>wcy</span> 👍（4） 💬（1）<div>作业1：改用secret可以，这个简单，把data里对应的值用base64编码就行，对应pod的yml改下
作业2：nginx改成pod 运行是成功的， 但是port-forward出来，linux虚机上用firefox打开页面是ok的。但在shell终端本地浏览器访问不了，看了下应该是port-forward的问题，映射的端口绑定在Linux虚机127.0.0.1上，所以virtualbox转发不出来。
nginx cm:
apiVersion: v1
kind: ConfigMap
metadata:
  name: ngx-cm
data:
  nginx.conf: |
    server {
    #  listen 80;
       listen 8080;
    #   default_type text&#47;html;

       location &#47; {
           proxy_http_version 1.1;
           proxy_set_header Host $host;
           proxy_pass http:&#47;&#47;172.17.0.10:80;
       }
     }

nginx pod配置：
apiVersion: v1
kind: Pod
metadata:
  name: wp-ngx-pod
  labels:
    env: test

spec:
  containers:
  - image: nginx:alpine
    name: wp-ngx
    ports:
    - containerPort: 8080
    volumeMounts:
    - mountPath: &#47;etc&#47;nginx&#47;conf.d&#47;
      name: myngxconf

  volumes:
  - name: myngxconf
    configMap:
      name: ngx-cm
      items:
      - key: nginx.conf
        path: default.conf
</div>2022-08-04</li><br/><li><img src="" width="30px"><span>edward</span> 👍（3） 💬（2）<div>kubectl port-forward 老师请教下 这个命令设置端口转发后，怎么查看和取消？</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（2）<div>请教老师几个问题：
Q1：MariaDB和WP可以跑在一个POD里面吗？

Q2：文中的prefix是什么意思？
文中定义mariadb-pod.yml的时候，有一个prefix: &#39;MARIADB_&#39;， 这是什么意思？
是把configMap中的变量名字前面加上这个前缀作为pod中的变量名称吗？
即：pod中的变量名称 = MARIADB_&#39; + configMap中的变量名称。
Q3：关于转发的疑问
文中有一句：“因为 WordPress 网站使用了 URL 重定向，直接使用“8080”会导致跳转故障”。 如果没有nginx，宿主机上用浏览器直接访问WP的8080端口，则会因为WP内部实现机制而产生错误； 如果加上nginx，nginx去访问WP的8080端口，就没事。 是这样吗？</div>2022-07-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（3） 💬（3）<div>有在操作过程中遇到几个问题，还烦请老师指点

1、前面 2 个步骤中，在 kubectl apply -f *-pod.yml 之前是不是也得 apply 一下之前定义的 configMap 对象？

2、对于反向代理，不是特别的理解，老师能简单解释一下反向代理，并附带说明这里 Nginx 这里作为反向代理的目的是什么吗？

3、`minikube dashboard` 无法在命令行显示界面，我将 URL 复制粘贴到 Ubuntu 虚拟机图形界面上的浏览器中，但回复的 JSON 中显示 404？不太清楚有没有更好的方法
Opening http:&#47;&#47;127.0.0.1:38539&#47;api&#47;v1&#47;namespaces&#47;kubernetes-dashboard&#47;services&#47;http:kubernetes-dashboard:&#47;proxy&#47; in your default browser...
Error: no DISPLAY environment variable specified

4、对于思考题的 2，我创建一个了 nginx Pod，然后将其配置文件通过 kubectl cp 拷贝到 Pod 容器中的对应位置，但是发现并不起作用，本来想着重启 Pod 让配置生效，但是并没有找到对应的指令。这里是不是需要其他的 K8S API 对象的帮助？</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（2） 💬（1）<div>第四步 Nginx 部分使用 docker 启动命令把 -v 后面的 &#47;tmp&#47;proxy.conf 改为 `pwd`&#47;proxy.conf 即可，跟 dokcer 实战部分保持一致</div>2023-05-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/g4os8I4iaB6jn06PsvyqI1BooV5XbOC0vI3niaJ4I3SlAhkbBKG2eewlPHHJ4ROcDia18bbPFSZPDXXmgHXtrBlLg/132" width="30px"><span>Geek_f2f06e</span> 👍（2） 💬（1）<div>老师我有一个疑问想请教您：
这里把每个应用都封装成pod，为什么不将MariaDB和WordPress封装到一个pod里面，pod的意义不就是将多个密切的容器封装在一起</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/d5/73334a95.jpg" width="30px"><span>doos</span> 👍（2） 💬（1）<div>这个入门写的太好了，我当时学是先学习docker，研究了3个月docker，后来才慢慢去接触k8s学了半年，感觉内容太多了，而且知识比较分散</div>2023-02-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/cK4aAENG9h42KqeibyVNTeSUichzhv6zH1nA6iah4u6USqITMDA6qzuiaKY3of68tROwSzuRIsPpLnqgVW8ClMRH2Q/132" width="30px"><span>Geek_39bdd5</span> 👍（2） 💬（4）<div>kubectl get pod -o wide查看的时候ip显示是none是怎么回事
</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/cf/d5382404.jpg" width="30px"><span>RRR</span> 👍（2） 💬（2）<div>两个问题

1. port-forward 实际在生产用的多么？应该都是 ingress 吧
2. 老师后面能讲讲 helm 和 Istio 吗，他们和 k8s 关系是什么，我看不明白</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/52/56dbb738.jpg" width="30px"><span>牙小木</span> 👍（1） 💬（1）<div>注意wp-pod.yaml中的HOST值，需要按照自己机器上的来。
tb@tb-laptop:~$ k get pod maria-pod -o wide
NAME        READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
maria-pod   1&#47;1     Running   0          26m   10.244.0.76   minikube   &lt;none&gt;           &lt;none&gt;

</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/c8/695f838c.jpg" width="30px"><span>文静的安迪</span> 👍（1） 💬（1）<div>老师，我所有的课程都跟着你的这个课程走的，但是在本文中，创建mariadb-pod的时候，一只拉取镜像失败，但是我本地这个镜像很早就下载下来了的，但是pod一直无法创建成功ImagePullBackOff，看日志是拉取镜像失败，为什么我本地有还要去拉镜像呢？

ubuntu@ip-10-0-12-235:~$ kubectl get pod
NAME        READY   STATUS             RESTARTS   AGE
maria-pod   0&#47;1     ImagePullBackOff   0          5m17s

ubuntu@ip-10-0-12-235:~$ docker images
REPOSITORY       TAG       IMAGE ID       CREATED         SIZE
mariadb          10        4af0c16be4b1   12 hours ago    403MB
alpine           latest    5e2b554c1c45   2 days ago      7.33MB
hello-world      latest    9c7a54a9a43c   7 days ago      13.3kB
nginx            1.23      448a08f1d2f9   8 days ago      142MB
nginx            latest    448a08f1d2f9   8 days ago      142MB
redis            latest    116cad43b6af   8 days ago      117MB
kicbase&#47;stable   v0.0.39   67a4b1138d2d   5 weeks ago     1.05GB
nginx            alpine    8e75cbc5b25c   6 weeks ago     41MB
busybox          latest    7cfbbec8963d   8 weeks ago     4.86MB
ubuntu           latest    6b7dfa7e8fdb   5 months ago    77.8MB
wordpress        5         140ebc8d8136   12 months ago   605MB


</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/89/c8/53085ffb.jpg" width="30px"><span>tzhiyu</span> 👍（1） 💬（2）<div>运行下面这行命令之后
kubectl apply -f wp-pod.yml

没有出现老师图片上出现的&quot;configmap&#47;maria-cm created&quot;, 是因为我没有单独写maria-cm.yml导致的吗
</div>2023-04-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Gtf3tMDmYRoCL9Eico52ciatacq4PUHfQ8icQIYKV6KLDAJyTa8ZnLXMKf05pEice5RnEagocFobca5zv8jwyPhNKA/132" width="30px"><span>Geek_9d43c0</span> 👍（1） 💬（1）<div>我有个疑问 mariadb启动的时候 拉取 在maria-cm里面声明的配置 这个配置的字段启动的时候是怎么找到的 因为我们在docker启动的时候是会显式的配置启动参数 如果加了统一的前缀不会影响mariadb启动找自己的配置吗 </div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/11/89ba9915.jpg" width="30px"><span>永远的草莓地</span> 👍（1） 💬（2）<div>有个疑问，maria db 创建之后会有一个 ip ，这个 ip 直接就可以让其他 pod 访问，这样不是太不安全了吗？</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（1） 💬（1）<div>第一个问题：我并不能在一个文件直接创建configmap对象和pod
我需要执行configmap对象的yml文件 然后在执行pod的yml文件</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/31/e5/8d45547d.jpg" width="30px"><span>随遇而安</span> 👍（1） 💬（1）<div>老师，课程的源码有吗？就是每个内容中用到的yml文件。为啥我觉得应该先kubectl apply -f cm.yml之后，etd才会有cm的配置信息啊。我看到的pod的yml中，直接引用了cm配置，不对吧</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/d2/0e/579fc19b.jpg" width="30px"><span>conorzhong</span> 👍（1） 💬（2）<div>文中缺少kubectl apply -f maria-cm.yml</div>2022-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8f/48/c7fb8067.jpg" width="30px"><span>zzz</span> 👍（1） 💬（1）<div>Hi chrono , 出现这样的问题,调试了一个下午：
ubuntu@master:~&#47;k8s02p&#47;k8s&#47;worldPress$ k get pods  -o wide
NAME        READY   STATUS             RESTARTS        AGE     IP            NODE       NOMINATED NODE   READINESS GATES
maria-pod   1&#47;1     Running            0               29m     10.244.1.11   worker01   &lt;none&gt;           &lt;none&gt;
wp-pod      0&#47;1     CrashLoopBackOff   3 (2m35s ago)   3m23s   10.244.1.14   worker01   &lt;none&gt;           &lt;none&gt;

通过 k logs 检查：
ubuntu@master:~&#47;k8s02p&#47;k8s&#47;worldPress$ k logs wp-pod 
wordpress 09:54:52.41 
wordpress 09:54:52.42 Welcome to the Bitnami wordpress container
wordpress 09:54:52.42 Subscribe to project updates by watching https:&#47;&#47;github.com&#47;bitnami&#47;containers
wordpress 09:54:52.43 Submit issues and feature requests at https:&#47;&#47;github.com&#47;bitnami&#47;containers&#47;issues
wordpress 09:54:52.44 
wordpress 09:54:52.45 INFO  ==&gt; ** Starting WordPress setup **
realpath: &#47;bitnami&#47;apache&#47;conf: No such file or directory
wordpress 09:54:52.55 INFO  ==&gt; Configuring Apache ServerTokens directive
wordpress 09:54:52.62 INFO  ==&gt; Configuring PHP options
wordpress 09:54:52.63 INFO  ==&gt; Setting PHP expose_php option
wordpress 09:54:52.69 INFO  ==&gt; Validating settings in MYSQL_CLIENT_* env vars
wordpress 09:54:52.87 WARN  ==&gt; Hostname mariadb could not be resolved, this could lead to connection issues
wordpress 09:54:52.88 ERROR ==&gt; The WORDPRESS_DATABASE_PASSWORD environment variable is empty or not set. Set the environment variable ALLOW_EMPTY_PASSWORD=yes to allow a blank password. This is only recommended for development environments.

但是wp-cm.yaml 里面，HOST应该是没有配置错误的：
ubuntu@master:~&#47;k8s02p&#47;k8s&#47;worldPress$ cat wp-cm.yaml 

apiVersion: v1
kind: ConfigMap
metadata:
  name: wp-cm
data:
  HOST: &#39;10.244.1.11&#39;
  USER: &#39;wp&#39;
  PASSWORD: &#39;123&#39;
  NAME: &#39;db&#39;
</div>2022-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/3f/84/47f7b661.jpg" width="30px"><span>你好极客时间</span> 👍（1） 💬（3）<div>老师好，我这里访问127.0.0.1:80，报错502，是wordpress的问题么？

[root@localhost ~]# curl http:&#47;&#47;127.0.0.1
&lt;html&gt;
&lt;head&gt;&lt;title&gt;502 Bad Gateway&lt;&#47;title&gt;&lt;&#47;head&gt;
&lt;body&gt;
&lt;center&gt;&lt;h1&gt;502 Bad Gateway&lt;&#47;h1&gt;&lt;&#47;center&gt;
&lt;hr&gt;&lt;center&gt;nginx&#47;1.23.2&lt;&#47;center&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;
[root@localhost ~]#
</div>2022-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f3/37/30a09a4a.jpg" width="30px"><span>路先生</span> 👍（1） 💬（2）<div>pod一直是ContainerCreating状态，几分钟后变ImagePullBackOff，拉取不了mariadb:10镜像
执行minikube delete
minikube start --kubernetes-version=v1.23.3 --image-mirror-country=&#39;cn&#39; --image-repository=&#39;registry.cn-hangzhou.aliyuncs.com&#47;google_containers&#39; --force
把repository换成国内的还是老样子，卡半天了
kubectl describe pod maria-pod的Events:
Normal  Pulling    4m47s  kubelet            Pulling image &quot;mariadb:10&quot;</div>2022-11-16</li><br/><li><img src="" width="30px"><span>edward</span> 👍（1） 💬（2）<div>老师请问下，为什么我在本地ubuntu下ip addr 和我进入nginx的docker容器内部执行ip addr 没看到同一个IP呢，启动docker时确实使用了 --net=host 参数。</div>2022-11-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ1VPGSQg7SqrN1Gutx31Kicks2icZjTCg1gZoDLfEcSSricYD6l5qQgE3MkMpqlhkM4gMicymOYzaudg/132" width="30px"><span>可可</span> 👍（1） 💬（1）<div>kubectl apply -f wp-pod.yml执行后每次都失败，看了一下kubectl describe pod wp-pod，发现是拉去镜像超时。我就纳闷为啥我本地存在wordpress:5的docker镜像，为啥这里找不到呢。后来在网上看到minikube使用独立的docker daemon，不同于本地的docker守护进程。所以需要先把本地的docker镜像导入到minikube之中才能使用。
docker save wordpress:5 | (eval $(minikube docker-env) &amp;&amp; docker load)
此命令将镜像保存为tar存档,然后将镜像加载到minikube中。这时候删除掉之前apply失败的pod，重新apply就成功了。</div>2022-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/bf/39151455.jpg" width="30px"><span>Aioria</span> 👍（1） 💬（1）<div>老师，有个疑问，` kubectl port-forward`这条命令是否也能在.yml文件中描述呢？运行Pod后再以命令方式映射端口，似乎不利于CI&#47;CD。</div>2022-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>老师，实体对象和非实体对象是怎么区分的？ 带有容器的就是实体对象吗？</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>老师，docker run -d --rm \ --net=host ，这里的--net=host 起什么作用啊？加了以后，直接拒绝访问了，之前不都是会端口映射用来访问的吗？</div>2022-08-02</li><br/>
</ul>