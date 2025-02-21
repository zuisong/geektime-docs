你好，我是南柯。

前面我们已经学习了DALL-E 2、Imagen、DeepFloyd、SDXL这些AI绘画的明星模型。这一讲我们就一起来探讨Midjourney，它是当下公认的AI绘画最强模型。

在[第3讲](https://time.geekbang.org/column/article/676927)，我们便已领略过Midjourney的文生图、图像融合和垫图生成能力。从22年11月的Midjourney v4、Nijijourney，到今年3月的Midjourney v5，MJ凭借其高质量的生成效果、30美元一个月的付费服务，实现了非常可观的收入。因此，训练出对标Midjourney的模型也成为了很多大企业追求的目标。

在我写这一讲内容的时候，Midjourney背后的技术并没有公开。今天这一讲，我们不妨一起猜猜看，Midjourney这个AI绘画圈子里最值钱的“技术方案”是怎样的。

特别提示一下，我们这一讲的分析会涉及很多进阶篇的背景知识，比如DALL-E 2、Imagen、SD模型背后的技术原理等，推荐你课前进行温习。

## 回顾Midjourney的发展

不知道你是否思考过这个问题：做一个Midjourney这样的产品，需要多少人？

国内的互联网公司可以轻松投入数百人去做类似的项目。实际上呢，在Midjourney v4发布的时期，这个公司只有不到20名全职员工。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/14/45/adf079ae.jpg" width="30px"><span>杨松</span> 👍（0） 💬（2）<div>老师，请教下midjourney可以实现图生图吗？如果可以的话，是不是质量会比sd要好些？
</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/e4/7bbec200.jpg" width="30px"><span>董义</span> 👍（0） 💬（1）<div>很有意思,南柯老师思路清晰,娓娓道来,个中原理理解深刻,厉害厉害.</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（1） 💬（0）<div>老师真是锐智、思路清晰，分析的有理有据。</div>2023-10-26</li><br/>
</ul>