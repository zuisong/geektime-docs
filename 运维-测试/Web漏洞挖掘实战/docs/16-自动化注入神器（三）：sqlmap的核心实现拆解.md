你好，我是王昊天。

在上节课，我们学习了sqlmap中一个非常重要的函数——start函数。我们了解到，它既可以为每个目标配置请求参数，也会对目标进行一些必要的检测，例如判断目标是否存在waf的保护等。

在讲到如何检测waf时，我们遇到了一个比较陌生的概念，页面相似度。上节课，我给出了一个简单的示例，来帮助你理解它的含义，但是并没有告诉你，页面相似度是如何计算出来的。相信经过这节课的学习，你就可以解决这个问题。

## 再看checkWaf函数

**为了研究页面相似度算法，我们首先需要找到计算页面相似度的代码。**回顾一下上节课的内容，我们在checkwaf函数中学习了页面相似度的概念，但是并未深入研究这一点。现在让我们回到sqlmap的checkWaf函数，着重观察下面这段代码。在这段代码中，系统会判断Request.queryPage函数的返回值是否小于sqlmap设定的默认页面相似度阈值（IPS\_WAF\_CHECK\_RATIO），如果小于，那么就认为存在waf，否则就会认为不存在waf。我们可以从`lib.core.settings.py`中得出该阈值的大小为 0.5。

```python
try:
    retVal = (Request.queryPage(place=place, value=value, getRatioValue=True, noteResponseTime=False, silent=True, raise404=False, disableTampering=True)[1] or 0) < IPS_WAF_CHECK_RATIO
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/4e/fd/4e8c9743.jpg" width="30px"><span>clay</span> 👍（1） 💬（0）<div>对WAF的检测可以搜集一些国内外WAF的常见特征吧，比如长亭雷池、安全狗、FortiWeb等，这些响应包里都会有强特征</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-03-15</li><br/>
</ul>