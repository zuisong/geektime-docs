我在前面的专栏分析高可用复杂度的时候提出了一个问题：高可用和高性能哪个更复杂，大部分同学都分析出了正确的答案：高可用更复杂一些，主要原因在于异常的场景很多，只要有一个场景遗漏，架构设计就存在可用性隐患，而根据墨菲定律“可能出错的事情最终都会出错”，架构隐患总有一天会导致系统故障。因此，我们在进行架构设计的时候必须全面分析系统的可用性，那么如何才能做到“全面”呢？

我今天介绍的FMEA方法，就是保证我们做到全面分析的一个非常简单但是非常有效的方法。

## FMEA介绍

FMEA（Failure mode and effects analysis，故障模式与影响分析）又称为失效模式与后果分析、失效模式与效应分析、故障模式与后果分析等，专栏采用“**故障模式与影响分析**”，因为这个中文翻译更加符合可用性的语境。FMEA是一种在各行各业都有广泛应用的可用性分析方法，通过对系统范围内潜在的故障模式加以分析，并按照严重程度进行分类，以确定失效对于系统的最终影响。

FMEA最早是在美国军方开始应用的，20世纪40年代后期，美国空军正式采用了FMEA。尽管最初是在军事领域建立的方法，但FMEA方法现在已广泛应用于各种各样的行业，包括半导体加工、餐饮服务、塑料制造、软件及医疗保健行业。FMEA之所以能够在这些差异很大的领域都得到应用，根本原因在于FMEA是一套分析和思考的方法，而不是某个领域的技能或者工具。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（103） 💬（4）<div>我们公司也在用这套方法，这套方法其实就是多设计一些异常case，系统能够依然保持稳定，当然正常的case也是很重要的。</div>2018-06-21</li><br/><li><img src="" width="30px"><span>yason li</span> 👍（33） 💬（1）<div>请教老师：
根据网上查到的资料发现，经过多年的演进FMEA从定性和定量两个维度分别延伸出了FMECA和FMEDA，实际进行架构分析时是不是使用FMECA会更好一些？
还有就是FMEA分析貌似比较适合系统中单点故障的评估。如果系统比较复杂完成故障的原因有可能是多点同时互相影响那么评估时候是不是使用FTA 故障树分析更合适呢？</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（17） 💬（1）<div>MySQL 主备机，当业务服务器检测到主机无法连接后，自动连接备机，这个是需要这程序来感知主机是否联通的吗？若是，这个怎么写这个程序呢？还有如何自动切换到备机呢？我基础太差了，谢谢老师的每次回答我的问题。

</div>2018-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/37/ffa8579c.jpg" width="30px"><span>赵春辉</span> 👍（11） 💬（1）<div>之前搞过一些军方的项目，就是搞FMEA的，主要做硬件的可靠性分析，没想到在这里能看到。</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（8） 💬（1）<div>如果一个公司的架构师连公司本身的业务都不清楚的情况下，直接进行架构设计，这样做出来的架构能用么？是不是您所说的PPT架构师？</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/61/ef/ac5e914d.jpg" width="30px"><span>麦耀锋</span> 👍（7） 💬（1）<div>例如，“所有用户都无法修改资料”，有的人认为是高，有的人可能认为是中，这个没有绝对标准，一般建议相关人员讨论确定即可。也不建议花费太多时间争论，争执不下时架构师裁定即可。

上面这一段，实际上在“争执不下”的时候，make decision的不是架构师，而是产品经理或者业务负责人。因为只有产品、业务的人才知道，这个影响对于用户而言意味着什么，影响有多大。架构师一般不具备这方面的知识。</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/fd/1e3d14ee.jpg" width="30px"><span>王宁</span> 👍（7） 💬（1）<div>
HDFS可以从
网络原因分片传输
存储分片大小
DataNode故障
NameNoe故障
如果两个NameNode都出现问题这个时候就需要人工介入了吧。</div>2018-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e3/8a/a256607d.jpg" width="30px"><span>Hook</span> 👍（6） 💬（1）<div>请教老师：
FMEA 实战表格中（正文的倒数第二张图），故障原因是 “MySQL 服务器断电” 对应了 2 个功能点，分别为：登录、注册。
其中，“登录”功能点它的“后续规划”列中写的是“增加备份 MySQL”，而“注册”功能点对应的是“无，因为即使增加备份机器，也无法作为主机写入”。
我的问题是：
“注册”功能点对应的后续规划可不可以是：“增加 mysql 主从切换功能”呢？老师写“无”是从什么角度来思考“后续规划”的。</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（5） 💬（1）<div>FMEA除了分析高可用，也能分析其他架构吗，比如高性能，冗余等架构？</div>2018-07-28</li><br/><li><img src="" width="30px"><span>Geek_9f2339</span> 👍（4） 💬（1）<div>FMEA  faile model ,effects anlysis

核心是针对功能，模块进行分析，评估出功能不可用的原因，以及后果，和相应的解决方案
其中评估的核心是对 功能不可用的原因进行 风险、原因，后果，解决方案
如：0.1%的概率 因为 A原因造成 灾难性的 影响范围为30%的XX后果， 相对应的解决方案是什么

当这样的评估足够多的时候，再根据相对应的优先级，进行处理
当出现解决方案冲突点的时候，就要架构师和业务人员进行确定分析 具体的实行方案是什么

其中针对一些Case 可以有相应的解决方案，不单单只是技术手段，可是一业务手段（增加业务限制），管理手段（排除一些隐患，更换一些可能出问题的硬件，或者升级配置等）等</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/62/a45d8f3e.jpg" width="30px"><span>邱昌ོ</span> 👍（3） 💬（1）<div>老师，Mysql响应慢超过5秒，是如何做出影响60%的结论？ 实际应用中这种如何评估？</div>2018-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/e5/aa579968.jpg" width="30px"><span>王磊</span> 👍（3） 💬（1）<div>hdfs
对于datanode failure, hdfs的应对方式是数据存在多份拷贝，当某个结点down掉后，系统会检测到 under replication, 数据的其他拷贝会在其他可用结点上再增加一份拷贝;
对于那么node failure，hdfs
的应对方式是secondary namenide.</div>2018-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（2） 💬（1）<div>如何做容错机制呢？
比如for (int i = 0; i &lt; length; i++)
            {
                try
                {

                }
                catch (Exception)
                {
                    
                 
                }
            }
这个也算吗?及时程序中一项出现异常，依然会跑完。</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（1）<div>第一次听说这个，长见识了，实际工作中也会分析下系统是否高可用，不过没这个系统，主要集中在代码逻辑层面。
FMEA——故障模式与影响分析。</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（1） 💬（2）<div>如何在SQL SERVER中找慢查询语句呢？你说log配置，怎么配？谢谢</div>2018-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/ca/b1/044d3e98.jpg" width="30px"><span>杨恒</span> 👍（0） 💬（1）<div>我们用的是DFMEA, 影响因素是 严重程度*发生概率*发现难度。超过指标，提出对应方案，再次检查三个因素的影响，直达到达标准。</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/87/5f/6bf8b74a.jpg" width="30px"><span>Kepler</span> 👍（0） 💬（1）<div>有些复杂了，感觉这套方法论</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ba/8e/4645afae.jpg" width="30px"><span>Drake敏</span> 👍（0） 💬（1）<div>感觉服务器负载keepalived和mysql主从，数据备份是每家公司必定要考虑的点</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f4/8c/0866b228.jpg" width="30px"><span>子房</span> 👍（0） 💬（1）<div>这套分析方法和混沌实验一样的方法论么？</div>2021-09-07</li><br/><li><img src="" width="30px"><span>mxmkeep</span> 👍（0） 💬（1）<div>请问双网卡如何解决网络故障？这种架构一般是同同一内网吧？</div>2021-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/db/d70eb05e.jpg" width="30px"><span>森</span> 👍（0） 💬（1）<div>MySQL主备，主机挂掉了，连接备机。有这方面的插件，还是在配置里写死？修改配置为备机的漂移IP重启服务。谢谢老师解答，没有做过这方面的东西</div>2018-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（0） 💬（1）<div>什么情况下检测告警呢？能举例几个说明一下么？</div>2018-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（0） 💬（1）<div>比如我想超过三秒查不出结果就预警给相关的负责人，这个能在log里面配置吗</div>2018-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/2a/31e0085f.jpg" width="30px"><span>LC</span> 👍（22） 💬（1）<div>FMEA分析表：
1、功能点；2、故障模式；3、故障影响；4、严重程度；5、故障原因；6、故障概率；7、风险程度；8、已有措施；9、规避措施；10、解决措施；11、后续规划</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1b/70/547042ee.jpg" width="30px"><span>谭方敏</span> 👍（4） 💬（0）<div>fmea(failure mode and effects analysis )全称为故障模式与影响分析。

fmea的整体思路：
给出初始的架构设计图。
假设架构中某个部件发生故障。
分析此故障对系统功能造成的影响。
根据分析结果，判断架构是否需要进行优化。
</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/fd/1e3d14ee.jpg" width="30px"><span>王宁</span> 👍（3） 💬（0）<div>这个名词虽然不熟悉，不过这几个步骤在风险管理里面很熟悉。
风险程度=严重程度*故障概率等。</div>2018-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/6b/f61d7466.jpg" width="30px"><span>prader26</span> 👍（1） 💬（0）<div>FMEA（Failure mode and effects analysis，故障模式与影响分析）又称为失效模式与后果分析、失效模式与效应分析、故障模式与后果分析等，专栏采用“故障模式与影响分析”，因为这个中文翻译更加符合可用性的语境。
具体包括
1 功能点 2故障模式  3 故障影响 4 严重程度  5 故障原因  6故障概率 7 风险程度 8 已有措施 9 规避措施 10 解决措施</div>2021-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/29/2478f7d0.jpg" width="30px"><span>CPF</span> 👍（0） 💬（0）<div>risk assumption issue dependency</div>2021-03-14</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>        实战例子中的初始架构还存在如下故障模式:应用服务器故障、缓存和DB中数据不一致、缓存本身可能击穿或血崩都需要自己架构层面考虑。
        改进后的架构又会引入新的问题，主备发生脑裂、倒换时延要求是否满足SLA等架构上的考虑</div>2019-09-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLLUic3XzxET3L3QXxcTbeg96GMx1HkiaiaZdudchmOmtPnuEPHK5vYEeMkvJR098XljMbXDialYib3z6w/132" width="30px"><span>gkb111</span> 👍（0） 💬（0）<div>fnea方法，功能点，故障模式，故障原因，等，影响程度，改进措施等</div>2019-02-26</li><br/>
</ul>