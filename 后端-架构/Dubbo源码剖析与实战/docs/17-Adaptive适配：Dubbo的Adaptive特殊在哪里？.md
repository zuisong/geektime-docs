你好，我是何辉。

有了上一讲“Compiler 编译”的基础，相信你在今天Dubbo源码第六篇 Adaptive 适配，会比较轻松。

其实Adaptive我们见过好几次了。还记得在“[SPI 机制](https://time.geekbang.org/column/article/620900)”中提到的 ExtensionLoader 类么，我们在认真研究 ExtensionLoader 源码时，发现这个类里有一个获取自适应扩展点的方法（getAdaptiveExtension）。

深入 Dubbo SPI 机制的底层原理时，在加载并解析 SPI 文件的逻辑中，你会看到有一段专门针对 Adaptive 注解进行处理的代码；在 Dubbo 内置的被 @SPI 注解标识的接口中，你同样会看到好多方法上都有一个 @Adaptive 注解。

这么多代码和功能都与 Adaptive 有关，难道有什么特殊含义么？Adaptive究竟是用来干什么的呢？我们开始今天的学习。

## 自适应扩展点

照例还是从直接的方式——代码着手，我们就先从 ExtensionLoader 的 getAdaptiveExtension 方法开始吧。

不过，一开始就有点小障碍，从 ExtensionLoader 的使用方式上看，我们得找个接口传进去，但是这一时半会也不知道传什么接口才好啊。

别慌，回忆我们在“[点点直连](https://time.geekbang.org/column/article/613319)”学过一个小技巧，如果不知道源码的某个方法如何使用，最好的第一手资料就是源码，从源码中寻找别人使用这个方法的正确姿势。按照小技巧的思路，看下 getAdaptiveExtension 方法有多少个方法被调用。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/0d/3c/282428e5.jpg" width="30px"><span>Ahaolin</span> 👍（1） 💬（1）<div>https:&#47;&#47;ahaolin-public-img.oss-cn-hangzhou.aliyuncs.com&#47;img&#47;202303030954605.png</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4e/78/ee4e12cc.jpg" width="30px"><span>Lum</span> 👍（0） 💬（1）<div>这里在生成代理类得时候会根据该注解判断是否有value值，如果没有就通过小写字母分开为点camelToSplitName，如果有就按照注解的value值进行赋值</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4e/78/ee4e12cc.jpg" width="30px"><span>Lum</span> 👍（0） 💬（1）<div>老师讲的真好，层层深入，对dubbo的spi有了更深的理解了，期待学完课把dubbo所有的流程串起来</div>2023-03-01</li><br/>
</ul>