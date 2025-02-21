你好，我是静远。

今天我们来聊一聊系统架构面临新技术到来的时候该如何思考，以及如何引入新技术。

构建一个新的系统架构，因为没有历史包袱，无论是在技术选型还是在开发部署上都比较方便。但是，“老”的应用服务由于已有的运行业务和原有技术架构的包袱，考虑的事情就比较多了。

Serverless也是如此，它在开发、测试、部署、运维等方面跟传统服务的形态不一样，近些年来，Serverless形态的PaaS产品越来越多，选择合适的业务、通过合适的途径来迭代我们的服务，也成为了一件复杂的工程。

今天这节课，我将结合与客户打交道的沉淀，跟你一起来聊聊传统服务迁移到Serverless技术架构的经验，最后完成一次迁移的实操。希望通过这样的方式，让你在做技术决策的时候，对“用与不用”“自建还是上云”“用一个或多个功能”等等这些细节都有一个相对全面的了解。

## 你真的需要迁移吗？

通常来说，但凡要做技术改造或者迁移，无非出于以下3个因素。

- **架构**：现有的技术架构不足以支撑业务的流量增长，“**系统扛不住**”了；
- **人员**：人手不够，可能是人的数量不够、人的知识储备不够，“**人扛不住**”了；
- **成本**：归根到底，还是“**钱扛不住**”，尤其是初创公司或是大公司里面的创新团队，业务还没起来，预算就那么多，该怎么办？
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/43/04/9680dade.jpg" width="30px"><span>AcelXiao</span> 👍（0） 💬（1）<div>传统服务一个业务函数有大量第三方依赖，如会查db，会发mq，会依赖其他服务接口， 这种怎么迁移？适合迁移吗？</div>2024-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>最小实例为1，为什么费用会降低10倍呢</div>2023-08-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIB01SLWDtaf0meUkDax2yLowZS7x0oPj9vgMUP2qFaXnMZD2wgiaaGFCuicBZf1AyW5Hlss2Clpgg/132" width="30px"><span>xiaojuan200804</span> 👍（0） 💬（1）<div>而目前 Serverless 托管服务最小实例为 1，这块应该是指paas吧</div>2023-03-10</li><br/>
</ul>