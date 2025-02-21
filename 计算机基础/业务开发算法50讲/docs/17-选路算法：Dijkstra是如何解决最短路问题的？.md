你好，我是微扰君。

在掌握操作系统中的一些经典算法之后，我们来学习计算机的另一大基础课——计算机网络中的算法。计算机网络，当然也是一个历史悠久的科研方向，可以说之所以现在计算机世界如此繁荣，计算机网络发挥着巨大的作用，是整个互联网世界的基石。

复杂的计算机网络中自然也产生了许多算法问题，比如许多经典的图论算法都是在计算机网络的研究背景中诞生的。在这一章我们会挑选几个有趣的问题一起讨论，主要涉及两种场景，计算机网络网络层的选路算法、传输层协议TCP中的滑动窗口思想。

今天我们先来学习选路算法，有时它也被称为路由算法，“路由”这个词相信你应该很熟悉，没错，说的就是路由器里的路由。

## 路由

我们知道，计算机网络的作用，就是通过把不同的节点连接在一起从而交换信息、共享资源，而各个节点之间也就通过网络形成了一张拓扑关系网。

比如在一个局域网下，节点A要给节点B发送一条消息，如果A和B并没有直接通过网络相连，可能就需要经过其他路由设备的几次转发，这时我们需要在整个网络拓扑图中找到一条可到达的路径，才能把消息发送到目的地。

每台路由器都是一台网络设备，也就是网络中的一个节点，在其中就保存有一张路由表，**每次网卡收到包含目标地址的数据包（packet）时，就会根据路由表的内容决定如何转发数据**。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（3） 💬（1）<div>Dijkstra 算法是逐步构建最短路径树，树中的节点的最短距离不依赖于树外节点，这样才可以一个节点加入最短路径树之后，距离不再改变。负权节点的存在会让加入最短路径树的节点的真实最短路径会因为不在树中的节点而改变，整个算法也就无效了。
如果用最小堆作为数据结构选择最短路径，可以让内存循环的复杂度降为lg V，最终的复杂度可以降为(V+E)lg V
</div>2022-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/eb/19/0d990b03.jpg" width="30px"><span>ZeroIce</span> 👍（1） 💬（1）<div>有时候在想:负权边的意义是什么? 应用场景在哪里?🤪</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/0d/00424e81.jpg" width="30px"><span>到道可道</span> 👍（0） 💬（1）<div>Dijkstra的Java实现
private int dijkstra(List&lt;int[]&gt;[] graph, int src, int k, int dst) {
        &#47;&#47; 从起点src到达节点i的最短路径权重为distTo[i]
        int[] distTo = new int[graph.length];
        &#47;&#47; 定义：从起点src到节点i，至少要经过nodeNumTo[i]个节点
        int[] nodeNumTo = new int[graph.length];
        Arrays.fill(distTo, Integer.MAX_VALUE);
        Arrays.fill(nodeNumTo, Integer.MAX_VALUE);
        &#47;&#47; base case
        distTo[src] = 0;
        nodeNumTo[src] = 0;

        &#47;&#47; 优先队列，costFromSrc较小的排在前面
        Queue&lt;State&gt; pq = new PriorityQueue&lt;&gt;((a, b) -&gt; a.costFromSrc - b.costFromSrc);
        &#47;&#47; 从起点src开始进行BFS
        pq.offer(new State(src, 0, 0));
        while (!pq.isEmpty()) {
            State curState = pq.poll();
            int curId = curState.id;
            int curCostFromSrc = curState.costFromSrc;
            int curNodeNumFromSrc = curState.nodeNumFromSrc;

            if (curId == dst) {
                &#47;&#47; 找到最短路径
                return curCostFromSrc;
            }
            if (curNodeNumFromSrc == k) {
                &#47;&#47; 中转次数耗尽
                continue;
            }
            &#47;&#47; 将curId 的相邻节点装入队列
            for (int[] neighbor : graph[curId]) {
                int nextId = neighbor[0];
                int costToNextNode = curCostFromSrc + neighbor[1];
                &#47;&#47; 中转次数
                int nextNodeNumFromSrc = curNodeNumFromSrc + 1;
                &#47;&#47; 更新dp table
                if (distTo[nextId] &gt; costToNextNode) {
                    distTo[nextId] = costToNextNode;
                    nodeNumTo[nextId] = nextNodeNumFromSrc;
                }
                &#47;&#47; 剪枝
                if (costToNextNode &gt; distTo[nextId] &amp;&amp; nextNodeNumFromSrc &gt; nodeNumTo[nextId]) {
                    continue;
                }
                pq.offer(new State(nextId, costToNextNode, nextNodeNumFromSrc));
            }
        }

        return -1;
    }
</div>2022-03-06</li><br/>
</ul>