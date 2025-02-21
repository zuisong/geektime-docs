你好，我是黄佳。

大语言模型不仅可以生成文本摘要，还可以读取数据、做出直观的可视化，并生成有意义的见解。这种见解，是任何传统计算机程序所无法给出的，在大语言模型出现之前，也只有人类能够做出。

今天，我们要探索如何利用OpenAI的大语言模型完成一个有趣的商业案例：分析畅销歌曲数据，生成行业报告并创建PPT。我们将经历从原始数据到精美PPT的全过程，体验大语言模型的强大能力。

## 项目目标：流行音乐趋势分析

先来看看这份从Spotify App中搜集来的，播放量最多的流行音乐数据表。

![图片](https://static001.geekbang.org/resource/image/2b/17/2b4d698fc7dbac58152c77f46d6ded17.png?wh=3140x1163)

这些属性从多个角度刻画了流行音乐的特点，包括其发行时间、在各大平台的表现、音乐特性等。

假设我们是一家名为“鸟语乐境”的流行音乐分享平台，我们需要通过分析这些数据来洞察当下流行音乐的趋势，了解大众的音乐品味。同时，这些信息对于音乐制作人、歌手和音乐平台也有重要的参考价值，有助于他们创作和推荐符合市场需求的音乐作品。

我们将让AI来帮我们梳理数据，生成图片，以及基于数据生成观点和简介，最后自动创建生成较为靠谱的PPT。

![图片](https://static001.geekbang.org/resource/image/ba/87/ba41f8a68bdfd278e83402c08f502487.png?wh=1345x545)

## 项目整体流程

这个数据分享项目的整体流程如下图所示，在这个过程中，最主要的环节，都将由AI完成。

![图片](https://static001.geekbang.org/resource/image/f8/27/f8aabee1112ef87fb0e5f58145f2e227.jpg?wh=882x887)

这个项目的核心环节是OpenAI的Assistant替我们生成数据可视化，以及在数据中寻找和挖掘趋势和洞见。整个过程，我们只需要通过提示词来对Assistant进行一些小小的引导和启发即可。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLFvhaPbJ1sBZqr8GQRVDiaxsicukAETVzjqmBRba2WqibbmX3NmoPIkaNEnBvyaWobyCjGN0FJgGnKQ/132" width="30px"><span>Geek_9948a5</span> 👍（0） 💬（0）<div>这里的Assiatants生成了我们制作PPT的素材 1.图片 2.观点摘要。最后我们使用了python工具组装了这些材料。如果第三部能自动完成就好了</div>2024-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（0）<div>在数据可视化环节，感觉Assistants已经完全代替了langchain agent，不知道Assistant会不会成为各家大模型的标配。</div>2024-06-26</li><br/>
</ul>