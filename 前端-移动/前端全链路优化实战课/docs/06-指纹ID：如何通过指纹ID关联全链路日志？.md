你好，我是三桥。

在之前的课程当中，我们设计了一套基于最少字段原则的全链路日志模型。你还记得数据模型中提到的fpId字段吗？

对，它就是指纹ID。在我们深入探讨指纹ID之前，先来看看前端同学在实际项目遇到的一种情况。这次，我们以极客时间的网站为例。

通常，一个Web网站总会有陌生的访客通过浏览器访问。我注意到极客官网会对陌生访客自动弹出一个提供双方意向匹配度的产品功能，给用户推荐合适的内容。

![图片](https://static001.geekbang.org/resource/image/11/03/1160479530cb678897632c70cdf36b03.png?wh=1284x1330)

咱们来看看这个业务场景，用户在选好信息选项后，直接提交并跳转至登录页面。登录成功后，页面会自动跳转至个人主页。

我们假设，你进入个人中心页面时发现很多地方都是空白的，没任何数据显示，包括推荐购买课程的列表。

在这种情况下，我们的前端同学只能针对发生这个问题的用户检查接口是否存在问题。虽然检查结果显示接口没有问题，但我们还是无法追踪用户登录前的流程状态，因为我们无法关联任何未登录用户的交互日志。

想一下，如果我们能在用户访问我们的服务时提供有一个唯一的标识，并将这个标识和用户的行为日志关联起来，那么是不是无论用户是否登录，我们都可以追踪到用户的行为轨迹了？

## 指纹ID

我们每个人的指纹都是独一无二的，浏览器指纹也是同样道理。由于浏览器提供了很多有价值的特性给前端同学通过代码获取，例如UserAgent、分辨率、色彩深度、系统平台、语言、触摸屏、地理位置、语言支持特性、图像特性等等。**所以，我们只要收集这些具有较高辨析度的信息，并进行一定的计算处理，就能生成一个能唯一标识当前浏览器的值，也就是我们所说的指纹ID。**
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/86/73/5190bbde.jpg" width="30px"><span>苏果果</span> 👍（0） 💬（0）<div>06源码：
https:&#47;&#47;github.com&#47;sankyutang&#47;fontend-trace-geekbang-course&#47;blob&#47;main&#47;trace-sdk&#47;src&#47;core&#47;fingerprint.ts

完整源码入口：
https:&#47;&#47;github.com&#47;sankyutang&#47;fontend-trace-geekbang-course</div>2024-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e4/c9/651c54a7.jpg" width="30px"><span>嘿~那个谁</span> 👍（0） 💬（1）<div>课程中的内容没有课间和源码吗？</div>2024-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/49/2f/590142fb.jpg" width="30px"><span>JuneRain</span> 👍（0） 💬（5）<div>没太理解这个指纹ID为什么要利用 canvas 来生成，直接利用指定字符串 &quot;geekbang&quot; 然后转成 base64 格式再截取不也一样的效果？</div>2024-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（0） 💬（5）<div>有了指纹ID，还需要 traceId 吗？</div>2024-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（1） 💬（0）<div>同一个型号的手机加同一个版本的浏览器生成出来的画布也会不同么？</div>2024-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/85/7e/dc5ee66c.jpg" width="30px"><span>天天</span> 👍（0） 💬（0）<div>canvas这个原理确实没讲清楚，我猜就算是同一个型号的手机，同个版本的浏览器，用canvas画一个图案出来也不一样</div>2024-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/09/afbc9616.jpg" width="30px"><span>雪舞</span> 👍（0） 💬（1）<div>bin2hex 这个是自定义函数吗？作用是干嘛的？函数定义是怎样的？</div>2024-05-17</li><br/>
</ul>