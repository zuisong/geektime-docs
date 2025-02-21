你好，我是姚秋辰。

在上节课中，我们借助Sleuth和Zikpin的合力，搭建了一套调用链追踪系统，它可以帮助我们串联调用链中的上下游访问单元，快速定位线上异常出现在哪个环节。不过呢，光有Tracing能力似乎还不够，如果我们想要更深一步调查异常背后的原因，那必须完整还原这个异常问题的案发现场。

在线上环境中，我们无法像操作本地开发环境一样去打断点一步步调试问题，服务器的Remote Debug端口通常也是被禁用的，我们唯一能重现案发现场的途径就是**日志信息**。因此，我们还要去构建一套**日志检索系统**，作为线上异常排查的辅助工具。

今天，我就来带你通过ELK组件来搭建日志检索系统，完成整个调用链追踪方案的最后一块拼图。在这个过程中，你会知道如何使用Docker搭建ELK镜像，以及如何把应用程序对接到Logstash日志收集器，当然了，还有如何在UI界面查询日志。

在开始之前，我们先来看看什么是ELK吧。

## 什么是ELK？

ELK并不是一个技术框架的名称，它其实是一个三位一体的技术名词，ELK的每个字母都来自一个技术组件，它们分别是Elasticsearch（简称ES）、Logstash和Kibana。取这三个组件各自的首字母，就组成了所谓的ELK。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/96/fb/af39abb1.jpg" width="30px"><span>黄叶</span> 👍（16） 💬（1）<div>window版本搭建
3个软件都可以前往该中心下载，注意es和kibana版本要一样，链接：https:&#47;&#47;elasticsearch.cn&#47;download&#47;
1.安装es
下载后，进入bin目录，elasticsearch.bat 
测试：localhost:9200
2.安装kibana
下载后，进入bin目录，kibana.bat
测试：localhost:5601
3.安装logstash
需要修改配置，如下
input {
  tcp {
    #模式选择为server
    mode =&gt; &quot;server&quot;
    #ip和端口根据自己情况填写，端口默认4560,对应下文logback.xml里appender中的destination
    host =&gt; &quot;localhost&quot;
    port =&gt; 4560
    #格式json
    codec =&gt; json_lines
  }
}
output {
  elasticsearch {
    action =&gt; &quot;index&quot;
    #这里是es的地址，多个es要写成数组的形式
    hosts  =&gt; &quot;localhost:9200&quot;
    #用于kibana过滤，可以填项目名称
    index  =&gt; &quot;applog&quot;
  }
}
启动：进入bin，cmd输入logstash -f logstash.conf
测试：localhost：9600</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/60/1b/37a1eb91.jpg" width="30px"><span>威威威小哥</span> 👍（11） 💬（2）<div>老师，请问有了elk还需要集成zipkin吗？ Sleuth打的日志都可以被收集到elk，那zipkin还有意义吗</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（3）<div>老师请教一个问题啊：
Q1：docker restart geekbang
这里“geekbang”是笔误吗？前面ELK的名字是“elk”啊。</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/8f/aa0c2471.jpg" width="30px"><span>zx</span> 👍（2） 💬（1）<div>请问老师，生产环境  一般创建日志索引有什么规范没 像您文章中说的 通过配置文件表达式动态生成索引 可以大概讲一下这块思路吗</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e7/9e/5853da22.jpg" width="30px"><span>张逃逃</span> 👍（2） 💬（1）<div>请问老师，我想log request的参数应该怎么写？</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/55/4d/2b2834a9.jpg" width="30px"><span>郭行知</span> 👍（0） 💬（1）<div>生产环境为什么要先用filebeat读取文件再发送给logstash？既然logstash本身有读文件的功能，为什么不直接用logstash读取文件写到存储里？前者有何优势？</div>2023-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/d7/31d07471.jpg" width="30px"><span>牛年榴莲</span> 👍（0） 💬（1）<div>打本地日志的时候，推荐使用JSON格式还是像本节console那样的日志格式</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ca/97/87f1f07c.jpg" width="30px"><span>罗逸</span> 👍（0） 💬（1）<div>docker 运行elk Elasticsearch启动，容器也进不去

starting elasticsearch server [fail]，
Couldn&#39;t start Elasticsearch. Exiting.
Elasticsearch log follows below.
cat: &#47;var&#47;log&#47;elasticsearch&#47;elasticsearch.log: No such file or directory</div>2022-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/4c/2b/8df2453e.jpg" width="30px"><span>ziky</span> 👍（0） 💬（1）<div>请问一下老师：docker不是部署在虚拟机上吗，那么这个ip地址就会发生改变，为什么ip还是localhost </div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/c7/037235c9.jpg" width="30px"><span>kimoti</span> 👍（0） 💬（3）<div>用ELK的目的是为了看日志排错,这样配置可以看到错误信息吗？毕竟仅有TraceID和Span ID还是不知道发生了什么错误？</div>2022-02-04</li><br/><li><img src="" width="30px"><span>Geek_0b93c0</span> 👍（3） 💬（2）<div>mac m1 启动 不了</div>2022-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/d7/31d07471.jpg" width="30px"><span>牛年榴莲</span> 👍（2） 💬（1）<div>也是给了docker10个G内存才起来，给到8个G都不行</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d9/31/22fc55ea.jpg" width="30px"><span>Believe</span> 👍（0） 💬（0）<div>如果slueh + zipkin将日志持久化到es之后 还需要对接elk容器吗</div>2024-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/34/31/e41b0a92.jpg" width="30px"><span>杨涛</span> 👍（0） 💬（0）<div> [elk] unable to install syscall filter: 
java.lang.UnsupportedOperationException: seccomp unavailable: CONFIG_SECCOMP not compiled into kernel, CONFIG_SECCOMP and CONFIG_SECCOMP_FILTER are needed</div>2024-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bd/04/fc82a7f1.jpg" width="30px"><span>qwfys200</span> 👍（0） 💬（0）<div>可以配置docker的阿里云镜像环境(mirror)，这样，下载就快了。</div>2022-09-03</li><br/>
</ul>