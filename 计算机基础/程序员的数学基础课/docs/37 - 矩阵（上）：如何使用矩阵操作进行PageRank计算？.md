你好，我是黄申。今天我来说说矩阵。

前面我说过，矩阵由多个长度相等的向量组成，其中的每列或者每行就是一个向量。从数据结构的角度来看，我们可以把向量看作一维数组，把矩阵看作二维数组。

具有了二维数组的特性，矩阵就可以表达二元关系了，例如图中结点的邻接关系，或者是用户对物品的评分关系。而通过矩阵上的各种运算操作，我们就可以挖掘这些二元关系，在不同的应用场景下达到不同的目的。今天我就从图的邻接矩阵出发，展示如何使用矩阵计算来实现PageRank算法。

## 回顾PageRank链接分析算法

在讲马尔科夫模型的时候，我已经介绍了PageRank链接分析算法。所以，在展示这个算法和矩阵操作的关系之前，我们快速回顾一下它的核心思想。

PageRank是基于马尔科夫链的。它假设了一个“随机冲浪者”模型，冲浪者从某张网页出发，根据Web图中的链接关系随机访问。在每个步骤中，冲浪者都会从当前网页的链出网页中，随机选取一张作为下一步访问的目标。此外，PageRank还引入了随机的跳转操作，这意味着冲浪者不是按Web图的拓扑结构走下去，只是随机挑选了一张网页进行跳转。

基于之前的假设，PageRank的公式定义如下：

![](https://static001.geekbang.org/resource/image/55/6d/553f1e841d71ac34db7161cb9974e56d.png?wh=490%2A126)

其中，$p\_{i}$表示第$i$张网页，$M\_{i}$是$p\_{i}$的入链接集合，$p\_{j}$是$M\_{i}$集合中的第$j$张网页。$PR\_{(p\_{j})}$表示网页$p\_{j}$的PageRank得分，$L\_{(p\_{j})}$表示网页$p\_{j}$的出链接数量，$\\frac{1}{L\_{(p\_{j})}}$就表示从网页$p\_{j}$跳转到$p\_{i}$的概率。$α$是用户不进行随机跳转的概率，$N$表示所有网页的数量。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/ce/27fe1845.jpg" width="30px"><span>晨曦后浪</span> 👍（8） 💬（1）<div>使用networkx中的pagerank函数,计算出来的数值和直接基于矩阵计算出来的数值有一点点差别,但相对大小还是一样的

import networkx as nx
import matplotlib.pyplot as plt

# 创建有向图
G = nx.DiGraph()
# 添加带权重有向边
G.add_weighted_edges_from([(1, 3, 1), (2, 1, 1), (2, 3, 1), (3, 1, 1), (5, 2, 1)])
# 添加孤立节点
G.add_node(4)
# 计算pagerank值
pagerank_list = nx.pagerank(G, alpha=0.85)
print(&quot;pagerank 值是：&quot;, pagerank_list)

nx.draw(G, with_labels=True, font_weight=&#39;bold&#39;)
plt.show()


pagerank 值是： {1: 0.43042160902192195, 3: 0.43042160902192195, 2: 0.06686758646711714, 5: 0.03614459774451953, 4: 0.03614459774451953}</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/d0/49b06424.jpg" width="30px"><span>qinggeouye</span> 👍（5） 💬（1）<div>思考题
https:&#47;&#47;github.com&#47;qinggeouye&#47;GeekTime&#47;blob&#47;master&#47;MathematicProgrammer&#47;37_Matrix2PageRank&#47;lesson37_1.py

        # 计算前后两次的 PageRank 数值的误差，判断是否需要结束迭代
        delta = list(map(abs, (pr&#47;pr_tmp)))  # pr_tmp 是前一次的值
        delta = abs(np.max(delta) - 1)  # 最大误差的百分比
        if delta &lt;= delta_threshold:
            return pr
        else:
            continue

经计算，示例最大循环 6 次，迭代结束。
round 6 [[0.46010028 0.03905229 0.46010028 0.02037357 0.02037357]]</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（4） 💬（1）<div>茶艺师学编程

可惜我目前还没有能力去跑代码。

但整篇课文消化下来，pagerank这么复杂的函数，用矩阵“嵌套”两层就搞定了……体会到矩阵工具的强大。</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（1） 💬（1）<div>以上两个公式在形式上是基本一致的。。。怎么看出是一致的？简化公式和矩阵点乘公式</div>2020-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（10） 💬（0）<div>一直想搞明白pagerank的计算流程，这节课真值</div>2019-03-11</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（3） 💬（1）<div>邻接矩阵的行表示每个节点出边，列表示每个节点的入边。行做归一化是为了出边平均分配权重，矩阵的乘法恰好按照入边累加pr值。
随机跳转还是线性关系，依然可以用矩阵处理，这里用到矩阵分块思想。</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/fa/266bcb89.jpg" width="30px"><span>等待</span> 👍（2） 💬（1）<div>pagerank的时间复杂度是O( r * n^ 2)，其中，r是指迭代次数。
当数据量达到一定的程度的时候，network联图的建立都无法完成的时候，我们应该如何处理呢？
这里的大数据量大概是300万条数据的样子。谢谢</div>2020-04-01</li><br/><li><img src="" width="30px"><span>Geek_3e9d7d</span> 👍（0） 💬（0）<div>思考题：
for i in range(0, 20):
  pre_pr = pr
  pr = np.dot(pr, adj)

  pr_jump = np.full([N,2], [[0, 1&#47;N]])
  pr_jump[:, :-1] = pr.transpose()

  pr = np.dot(pr_jump, jump)

  pr = pr.transpose()
  pr = pr &#47; pr.sum()

  print(&quot;rount&quot;, i+1, pr)
  
  diff = np.mean(np.abs(pr - pre_pr))
  if diff &lt; 0.000001:
    break</div>2024-04-07</li><br/><li><img src="" width="30px"><span>013923</span> 👍（0） 💬（0）<div>Never too old to learn!</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（0） 💬（0）<div>思考题：
我尝试改了一下老师的代码，把迭代结束条件改为计算前后两次PageRank向量的差的平均值是否小于指定精度，发现这个迭代过程收敛很快，只用了7轮循环就结束了，程序部分代码如下，不当之处请老师指正：
# 采样迭代方式，判断前后两次PageRank向量的差的平均值是否小于指定精度。
pricision = 1e-9 # 设置计算精度
last_pr = None
i = 0
while True:
    # 进行点乘，计算Σ(PR(pj)&#47;L(pj))
    pr = np.dot(pr, adj)

    # 转置保存Σ(PR(pj)&#47;L(pj))结果的矩阵，并增加长度为N的列向量，其中每个元素的值为1&#47;N，便于下一步的点乘。
    pr_jump = np.full([N, 2], [[0, 1&#47;N]])
    
    pr_jump[:,:-1] = pr.transpose() 

    # 进行点乘，计算α(Σ(PR(pj)&#47;L(pj))) + (1-α)&#47;N)
    pr = np.dot(pr_jump, jump)

    # 归一化PageRank得分，由于计算后pr是列向量，因此需要做转置
    pr = pr.transpose()
    pr = pr &#47; pr.sum()
    
    print(&quot;round&quot;, i + 1, pr)
   
    if last_pr is not None:
        diff = np.average(np.absolute(pr - last_pr))
        if diff &lt;= pricision:
            break
    last_pr = pr.copy()
    i += 1
############程序输出#############
round 1 [[0.37027027 0.24864865 0.37027027 0.00540541 0.00540541]]
round 2 [[0.46740902 0.02498642 0.46740902 0.02009777 0.02009777]]
round 3 [[0.46023676 0.03878962 0.46023676 0.02036842 0.02036842]]
round 4 [[0.46010283 0.03904738 0.46010283 0.02037348 0.02037348]]
round 5 [[0.46010033 0.0390522  0.46010033 0.02037357 0.02037357]]
round 6 [[0.46010028 0.03905229 0.46010028 0.02037357 0.02037357]]
round 7 [[0.46010028 0.03905229 0.46010028 0.02037357 0.02037357]]</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/85/a1/2442332c.jpg" width="30px"><span>郭俊杰</span> 👍（0） 💬（1）<div>#上面的代码中pr变值改为pr_tmp
#==========================
i = 0
errorRate = 0.000001
while (True):
    # 进行点乘，计算Σ(PR(pj)&#47;L(pj))
    pr = np.dot(pr_tmp, adj)

    # 转置保存Σ(PR(pj)&#47;L(pj))结果的矩阵，并增加长度为N的列向量，其中每个元素的值为1&#47;N，便于下一步的点乘。
    pr_jump = np.full([N, 2], [[0, 1 &#47; N]])
    pr_jump[:, :-1] = pr.transpose()

    # 进行点乘，计算α(Σ(PR(pj)&#47;L(pj))) + (1-α)&#47;N)
    pr = np.dot(pr_jump, jump)

    # 归一化PageRank得分
    pr = pr.transpose()
    pr = pr &#47; pr.sum()

    delta = list(map(abs, (pr&#47;pr_tmp)))
    delta = abs(np.max(delta)-1)
    if delta &lt;= errorRate:
        break
    else:
        pr_tmp = pr
        i += 1
        continue

print(&#39;round:&#39;, i)
print(&#39;pr:&#39;, pr)
</div>2020-06-04</li><br/>
</ul>