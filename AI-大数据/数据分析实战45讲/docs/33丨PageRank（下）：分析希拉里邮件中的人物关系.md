上节课我们讲到PageRank算法经常被用到网络关系的分析中，比如在社交网络中计算个人的影响力，计算论文的影响力或者网站的影响力等。

今天我们就来做一个关于PageRank算法的实战，在这之前，你需要思考三个问题：

1. 如何使用工具完成PageRank算法，包括使用工具创建网络图，设置节点、边、权重等，并通过创建好的网络图计算节点的PR值；
2. 对于一个实际的项目，比如希拉里的9306封邮件（工具包中邮件的数量），如何使用PageRank算法挖掘出有影响力的节点，并且绘制网络图；
3. 如何对创建好的网络图进行可视化，如果网络中的节点数较多，如何筛选重要的节点进行可视化，从而得到精简的网络关系图。

## 如何使用工具实现PageRank算法

PageRank算法工具在sklearn中并不存在，我们需要找到新的工具包。实际上有一个关于图论和网络建模的工具叫NetworkX，它是用Python语言开发的工具，内置了常用的图与网络分析算法，可以方便我们进行网络数据分析。

上节课，我举了一个网页权重的例子，假设一共有4个网页A、B、C、D，它们之间的链接信息如图所示：

![](https://static001.geekbang.org/resource/image/47/ea/47e5f21d16b15a98d4a32a73ebd477ea.png?wh=1711%2A1171)  
针对这个例子，我们看下用NetworkX如何计算A、B、C、D四个网页的PR值，具体代码如下：
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（7） 💬（1）<div>pagerank 值是： {&#39;C&#39;: 0.22514635472743896, &#39;A&#39;: 0.3245609358176832, &#39;D&#39;: 0.22514635472743894, &#39;B&#39;: 0.22514635472743896}

import networkx as nx
# 创建有向图
G = nx.DiGraph()
# 有向图之间边的关系
edges = [(&quot;A&quot;, &quot;B&quot;), (&quot;A&quot;, &quot;C&quot;), (&quot;A&quot;, &quot;D&quot;), (&quot;B&quot;, &quot;A&quot;), (&quot;B&quot;, &quot;D&quot;), (&quot;C&quot;, &quot;A&quot;), (&quot;D&quot;, &quot;B&quot;), (&quot;D&quot;, &quot;C&quot;)]
for edge in edges:
    G.add_edge(edge[0], edge[1])
pagerank_list = nx.pagerank(G, alpha=0.85)
print(&quot;pagerank 值是：&quot;, pagerank_list)
</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/83/684361be.jpg" width="30px"><span>永降不息之雨</span> 👍（5） 💬（4）<div>老师关于希拉里邮件的案例，这一段一直看不懂。
我print(temp)只有得到两个人名，
但是我print(edges_weights_temp)后
除了人名，后面还多了一个数字，
老师这数字是怎么来的，这段语法能帮忙解释一下吗？
    temp=(rew[0],row[1])
if temp not in edges_weights_temp:
        edges_weights_temp[temp] = 1
    else:
        edges_weights_temp[temp] = edges_weights_temp[temp] + 1
</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a3/f9/9180d6d1.jpg" width="30px"><span>szm</span> 👍（4） 💬（1）<div>有2个问题：
第一个：pagerank已经是字典类型了，为什么还要用pagerank_list = {node: rank for node, rank in pagerank.items()}将其转换为字典呢？是不是删掉这个语句也没关系？
第二个：阈值大于0.005的图仍有很多重叠在一起，无法观看，请问怎样才能让画出来的图像美观呢？</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e4/4a/63e46022.jpg" width="30px"><span>WS</span> 👍（2） 💬（1）<div>老师，怎么筛选出某个人物的有向图？</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（2） 💬（1）<div>import networkx as nx
# 创建有向图
G = nx.DiGraph()
# 有向图之间边的关系
edges = [(&quot;A&quot;, &quot;B&quot;), (&quot;A&quot;, &quot;C&quot;), (&quot;A&quot;, &quot;D&quot;), (&quot;B&quot;, &quot;A&quot;), (&quot;B&quot;, &quot;D&quot;), (&quot;C&quot;, &quot;A&quot;), (&quot;D&quot;, &quot;B&quot;), (&quot;D&quot;, &quot;C&quot;)]
for edge in edges:
    G.add_edge(edge[0], edge[1])
pagerank_list = nx.pagerank(G) #alpha为阻尼因子，默认值：0.85
print(&quot;pagerank值是：&quot;, pagerank_list)

pagerank值是： {&#39;A&#39;: 0.3245609358176831, &#39;B&#39;: 0.22514635472743894, &#39;C&#39;: 0.22514635472743894, &#39;D&#39;: 0.22514635472743894}</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（2） 💬（1）<div>1、pagerank_list=nx.pagerank(G,alpha=1)理解
参考链接：https:&#47;&#47;networkx.github.io&#47;documentation&#47;networkx-1.10&#47;reference&#47;generated&#47;networkx.algorithms.link_analysis.pagerank_alg.pagerank.html
alpha指的是阻尼因子。根据公式了解到，这因子代表用户按照跳转链接来上网的概率。
题目说15%的概率随机跳转，所以阻尼因子为0.85

2、代码
import networkx as nx
# 创建有向图
G=nx.DiGraph()
# 有向图之间边的关系
edges = [(&quot;A&quot;, &quot;B&quot;), (&quot;A&quot;, &quot;C&quot;), (&quot;A&quot;, &quot;D&quot;), (&quot;B&quot;, &quot;A&quot;), (&quot;B&quot;, &quot;D&quot;), (&quot;C&quot;, &quot;A&quot;), (&quot;D&quot;, &quot;B&quot;), (&quot;D&quot;, &quot;C&quot;)]
for edge in edges:
    G.add_edge(edge[0],edge[1])
pagerank_list=nx.pagerank(G,alpha=0.85)
print(&#39;pagerank 值是: &#39;, pagerank_list)

3、结果
pagerank 值是:  {&#39;A&#39;: 0.3245609358176831, &#39;B&#39;: 0.22514635472743894, &#39;C&#39;: 0.22514635472743894, &#39;D&#39;: 0.22514635472743894}

</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/aa/d1/076482f3.jpg" width="30px"><span>白夜</span> 👍（2） 💬（1）<div>默认阻尼就是0.85，alpha去掉完事、、
pagerank 值是： {&#39;A&#39;: 0.3245609358176831, &#39;B&#39;: 0.22514635472743894, &#39;C&#39;: 0.22514635472743894, &#39;D&#39;: 0.22514635472743894}</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/86/d7/46842f90.jpg" width="30px"><span>小晨</span> 👍（1） 💬（2）<div>#!&#47;usr&#47;bin&#47;env python
# -*- coding:utf-8 -*-
# Author:Peter

import networkx as nx
import matplotlib.pyplot as plt

def show_graph(graph):
    # 使用Sprint Layout布局，类似中心放射状

    positions = nx.spring_layout(graph)
    # 设置网格图中的节点大小，大小与pagerank无关，因为pagerank值很小所以需要*20000
    nodesize = [x[&#39;pagerank&#39;] * 20000 for v , x in graph.nodes(data=True)]
    # 设置网络图中的边长度
    # edgesize = [np.sqrt(e[2][&#39;weight&#39;]) for e in graph.edges(data=True)]
    # 绘制节点
    nx.draw_networkx_nodes(graph , positions , node_size=nodesize , alpha=0.4)
    # 绘制边
    nx.draw_networkx_edges(graph , positions  , alpha=0.2)
    # 绘制节点的 label
    nx.draw_networkx_labels(graph , positions , font_size=10)
    #所有人物关系的关系图
    plt.show()

# 创建有向图
G = nx.DiGraph()
# 有向图之间边的关系
edges = [(&quot;A&quot;, &quot;B&quot;), (&quot;A&quot;, &quot;C&quot;), (&quot;A&quot;, &quot;D&quot;), (&quot;B&quot;, &quot;A&quot;), (&quot;B&quot;, &quot;D&quot;), (&quot;C&quot;, &quot;A&quot;), (&quot;D&quot;, &quot;B&quot;), (&quot;D&quot;, &quot;C&quot;)]
for edge in edges:
    G.add_edge(edge[0],edge[1])
pagerank = nx.pagerank(G)
print(&#39;Pagerank值：&#39;,pagerank)
# 获取每个节点的pagerank数值
pagerank_list = {node: rank for node, rank in pagerank.items()}
# 将 pagerank 数值作为节点的属性
nx.set_node_attributes(G, name = &#39;pagerank&#39;, values = pagerank)
# 画网络图
show_graph(G)</div>2021-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/8f/ccce7df1.jpg" width="30px"><span>小匚</span> 👍（1） 💬（1）<div>老师好，我在跑的时候发现提示没有这个 edge_size 参数，我直接去掉了也跑出了和文章中相同的结果。nx.draw_networkx_edges(graph, positions, alpha=0.2)</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/fa/266bcb89.jpg" width="30px"><span>等待</span> 👍（1） 💬（3）<div>老师您好，想询问以下就是，在分析希拉里的邮件人物关系的过程中，阻尼因子为0.85是什么意思呢？什么情况之下才要阻尼因子为1呢？
麻烦老师了</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（1） 💬（1）<div>%15跳转概率，对应的阻尼因子是0.85 ， 阻尼因子默认就是0.85，所以在创建的时候可以直接省略啊alpha参数的设定。
import networkx
#创建有向图
digraph = networkx.DiGraph()
#有向图之间边的关系
edges = [(&quot;A&quot;, &quot;B&quot;), (&quot;A&quot;, &quot;C&quot;), (&quot;A&quot;, &quot;D&quot;), (&quot;B&quot;, &quot;A&quot;), (&quot;B&quot;, &quot;D&quot;), (&quot;C&quot;, &quot;A&quot;), (&quot;D&quot;, &quot;B&quot;), (&quot;D&quot;, &quot;C&quot;)]
for edge in edges:
    digraph.add_edge(edge[0],edge[1])
pagerank_list = networkx.pagerank(digraph)
print(&#39;PageRank 值是：&#39;,pagerank_list)
输出结果：
PageRank 值是： {&#39;A&#39;: 0.3245609358176831, &#39;B&#39;: 0.22514635472743894, &#39;C&#39;: 0.22514635472743894, &#39;D&#39;: 0.22514635472743894}</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/92/69c2c135.jpg" width="30px"><span>厚积薄发</span> 👍（0） 💬（1）<div>老师，问一下哈，edges_weights_temp = defaultdict(list)这行代码 使用list 是不是可以换成int,换成int,我试了一下也是可以的，使用defaultdict(list) 有什么特殊的用吗？</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（0） 💬（1）<div>将alpha=0.85
pagerank值为： {&#39;A&#39;: 0.3245609358176831, &#39;B&#39;: 0.22514635472743894, &#39;C&#39;: 0.22514635472743894, &#39;D&#39;: 0.22514635472743894}</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（1） 💬（0）<div>提问：
 UserWarning: Pandas doesn&#39;t allow columns to be created via a new attribute name - see https:&#47;&#47;pandas.pydata.org&#47;pandas-docs&#47;stable&#47;indexing.html#attribute-access

不允许列被新属性创建？？？

点击网页进去，也没有找到这个警告。
需要修改或者别的什么东西吗？</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/86/79/066a062a.jpg" width="30px"><span>非同凡想</span> 👍（0） 💬（0）<div>import networkx as nx


def test_page_rank():
    G = nx.DiGraph()
    edges = [(&quot;A&quot;, &quot;B&quot;), (&quot;A&quot;, &quot;C&quot;), (&quot;A&quot;, &quot;D&quot;), (&quot;B&quot;, &quot;A&quot;), (&quot;B&quot;, &quot;D&quot;), (&quot;C&quot;, &quot;A&quot;), (&quot;D&quot;, &quot;B&quot;), (&quot;D&quot;, &quot;C&quot;)]

    for edge in edges:
        G.add_edge(edge[0], edge[1])
    pagerank_list = nx.pagerank(G, alpha=0.85)
    print(pagerank_list)

test_page_rank()

{&#39;A&#39;: 0.3245609358176831, &#39;B&#39;: 0.22514635472743894, &#39;C&#39;: 0.22514635472743894, &#39;D&#39;: 0.22514635472743894}</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（0） 💬（0）<div>交作业，好累啊，
https:&#47;&#47;github.com&#47;LearningChanging&#47;Data-analysis-in-action&#47;tree&#47;master&#47;33-PageRank%EF%BC%88%E4%B8%8B%EF%BC%89%EF%BC%9A%E5%88%86%E6%9E%90%E5%B8%8C%E6%8B%89%E9%87%8C%E9%82%AE%E4%BB%B6%E4%B8%AD%E7%9A%84%E4%BA%BA%E7%89%A9%E5%85%B3%E7%B3%BB</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/68/006ba72c.jpg" width="30px"><span>Untitled</span> 👍（0） 💬（0）<div>结果：
{&#39;A&#39;: 0.32456093581768314, &#39;B&#39;: 0.22514635472743894, &#39;D&#39;: 0.2251463547274389, &#39;C&#39;: 0.22514635472743894}

代码：
import networkx as nx
edges = [(&#39;A&#39;,&#39;B&#39;),(&#39;A&#39;,&#39;D&#39;),(&#39;A&#39;,&#39;C&#39;),(&#39;B&#39;,&#39;A&#39;),(&#39;B&#39;,&#39;D&#39;),(&#39;C&#39;,&#39;A&#39;),(&#39;D&#39;,&#39;B&#39;),(&#39;D&#39;,&#39;C&#39;)]
G1 = nx.DiGraph()
G1.add_edges_from(edges)
pagerank_list = nx.pagerank(G1, alpha=0.85)</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/d2/2cf975ea.jpg" width="30px"><span>S.Mona</span> 👍（0） 💬（0）<div>pagerank计算的影响力，搜索结果按照影响力评分排序，这个和ElasticSearch的相关度评分排序搜索排序搜索结果有什么异同？</div>2019-10-16</li><br/>
</ul>