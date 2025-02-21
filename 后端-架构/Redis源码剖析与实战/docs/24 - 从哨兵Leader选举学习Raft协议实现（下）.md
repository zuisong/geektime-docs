你好，我是蒋德钧。

上节课，我给你介绍了Raft协议的基本流程，以及哨兵实例工作的基本过程。哨兵是通过serverCron函数的周期性执行，进而在serverCron中调用sentinelTimer函数，实现周期性处理哨兵相关的时间事件。而sentinelTimer函数处理的时间事件，就包括了对哨兵监听的每个主节点，它会通过调用sentinelHandleRedisInstance函数，来检查主节点的在线状态，并在主节点客观下线时进行故障切换。

另外，我还带你了解了sentinelHandleRedisInstance函数执行过程的前三步操作，分别是重连断连的实例、周期性给实例发送检测命令，检测实例是否主观下线，这也分别对应了sentinelReconnectInstance、sentinelSendPeriodicCommands和sentinelCheckSubjectivelyDown这三个函数，你可以再回顾下。

那么，今天这节课，我接着来给你介绍sentinelHandleRedisInstance函数执行过程中的剩余操作，分别是检测主节点是否客观下线、判断是否需要执行故障切换，以及需要故障切换时的哨兵Leader选举的具体过程。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（11） 💬（2）<div>1、一个哨兵检测判定主库故障，这个过程是「主观下线」，另外这个哨兵还会向其它哨兵询问（发送 sentinel is-master-down-by-addr 命令），多个哨兵都检测主库故障，数量达到配置的 quorum 值，则判定为「客观下线」

2、首先判定为客观下线的哨兵，会发起选举，让其它哨兵给自己投票成为「领导者」，成为领导者的条件是，拿到超过「半数」的确认票 + 超过预设的 quorum 阈值的赞成票

3、投票过程中会比较哨兵和主库的「纪元」（主库纪元 &lt; 发起投票哨兵的纪元 + 发起投票哨兵的纪元 &gt; 其它哨兵的纪元），保证一轮投票中一个哨兵只能投一次票

课后题：哨兵在 sentinelTimer 函数中调用 sentinelHandleDictOfRedisInstances 函数，对每个主节点都执行 sentinelHandleRedisInstance 函数，并且还会对主节点的所有从节点也执行 sentinelHandleRedisInstance 函数，那么，哨兵会不会判断从节点的主观下线和客观下线？

sentinelHandleRedisInstance 函数逻辑如下：

void sentinelHandleRedisInstance(sentinelRedisInstance *ri) {
    ...

    &#47;* Every kind of instance *&#47;
    &#47;&#47; 判断主观下线
    sentinelCheckSubjectivelyDown(ri);

    ...

    &#47;* Only masters *&#47;
    if (ri-&gt;flags &amp; SRI_MASTER) {
        &#47;&#47; 判断客观下线
        sentinelCheckObjectivelyDown(ri);
        if (sentinelStartFailoverIfNeeded(ri))
            sentinelAskMasterStateToOtherSentinels(ri,SENTINEL_ASK_FORCED);
        sentinelFailoverStateMachine(ri);
        sentinelAskMasterStateToOtherSentinels(ri,SENTINEL_NO_FLAGS);
    }
}

可以看到，无论主库还是从库，哨兵都判断了「主观下线」，但只有主库才判断「客观下线」和「故障切换」。</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（8） 💬（0）<div>首先回到老师的问题：哨兵会判断从节点的主观下线和客观下线吗？
答:根据代码，我认为只会判断主观下线，并且在当前实例中，主观下线的slave实例是不能被选举的。

1、首先我们会发现在sentinelHandleDictOfRedisInstances函数中是存在递归调用的，当发现传入的instances是master的时候会继续对其slaves和sentinels进行递归调用，代码如下：
        if (ri-&gt;flags &amp; SRI_MASTER) {
            &#47;&#47;对哨兵和slaves都进行判断
            sentinelHandleDictOfRedisInstances(ri-&gt;slaves);
            sentinelHandleDictOfRedisInstances(ri-&gt;sentinels);
            if (ri-&gt;failover_state == SENTINEL_FAILOVER_STATE_UPDATE_CONFIG) {
                switch_to_promoted = ri;
            }
        }


2、但是在调用sentinelHandleRedisInstance中的时候，只有msater才会进行【客观下线】判断，而其他实例只会进行【主观下线】判断

调用路径如下：
    master实例: sentinelHandleRedisInstance -&gt; sentinelCheckSubjectivelyDown -&gt; sentinelCheckObjectivelyDown
    其它实例: sentinelHandleRedisInstance -&gt; sentinelCheckSubjectivelyDown

在sentinelHandleRedisInstance中判断【客观下线】的代码如下所示：
        &#47;* Only masters 只有master才执行 *&#47;
        if (ri-&gt;flags &amp; SRI_MASTER) {
            &#47;&#47;判断客观下线
            sentinelCheckObjectivelyDown(ri);
            if (sentinelStartFailoverIfNeeded(ri))
                sentinelAskMasterStateToOtherSentinels(ri,SENTINEL_ASK_FORCED);
            &#47;&#47;调用状态机方法
            sentinelFailoverStateMachine(ri);
            sentinelAskMasterStateToOtherSentinels(ri,SENTINEL_NO_FLAGS);
        }

3、已经被标记了主观下线的slave，在执行sentinelSelectSlave的时候会直接跳过，我理解是在当前投票实例的角度，如果某个slave是主观下线的，它在该实例的投票是不能参选的，当前所处的状态机状态是 SENTINEL_FAILOVER_STATE_SELECT_SLAVE。
    代码如下：
    while((de = dictNext(di)) != NULL) {
        sentinelRedisInstance *slave = dictGetVal(de);
        mstime_t info_validity_time;
        &#47;&#47;被标记主观下线或者客观下线的直接跳过
        if (slave-&gt;flags &amp; (SRI_S_DOWN|SRI_O_DOWN)) continue;
        ...........
        instance[instances++] = slave;
    }
    ......
    if (instances) {
        &#47;&#47;先按照优先级排序
        &#47;&#47;如果优先级一样再按照 slave_repl_offset 来进行排序（选延迟最小的）
        qsort(instance,instances,sizeof(sentinelRedisInstance*),
            compareSlavesForPromotion);
        selected = instance[0];
    }
</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/69/719ec5d0.jpg" width="30px"><span>Jian</span> 👍（1） 💬（0）<div>硬是对了代码看了3遍才看懂：）</div>2022-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/46/ae/6003be4a.jpg" width="30px"><span>木</span> 👍（0） 💬（0）<div>这里有一个很奇怪的问题，选举主节点的时候怎么能够设置2倍的配置时间呢，如果在2倍的配置时间还没有完全主从切换，又会怎么样呢</div>2023-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/9a/9b/cc08f6b3.jpg" width="30px"><span>e⃰v⃰a⃰n⃰</span> 👍（0） 💬（2）<div>我想问假如master宕机了，直接在其他的从节点中随机一个做为主节点不就行了吗？为啥还要选举？选举也是随机啊！</div>2022-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dr34H3hOMVsibL0XV1iaBWFiaTnYssX8sNjmJDpiaBUVv2X39nFzDjNpe288cKkZfH3P9sVRxZ1lzYZEcRR3vJNYtA/132" width="30px"><span>Benson_Geek</span> 👍（0） 💬（3）<div>master 记录的 Leader 的纪元（master-&gt;leader_epoch）
求问这个到底是什么东西。。。。。。。。。。。。。。。。。。。。。。。。。救命</div>2021-12-25</li><br/>
</ul>