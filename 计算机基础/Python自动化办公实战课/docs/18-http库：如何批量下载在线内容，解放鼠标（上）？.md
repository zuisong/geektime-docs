你好，我是尹会生。

我在前段时间遇到了下载大量图片的需求。具体来说，是在我训练AI识别猫时，必须要在电脑中存储大量猫的图片。但搜索到的图片都在网页中，我就需要先把它们一个个手动下载下来，再保存，然后才能进行后续的工作。

而且，随着我对AI训练工作的日益增多，这类需求会越来越丰富，我不仅要下载猫的图片，还要下载大量其他各种动物的图片。相信类似这种批量下载网页中的图片的需求，你在工作中会经常遇到。而这类需求，刚好能够使用Python的“requests-html”库实现批量下载，提高我们的工作效率。

因此呢，这节课我就以搜索到的猫的图片为例，给你讲解一下，我是怎么来批量下载图片的。

## 批量下载图片的准备工作

我把实现图片自动化批量下载的过程，拆分成四段难度逐渐递增的代码。这四段代码分别实现的是以下四个功能：

1. 访问HTTP服务器，得到搜索结果的整个网页；
2. 在访问服务器之后下载一张图片；
3. 找到多张图片的相似地址；
4. 提取相似地址，下载多张图片。

前两个功能，是批量下载图片的准备工作和前提。掌握了这两个功能，那么批量下载图片实现起来就容易多了。所以接下来，我们先来学习这两项准备工作。

### 访问HTTP服务端的资源

我们从难度最低的一段代码开始，怎么通过访问HTTP服务器，从而得到猫的搜索结果的整个网页。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1K4cjPHHvHhKia7fHTt3GkoOG0xCWm8k9uh7CjSKRIMJIL7vWOwXD8eNGV43w9vlia74cEdrStHbJrQNUjwbH2pQ/132" width="30px"><span>Geek_a1056f</span> 👍（1） 💬（1）<div>老师，这个爬虫有什么区别吗</div>2023-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b3/b6/ac302d89.jpg" width="30px"><span>36度道</span> 👍（1） 💬（1）<div>requests-html库和requests库之间有什么区别吗？</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/bf/b5/052ba282.jpg" width="30px"><span>星辰</span> 👍（0） 💬（1）<div>通过百度图片搜索批量下载有完整代码吗？</div>2021-12-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo7TMNJeTq63vLeKJXPPDS3shGa52wdBOFoO7boSkw3yEOdKvBMF1JG6xbIcnhw4bWyT0JCUYO74w/132" width="30px"><span>Len</span> 👍（0） 💬（1）<div>凄凄切切</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/fe/be/5cb1ddca.jpg" width="30px"><span>小行迹</span> 👍（0） 💬（0）<div>请问get_picID_from_url()这个函数是如何实现的？</div>2025-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4c/b5/fcede1a9.jpg" width="30px"><span>IT小村</span> 👍（0） 💬（0）<div>Python的beatiful soup更胜一筹</div>2022-06-01</li><br/>
</ul>