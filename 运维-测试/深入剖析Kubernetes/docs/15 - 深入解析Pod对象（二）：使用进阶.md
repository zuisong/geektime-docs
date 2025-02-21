你好，我是张磊。今天我和你分享的主题是：深入解析Pod对象之使用进阶。

在上一篇文章中，我深入解析了Pod的API对象，讲解了Pod和Container的关系。

作为Kubernetes项目里最核心的编排对象，Pod携带的信息非常丰富。其中，资源定义（比如CPU、内存等），以及调度相关的字段，我会在后面专门讲解调度器时再进行深入的分析。在本篇，我们就先从一种特殊的Volume开始，来帮助你更加深入地理解Pod对象各个重要字段的含义。

这种特殊的Volume，叫作Projected Volume，你可以把它翻译为“投射数据卷”。

> 备注：Projected Volume是Kubernetes v1.11之后的新特性

这是什么意思呢？

在Kubernetes中，有几种特殊的Volume，它们存在的意义不是为了存放容器里的数据，也不是用来进行容器和宿主机之间的数据交换。这些特殊Volume的作用，是为容器提供预先定义好的数据。所以，从容器的角度来看，这些Volume里的信息就是仿佛是**被Kubernetes“投射”（Project）进入容器当中的**。这正是Projected Volume的含义。

到目前为止，Kubernetes支持的Projected Volume一共有四种：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（46） 💬（15）<div>在使用PodPreset对象时,发现并未生效,最终才知道是因为当初安装时未启用 Pod Preset.然后参考[https:&#47;&#47;kubernetes.io&#47;docs&#47;concepts&#47;workloads&#47;pods&#47;podpreset&#47;#enable-pod-preset] 修改  [&#47;etc&#47;kubernetes&#47;manifests&#47;kube-apiserver.yaml] 中的spec.containers.command:   修改原[ - --runtime-config=api&#47;all=true]为[- --runtime-config=api&#47;all=true,settings.k8s.io&#47;v1alpha1=true], 新加一行[- --enable-admission-plugins=PodPreset] 可以等自动生效也可以强制重启[systemctl restart kubelet]. 然后再重新创建,就可以在pod中看见spec.containers.env.name:DB_PORT等信息了.</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（22） 💬（6）<div>我记得deployment所创建的pod restart策略只支持aways。是我使用的版本太低了吗？</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3f/b7/0d8b5431.jpg" width="30px"><span>snakorse</span> 👍（20） 💬（1）<div>probe的原理是通过sidecar容器来实现的吗</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/45/5c/d983c652.jpg" width="30px"><span>章宇军</span> 👍（14） 💬（2）<div>“需要注意的是，Secret 对象要求这些数据必须是经过 Base64 转码的，以免出现明文密码的安全隐患。” base64 等同于明文吧……我理解是主要是为了 binary 类型的数据。</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b8/22/6d63d3fc.jpg" width="30px"><span>寞月</span> 👍（12） 💬（2）<div>老师好，probe我们在生产实际应用中，有个问题。就是，每次新部署的时候，旧容器要做graceful delete，这个会触发kubelet的delete逻辑。 只有在容器被kill以后，k8s才会remove 这个探针。即，容器已经收到kill信号在停服务了，但是探针还在检测于是一直报错。   不知道有没有配置可解决这个问题。</div>2018-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/2f/04882ff8.jpg" width="30px"><span>龙坤</span> 👍（10） 💬（4）<div>老师你好，有句话不太明白
原文：“相信你一定有过这样的想法：我现在有了一个 Pod，我能不能在这个 Pod 里安装一个 Kubernetes 的Client，这样就可以从容器里直接访问并且操作这个 Kubernetes 的 API 了呢？”

1. 这里可以举个简单例子吗？
2.“kubernetes的client”指的是什么？
3. 操作“kubernetes的API”这里的API由指什么？

小白问题，过不了这关，听得有点晕。见谅
</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（9） 💬（2）<div>复习了下容器的检查探针, 有几个点还是没太明白, 还望老师能解答下:
1.  restartPolicy : 这个restartPolicy是重启的Pod的Container, 那么重启的时机是根据Container结束时返回的状态码吗? 
2. restart 和 probe的关系:  Pod某个容器的livenessProbe 返回fail, 这个时候Container并没有结束, 只是状态检查是失败的, 那为什么Container也会重启呢?  这个重启动作是谁发起的呢?
3. readnessProbe:  如果某个Pod含多个Container, 且每个都有readnessProbe, 那是不是说只有全部Container的Probe返回success, 该Pod才会是 readness呢? </div>2018-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（8） 💬（1）<div>在讲述livenessProbe的时候说到：虽然是 Restart（重启），但实际却是重新创建了容器；那之前那个还在运行的liveness容器被自动销毁了吗？
</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（4） 💬（2）<div>文章中的代码 dapi-volume.yaml 格式不对,被取消了缩进,导致直接贴出来使用会报错.
还有按文章中的命令 kubectl create secret generic user --from-file=.&#47;username.txt ,在pod中[ kubectl exec -it test-projected-volume -- &#47;bin&#47;sh]展示的目录不是user,而是username.txt. 可以通过[kubectl edit secrets user]手动修改data:下的字段名.</div>2018-09-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTILhHQ6S5c2QEGNoiaL5LicibKah5wOZIh8iaWloM5XfDeW4aJwLicWlqceUVFEBicMzpqyFWDFEmVeibhFg/132" width="30px"><span>风行传说</span> 👍（4） 💬（2）<div>老师，我想问一下，您文章里面讲到的pod.spec.volumes.projected.sources下的这四种对象中的configMap secret 和pod.spec.volumes下的configMap secret是否有区别，如果没有区别那为何相同的功能对象要设置在两个不同的对象下面呢？这点让我不是特别理解，希望您能给予一下解答，谢谢！</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/fc/f46062b6.jpg" width="30px"><span>abc</span> 👍（4） 💬（2）<div>更重要的是，像这样通过挂载方式进入到容器里的 Secret，一旦其对应的 Etcd 里的数据被更新，这些 Volume 里的文件内容，同样也会被更新。
———————
想问一下，secret是可以直接挂载使用的，加个projects volumes的方式有啥好处？是自动更新吗</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/07/bf8c31fb.jpg" width="30px"><span>周娄子</span> 👍（3） 💬（1）<div>podpreset我觉得不要什么情况都用，还是坚持所见即所得。</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（2） 💬（1）<div>老师好，请问java web项目的日志输出到分布式存储里面，怎么方便查看保存好的日志呢</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/23/a0966b4d.jpg" width="30px"><span>Tim Zhang</span> 👍（2） 💬（1）<div>pv是1.11以后？</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/14/f844ecca.jpg" width="30px"><span>҉</span> 👍（1） 💬（2）<div>podpreset 支持的参数太少了。

nodeSelector 、affinity 这种好像都没有。。</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/37/7f575aec.jpg" width="30px"><span>vx:jiancheng_goon</span> 👍（1） 💬（1）<div>k8s client指的是kubectl吗？</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/37/7f575aec.jpg" width="30px"><span>vx:jiancheng_goon</span> 👍（1） 💬（1）<div>老师好，我们的平台要接入很多来自于不同团队的产品。他们的健康检查方式都类似于在容器里执行一个checkhealth的脚本，根据检查脚本的返回结果来判断。是否可以无缝接入到k8s呢？</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/6d/3c2a5143.jpg" width="30px"><span>二进制傻瓜</span> 👍（0） 💬（1）<div>信息量太大了。。。</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/6a/fdb4e298.jpg" width="30px"><span>卢彦均</span> 👍（0） 💬（1）<div>文中有个地方是否写错了？
“所以，你的 Pod 其实可以暴露一个健康检查 URL（比如 &#47;healthz）。。。”
应该是容器应用暴露一个url，而不是Pod吧？</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（0） 💬（1）<div>能不能给一个一次性任务，执行完就退出的示例</div>2018-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（1）<div>请问yaml文件开头的apiversion 是起什么作用的？可以随便写？</div>2018-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ae/c4/806fd588.jpg" width="30px"><span>Frank</span> 👍（0） 💬（1）<div>老师您好，有两个小问题
1、我在实践的时候发现pod启动后，容器里挂载的只有serviceaccount的token,ca和cert文件并未有加载(集群版本是1.10，是手动一个个组件部署配置启动的，当前并未使用安全接口启动)，在这种情况下&#47;run&#47;secrets&#47;kubernetes.io&#47;serviceaccount不存在ca和cert文件是正常的吗？

2、由于#1，这使得在启动kubedns和dashboard时都只能指定master-url来连接，不然容器就会报错退出。这是因为kubedns和dashboard这些程序都是按您说的默认使用kubernetes 官方原生的client，所以默认自动启用安全连接读取&#47;run&#47;secrets&#47;kubernetes.io&#47;serviceaccount下的ca和cert文件吗？</div>2018-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/28/eec9220b.jpg" width="30px"><span>jimmy</span> 👍（0） 💬（1）<div>获取 Pod 容器运行后才会出现的信息，使用sidecar，这个不太理解，在pod里增加一个辅助容器？怎么获取Pod 容器运行后才会出现的信息呢？</div>2018-10-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJicBibF1UEOAhicickjCRXzVBDDyAMTw5C7EP3IPSKyTqWjvtmicB4AFu0B72BVyxFAVnNHrbx672p2Ow/132" width="30px"><span>多肉</span> 👍（0） 💬（3）<div>请问个问题，为什么我的容器目录中得到得文件是 .txt文件，而不是文章中所说得user和pass呢？
root@test-projected-volume:&#47;# ls &#47;project-volume&#47;
password.txt username.txt
我secrets是安装根据username.txt文件创建得admin和pass secrets对象</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/86/8211935c.jpg" width="30px"><span>Vincent</span> 👍（0） 💬（1）<div>文中Download api 的yml文件好像有问题，创建会报错
error: error validating &quot;downloadapi-volume.yaml&quot;: error validating data: ValidationError(Pod.spec.volumes[0].projected.sources[0]): unknown field &quot;items&quot; in io.k8s.api.core.v1.VolumeProjection; if you choose to ignore these errors, turn validation off with --validate=false

看了官档要这样才能创建成果
apiVersion: v1
kind: Pod
metadata:
  name: test-downwardapi-volume
  labels:
    zone: us-est-coast
    cluster: test-cluster1
    rack: rack-22
spec:
  containers:
    - name: client-container
      image: k8s.gcr.io&#47;busybox
      command: [&quot;sh&quot;, &quot;-c&quot;]
      args:
      - while true; do
          if [[ -e &#47;etc&#47;podinfo&#47;labels ]]; then
            echo -en &#39;\n\n&#39;; cat &#47;etc&#47;podinfo&#47;labels; fi;
          sleep 5;
        done;
      volumeMounts:
        - name: podinfo
          mountPath: &#47;etc&#47;podinfo
          readOnly: false
  volumes:
    - name: podinfo
      downwardAPI:
        items:
          - path: &quot;labels&quot;
            fieldRef:
              fieldPath: metadata.labels


不知道说的是不是对的？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/54/552bde40.jpg" width="30px"><span>Yiliu</span> 👍（0） 💬（1）<div>istio的自动添加sidecar是不是就是用的preset</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（0） 💬（1）<div>deployment创建的pod只支持restart aways，是为了让pod保存始终出于预期运行状态的概念吗?
所有文章中写的pod的各种重启方式，是专门指单独创建pod的情况下?

极客时间不能直接回复作者的回复好麻烦啊哈哈哈，感觉交流会断掉。
谢谢张磊一直都在保持回复，教程太棒了。</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/41/82306dfe.jpg" width="30px"><span>包子</span> 👍（0） 💬（1）<div>一般的容器在不访问server api时，Service account token挂载可以关掉吗老师，没什么影响吧？</div>2018-09-26</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（172） 💬（14）<div>Kuberentes可以理解为操作系统，那么容器就是进程，而Pod就是进程组or虚拟机（几个进程关联在一起）。

Pod的设计之初有两个目的：
（1）为了处理容器之间的调度关系
（2） 实现容器设计模式： Pod会先启动Infra容器设置网络、Volume等namespace（如果Volume要共享的话），其他容器通过加入的方式共享这些Namespace。

如果对Pod中的容器启动有顺序要求，可以使用Init Contianer。所有Init Container定义的容器，都会比spec.containers定义的用户容器按顺序优先启动。Init Container容器会按顺序逐一启动，而直到它们都启动并且退出了，用户容器才会启动。

Pod使用过程中的重要字段：
（1）pod自定义&#47;etc&#47;hosts:  spec.hostAliases
（2）pod共享PID : spec.shareProcessNamespace 
（3）容器启动后&#47;销毁前的钩子： spec.container.lifecycle.postStart&#47;preStop
（4）pod的状态：spec.status.phase
（5）pod特殊的volume（投射数据卷）:
   5.1) 密码信息获取：创建Secrete对象保存加密数据，存放到Etcd中。然后，你就可以通过在Pod的容器里挂载Volume的方式，访问到这些Secret里保存的信息
  5.2）配置信息获取：创建ConfigMap对象保存加密数据，存放到Etcd中。然后，通过挂载Volume的方式，访问到ConfigMap里保存的内容
  5.3）容器获取Pod中定义的静态信息：通过挂载DownwardAPI 这个特殊的Volume，访问到Pod中定义的静态信息
  5.4) Pod中要访问K8S的API：任何运行在Kubernetes集群上的应用，都必须使用这个ServiceAccountToken里保存的授权信息，也就是Token，才可以合法地访问API Server。因此，通过挂载Volume的方式，把对应权限的ServiceAccountToken这个特殊的Secrete挂载到Pod中即可
  （6）容器是否健康： spec.container.livenessProbe。若不健康，则Pod有可能被重启（可配置策略）
  （7）容器是否可用： spec.container.readinessProbe。若不健康，则service不会访问到该Pod
</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/3e/534db55d.jpg" width="30px"><span>huan</span> 👍（67） 💬（1）<div>不实践，就无法理解为什么pod这么设计，这里给了我自己的实践的记录：

https:&#47;&#47;github.com&#47;huan9huan&#47;k8s-practice&#47;tree&#47;master&#47;15-pod-advanced

仅供参考。</div>2018-09-26</li><br/>
</ul>