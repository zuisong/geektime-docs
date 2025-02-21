你好，我是轩脉刃。

在上一节课，比对了 Gin 框架和我们之前写的框架，明确框架设计的目标是，要设计出真正具有实用性的一个工业级框架，所以我们接下来会基于现有的比较成熟的 Gin 框架，并且好好利用其中间件的生态，站在巨人的肩膀，继续搭建自己的框架。

## 如何借力，讨论开源项目的许可协议

有的人可能就有点困惑了，这样借鉴其他框架或者其他库不是侵权行为吗？

要解答这个问题，我们得先搞清楚站在巨人肩膀是要做什么操作。借鉴和使用 Gin 框架作为我们的底层框架基本思路是，以复制的形式将 Gin 框架引入到我们的自研框架中，替换和修改之前实现的几个核心模块。

我们后续会在这个以 Gin 为核心的新框架上，进行其余核心或者非核心框架模块的设计和开发，同时我们也需要找到比较好的方式，能将 Gin 生态中丰富的开源中间件进行复制和使用。

现在我们再来回答是否侵权的问题，首先得了解开源许可证，并且知道可以对 Gin 框架做些什么操作？

开源社区有非常多的开源项目，每个项目都需要有许可说明，包含：是否可以引用、是否允许修改、是否允许商用等。目前的开源许可证有非常多种，每个许可证都是一份使用这个开源项目需要遵守的协议，而主流的开源许可证在 OSI 组织（开放源代码促进会）都有 [登记](https://opensource.org/licenses) 。**最主流的开源许可证有 6 种：Apache、BSD、GPL、LGPL、MIT、Mozillia**。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（1） 💬（1）<div>大家不要只看文章不看github的代码 很细节的放在文章中 很占篇幅 一般都是说个思路 然后自己去迁移
不过 github的代码有些细节没处理好
 IRequest 很多方法其实已经删除了 但是接口定义还在 会让人迷糊  所以会有小伙伴说没有实现所有办法 这个得自己去判断思考的。
不过希望老师之后可以注意下</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（1）<div>作为 方法名叫做 QueryAll 以及 Form  和 Param 这种方法 改变成 DefaultXXX 方法签名语义上并没有default的属性  老师这里是否可以修改下 还是说也是合理的</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（0） 💬（1）<div>有没有可能将gin封装一个provider，然后在封装的provider里面加container，这样就不用在gin源码上更改了呢？</div>2021-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7rprdxQqcea53sw1HCz1YZjQNlSvWg7GETnWYicZLYOQR2GUMOwUnrhAIYzUKJt1zZhUv9icOCztQ/132" width="30px"><span>鸭补一生如梦</span> 👍（13） 💬（7）<div>现在定制的是 gin 的 1.7.3 版本，那么后续 gin 升级了，尤其是频繁升级，我们如何快速及时的进行升级更新？
或者说隔一段时间再更新？</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d7/f2/82e1dc03.jpg" width="30px"><span>181</span> 👍（3） 💬（2）<div>--- FAIL: TestContextFormFileFailed (0.00s)
panic: runtime error: invalid memory address or nil pointer dereference [recovered]
        panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x18 pc=0x6678d2]


这是啥原因</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/0f/da7ed75a.jpg" width="30px"><span>芒果少侠</span> 👍（3） 💬（5）<div>迁移完成后，遇到testcase不通过的问题。
https:&#47;&#47;github.com&#47;gin-gonic&#47;gin&#47;blob&#47;21125bbb3f550dbfa4c64151f7e01f58dd64e2b8&#47;context_test.go#L352
如果是这个testcase，修改正则中包路径那部分即可（与自己项目go module path保持一致即可）。</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/01/82/041cea49.jpg" width="30px"><span>tiger</span> 👍（2） 💬（0）<div>感觉整合了gin有点没有了自己写一个框架的感觉，我还是选择了分开放，分别同步了两边的一些方法。示例的框架简陋是简陋，不过一路顺下来思路还是很清晰的，引入了gin有种思路被打断了的感觉。</div>2023-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/45/62/3c6041e7.jpg" width="30px"><span>木小柒</span> 👍（2） 💬（1）<div>DefaultQueryXXX 是不是没有实现 形如: foo.com?a=1&amp;b=bar&amp;c[]=bar 中 c 的获取？
我看 默认就支持 c=1&amp;c=2&amp;c=3 能获取到 c 的 slice [1, 2, 3]
但是 c[]=1&amp;c[]=2&amp;c[]=3 是获取不到的，除了自己解析不知道有没有更正常一点的方式</div>2021-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/b7/058276dc.jpg" width="30px"><span>i_chase</span> 👍（1） 💬（0）<div>http.request和response其实没有可扩展的，所以gin没有使用接口吧</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/87/92/9ac4c335.jpg" width="30px"><span>🌿</span> 👍（1） 💬（0）<div>hade_request.go,hade_response.go,hade_context.go；类型、结构体、方法等命名可采用Object-C的前缀命名规则</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/e7/fb/146d0556.jpg" width="30px"><span>一苇以航</span> 👍（0） 💬（1）<div>?       github.com&#47;gohade&#47;hade&#47;framework&#47;gin&#47;internal&#47;json      [no test files]
        E:&#47;jikeshijian&#47;xuboyu-hade&#47;framework&#47;gin&#47;gin_integration_test.go:220 +0x9a
created by github.com&#47;gohade&#47;hade&#47;framework&#47;gin.TestFileDescriptor in goroutine 223
        E:&#47;jikeshijian&#47;xuboyu-hade&#47;framework&#47;gin&#47;gin_integration_test.go:218 +0x210   怎么解决？
</div>2024-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/55/2f4055f6.jpg" width="30px"><span>void</span> 👍（0） 💬（0）<div>这节的代码并没有把 IRequest 接口的方法都实现呀</div>2021-11-12</li><br/>
</ul>