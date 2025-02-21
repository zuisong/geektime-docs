你好，我是黄鸿波。

在前面的课程中，我们讲解了几种不同的召回算法，在这节课中我们会继续前面的课程，学习一个新的召回算法——YouTubeDNN模型。YouTubeDNN模型因为内容比较多，我把它分成了上下两篇，我们这节课先聚焦YouTubeDNN模型的概念和召回原理，在下节课实现一个基于YouTubeDNN的召回。

## **YouTubeDNN模型的概念及结构**

上一节课中说到比较经典的U2I模型有两种，一种是DSSM，另一种就是这节课要讲解的基于YouTubeDNN的召回模型。

YoutubeDNN是Youtube用于做视频推荐的落地模型，可以说是最近几年来推荐系统中的经典模型。其大体思路就是召回阶段使用多个简单的模型来进行筛选，这样可以大量地筛除相关度较低的内容，而排序阶段则是使用相对复杂的模型来获得精准的推荐结果。因此，YouTubeDNN实际上包含了两个部分：召回和排序。这里我们主要讲解YouTubeDNN模型中的召回部分。

YouTubeDNN模型的召回主要是完成候选视频的快速筛选（在论文中被称为 Candidate Generation Model），也就是候选集的生成模型。在这一部分中，模型要做的就是将整个YouTube数据库中的视频数量由百万级别降到数百级别。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>YoutubeDNN是运行在网站后端吧，其运行需要很多机器资源吗？</div>2023-06-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIUXWqIBiadT4H3XvpcLeOkeocfmpInuhCoHviaUrX7B0N8wnOicnqHZeicKg1SlLk070EFRya1RPQIicw/132" width="30px"><span>爱极客</span> 👍（0） 💬（1）<div>老师，这节课的理论，后面会有使用案例吗？</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2c/bc/5311e976.jpg" width="30px"><span>Emma</span> 👍（0） 💬（0）<div>“没有曝光过的内容理论上有可能被点击过”老师这个怎么理解呢？为什么没有曝光过的内容会被点击过呢</div>2024-09-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIUXWqIBiadT4H3XvpcLeOkeocfmpInuhCoHviaUrX7B0N8wnOicnqHZeicKg1SlLk070EFRya1RPQIicw/132" width="30px"><span>爱极客</span> 👍（0） 💬（0）<div>&quot;作者将用户看完的内容作为正样本，再从视频库里随机选取一些样本作为负样本&quot;。请问老师，这里的“正样本”是指代-&gt; “样本来自全部观看记录，也就是说，观看记录包括用户被推荐的内容，再加上用户自己搜索或者在其他地方点击的内容” 吗？</div>2024-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/ba/42/5ca553bd.jpg" width="30px"><span>Weitzenböck</span> 👍（0） 💬（0）<div>example age也是个不很错的Trick，因为用户更偏爱观看比较新的视频。</div>2024-02-23</li><br/>
</ul>