你好，我是徐文浩。

前面我们已经学完了文本和音频的部分。接下来，我们就要进入课程的最后一部分，也就是图像模块了。

与视觉和语音一样，Transformer架构的模型在过去几年里也逐渐成为了图像领域的一个主流研究方向。自然，发表了GPT和Whisper的OpenAI也不会落后。一贯相信“大力出奇迹”的OpenAI，就拿4亿张互联网上找到的图片，以及图片对应的ALT文字训练了一个叫做CLIP的多模态模型。今天，我们就看看在实际的应用里怎么使用这个模型。在学习的过程中你会发现，**我们不仅可以把它拿来做常见的图片分类、目标检测，也能够用来优化业务场景里面的商品搜索和内容推荐。**

## 多模态的CLIP模型

相信你最近已经听到过很多次“多模态”这个词儿了，无论是在OpenAI对GPT-4的介绍里，还是我们在之前介绍llama-index的时候，这个名词都已经出现过了。

**所谓“多模态”，就是多种媒体形式的内容。**我们看到很多评测里面都拿GPT模型来做数学试题，那么如果我们遇到一个平面几何题的话，光有题目的文字信息是不够的，还需要把对应的图形一并提供给AI才可以。而这也是我们通往通用人工智能的必经之路，因为真实世界就是多模态的。我们每天除了处理文本信息，还会看视频、图片以及和人说话。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/55/36/791d0f5e.jpg" width="30px"><span>pomyin</span> 👍（1） 💬（2）<div>商品搜索与以图搜图部分，其中search函数部分代码有误（ training_split[i][&quot;image&quot;] ），我查了huggingface的Dataset数据类型，应该改成：training_split.select([i])[&quot;image&quot;]。我的python 3.7，transformers是4.28.1。</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>Q1：笔记本，win10，安装了Anaconda，这个环境可以吗？我安装了Pycharm。应该是Pycharm用来编写代码，Anaconda提供底层支持，是这样吗？
Q2：用某个人的声音来播音或者阅读一段文字，有成熟的方案吗？
比如，想用特朗普的声音来播报一段新闻，或者读一篇文章，是否有成熟的方案？开源或商用的都可以。</div>2023-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/21/14/423a821f.jpg" width="30px"><span>Steven</span> 👍（1） 💬（1）<div>目标检测部分，我的 transformers 版本是 4.24.0，文中代码执行异常，修改成下面的代码得到结果：
detected = detector(&quot;.&#47;data&#47;cat.jpg&quot;,
    text_queries=[&quot;cat&quot;, &quot;dog&quot;, &quot;truck&quot;, &quot;couch&quot;, &quot;remote&quot;])[0]
</div>2023-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（0） 💬（1）<div>调用了几个模型对图片进行零样本分类，试验图像使用的是本课中的&#39;两只猫咪&#39;，为便于模型间的比较，取完全相同的分类参数: candidate_labels=[&quot;cat&quot;, &quot;dog&quot;, &quot;truck&quot;, &quot;couch&quot;, &quot;remote&quot;]。

模型1: task=&quot;zero-shot-image-classification&quot;, model=&quot;openai&#47;clip-vit-large-patch14&quot;
模型2: task=&quot;zero-shot-image-classification&quot;, model=&quot;laion&#47;CLIP-ViT-H-14-laion2B-s32B-b79K&quot;
模型3: task=&quot;zero-shot-classification&quot;, model=&quot;typeform&#47;distilbert-base-uncased-mnli&quot;
模型4: task=&quot;zero-shot-classification&quot;, model=&quot;MoritzLaurer&#47;mDeBERTa-v3-base-mnli-xnli&quot;

下面是各个模型运算的结果:

model             cat          dog         truck        couch       remote
1              15.03%      0.02%      0.01%      78.11%      6.82% 
2              15.04%      0.00%      0.00%      84.95%      0.01%
3              13.22%     11.75%    18.13%      36.99%     19.90%
4              18.52%     16.02%    13.60%      24.22%     27.64%

这几个模型的结果都不如 task=&quot;zero-shot-object-detection&quot;, model=&quot;google&#47;owlvit-base-patch32&quot;
谷歌这个模型的优点是从图中分辨出两只猫和两个遥控器。

最后是一个中文模型，model_id=&quot;lyua1225&#47;clip-huge-zh-75k-steps-bs4096&quot;
https:&#47;&#47;huggingface.co&#47;models?pipeline_tag=zero-shot-image-classification&amp;language=zh&amp;sort=downloads

[&quot;猫&quot;,    &quot;狗&quot;,   &quot;拖车&quot;,   &quot;长沙发&quot;,  &quot;遥控器&quot;]
[0.996     0.       0.          0.004          0.   ]

没有识别出遥控器。</div>2023-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（1） 💬（0）<div>老师，文本向量搜素图片那里下面这段代码是报错的
results = [ {&quot;image&quot;: training_split[i][&quot;image&quot;], &quot;distance&quot;: distances[0][j]} for j, i in enumerate(indices[0]) ]

我试了图片搜素图片结果发现可以就把那段代码拿过来发现文本搜素图片产品对了
 results = [  
      {&quot;image&quot;: training_split[i.item()][&quot;image&quot;], &quot;distance&quot;: distances[0][j]} 
        for j, i in enumerate(indices[0])
    ]
这段代码就可以了</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（0） 💬（0）<div>文本向量搜素商品时
 results = [  
      {&quot;image&quot;: training_split[i][&quot;image&quot;], &quot;distance&quot;: distances[0][int(j)]} 
        for j, i in enumerate(indices[0])
    ]
这段代码报错：
TypeError: Wrong key type: &#39;1461&#39; of type &#39;&lt;class &#39;numpy.int64&#39;&gt;&#39;. Expected one of int, slice, range, str or Iterable.
请问大家有什么方案吗，搜了gpt也没有给解决方案
</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/8c/a5/0229d33f.jpg" width="30px"><span>Tang</span> 👍（0） 💬（0）<div>徐老师你好，我测试了下猫狗图片的目标检测，结果猫和狗都检测成了狗</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/91/51/3da9420d.jpg" width="30px"><span>糖糖丸</span> 👍（0） 💬（0）<div>请问要运行可生产使用的CLIP模型，大概需要怎么样的机器配置（主要指显卡）呢？
另外不知道图片搜索的响应时间大概在什么量级？ 是100ms级别，还是10s级别的？</div>2023-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/20/78/ea35cd99.jpg" width="30px"><span>新田小飞猪</span> 👍（0） 💬（0）<div>老师好，有没有对计算机音频&#47;音乐处理相关的深度学习资料的推荐啊</div>2023-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/82/5b/df97e03c.jpg" width="30px"><span>Santiago</span> 👍（0） 💬（0）<div>欢度五一</div>2023-04-28</li><br/>
</ul>