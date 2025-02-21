你好，我是潘野。

在做云原生训练营助教的时候，很多同学对“不可变基础设施”这一个概念不太理解，如果你在网络上搜索“不可变基础设施”，往往会到得这样的说法：

> 不可变基础设施是指一种基于代码和配置的基础设施管理方法，其中所有的更改和配置都是通过重新构建和替换来实现的，而不是直接修改现有的设施。这种方法的目标是确保系统的稳定性和一致性，减少人为错误和配置漂移，并提高系统的可靠性和可管理性。

很多同学读了之后一头雾水，产生了后面这些疑问。

- 我用puppet或者ansible不也是代码方式来管理基础设施，这样不是也能保证一致性吗？
- 如果更改配置都是通过替换实例的方式，这样做的成本是不是太高了？
- 没看出“不可变”的好处在哪里？

今天这节课，我就带你重新理解一下“不可变基础设施”，看看它究竟带来了什么样的管理优势。最后，我还会带你一起体验下，不可变基础设施中的新星bottlerocket如何使用。

## 运维之痛：给操作系统打补丁

通过前面的学习，我们知道了在虚拟机时代，的确可以通过Puppet、Saltstack、Ansible这类配置管理工具来实现IaC。即便到今天，这些工具也仍然在运维管理工作中非常流行。

以往比较常见的运维工作就是给虚拟机打安全补丁，或者是升级主机内核，这时我们的做法基本都是更改Puppet的配置文件，配置推送到目标机器，并且联系业务团队安排时间做主机重启。用这种方式管理的机器，我们叫做**可变基础架构**。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2d/e7/72/4cec29a8.jpg" width="30px"><span>暴躁的蜗牛</span> 👍（3） 💬（1）<div>bottlerocket 是可以替代 容器的 Alpine Linux吗 感觉虽然都是操作系统 是否某些应用会指定 操作系统的版本 这样对 系统bottlerocket  有影响吗</div>2024-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/b5/e9/f1aa07d6.jpg" width="30px"><span>alex run</span> 👍（3） 💬（1）<div>老师，能谈一下私有云落地bottlerocket的做法吗？ 然后我想问一下，将传统操作系统替换成bottlerocket是有必要做的一件事情吗？ 回报会高于投入吗？</div>2024-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/62/b1/3d1fc497.jpg" width="30px"><span>三万棵树</span> 👍（0） 💬（2）<div>Bottlerocket 这个在国内的落地情况 想咨询您一下</div>2024-03-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Wo6BMoLTHHWTTg2y3jKIaA3TVuyxsd1a3f118GSiaymop7KHxxTkJwlxGb3qQMyBoD7t8y4lFbKVhHqhmf7Ngibw/132" width="30px"><span>二十三</span> 👍（0） 💬（0）<div>国内公有云貌似都还没有支持</div>2024-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（0） 💬（0）<div>Bottlerocket 这个在国内用的多吗？</div>2024-03-29</li><br/>
</ul>