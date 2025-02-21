你好，我是陈东。

在搜索引擎的检索结果中，排在前面几页的检索结果往往质量更好，更符合我们的要求。一般来说，这些高质量检索结果的排名越靠前，这个搜索引擎的用户体验也就越好。可以说，检索结果的排序是否合理，往往决定了一个检索系统的质量。

所以，在搜索引擎这样的大规模检索系统中，排序是非常核心的一个环节。简单来说，排序就是搜索引擎对符合用户要求的检索结果进行打分，选出得分最高的K个检索结果的过程。这个过程也叫作Top K检索。

今天，我就和你仔细来聊一聊，搜索引擎在Top K检索中，是如何进行打分排序的。

## 经典的TF-IDF算法是什么？

在搜索引擎的应用场景中，检索结果文档和用户输入的查询词之间的相关性越强，网页排名就越靠前。所以，在搜索引擎对检索结果的打分中，查询词和结果文档的相关性是一个非常重要的判断因子。

那要计算相关性，就必须要提到经典的TF-IDF算法了，它能很好地表示一个词在一个文档中的权重。TF-IDF算法的公式是：**相关性= TF`*`IDF**。其中，TF是**词频**（Term Frequency），IDF是**逆文档频率**（Inverse Document Frequency）。

在利用TF-IDF算法计算相关性之前，我们还要理解几个重要概念，分别是词频、文档频率和逆文档频率。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="" width="30px"><span>INFRA_1</span> 👍（25） 💬（4）<div>老师是否typo，使用堆排序的最终时间复杂度应该是nlogk吧</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（11） 💬（6）<div>请教老师一个面试题相关的top k问题，100 GB 的 URL 文件，进程中使用最多 1 GB 内存，计算出现次数 Top 100 的 URL 和各自的出现次数，性能越快越好。我现在的想法是把大文件依次读取url求哈希，分为100个小文件。小文件多线程统计个数后，构建一个100大小的大顶堆。最后把100个大顶堆，再够成一个100大小的小顶堆。</div>2021-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（9） 💬（4）<div>太难了，跟不上了，每次看到一堆公式里面的各种符号都是很排斥然后就放弃了阅读。。。数学果然是分水岭</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（6） 💬（1）<div>我怎么感觉是构建训练集标注数据最耗时呢😂😂😂。
正经点，我觉得打分不应该是在查询的时候实时算，每个词项的分数应该以一定的频率更新，毕竟只要文档基数上来了，加些文档，词项的分数影响不大。还有就是老师这里说的是查询项包含多个词项，然后用多个词项的分数代表文档分数，但这前提条件是词项是and且同比重，如果是or啥的，好了我不想了我头大。感觉老师这块打分排序整体上的逻辑没有和之前的搜索串连上，让我有种脱节的感觉。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/62/24/07e2507c.jpg" width="30px"><span>托尼斯威特</span> 👍（3） 💬（2）<div>老师你好, 能否重新阐述一下打分是什么时候起作用的? 
根据前几节的内容, 如果我搜索&quot;极客 时间 检索 技术&quot;, 它会被拆分成4个token, 返回4个 posting list, 然后作多路归并, 得到同时含有4个token 的doc id列表. 

4个token在每个doc 里的 TF 都不一样, 每个token的IDF也不一样, 最后怎么影响 搜索结果的排序? </div>2021-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9d/8a/a2d34896.jpg" width="30px"><span>一元(eudict)</span> 👍（3） 💬（3）<div>老师你好，我有一个问题想请教，log(10)为什么等于1呢？不应该是lg(10)才等于1吗？仅仅log(10)并未标明底数呀？其实在前面的表示时间复杂度上就有此疑问，但后面想想时间复杂度仅仅是表示的变化趋势并不是具体的值也就能说通了。但这儿确实有些不解</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/3f/6f62f982.jpg" width="30px"><span>wangkx</span> 👍（2） 💬（1）<div>使用堆排序替换全排后，打分应该是最耗时的。个人感觉是打分的计算过程复杂，涉及到较多的特殊运算。现代一般的CPU面向的不是纯“算数”了，在当前大数据环境下，大量的纯数据计算需要使用对“算数”优化过的GPU来提高计算速度，还有就是把大量单一的数据运算变为矩阵运算（并行），也会显著提高数据的运算速度。

之前读过一些资料，机器学习不同于以往的编程，它是一种逆向思维--使用数据来编程；看到不少资料都把深度学习称为「用数据编程」，这是一种更高级的编程，也是未来新一代程序员需要掌握的方法。

在深度学习中，理论上我们不需要关注从A-&gt;B的推理逻辑，只要有标签化的数据，通过深度学习就能找到从A-&gt;B的计算模型。也就是说，机器学习适用性会更好，代价就是训练数据需要花费很多的时间。

一点点感悟，不知道自己理解的对不对。

</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（2） 💬（1）<div>有两个疑惑的地方，请教下老师。
1.文档频率df，随着文档数量的增多，df应该会重新计算么？如果是需要重新计算，也需要批量更新所有文档的分数吧？
2.机器学习计算分数，随着数量量增大，模型会越来越准确。此时是否需要对于之前已经算过分数的文档重新计算分数呢？</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/d3/2aa0177f.jpg" width="30px"><span>paulhaoyi</span> 👍（1） 💬（2）<div>关于问题2，机器学习打分，不只是可以考虑内容和检索词本身吧？还可以考虑用户，甚至环境，上下问，这里，是不是可以近似一个推荐逻辑了？感觉检索和推荐有点像EE问题的两端，一个倾向于精确些，一个倾向于扩展些？</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（1） 💬（2）<div>问题1，耗时的是打分，尤其是引入了深度学习的计算量大大超过了排序。
问题2，个人觉得机器学习打分的一个不可忽视的优点，那就是它会根据用户行为不断进行学习，不断优化自己，从而获得更好的用户体验。暂时没有使用过，老师可以后面举一个机器学习打分的具体算法和例子吗，机器学习毕竟有些笼统。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（0） 💬（1）<div>我觉得Top K 检索的过程的打分和排序，需要考虑数据量的大小和打分的规则综合考虑。</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（0） 💬（1）<div>第一个tfidf怎么算的？文档一不是10*10+10*1=110，文档二不是1*10+100*1=110吗？</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（0） 💬（2）<div>1.tf-idf和BM25现在可以用来做召回
2.在利用机器学习排序的时代，tdidf和BM25可以作为一个排序因子</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/95/4d/9ad560a8.jpg" width="30px"><span>代码诗人</span> 👍（0） 💬（0）<div>“在给所有的文档打完分以后，接下来，我们就要完成排序的工作了”
排序之前需要把一条倒排链上的所有doc都进行打分么？如果是热词，这个链可能会非常非常长，这里有什么优化方法么？预排序加截断么，可能会丢失结果</div>2024-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/33/bcf37f50.jpg" width="30px"><span>阿甘</span> 👍（0） 💬（0）<div>老师请教一下，像广告推荐很多时候打分排序是在检索的时候实时计算的，也是耗时最大的操作。对于搜索引擎，会不会也有这种情况？还是都是在构建索引的时候就打好分了？</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/3b/47d832f4.jpg" width="30px"><span>书豪</span> 👍（0） 💬（0）<div>bm25算法 我要设置一个阈值怎么设置 比如我要把70%相似度以上的找出来</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/3b/47d832f4.jpg" width="30px"><span>书豪</span> 👍（0） 💬（0）<div>老师，bm25算法是否可以老师，如果采用bm25算法计算相关性得分，那么能否根据最后计算的相关性数值，设定阈值来筛选相关文章呢？比如我用TFIDF向量计算文章余弦相似度，阈值大于0.7认为两篇文章相似是没问题的。但是bm25算法好像不能很好地设定一个阈值，来判定是否相似。有没有比较好的方式呢？</div>2021-11-25</li><br/>
</ul>