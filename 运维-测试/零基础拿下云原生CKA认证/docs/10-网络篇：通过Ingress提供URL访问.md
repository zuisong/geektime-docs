你好，我是雪飞。

上节课我介绍了 Service，它主要负责集群的服务发现和负载均衡。对于来自集群外部的访问，可以使用 NodePort 或者 LoadBalance 类型的 Service，K8s 会自动绑定集群节点的端口号，通过 “&lt;节点 IP&gt;:&lt;节点端口&gt;” 来访问 Service，从而最终访问到 Service 代理的应用 Pod。但是在微服务架构中，由于集群中通常运行着多个需要暴露到外部访问的应用，如果每个应用都通过这种 Service 绑定节点端口的方式访问，可能会导致节点端口管理变得复杂且存在安全隐患。

此外，Service 是通过 IP 地址和端口来提供网络访问，这是一种四层的负载均衡，我们在实际开发项目中，更多时候是通过 URL 地址来访问应用，这需要七层的负载均衡，例如我们常用的 Nginx Web 服务就可以使用域名来代理到不同的网络应用。

> 负载均衡可以分为四层和七层，分别对应 OSI 模型的传输层和应用层。  
> 四层负载均衡工作在传输层，负责处理 TCP/UDP 协议。根据源 IP、源端口号以及目的IP和目的端口号来转发流量到应用服务器。而七层负载均衡工作在应用层，可以根据 HTTP、HTTPS、DNS 等应用层协议来进行负载均衡，还可以基于 URL、浏览器类型、语言等内容来制定负载均衡策略。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/7e/48/5515c36f.jpg" width="30px"><span>Michael闫· ᴥ ·</span> 👍（0） 💬（2）<div>老师，安装ingress的时候有一个报错，如下：
error: failed to create ingress: Internal error occurred: failed calling webhook &quot;validate.nginx.ingress.kubernetes.io&quot;: failed to call webhook: Post &quot;https:&#47;&#47;ingress-nginx-controller-admission.ingress-nginx.svc:443&#47;networking&#47;v1&#47;ingresses?timeout=10s&quot;: context deadline exceeded
</div>2024-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/7e/48/5515c36f.jpg" width="30px"><span>Michael闫· ᴥ ·</span> 👍（0） 💬（2）<div>求教一下老师：
我用service的NodePort方式，公网+ip 可以正常登录nginx，但是在ingress这部分用域名+端口就不成功，想咨询下您这里的域名+端口里面的端口指的是哪个端口啊，我下面给您复制下我的代码：
[root@k8s-master ~]# kubectl get deployment,svc -n ingress-nginx
NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps&#47;ingress-nginx-controller   1&#47;1     1            1           41m

NAME                                         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
service&#47;ingress-nginx-controller             LoadBalancer   10.103.29.35   &lt;pending&gt;     80:30257&#47;TCP,443:32431&#47;TCP   41m
service&#47;ingress-nginx-controller-admission   ClusterIP      10.106.98.61   &lt;none&gt;        443&#47;TCP 

[root@k8s-master ~]# kubectl get svc
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1     &lt;none&gt;        443&#47;TCP        67m
my-service   NodePort    10.108.8.79   &lt;none&gt;        80:30001&#47;TCP   35m

运行service：http:&#47;&#47;120.27.143.120:30001&#47;   成功
运行ingress：http:&#47;&#47;myapp.address.com:32431&#47;   失败</div>2024-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/28/040f6f01.jpg" width="30px"><span>Y</span> 👍（0） 💬（1）<div>用命令可以正常访问Nginx，用my-ingress.yaml文件不行(访问308，404)。my-ingress.yaml里面不知道哪个地方有问题。</div>2024-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/4b/95812b15.jpg" width="30px"><span>抱紧我的小鲤鱼</span> 👍（0） 💬（1）<div>ingress controller 的service 需要暴露 443，用来处理https请求
deployment 的pod 层面并不需要暴露 443，加解密其实在ingress 层处理，pod只需要叫监听内部配置的端口，然后将service 的流量转发到这个端口</div>2024-07-19</li><br/>
</ul>