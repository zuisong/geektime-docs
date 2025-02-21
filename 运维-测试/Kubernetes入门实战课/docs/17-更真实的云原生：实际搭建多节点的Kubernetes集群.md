你好，我是Chrono。

到今天，你学习这个专栏的进度就已经过半了，在前面的“入门篇”我们了解了Docker和容器技术，在“初级篇”我们掌握了Kubernetes的基本对象、原理和操作方法，一路走下来收获很多。

现在你应该对Kubernetes和容器编排有了一些初步的认识，那么接下来，让我们继续深入研究Kubernetes的其他API对象，也就是那些在Docker中不存在的但对云计算、集群管理至关重要的概念。

不过在那之前，我们还需要有一个比minikube更真实的Kubernetes环境，它应该是一个多节点的Kubernetes集群，这样更贴近现实中的生产系统，能够让我们尽快地拥有实际的集群使用经验。

所以在今天的这节课里，我们就来暂时忘掉minikube，改用kubeadm（[https://kubernetes.io/zh/docs/reference/setup-tools/kubeadm/](https://kubernetes.io/zh/docs/reference/setup-tools/kubeadm/)）搭建出一个新的Kubernetes集群，一起来看看更真实的云原生环境。

## 什么是kubeadm

前面的几节课里我们使用的都是minikube，它非常简单易用，不需要什么配置工作，就能够在单机环境里创建出一个功能完善的Kubernetes集群，给学习、开发、测试都带来了极大的便利。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/65/d6/20670fd5.jpg" width="30px"><span>Obscure</span> 👍（51） 💬（5）<div>不需要写脚本来下载镜像啊，一条命令搞定：
kubeadm init \
--apiserver-advertise-address=192.168.137.100 \
--image-repository registry.aliyuncs.com&#47;google_containers \
--kubernetes-version v1.23.6 \
--service-cidr=10.96.0.0&#47;12 \
--pod-network-cidr=10.244.0.0&#47;16</div>2022-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（16） 💬（1）<div>终于跑起来了，提醒大家一件事，那就是新节点如何加入到k8s集群中，第一遍执行有提示，后续的话，可以执行kubeadm token create --print-join-command这条命令显示加入方式</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5d/11/e1f36640.jpg" width="30px"><span>怀朔</span> 👍（15） 💬（6）<div>本章质量略显不足 .主要如下几点
1、已经在考虑多节点不如把多集群考虑进去 这样才是真正的线上环境？
2、因为网络问题 考虑仓库不足 如何直接引用国内云厂商镜像仓库？ 讲解如何把海外镜像复制国内镜像岂不是更好？
3、生产中明显最关键是网络插件问题 和cidr块 网络冲突问题 通篇没有讲 令人略显单薄</div>2022-07-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJo05FofKFWYN3joX4OyCfVrU2kK7xvKdZ4Ho7bof893fE0jXk1OcB5sKLk4C1SviaNlibAiaCtp8aww/132" width="30px"><span>努力学习不准懈怠</span> 👍（14） 💬（2）<div>一定要关闭swap，不然kubelet无法启动！！！</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/82/ec/99b480e8.jpg" width="30px"><span>hiDaLao</span> 👍（13） 💬（1）<div>1. 装环境时可先装一台然后克隆；
2. kubeadm init时指定的apiserver的ip需要是自己环境上master节点的ip地址，如果指定错误，可通过sudo kubeadm reset重置；
3. kube-flannel.yml 文件在仓库的Documentation目录下，只用copy到环境上修改下net-config.json里面的Network的地址即可；
4. 执行scp ~&#47;.kube&#47;config到console节点时，需要先在console节点上通过mkdir ~&#47;.kube创建下目录</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/06/ff/047a7150.jpg" width="30px"><span>项**</span> 👍（12） 💬（1）<div>1. --apiserver-advertise-address 参数指定成master的ip地址，不然初始化阶段会超时
找这个问题找了很久

2.初始话失败再重新尝试需要清空环境
#重置
sudo kubeadm reset
#干掉kubelet进程
ps -ef|grep kubelet
sudo kill -9 进程id
#删掉配置目录
sudo rm -rf  &#47;etc&#47;kubernetes&#47;manifests&#47;
</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/95/8a/d74cdda5.jpg" width="30px"><span>这里的人都叫我八进制</span> 👍（10） 💬（7）<div>work节点NotReady解决办法

KubeletNotReady runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
1.  mkdir -p &#47;etc&#47;cni&#47;net.d

2. vi 10-flannel.conflist

{
  &quot;name&quot;: &quot;cbr0&quot;,
  &quot;plugins&quot;: [
    {
      &quot;type&quot;: &quot;flannel&quot;,
      &quot;delegate&quot;: {
        &quot;hairpinMode&quot;: true,
        &quot;isDefaultGateway&quot;: true
      }
    },
    {
      &quot;type&quot;: &quot;portmap&quot;,
      &quot;capabilities&quot;: {
        &quot;portMappings&quot;: true
      }
    }
  ]
}


3.

systemctl daemon-reload

systemctl restart kubelet</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/72/67/aa52812a.jpg" width="30px"><span>stark</span> 👍（6） 💬（1）<div>终于弄好了，坑不少 总结写在这里了 希望对朋友们有帮助https:&#47;&#47;blog.csdn.net&#47;xuezhiwu001&#47;article&#47;details&#47;128444657?spm=1001.2014.3001.5501</div>2022-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/27/791d0f5e.jpg" width="30px"><span>小林子</span> 👍（6） 💬（1）<div>老师为啥不用 Calico 网络插件了</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/f0/d9343049.jpg" width="30px"><span>星亦辰</span> 👍（4） 💬（1）<div>cat &lt;&lt;EOF | sudo tee &#47;etc&#47;yum.repos.d&#47;kubernetes.repo
[kubernetes] 
name=Kubernetes 
baseurl=https:&#47;&#47;mirrors.aliyun.com&#47;kubernetes&#47;yum&#47;repos&#47;kubernetes-el7-x86_64 
enabled=1 
gpgcheck=0 
repo_gpgcheck=0 
EOF

补充一个 Yum 的源 
</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/ad/4efd929a.jpg" width="30px"><span>老荀</span> 👍（3） 💬（3）<div>master 节点能显示正常
$ kubectl get node
NAME     STATUS   ROLES                  AGE     VERSION
master   Ready    control-plane,master   21m     v1.23.3
worker   Ready    &lt;none&gt;                 3m56s   v1.23.3

但是 worker 节点就显示
The connection to the server localhost:8080 was refused - did you specify the right host or port?

上面的教程里，worker 节点不就是提前下好镜像和 使用 join 加入集群吗？也没说要 拷贝 什么 配置文件啊，而且 worker 节点下 &#47;etc&#47;kubernetes 下也只有 kubelet.conf 这个配置文件，和 master 节点的不一样（admin.conf) 求助老师</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/94/25/3bf277e5.jpg" width="30px"><span>陈四丰</span> 👍（3） 💬（1）<div>安装成功！
中间遇到一个“坑”，提醒同学们。
在运行https:&#47;&#47;github.com&#47;chronolaw&#47;k8s_study&#47;blob&#47;master&#47;admin&#47;master.sh的时候，一定要把注释掉的# --apiserver-advertise-address=192.168.10.210 换成自己的IP地址，并添加进去，否则会以10.0.x.x的IP运行。
感谢罗老师，祝同学们学习顺利！</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（2）<div>请教老师几个问题：
Q1：脚本为什么对src_name两次赋值？
       脚本的for循环里面有如下两行：
       src_name=${name#k8s.gcr.io&#47;}    
       src_name=${src_name#coredns&#47;}
       为什么对同一个src_name两次赋值？

Q2：同一个虚拟机上是否可以同时按照minikube和kubeadm？
Q3：apiserver的IP应该是自己的虚拟机的IP，Pod地址段和虚拟机IP无关，采用私有地址段即可，
        是这样吗？
        文中提到：“apiserver 的服务地址是“192.168.10.210””，这个地址是作者自己虚拟机的IP，
        读者应该换成自己虚拟机的IP，是这样吗？
        文中提到：“我指定了 Pod 的地址段是“10.10.0.0&#47;16””，Pod的IP段和虚拟机无关，读者的环境
        也可以采用，对吗？</div>2022-07-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLoxAjJG76r6Qib0G1rcQvVOmPc70biapxg6ny3RFX7L5KKaJdib6zUIEicvYmhyiaQeHScVMc8KjHTHIQ/132" width="30px"><span>Geek_8497e1</span> 👍（3） 💬（1）<div>请问，生产环境，老师建议用二进制还是kubeadmin</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/25/06c86919.jpg" width="30px"><span>rexzhao</span> 👍（3） 💬（2）<div>kube-flannel.yml 文件是在哪个位置？是从哪来的？ 修改的内容对吗好像不是 yml 文件格式。</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/74/d5/56b3a879.jpg" width="30px"><span>poettian</span> 👍（2） 💬（2）<div>master node 为啥会运行 kubelet 等组件呢？看前面的教程，这些组件不应该是只在 worker node 上运行的，毕竟master node上不会启动pod</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/2b/22/441c4e51.jpg" width="30px"><span>逐書寄年</span> 👍（2） 💬（3）<div>感謝老師詳盡的解說！我有的問題是：
當我部屬完cluster，也成功加入 woker node 後，想嘗試啟動 nginx pod，使用 `kubectl get pod -o wide` 檢查狀態後，卻發現一直處於 `ContainerCreating` 的狀態。不知道有沒有線索可以知道從何 debug 呢？</div>2022-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/d6/2f5cb85c.jpg" width="30px"><span>xmr</span> 👍（2） 💬（1）<div>sudo kubeadm init \
    --pod-network-cidr=10.10.0.0&#47;16 \
    --apiserver-advertise-address=192.168.10.210 \
    --kubernetes-version=v1.23.3

--apiserver-advertise-address=192.168.10.210要改为master虚拟机的ip，否则会报错</div>2022-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（2） 💬（4）<div>老师，在配置 Master 节点的时候有问题，报错如下

ppeng@master:~$ sudo kubeadm init \
    --pod-network-cidr=10.10.0.0&#47;16 \
    --apiserver-advertise-address=192.168.10.210 \
    --kubernetes-version=v1.23.3
[sudo] password for ppeng:
[init] Using Kubernetes version: v1.23.3
[preflight] Running pre-flight checks
error execution phase preflight: [preflight] Some fatal errors occurred:
	[ERROR Port-10259]: Port 10259 is in use
	[ERROR Port-10257]: Port 10257 is in use
	[ERROR FileAvailable--etc-kubernetes-manifests-kube-apiserver.yaml]: &#47;etc&#47;kubernetes&#47;manifests&#47;kube-apiserver.yaml already exists
	[ERROR FileAvailable--etc-kubernetes-manifests-kube-controller-manager.yaml]: &#47;etc&#47;kubernetes&#47;manifests&#47;kube-controller-manager.yaml already exists
	[ERROR FileAvailable--etc-kubernetes-manifests-kube-scheduler.yaml]: &#47;etc&#47;kubernetes&#47;manifests&#47;kube-scheduler.yaml already exists
	[ERROR FileAvailable--etc-kubernetes-manifests-etcd.yaml]: &#47;etc&#47;kubernetes&#47;manifests&#47;etcd.yaml already exists
	[ERROR Port-10250]: Port 10250 is in use
[preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...`
To see the stack trace of this error execute with --v=5 or higher

前面的步骤都已成功，docker 也成功拉取了镜像，不清楚这里报错的原因是什么</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/d9/cf061262.jpg" width="30px"><span>新时代农民工</span> 👍（2） 💬（1）<div>老师请问下，成功按文中操作搭建集群，在测试运行 Nginx 的时候，通过expose 端口在NodePort， 为何只能在worker的node上访问， 而在master节点上，通过本地ip访问不了呢</div>2022-08-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqF6ViaDyAibEKbcKfWoGXe8lCbb8wqes5g3JezHWNLf4DIl92QwXX43HWv408BxzkOKmKb2HpKJuIw/132" width="30px"><span>Geek_b537b2</span> 👍（2） 💬（1）<div>入门好教程</div>2022-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/36/1d/f5486ffe.jpg" width="30px"><span>你的笑忘书</span> 👍（2） 💬（1）<div>希望老师补充下生产中，使用 kubeadm 部署集群的话，有哪些务必需要注意的点。</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/b9/8b/d0763d9a.jpg" width="30px"><span>进击的土豆</span> 👍（2） 💬（1）<div>老师，kubeadm和rke的区别是什么</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（2） 💬（1）<div>理解起来很方便</div>2022-07-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKx6EdicYYuYK745brMa9yAlkZs2YmzxRAm4BQ2kw9GbtcC8ebnQlyBfIJnGjH57ib4HVlQIpSbTrBw/132" width="30px"><span>dst</span> 👍（2） 💬（1）<div>终于到中级篇了，老师讲得很好，比较全面，尤其是画图的思维导图总结很实用</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（2） 💬（4）<div>为什么到目前为止，各大云计算公司大厂都没有做一个gcr.io  k8s的同步镜像站呢</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（2） 💬（1）<div>还是挺翔实的搭建教程!</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（2） 💬（2）<div>云原生三个字怎么理解</div>2022-07-29</li><br/><li><img src="" width="30px"><span>Geek_e47add</span> 👍（1） 💬（1）<div>init k8s 成功后使用 kubectl get node 显示error: no server found for cluster &quot;minikube&quot;，请问这是什么原因，然后我启动miniukube查kubectl get node只显示minikube这个节点
</div>2023-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/dd/37726c34.jpg" width="30px"><span>小马哥</span> 👍（1） 💬（1）<div>和我一样在虚拟机安装master节点, 然后通过克隆方式创建worker节点的小伙伴, 可能会遇到和我一样的问题: 在一切配置完成之后, 启动测试一个pod(nginx:alpine)会遇到该pod一直在创建中.
执行kubectl describe pod ngx, 发现&quot;Failed to create pod sandbox: rpc error:  ..........failed to set bridge addr: 
&quot;cni0&quot; already has an IP address different from 10.10.1.1&#47;24&quot; 总之就是nginx所在的pod一直pending中.

问题解决方法: 查看一下master与worker节点的cni0的网卡ip是否相同, 因为在可控worker节点的时候, 没有修改改节点IP. 修改完成, ngx所在po的的status马上恢复RUNNING.

好像是看到留言中有个小伙伴类似问题, 应该也是克隆导致的. 
另外我使用的VMWare虚拟机软件+Centos7.6的环境, kubernetes使用的1.23.6, 和老师的都不一样, 算是好好的踩了一下坑, 锻炼一下不同的解决问题的过程.</div>2023-05-27</li><br/>
</ul>