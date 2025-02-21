你好，我是景霄。

众所周知，我们当代的计算机都是图灵机架构。图灵机架构的本质，就是一条无限长的纸带，对应着我们今天的存储器。在工程学的演化中，逐渐出现了寄存器、易失性存储器（内存）和永久性存储器（硬盘）等产品。其实，这本身来自一个矛盾：速度越快的存储器，单位价格也越昂贵。因此，妥善利用好每一寸高速存储器的空间，永远是系统设计的一个核心。

回到 Python 应用层。

我们知道，Python 程序在运行的时候，需要在内存中开辟出一块空间，用于存放运行时产生的临时变量；计算完成后，再将结果输出到永久性存储器中。如果数据量过大，内存空间管理不善就很容易出现 OOM（out of memory），俗称爆内存，程序可能被操作系统中止。

而对于服务器，这种设计为永不中断的系统来说，内存管理则显得更为重要，不然很容易引发内存泄漏。什么是内存泄漏呢？

- 这里的泄漏，并不是说你的内存出现了信息安全问题，被恶意程序利用了，而是指程序本身没有设计好，导致程序未能释放已不再使用的内存。
- 内存泄漏也不是指你的内存在物理上消失了，而是意味着代码在分配了某段内存后，因为设计错误，失去了对这段内存的控制，从而造成了内存的浪费。

那么，Python 又是怎么解决这些问题的？换句话说，对于不会再用到的内存空间，Python 是通过什么机制来回收这些空间的呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（38） 💬（2）<div>思考题答案：

事实上算法可以写的很简单，这是个很经典的 dfs （深度优先搜索）遍历，从起点开始遍历，对遍历到的节点做个记号。遍历完成后，再对所有节点扫一遍，没有被做记号的，就是需要垃圾回收的。</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（24） 💬（4）<div>1. 循环引用情况下Python不立即回收内存，如果放任不管，即不显式调用gc.collect的话，Python的垃圾回收器自己会什么时候处理？
2. 最后介绍了内存泄露排查工具，哪种算内存泄露呢？接问题1，不立即回收算内存泄露吗？还是有其他场景</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/11/5d113d5c.jpg" width="30px"><span>天凉好个秋</span> 👍（10） 💬（3）<div>本文讲的垃圾回收算法在Java中也都有，当初在设计的时候是不是参考了Java？而且，Java中还有标记整理算法，可以解决回收内存不连续的问题，这个在Python中有没有考虑呢？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/96/af/da8fd6ed.jpg" width="30px"><span>　　星豪</span> 👍（5） 💬（1）<div>1. 在读文章的时候找了一个可能是错别字的地方，在循环引用那一节中，第四段试想一下，如果这段代码出现在生产环境中...但经过长时间运行“候”...。这一侯应该是后来的后吧？
2. 当垃圾回收器中新增对象减去删除对象达到相应的阈值时，就会对这一代对象启动垃圾回收。这一句话不是很明白，新增对象我理解的是新创建的对象或者是从上一代挪过来的对象，那么删除对象指的是哪些呢？或者说是如何进行指定哪些是应该被删除的对象呢？</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a8/f4/2abb4a4c.jpg" width="30px"><span>MirkoWei</span> 👍（3） 💬（1）<div>windows下使用objgraph遇到个问题：
`failed to execute [&#39;dot&#39;, &#39;-Tpdf&#39;], make sure the Graphviz executables are on your systems&#39; path`

安装objgraph的时候，需要的前置条件graphviz、xdot都安装了，系统环境变量也添加了，仍然找不到路径

之后通过stackoverflow得到解决办法，就是每次使用的时候，需要在代码前面手动添加环境变量
```
import os

os.environ[&quot;PATH&quot;] += os.pathsep + &#39;xxx&#47;Graphviz2.38&#47;bin&#47;&#39;
```
问题是解决了，但是每次都需要手动添加环境变量也太麻烦了，不知道是否有更好的解决办法</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/3f/6f62f982.jpg" width="30px"><span>wangkx</span> 👍（1） 💬（1）<div>课程越往后越有意思，发现了很多知识点盲区，这门课很值！</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/15/c6/f5c543ef.jpg" width="30px"><span>Switch</span> 👍（23） 💬（1）<div>思考题：
from typing import Set


class Graph:
    def __init__(self, value, nodes=None):
        self._value = value
        self._nodes: list = [] if nodes is None else nodes

    @property
    def value(self):
        return self._value

    @property
    def nodes(self):
        return self._nodes

    def node_add(self, node):
        self._nodes.append(node)

    def node_adds(self, nodes):
        self._nodes.extend(nodes)

    def node_del(self, node):
        self._nodes.remove(node)

    def __str__(self):
        return &quot;Graph {} nodes {}&quot;.format(self._value, [node.value for node in self.nodes])

    def __repr__(self):
        return self.__str__()


def dfs(start: Graph, includes: Set[Graph] = None) -&gt; Set[Graph]:
    if includes is None:
        includes = set()
    if start in includes:
        return includes
    includes.add(start)
    for s in start.nodes:
        includes.update(dfs(s, includes))
    return includes


if __name__ == &#39;__main__&#39;:
    A = Graph(&#39;A&#39;)
    B = Graph(&#39;B&#39;)
    C = Graph(&#39;C&#39;)
    D = Graph(&#39;D&#39;)
    E = Graph(&#39;E&#39;)
    F = Graph(&#39;F&#39;)
    has_nodes = {A, B, C, D, E, F}

    # A-&gt;B-&gt;E
    #  -&gt;C-&gt;E
    # B-&gt;A
    # D-&gt;F
    # F-&gt;D
    A.node_adds([B, C])
    B.node_adds([A, E])
    C.node_adds([E])
    D.node_adds([F])
    F.node_adds([D])
    graph_nodes = dfs(A, set())
    # OUT: {Graph B nodes [&#39;A&#39;, &#39;E&#39;], Graph E nodes [], Graph C nodes [&#39;E&#39;], Graph A nodes [&#39;B&#39;, &#39;C&#39;]}
    print(graph_nodes)
    # OUT: {Graph F nodes [&#39;D&#39;], Graph D nodes [&#39;F&#39;]}
    print(has_nodes - graph_nodes)
</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/0e/3fbc418d.jpg" width="30px"><span>youaresherlock</span> 👍（8） 💬（1）<div>四次引用，a，python 的函数调用栈，函数参数，和 getrefcount
不理解这里的函数调用栈、函数参数为什么增加了2次，这里有什么区别？他们两个不是一样的吗，函数参数在函数调用栈里，应该是一次啊</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/66/a0/c00fb984.jpg" width="30px"><span>你说呢</span> 👍（5） 💬（0）<div>可以这样理解么：python的垃圾回收机制，以引用计数算法为主、标记-删除算法为辅 来确定内存中哪些对象可以回收；而分代回收算法确定了垃圾是什么时候被回收。
</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（5） 💬（10）<div>请问一下，老师
执行关于objgraph代码，出现如下错误：
Graph viewer (xdot) and image renderer (dot) not found, not doing anything else
是不是还要安装什么软件？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1c/c4/3e593863.jpg" width="30px"><span>cool</span> 👍（3） 💬（1）<div>Python 的自动回收算法包括标记清除 ，标记清除怎么来解决循环引用垃圾回收的，专栏中讲解的没听懂，循环引用 能在图中遍历到</div>2020-07-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/JGPabHDickBjMJwVoJ7ZRGiaT21BibxvCJ9DR9Gvn3G1iazHQPTJQtkWwfFssYfGJsPahEB7sOnXScibkrsr4gx6LeA/132" width="30px"><span>微风漂过</span> 👍（3） 💬（0）<div>开头的代码
运行出错：ModuleNotFoundError: No module named &#39;psutil&#39;
安装出错：
pip install --upgrade psutil
Collecting psutil
  Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by &#39;ReadTimeoutError(&quot;HTTPSConnectionPool(host=&#39;pypi.org&#39;, port=443): Read timed out. (read timeout=15)&quot;)&#39;: &#47;simple&#47;psutil&#47;
  Could not find a version that satisfies the requirement psutil (from versions: )
No matching distribution found for psutil
请问这是什么原因？</div>2020-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/22/89/73397ccb.jpg" width="30px"><span>响雨</span> 👍（2） 💬（0）<div>思考题看的我一脸蒙蔽，无从下手</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/77/ab/1e583bd3.jpg" width="30px"><span>ァSgr</span> 👍（1） 💬（0）<div>思考题：
def dfs(graph: dict, start: str):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node] - visited)

    return visited

def unreachable_nodes(graph: dict, start: str):
    reachable_nodes = dfs(graph, start)
    all_nodes = set(node for nodes in graph.values() for node in nodes).union(graph.keys())
    return all_nodes - reachable_nodes

# 示例图结构
graph = {
    &quot;A&quot;: {&quot;B&quot;, &quot;C&quot;},
    &quot;B&quot;: {&quot;A&quot;, &quot;D&quot;, &quot;E&quot;},
    &quot;C&quot;: {&quot;A&quot;, &quot;F&quot;},
    &quot;D&quot;: {&quot;B&quot;},
    &quot;E&quot;: {&quot;B&quot;, &quot;F&quot;},
    &quot;F&quot;: {&quot;C&quot;, &quot;E&quot;},
    &quot;G&quot;: {&quot;H&quot;},
    &quot;H&quot;: {&quot;G&quot;}
}

print(unreachable_nodes(graph, &#39;A&#39;))

# 输出
{&#39;G&#39;, &#39;H&#39;}</div>2023-05-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJRCtuJkpyy2I29LxUsXwZGjicyzDAb3lo76KLX8gxUfawgSeNdQOibjibF0VNXEv7t2DiaIrBU4KcHyQ/132" width="30px"><span>瞌睡的咸鱼</span> 👍（1） 💬（0）<div>思考题——通过有向图的拓扑排序可以求出（可以参考《算法导论》去理解）</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/7d/c7e8cd34.jpg" width="30px"><span>干布球</span> 👍（1） 💬（2）<div>请问老师，问什么多次调用print(sys.getrefcount(a))，只有第一次会增加a的计数呢？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5b/81/8c38dff8.jpg" width="30px"><span>lcqbug</span> 👍（0） 💬（0）<div>现在的计算机架构 是图灵机？不是冯诺依曼架构吗</div>2024-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5b/81/8c38dff8.jpg" width="30px"><span>lcqbug</span> 👍（0） 💬（0）<div>判断不可达，不可达哪里呢？ 根是哪里</div>2024-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第24讲打卡~</div>2024-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/8f/ccce7df1.jpg" width="30px"><span>小匚</span> 👍（0） 💬（0）<div>想到了Java的内存回收机制，也是类似的，引用计数和引用不可达法。</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/48/a3/2df11999.jpg" width="30px"><span>Boom clap!!!</span> 👍（0） 💬（0）<div>windows 使用 objgraph时候报错Spawning graph viewer (xdot)，怎么办啊 老师</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（0） 💬（0）<div>老师是用linux重装的系统吗，因为我记得老师是用的苹果电脑</div>2020-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/12/f9/7e6e3ac6.jpg" width="30px"><span>Geek_04e22a</span> 👍（0） 💬（0）<div>class ListNode(object):
    &quot;&quot;&quot;
    节点数据结构
    val： 值
    node：有向边终点列表集合
    &quot;&quot;&quot;

    def __init__(self, x):
        self.val = x
        self.node = list()


def deep_list(a):
    &quot;&quot;&quot;
    深度优先遍历
    :param a:
    :return:
    &quot;&quot;&quot;

    if len(a.node) == 0:
        return

    for node in a.node:
        print(node.val)
        deep_list(node)


a = ListNode(&#39;a&#39;)
b = ListNode(&#39;b&#39;)
c = ListNode(&#39;c&#39;)
d = ListNode(&#39;d&#39;)
e = ListNode(&#39;e&#39;)
f = ListNode(&#39;f&#39;)

a.node = [b, c]
c.node = [e]


deep_list(a)</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/8a/891b0e58.jpg" width="30px"><span>wnz27</span> 👍（0） 💬（1）<div>gc.collect()，不是清除没有引用的对象吗，为什么循环引用代码里没有del a和del b可以垃圾回收呢？是老师手误吗？</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（0） 💬（0）<div>简单写了一个有向图的遍历程序，说明：
(1)有向图采用邻接链表存储
(2)有向图采用递归算法进行深度优先遍历
#邻接链表节点定义
class LinkNode:
    def __init__(self,data):
        self.data = data
        self.next = None
	
#邻接链表定义
class AdjoinList:
    def __init__(self):
        self.adjlist = {}  #存贮节点间的邻接关系
        self.vistlist = {} #存贮节点是否被访问，初始所有节点都是False
	
    #建立结点x1和x2的连接关系，其中，x1指向x2
    def addNode(self,x1,x2):

        #建立链接
        point = self.adjlist.setdefault(x1, None)
        lnode = LinkNode(x2)
        lnode.next = point
        self.adjlist[x1] = lnode
        self.adjlist.setdefault(x2, None)

        #初始化访问列表        
        self.vistlist.setdefault(x1,False)
        self.vistlist.setdefault(x2,False)

    #遍历图中所有结点
    def visitNode(self,nodevalue):
        if nodevalue is not None:
            self.vistlist[nodevalue] = True
            print(&#39;visist:&#39;, nodevalue)
            nextnode = self.adjlist[nodevalue]
                
            while nextnode is not None:

                if not self.vistlist[nextnode.data]:
                    self.visitNode(nextnode.data)
                
                nextnode = nextnode.next


    #输出未被访问的结点
    def showUnvistedNode(self):
        print(&#39;UnvistedNode:&#39;, &#39;,&#39;.join([x for x in self.vistlist if not self.vistlist[x]]))

#主程序
def main():
#BEGIN

    adlist = AdjoinList()

    #创建有向图，有向图简单示意如下：
    &#39;&#39;&#39;
    a--&gt;b--&gt;c
    |
    |
    d--&gt;e--&gt;f

    g--&gt;h--&gt;j
    
    &#39;&#39;&#39;
    adlist.addNode(&#39;a&#39;,&#39;b&#39;)
    adlist.addNode(&#39;a&#39;,&#39;d&#39;)
    adlist.addNode(&#39;b&#39;,&#39;c&#39;)
    adlist.addNode(&#39;d&#39;,&#39;e&#39;)
    adlist.addNode(&#39;e&#39;,&#39;f&#39;)
    adlist.addNode(&#39;g&#39;,&#39;h&#39;)
    adlist.addNode(&#39;h&#39;,&#39;j&#39;)

    #从a节点开始遍历有向图
    adlist.visitNode(&#39;a&#39;)

    #输出未访问的节点
    adlist.showUnvistedNode()

#END

if __name__ == &#39;__main__&#39;:
    main()</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（0） 💬（0）<div>思考题，就是图的遍历算法，深度优先或广度优先算法，标记每个节点，遍历后，没标记过的就是可以回收的垃圾。</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2b/6c/a2d3fe36.jpg" width="30px"><span>夏尔</span> 👍（0） 💬（0）<div>def func():
    show_memory_info(&#39;initial&#39;)
    a = [i for i in derange(10000000)]
    show_memory_info(&#39;after a created&#39;)
    return a

a = func()
show_memory_info(&#39;finished&#39;)

########## 输出 ##########

initial memory used: 47.96484375 MB
after a created memory used: 434.515625 MB
finished memory used: 434.515625 MB

这是本文第四个代码块，for i in range；多了de，变成了derange；</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（0） 💬（0）<div>老师，请问：除了循环引用，还有哪些错误的程序设计会造成内存泄漏，需要强制调用gc.collect()来垃圾回收？</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（0） 💬（0）<div>可否给一个内存泄露的实例，逃脱了gc的“法眼”？</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/4f/65abc6f0.jpg" width="30px"><span>KaitoShy</span> 👍（0） 💬（1）<div>请问一下，老师：
import sys

a= [1]

print(sys.getrefcount(a))

b = a
print(sys.getrefcount(a))

c,d,e,f,g,h = b,b,c,e,d,a
print(g)
print(sys.getrefcount(a))
-------


import sys...
2
3
[1]
6
为什么最后一次是6次？而g的值是正常的呢？</div>2019-07-04</li><br/>
</ul>