你好，我是秦晓辉。

前面三讲我们介绍了监控系统的一些基本概念，这一讲我们开始进入实操环节，部署监控系统。业界可选的开源方案很多，随着云原生的流行，越来越多的公司开始拥抱云原生，而云原生标配的监控系统显然就是 Prometheus，而且Prometheus的部署非常简单，所以这一讲我们就先来自己动手搭建Prometheus。

## 通用架构回顾

还记得我们上一讲介绍的监控系统通用架构吗？我们可以回顾一下。

![图片](https://static001.geekbang.org/resource/image/9e/f5/9edcfef623ea9583134533c3b4c477f5.png?wh=1920x781)

之所以说 Prometheus 比较容易搭建，是因为它把服务端组件，包括时序库、告警引擎、数据展示三大块，整合成了一个进程，组件的数量大幅减少。Prometheus生态的采集器就是各种Exporter，告警发送靠的是 AlertManager 组件，下面我们先来部署 Prometheus 模块。

## 部署 Prometheus

因为生产环境大概率是Linux的，所以我们选择Linux下的发布包，把Prometheus 和 Alertmanager 两个包都下载下来。

注：Prometheus 的下载地址：[https://prometheus.io/download/](https://prometheus.io/download/)

![图片](https://static001.geekbang.org/resource/image/cf/f7/cf6af0ffc5f3be2867f8a18d0cd254f7.png?wh=1920x1259)

下载之后解压缩，使用 systemd 托管启动，你可以参考下面的命令。

```bash
mkdir -p /opt/prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.37.1/prometheus-2.37.1.linux-amd64.tar.gz
tar xf prometheus-2.37.1.linux-amd64.tar.gz
cp -far prometheus-2.37.1.linux-amd64/*  /opt/prometheus/

# service 
cat <<EOF >/etc/systemd/system/prometheus.service
[Unit]
Description="prometheus"
Documentation=https://prometheus.io/
After=network.target

[Service]
Type=simple

ExecStart=/opt/prometheus/prometheus  --config.file=/opt/prometheus/prometheus.yml --storage.tsdb.path=/opt/prometheus/data --web.enable-lifecycle --enable-feature=remote-write-receiver --query.lookback-delta=2m --web.enable-admin-api

Restart=on-failure
SuccessExitStatus=0
LimitNOFILE=65536
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=prometheus



[Install]
WantedBy=multi-user.target
EOF

systemctl enable prometheus
systemctl start prometheus
systemctl status prometheus
```
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/88/ff81f846.jpg" width="30px"><span>凡人</span> 👍（2） 💬（2）<div>秦老师，你好，文章中 有两个小细节问题
1. 文章中没有提到 需要修改 prometheus.yml 中的  # - alertmanager:9093。
2. 163邮箱的smtp协议 非ssl端口号是25 (https:&#47;&#47;note.youdao.com&#47;ynoteshare&#47;index.html?id=f9fef46114fb922b45460f4f55d96853) </div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/52/21275675.jpg" width="30px"><span>隆哥</span> 👍（1） 💬（1）<div>①部署了prometheus，无法通过IP+9090访问，有可能是防火墙没有关闭，我使用的是CentOS系列
systemctl stop firewalld.service
systemctl disable firewalld.service
②添加node_exporter在Status -&gt; Targets无法查看，prometheus修改配置需要每次重新加载读取
systemctl restart prometheus
③如何添加报警规则
请在应用目录prometheus下创建一个rules文件夹，然后在文件夹中添加node_exporter.yml
[root@bogon prometheus]#mkdir -p rules &amp;&amp; cd rules &amp;&amp; vim node_exporter.yml
添加规则内容之后，配置prometheus.yml,这样子目录更美观，新重启服务systemctl restart prometheus
rule_files: 
  - &quot;rules&#47;node_exporter.yml&quot;
④为什么我grafana控制面板有时候图标会出现断层呢？

如果觉得教程麻烦，提供一键docker-compose剧本
version: &#39;3&#39;

networks:
  monitor:
    driver: bridge

services:
  prometheus:
    image: prom&#47;prometheus
    container_name: prometheus
    hostname: prometheus
    restart: always
    volumes:
      - &#47;data&#47;prometheus&#47;data:&#47;prometheus
      - &#47;data&#47;prometheus&#47;rules:&#47;etc&#47;prometheus&#47;rules
      - &#47;data&#47;prometheus&#47;conf&#47;prometheus.yml:&#47;etc&#47;prometheus&#47;prometheus.yml
    ports:
      - &quot;9090:9090&quot;
    networks:
      - monitor

  alertmanager:
    image: prom&#47;alertmanager
    container_name: alertmanager
    hostname: alertmanager
    restart: always
    volumes:
      - &#47;data&#47;alertmanager&#47;config&#47;alertmanager.yml:&#47;etc&#47;alertmanager&#47;alertmanager.yml
    depends_on:
      - prometheus
    ports:
      - &quot;9093:9093&quot;
    networks:
      - monitor

  node-exporter:
    image: quay.io&#47;prometheus&#47;node-exporter
    container_name: node-exporter
    hostname: node-exporter
    restart: always
    environment:
      TZ: Asia&#47;Shanghai
    volumes:
    depends_on:
      - prometheus
    ports:
      - &quot;9100:9100&quot;
    networks:
      - monitor

  grafana:
    image: grafana&#47;grafana
    container_name: grafana
    hostname: grafana
    restart: always
    volumes:
      - &#47;data&#47;grafana&#47;data:&#47;var&#47;lib&#47;grafana
    depends_on:
      - prometheus
    ports:
      - &quot;3000:3000&quot;
    networks:
      - monitor</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/b0/ab179368.jpg" width="30px"><span>hshopeful</span> 👍（15） 💬（2）<div>关于 pull 和 push 模式，个人的一些理解，有错误或遗漏的，希望老师指正：

pull 模式的优点：
1、pull 模式很容易判断监控对象的存活性，push 模式很难
2、pull 模式的监控配置在服务端，比较容易统一控制，push 模式的监控配置在客户端，需要引入类似配置中心的组件，由客户端去拉取监控配置，从配置变更到配置生效的难易程度和时效性，pull 模式占优
3、pull 模式可以按需获取监控指标，push 模式只能被动接收监控指标，当然 push 模式也可以在服务端增加指标过滤规则
4、pull 模式下，应用与监控系统的耦合比较低，push 模式下，应用于监控系统的耦合性较高

push 模式的优点：
1、针对移动端的监控，只能使用 push 模式，不能使用 pull 模式
2、push 模式支持天然的水平扩展，pull 模式水平扩展比较复杂
3、push 模式适合短生命周期任务，pull 模式不适合
4、pull 模式依赖服务发现模块，push 模式不依赖
5、push 模式只用保证网络的正向联通（能够发送数据到服务端），比较简单，而 pull 模式需要保证网络的反向联通（服务端能够抓取多种多样的客户端暴露的接口），相对复杂
6、pull 模式需要暴露端口，安全性存在隐患，而 push 模式不存在
7、在聚合场景和告警场景下，push 模式的时效性更好</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（3） 💬（1）<div>关于告警有一些建议和疑问：
1、告警分级(提示、严重、致命)全部邮件推送很难体现优先级，尤其是致命告警应该电话处理
2、目前社区是否有成熟的告警推送工具，比如企业微信机器人、钉钉机器人，这些需要自行编码实现？电话告警该如何实现呢？</div>2023-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e3/12/fd02db2e.jpg" width="30px"><span>April</span> 👍（2） 💬（2）<div>Prometheus没有提供很多管理上的API,又不想引入Service Discovery, 在targets变化后直接操作prometheus.conf有什么更为简单的方式吗？</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（1）<div>请问老师，在k8s里部署prometheus，有哪些比较好的方式呢。</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/52/21275675.jpg" width="30px"><span>隆哥</span> 👍（1） 💬（2）<div>为啥不用docker形式来做实践呢，我觉得systemctl这种托管还是对主机入侵比较大。</div>2023-01-16</li><br/><li><img src="" width="30px"><span>Geek_df0d4d</span> 👍（0） 💬（1）<div>请问生产上有什么prometheus的高可用方案吗</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/ac/aa/2f117918.jpg" width="30px"><span>孙宇翔</span> 👍（0） 💬（3）<div>老师您好，我想监控像摄像机这类设备的在线、离线，还有流量等数据，普罗米修斯是否合适，配置里面该怎么设置，完全没头绪。。。</div>2023-03-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKSVuNarJuDhBSvHY0giaq6yriceEBKiaKuc04wCYWOuso50noqDexaPJJibJN7PHwvcQppnzsDia1icZkw/132" width="30px"><span>Matthew</span> 👍（0） 💬（2）<div>老师，文章中提到的几个软件安装包，都需要从 github 上下载，但是下载速度太慢。能否提供下国内镜像源的地址呢？</div>2023-02-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKSVuNarJuDhBSvHY0giaq6yriceEBKiaKuc04wCYWOuso50noqDexaPJJibJN7PHwvcQppnzsDia1icZkw/132" width="30px"><span>Matthew</span> 👍（0） 💬（4）<div>github 下载太慢，有啥好办法吗？</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/13/67/910fb1dc.jpg" width="30px"><span>leeeo</span> 👍（0） 💬（1）<div>源码编译prometheus可以去掉ui部分吗？</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a1/69/0af5e082.jpg" width="30px"><span>顶级心理学家</span> 👍（0） 💬（1）<div>秦老师，有个问题是关于exporter多实例的问题。
我们环境是prometheus operator，例如 redis采用redis-exporter采集。这样就造成多个redis实例，实现成了多个exporter 来采集。redis exporter有案例支持一个exporter采集多个实例，但是没能实现。
目前就是一个exporter 启动多个container，用不同端口采集多个redis实例，这样container会随着redis实例增多而庞大。
想听听您的建议和想法。</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/23/26f8f45a.jpg" width="30px"><span>俺木饭 三克油😂😂</span> 👍（0） 💬（1）<div>老师问下如何做prom 和各类exporter之间的认证？比如公司安全需求所有接口需要做鉴权</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（0） 💬（2）<div>咨询下grafana端口外网通过ip无法访问可能是什么原因呢？3000端口在安全组已经放开了，防火墙也方阿奎了，另外Prometheus9090端口是正常用的。http:&#47;&#47;ip:3000&#47;login   
Request URL: http:&#47;&#47;39.107.88.69:3000&#47;login
Referrer Policy: strict-origin-when-cross-origin
Provisional headers are shown
Learn more
Upgrade-Insecure-Requests: 1</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/4b/33/48b278a4.jpg" width="30px"><span>SEVEN</span> 👍（0） 💬（1）<div>老师。如果想把启动用户改成prometheus，那systemd文件该怎么写？
[Unit]
Description=&quot;prometheus&quot;
Documentation=https:&#47;&#47;prometheus.io&#47;
After=network.target
[Service]
Type=simple
User=prometheus
Group=prometheus
WorkingDirectory=&#47;app&#47;prometheus&#47;prometheus&#47;
ExecStart=&#47;app&#47;prometheus&#47;prometheus&#47;prometheus  --config.file=&#47;app&#47;prometheus&#47;prometheus&#47;prometheus.yml --storage.tsdb.path=&#47;app&#47;prometheus&#47;prometheus&#47;data --web.enable-lifecycle --enable-feature=remote-write-receiver --query.lookback-delta=2m --web.enable-admin-api
Restart=on-failure
SuccessExitStatus=0
LimitNOFILE=65536
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=prometheus
[Install]
WantedBy=multi-user.target
我这么写但是启动失败
我们生产中对root权限的管理很严格。建议老师后面的课程能尽量以prometheus普通用户的权限讲。</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/22/8437fd56.jpg" width="30px"><span>embeder</span> 👍（0） 💬（1）<div>老师我想问问，这个课程展示大盘使用夜莺来完成的吗？业务需要收集整个机房所有机器的运行日志，公司现在用的是zabbix监控，我想把收集日志和监控系统一起搞一下。我觉得夜莺就挺适合我们的。</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/b0/ab179368.jpg" width="30px"><span>hshopeful</span> 👍（0） 💬（2）<div>秦老师，另外还有一个问题想请教下：
a、关于配置 SMTP 发件服务器的相关信息，使用 163 或者 qq 邮箱，网上能够找到 smtp_smarthost 的配置 smtp.163.com:465 和 smtp.qq.com:465，另外也能找到怎么去获取授权码。
b、使用这些外部邮箱作为发件服务器，可以向公司的邮箱点对点发送告警邮件，但是不能向公司的邮件组发送告警邮件（公司的邮件组默认设置的规则是拒收外部邮箱的邮件）
c、怎么去获取公司邮件服务器的 smtp_smarthost 的配置和相关授权码，老师能给下建议吗？公司内部的邮件服务器不知道谁维护的</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e4/1b/e8f5f5e4.jpg" width="30px"><span>大菠萝</span> 👍（0） 💬（1）<div>老师后面会讲讲 grafana自定义dashborad吗？</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：下载页面不是最新的，老师是用以前的图片写文章吗？
文章中，下载页面的图片，不是最新的。今天（1月16号）打开的下载页面和文章中的不同。（暂时没有发现历史版本的链接）
Q2：receivers中的web_hook为什么没有在route中配置？
receivers中的email在route中配置了，但web_hook却没有配置。
Q3：prometheus的架构算什么类型的架构？
文中提到“Grafana是插件式架构”，那么，prometheus的架构是什么类型？ 算C&#47;S架构吗？
Q4：不遵守GPL协议会有什么结果？
假如我创办一个小公司，用了GPL开源软件，做了二次开发但没有开源，会有什么后果？（个人感觉好像没事啊，难道有人来罚款吗）
Q5：Prometheus server是以pull方式从Pushgateway获取数据吗？
我的理解：short-lived jobs以push方式将数据推送到Pushgateway，但Pushgateway并不会将数据push到Prometheus server. Prometheus server还是通过pull从Pushgateway获取数据。</div>2023-01-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTINjIqCwibaXko2LB1gyDDvZlCmicOc1nlJYTv83lVADWrkKc3Z95RUj1xx2x5Y9u0CYDG7unldQwVA/132" width="30px"><span>Geek_d56774</span> 👍（1） 💬（0）<div>请问prometheus启动可以设置服务本身的日志输出级别和输出路径吗</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/45/b2/24dee83c.jpg" width="30px"><span>Ppppppp</span> 👍（1） 💬（0）<div>yaml文件 建议老老实实敲空格，尤其是到了一个新公司不熟悉机器配置的时候。</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5e/45/50424a7a.jpg" width="30px"><span>叶夏</span> 👍（1） 💬（1）<div>请问会讲Prometheus的高可用吗？</div>2023-01-17</li><br/>
</ul>