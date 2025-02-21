你好，我是陈天。

对一个软件系统来说，不同部门关心的侧重点不同。产品、运营和销售部门关心产品的功能，测试部门关心产品的缺陷，工程部门除了开发功能、解决缺陷外，还要不断地维护和优化系统的架构，减少之前遗留的技术债。

从长远看，缺陷和技术债对软件系统是负面的作用，而功能和架构对软件系统是正面的作用。

从是否对用户可见来说，相比可见的功能和缺陷，架构和技术债是不可见的，它们往往会被公司的决策层以各种理由忽视，尤其，当他们的 KPI / OKR 上都布满了急功近利的数字，每个季度或者每半个财年都是生死战（win or go home）的时候，只要能实现功能性的中短期目标，他们什么都可以牺牲。**不可见并且很难带来直接收益的架构设计，往往是最先被牺牲掉的**。

但架构以及架构相关的工作会带来长期的回报。

因为平时我们往系统里添加新的功能，会不可避免地增加系统的缺陷，潜在引入新的技术债，以及扰乱原本稳定的架构。这是一个熵增的过程。缺陷会拖累功能的表现，进一步恶化系统中的技术债；而技术债会延缓新功能的引入，放大已有的和未来的缺陷，并破坏现有的架构。这样一直持续下去，整个系统会进入到一个下降通道，直到无以为继。

为了避免这样的事情发生，**我们需要通过对架构进行维护性的工作，来减少缺陷，修复技术债，改善功能，最终将整个系统拉回到上升通道**。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/3a/e06f8367.jpg" width="30px"><span>HiNeNi</span> 👍（6） 💬（1）<div>老师，有空的时候能不能出一些宏的教程，声明宏还好，在网上一直没有找到比较好的过程宏的教程。因为之前接触过QT，了解到一些c++框架在用自己的方式（宏加上关键字扩展）对语言或程序的行为进行很有意义的扩展，所以感觉宏这一块还是大有可为的，不知道老师有空时能不能略授一二。</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4f/c1/7f596aba.jpg" width="30px"><span>给我点阳光就灿烂</span> 👍（4） 💬（1）<div>老师，可不可以具体给一个项目代码，关于插件架构的，特别好奇这种架构是怎样实现的
</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e6/58/a0f74927.jpg" width="30px"><span>gnu</span> 👍（2） 💬（1）<div>没想到 rust 课程还藏有架构设计思想的 bonus！惊喜了</div>2022-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/32/8d/91cd624b.jpg" width="30px"><span>幻境之桥</span> 👍（1） 💬（2）<div>流水线那个例子 Context 会不会很复杂，所有 Plug 之间感觉只能通过这个 Context 交互</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（1） 💬（1）<div>过去二十年时间，敏捷宣言（Agile Manifesto）和精益创业（Lean startup）对软件社区最大的负面影响就是，一大堆外行或者并没有深刻理解软件工程的从业者，过分追求速度，过度曲解 MVP（Minimum Viable Product），而忽视了从起点出发前，必不可少的架构和设计功夫，导致大部分技术债实际上是架构和设计阶段的债务。

不能再认同了～</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/6a/b1e05143.jpg" width="30px"><span>榴莲味山楂片</span> 👍（0） 💬（1）<div>努力消化</div>2022-10-02</li><br/><li><img src="" width="30px"><span>Geek_4ca442</span> 👍（0） 💬（1）<div>老师请教个问题：如果在 kvServer 中保存的是一个结构体，value字段是要存储的值。
类似下面的功能该如何实现？传进来的参数val需要用到两次，尽管逻辑上只可能用到一次。
或者在 if ... else 语句中有类似的情况，如何实现比较好？是不是只能clone？

pub fn set&lt;T: Any + Send + Sync, K: Into&lt;String&gt;&gt;(&amp;self, key: K, val: T) {
        self.map.entry(key.into())
        .and_modify(|o| {
            *o.value = val;
            &#47;&#47; ...一些其它相关的处理
        })
        .or_insert(Value {
            count: 0,
            value: val,
        });
}</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a3/87/eb923eb3.jpg" width="30px"><span>0@1</span> 👍（0） 💬（4）<div>老师，有没有出Rust高级课程的计划</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/32/8d/91cd624b.jpg" width="30px"><span>幻境之桥</span> 👍（0） 💬（1）<div>插件化设计主要是把系统的核心能力提炼出来，供插件开发者使用，让他们的奇思妙想壮大系统生态</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/ed/3dbe915b.jpg" width="30px"><span>乌龙猹</span> 👍（0） 💬（1）<div>今天这篇更新不仅属于干货 还非常硬  实在是不想结束这段学习之旅  虽然rust 只是刚入门  但老师深入浅出地规划了 rust 的roadmap  日后定当反复研读 以求融会贯通。最后 非常期待老师未来能推出elixir 编程第一课  到时候一定支持  也该有人来向国内开发者推荐推荐 elixir 这门语言了  </div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d3/ef/b3b88181.jpg" width="30px"><span>overheat</span> 👍（0） 💬（1）<div>Rhai看描述不错哦，类javascript，有人深度使用过吗？</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/72/e2/9a19b202.jpg" width="30px"><span>阳阳</span> 👍（4） 💬（0）<div>强烈要求老师出新课程，架构课程和Rust高级。</div>2022-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/26/1f/1af5d4ed.jpg" width="30px"><span>光华路小霸王</span> 👍（0） 💬（0）<div>敏捷很大程度上降低了质量，对 client 端开发确实很痛苦</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（0）<div>你只有有了足够的替代方案，才谈得上权衡。</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/22/19585900.jpg" width="30px"><span>彭亚伦</span> 👍（0） 💬（0）<div>茅塞顿开了属于是~</div>2021-12-15</li><br/>
</ul>