我们知道，Google大数据“三驾马车”的第一驾是GFS（Google 文件系统），而Hadoop的第一个产品是HDFS，可以说分布式文件存储是分布式计算的基础，也可见分布式文件存储的重要性。如果我们将大数据计算比作烹饪，那么数据就是食材，而Hadoop分布式文件系统HDFS就是烧菜的那口大锅。

厨师来来往往，食材进进出出，各种菜肴层出不穷，而不变的则是那口大锅。大数据也是如此，这些年来，各种计算框架、各种算法、各种应用场景不断推陈出新，让人眼花缭乱，但是大数据存储的王者依然是HDFS。

为什么HDFS的地位如此稳固呢？在整个大数据体系里面，最宝贵、最难以代替的资产就是数据，大数据所有的一切都要围绕数据展开。HDFS作为最早的大数据存储系统，存储着宝贵的数据资产，各种新的算法、框架要想得到人们的广泛使用，必须支持HDFS才能获取已经存储在里面的数据。所以大数据技术越发展，新技术越多，HDFS得到的支持越多，我们越离不开HDFS。**HDFS也许不是最好的大数据存储技术，但依然最重要的大数据存储技术**。

那我们就从HDFS的原理说起，今天我们来聊聊HDFS是如何实现大数据高速、可靠的存储和访问的。

Hadoop分布式文件系统HDFS的设计目标是管理数以千计的服务器、数以万计的磁盘，将这么大规模的服务器计算资源当作一个单一的存储系统进行管理，对应用程序提供数以PB计的存储容量，让应用程序像使用普通文件系统一样存储大规模的文件数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/aa/65e78697.jpg" width="30px"><span>上个纪元的赵天师</span> 👍（120） 💬（4）<div>听过本期音频，我想，在现实的条件下，实现这样的设想非常困难，例如：【1】用户空间（尤其是手机，iPad）不能保障高可用的性能，随时被访问被验证；【2】网络条件要求过高，尤其是被需求或者需要均衡时频繁的文件迁移；【3】要验证HDFS所有备份块的可用性，因此个人中端上不能过多不同用户，过碎的数据块；【4】为了保证系统的高效一般一块数据不会过小，要不然会浪费过多的计算资源（进程），如果单块数据在128M左右，自然会受到终端存储规模的制约【5】等等诸多隐患。因此，稳定的分布式端点还是必要的，不然文件将在诸多节点中频繁移动浪费大量的网络资源。【补】过于复杂的架构网络，对验证的响应延时也造成了麻烦。边走边打字暂时先想到这些😬</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d0/5d/9f9d73fe.jpg" width="30px"><span>文大头</span> 👍（43） 💬（1）<div>1、互联网上用户交分散，需要用CDN的模式，分层分区域部署NameNode，NameNode上数据汇总到上级，上级数据按需分发到下级。同一个区域的用户（DataNode）分配到同一个NameNode
2、用户DataNode机器可用性极差，按10%算，平均一个数据需要10个备份。不过可以有一定策略改进，比如让用户活跃时间跟用户等级挂钩，等级跟功能挂钩，以鼓励用户增加在线时间；存储数据可以分级别，高级别数据备份更多，可用性安全性速度更高，级别低备份少。
3、安全性考虑，其他用户存储在NameNode上的数据，不能被宿主机破解查看和修改
暂时想了这些，感觉再想下去要变成百度网盘或者迅雷了</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/72/5c801d71.jpg" width="30px"><span>牛油果</span> 👍（15） 💬（1）<div>讲技术不讲技术脉络的也都是流氓啊。那些去中心化存储的区块链项目，就没谁写出去中心存储应是借鉴或发展于hdfs等分布式存储方案。raid到hdfs立马好理解多了。我是看过ipfs，storj，sia等几个去中心化的存储方案。通过看今天的内容，我突然感觉开窍了，他们整得太复杂了，基于hdfs加上存储时空证明就能实现去中心化存储，实现高可用的技术细节考虑的当然不同了，而存储时空权益就把终端的高可用工作分散到具体用户了。当然，namenode是中心化部署还是代理节点部署还是要考虑一下。另，通过用户贡献的存储时长和空间换来的受益，这对用户的约束可能会随时间变化而减少，进而存储的可用性是不稳定的，但这里我想了两个方案:1，用户贡献出来的资源是为了储值的，获得权益是要零存整取，加大惩罚成本(这个估计他们实际做的会想到，我当时看时反正没看到)；2，整个分布式系统加一套蓝光备份系统，这种低成本数据存储方案是对要求高可用数据的备选项。</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/cf/7bec93d8.jpg" width="30px"><span>朱国伟</span> 👍（11） 💬（2）<div>关于DataNode 故障容错感觉处理起来好复杂啊 假设numReplicas=2 由于机器故障导致DataNode 1宕机 此时为了保证numReplicas=2会复制数据 像下面的情况怎么处理呢
- 等全部复制完了  DataNode1重启了 那此时numReplicas=3 这种情况会处理吗？
- 或者复制到一半（即有些Block还没来得及复制） DataNode1重启了 这种情况又怎么办
- 或者集群勉强够用 实在没有多余的机器来复制DataNode1对应的数据了 又该如何

并且要是掉电或是网络异常 可能不是一个DataNode宕机 可能是怎个机架整个机房的DataNode的都宕机了 

</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c0/c4/dfbad982.jpg" width="30px"><span>张晓生</span> 👍（10） 💬（1）<div>如果在一台nameNode服务器元数据有修改但是还没来得及热备到从nameNode服务器，这个时候刚好主nameNode服务器挂了，zookeeper选举出新的主服务器(之前的从节点)，就会造成当前的主nameNode节点数据不正确。请问这种问题怎么解决呢？</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/d4/2ed767ea.jpg" width="30px"><span>wmg</span> 👍（7） 💬（1）<div>类似于hdfs的机制，只不过将用户设备作为datanode，namenode是中心化的（否则和区块链就比较类似）。有几个问题需要考虑：1.用户设备存储空间有限，所以block的大小不能太大；2.由于block不能太大所以元数据会比较大，对namenode存储空间要求较高；3.由于datanode是不可信的，所以需要对datanode设计身份识别机制，存储的数据也必须是加密，副本数量也要设置的多一些；4.由于所有的datanode都需要和namenode通信，所以datanode的数量会有限制，这样就限制了整个集群的存储空间，可以考虑多集群的方式，用户注册的时候利用负载平衡算法将用户划分到其中一个集群。暂时想到这么多，请老师指教。</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（7） 💬（1）<div>这个思考题的实现思路是和IPFS的实现思路应该一样的</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/53/b4590ccc.jpg" width="30px"><span>阿文</span> 👍（3） 💬（1）<div>请问下，数据报错转到其他 DataNode 上读取备份数据。这个过程需要 经过 NameNode 吗？</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/1e/1e48fd05.jpg" width="30px"><span>极无宪</span> 👍（3） 💬（1）<div>如果 DataNode 监测到本机的某块磁盘损坏，就将该块磁盘上存储的所有 BlockID 报告给 NameNode？
如果已经损坏了，DataNode怎么获取到BlockID的，BlockID与数据不是存在一起的吗？</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/de/fabe5f93.jpg" width="30px"><span>谢烟客</span> 👍（3） 💬（1）<div>既然 DataNode 已经完成了冗余备份了，是不是我们就可以在 DataNode 节点的存储选用上使用 raid0 提升一下性能呢？</div>2018-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/F9CTB6Fkv6pyaP3iaYkSDC6ksv0GXsZOXyzeudxPDiczxuAibQNNibNXc4HRScMQyrSoZ4b2cEfkNlO6uM7hhJyURg/132" width="30px"><span>龙儿快看我的大雕</span> 👍（2） 💬（1）<div>老师，您说hadoop的hdfs是依赖zookeeper实现的，但是我在网上跟着集群搭建的步骤来弄，都没看到要安装zookeeper，这是咋回事？</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/c7/a7a5df8b.jpg" width="30px"><span>达子不一般</span> 👍（2） 💬（1）<div>dataNode1应该是返回客户端写成功之后然后再异步复制到其他dataNode2上吧？这个时候如果dataNode1宕机了怎么办？</div>2019-10-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep8ibEQqN1Slfh9Vg0YJcXcico7NKfl9evCeMpNKZCVE2KWtz3f404LejIsGFFzcubpW5WvhC9ibYevQ/132" width="30px"><span>子榕</span> 👍（2） 💬（2）<div>老师请问下hdfs一般集群规模都会上百吗？那像我们小公司是不是没有意义啦，我们现在每天日志量100g左右，适合用hdfs来存储吗？单机采购什么规格的合适（几核几g多少t存储）？</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（2） 💬（1）<div>关于分布式文件系统，我想向老师提个问题：
DataNode的备份在同步过程中假如出现了错误，NameNode在读取时校验后放弃某个DataNode的数据块，那么会重新为DataNode的那块数据生成新的备份么？
这些极端的情况，分布式文件系统是不是也无法百分百顾及，在设计上还是会保留容忍么？</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/19/c756aaed.jpg" width="30px"><span>鸠摩智</span> 👍（2） 💬（1）<div>如果hdfs的元数据信息超过了单台namenode的存储上限，要怎么解决呢？</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/35/114c045d.jpg" width="30px"><span>BW-Panda</span> 👍（1） 💬（1）<div>思考题答案就是现在IPFS的实现吧</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/68/afb36ef6.jpg" width="30px"><span>iWill</span> 👍（0） 💬（1）<div>如果有多个从NameNode， DataNode 也会向所有的从NameNode上报数据吗？</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（1）<div>HDFS块大小是M，如200M，电商类文件小而多，请求多，用hadoop合适吗？反应慢怎么解决，每台机子放少点？有直接监控hadoop的工具吗？</div>2018-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a3/d1/a30a4d06.jpg" width="30px"><span>张闯</span> 👍（0） 💬（1）<div>将用户设备作为DataNodes，平台部署服务器作为NameNode。为提高文件访问性能，一方面，用户数据块优先存储一份在自己的设备上。另一方面，用户设备也同时作为微型NameNode，缓存当前用户自己的数据块信息。仅在写入新数据时需要访问中心NameNode，并通过中心服务器传输数据块到其他用户的设备。</div>2018-11-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/hEOjv6QSUzoksATK55ib2ORZURG4s8oVlI6CTH2TLXkqVHwLeMRpLBmUYOKib6WrrboU8LSklUFWBvR59Dmmu79A/132" width="30px"><span>胡杨</span> 👍（0） 💬（1）<div>这个问题更像区块链的设计，可以说每个设备都可以成为数据中心</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/10/3a/053852ee.jpg" width="30px"><span>张小喵</span> 👍（22） 💬（1）<div>西电bbs，西电睿思就是使用这个原理，睿思上有庞大的数据，比如上万部电影，电视剧，学习资料，等等，都是分布式存储在睿思用户的本地pc上的，使用的是uTorrrent客户端，每次下载都是从在线的同学的pc上并行下载，下载速度很快，由于校园网内部之间走的流量是不计费的，所以在费用上面没有任何制约，本地存储的数据被他人下载的越多，会赢得更多的金币，使用金币可以去下载资源，以及“炫富”，伸手党如果总是关闭本地共享存储客户端，没有流量，那么他们能下载的资源会越来越有限，最后只能下载免费资源。金币奖励机制保证了平台的良性发展。很nice。 移动端作为共享存储客户端的话，我觉得流量费是个很大的限制，没有人想被在不知情的情况下被消费自己的移动流量，毕竟不是免费的。而且可恶的三大运营商还会限速.....我觉得，如果什么时候本地存储足够多了，流量足够便宜了，网速足够快了，客户端安全做的足够好了 那么这种共享存储的模式才会全面推广。</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/2c/900cb4f0.jpg" width="30px"><span>方得始终</span> 👍（22） 💬（1）<div>最近两大Hadoop发行商Cloudera 和Hortonworksg合并,网上包括极客时间也报道过HDFS跟云端对象存储系统已没有性能和价格上的优势.在我工作实践中也碰见过HDFS上存储的文件丢失,虽然只是一个机架(rack)断电.请问老师对此有何看法?</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（15） 💬（0）<div>老师、我想提一个问题： 主NameNode 向 Sared Edits 写数据的过程中、主Namenade 没洗完的数据是不是会丢失？ 那这样 从NameNode被选举为主NameNode 后，是不是会有一部分数据找不见存在哪个DataNode上了？ 大家都可以回答哈 另外 一个数据块 在什么情况下、不是一个分区？</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（9） 💬（1）<div>关于思考题的想法:首先这个就是各大厂商的提出的云服务的概念。而对于手机、ipad的这些设备作为分布式容器的一部分，是不可取的。首先不能不确保手机的网速的可用性，而且三大运营商都有流量这个概念。第二，手机无法实时的给NameNode进行发送心跳，因为用户可以主动关闭网络，或者用户在无网区域。</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/19/c756aaed.jpg" width="30px"><span>鸠摩智</span> 👍（8） 💬（0）<div>如果在hdfs上存储了大量的小文件，每个文件都不到一个块（128M）大小。而每个文件确实是单独的，比如一张张图片，不能把它们合并为一个大文件，这样即使一个文件namenode只存储几字节的元数据，是不是也有可能超出namenode单台机器限制了呢？</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/52/3e/a0614b62.jpg" width="30px"><span>Jack Zhu</span> 👍（4） 💬（2）<div>“如果 DataNode 监测到本机的某块磁盘损坏，就将该块磁盘上存储的所有 BlockID 报告给NameNode。”
有个疑问，望解答:磁盘损坏，怎么获得BlockID，BlockID存在哪？</div>2018-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/WN351R6WwfnlILLdnH4xsUTJCG2mYFRuibdNHBJFicTHXGiaR3lxBYGmagJhicibRWFPB7fGYnDrtV9GFQtwDo1d73A/132" width="30px"><span>黄谦敏</span> 👍（3） 💬（0）<div>主要解决问题

  1如何管理这样一个超大规模的分布式文件系统？

    1.1DataNode的大小不一、性能不一、网络状况不一。

    1.2DataNode注销频繁

    1.3DataNode上可能出现的影响可用性的问题

      1.3.1文件被修改（人为删除，恶意修改）

      1.3.2 DataNode完全不可用（网络问题、用户直接卸载、刷机）

      1.3.3 占用设备过多存储空间，影响设备正常使用（定位是利用闲置空间，不能影响其他功能）

      1.3.4 占用设备过多网络资源，影响设备正常使用。

    1.4对NameNode的处理能力要求超高

    1.5网络交换问题

    1.6数据安全问题

    1.7 进行高效的读写

  2如何向使用方收取费用

  3如何向服务方支付费用

解决方案

  从基础的HDFS架构出发

  1.1客户端注册为集群DataNode时，需要向NameNode提交可提供的存储大小。集群在收到注册请求后，向客户端发送一些测试数据，以检测DataNode的处理能力，并对处理能力进行评级。并向DataNode返回结果——注册成功或不成功。

  1.2对于正常注销，NameNode收到注销请求后，查找该DataNode有哪些数据块，分配任务给具有相同数据块的DataNode，并让其再备份一份数据到其他DataNode。

  1.3.1对于存储在 DataNode 上的数据块，计算并存储校验和（CheckSum）。在读取数据的时候，重新计算读取出来的数据的校验和，如果校验不正确就抛出异常，应用程序捕获异常后就到其他 DataNode 上读取备份数据。——抄的。

  每次DataNode的异常都把情况记录在DataNode。对于频繁出现异常的DataNode，通过客户端向对其使用者进行提醒并指导处理方法，并提示可能被取消资格的风险。对于指导后可用性依然很差的DataNode，注销其资格，转移备份并结算费用。

  1.3.2心跳通信，如果超时为发送，以宕机处理，频繁宕机的设备需要降级处理。

  1.3.3DataNode提供修改闲置空间的功能，如果需要减少闲置空间，分析新闲置空间下，需要删除数据块，并告知NameNode，NameNode进行记录，并返回新DataNode地址，旧DataNode把数据块发向新DataNode。完成后删除旧DataNode中的传输出去的数据块。

  1.3.4DataNode在客户端设置闲置带宽，并告知NameNode，NameNode对DataNode进行降级。如果实在不能再降，则劝退DataNode。

  1.4把NameNode从服务器上升为集群，即有两个NameNode集群，通过ZooKeeper选举主NameNode集群。全球的DataNode的元数据信息分布式地存储在NameNode的集群当中。（自认为这点还是有点创新，也有点套娃。）

  1.5依旧是对DataNode进行评级

  1.6依旧是对DataNode进行评级，传输的文件进行加密处理（本人加密门外汉）

  1.7 通过DataNode评级。在高等级DataNode中存储高访问频率数据，高等级用户的数据。评级低的DataNode存储不常访问的数据、或注销资格。

  2.根据需要的网络传输级别、实际使用的空间大小、实际使用的时长，支付费用。

  3.根据服务能力评级、实际支出空间大小、实际使用时长，收取费用。

写的有点多。</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/10/3a/053852ee.jpg" width="30px"><span>张小喵</span> 👍（3） 💬（0）<div>补充一点，西电睿思平台的 也有“冗余备份“的思想，学生使用ut客户端下载了电影、学习资料等文件到本地pc，那么这个pc就是一个DataNode，一个电影肯定会有很多人下载，那么这些所有下载了这个电影的同学的pc中的下载数据就形成了“冗余备份”</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/c6/1f471053.jpg" width="30px"><span>姜文</span> 👍（3） 💬（0）<div>首先要部署个name node存储元数据，记录用户数据存储的位置，为保证name node的高可用，必须做备份，通过zookeeper选举主 name node，data node就是全世界的移动设备，用户的数据要做备份，至少三份，用户的app必须和name node的主备服务器做心跳，用于移动设备故障时能主动上报或者name node能及时发现保证数据可用。用户如果要存储数据必须通知name node做好元数据记录及datanode的数据备份。第一次回答，请老师指教。</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3f/2f/8513c4d3.jpg" width="30px"><span>a(๑≖ิټ≖ิ)✌</span> 👍（2） 💬（0）<div>IPFS和迅雷的玩客云不都是这样设计的吗，涉及到很多用户的话，肯定要多冗余一些备份，这样挂掉一堆依然保证可用；为了保证速度，用户在首次取数据时把数据存在本地和周边用户节点上，下次查询就会很快了。这个系统最重要的问题是成本问题吧</div>2020-10-09</li><br/>
</ul>