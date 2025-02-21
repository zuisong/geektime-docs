我们前面在讲标准化的时候，对关键的运维对象做了识别，主要分为两个部分：

- **基础设施层面**：IDC机房、机柜、机架、网络设备、服务器等；
- **应用层面**：应用元信息、代码信息、部署信息、脚本信息、日志信息等。  
  这两部分是整个运维架构的基础部分，运维团队是维护的Owner，需要投入较大的精力去好好地规划建设。

当我们识别出运维对象和对象间的关系，并形成了统一的标准之后，接下来要做的事情就是将这些标准固化，固化到某个信息管理平台中，也就是我们常说的**配置管理**，专业一点就叫作 **CMDB**（Configuration Management DataBase）。

其实，如果我们找准了需求和问题在哪里，你会发现技术手段和平台叫什么就真的不重要了，只要是内部能够达成一个统一共识的叫法就好。

关于如何打造CMDB和应用配置管理，我之前有一篇公开的文章《有了CMDB，为什么还需要应用配置管理》，写得已经比较细致了，会在下一期发布出来，但不占用我们专栏的篇幅。

今天我主要来聊一聊CMDB的前世今生，帮助你更加深刻地理解这个运维核心部件，对我们后面开展CMDB的建设大有裨益。

## CMDB源起

CMDB并不是一个新概念，它源于ITIL（Information Technology Infrastructure Library，信息技术基础架构库）。而ITIL这套理论体系在80年代末就已经成型，并在当时和后来的企业IT建设中作为服务管理的指导理论得到广泛推广和实施。但是为什么这个概念近几年才被我们熟知？为什么我们现在才有意识把它作为一个运维的核心部件去建设呢？
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/03/9e5c2259.jpg" width="30px"><span>宵伯特</span> 👍（7） 💬（1）<div>是不是可以理解为如今的大部分的资源编排服务，持续集成持续交付服务都属于CMDB的范畴？</div>2018-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/75/86b9833c.jpg" width="30px"><span>Hulk Wu</span> 👍（3） 💬（4）<div>赵哥好，我不是做运维工作的，但是希望能了解下 CMDB 的相关工具可以吗，比如 excel 以外有哪些工具可以实施 CMDB 呢，谢谢赵哥。</div>2018-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（6） 💬（0）<div>CMDB - Configuration Management DataBase
这篇文章在一定程度上回答了我之前提的问题，当我们的解决方案完全通过公有云进行托管时，和基础设施相关的维护工作，例如虚机、网络等，由云厂商来维护，对于研发和运维团队来说，更多的关注点是在应用上面。
CMDB的焦点由硬件转向应用，我理解是一个进步。</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（1） 💬（1）<div>文中提到的某公司，依旧存在excel表格管理资产的情况，直观原因是资金，人力需要足够的资金投入，资金投入就会纳入部门收益考核，这种非明显收益的投入，会影响部分领导升职，所以不会被关注，上级领导不推动，下面部门领导不关注。下级部门即便有实力推动，也局限于校招生推动，因为社招大部分不能签集团或者省公司，收益低于付出，少做就会少错。
能推动CMDB落地的，还是依赖各产品供应商免费赠送或者打包销售，捆绑在服务器，存储这类领导可以直观看到的资产上。</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/2d/9c971119.jpg" width="30px"><span>若丶相依</span> 👍（1） 💬（0）<div>最开始没有理解这些概念，到了新公司运维人员多了之后慢慢去思考什么是运维架构，重新再看课程，学习了很多。</div>2021-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/81/28418795.jpg" width="30px"><span>衣申人</span> 👍（1） 💬（0）<div>你好，我还是没搞清楚cmdb和itil的概念，以及应该做成什么样子？某些大型公司做成了什么样子？可以分享更多吗？</div>2018-07-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/pGCqjC9FJxK1WuzD3DApoQh5ej83bXc2D9eibldu95SkicC806yVb2IJ8IfMXExnbUDoHUzgV9tzpKEZxCibnyjJQ/132" width="30px"><span>Star</span> 👍（0） 💬（0）<div>我感觉cmdb也在演进，互联网cmdb算2.0版，接下来物联网cmdb就是3.0</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/30/5e/60f8eff6.jpg" width="30px"><span>林柏</span> 👍（0） 💬（0）<div>运营商像广东电信，在2001年就有完整的cmdb数据库和管理系统，远比互联网企业要早。</div>2022-02-19</li><br/>
</ul>