你好，我是卢誉声。从今天开始，我们正式进入动态规划套路模块。

不知道你是否跟我有过相似的经历，那就是提起动态规划，最先想到的就是背包问题。事实上，背包问题分很多种，大多数人首先遇到的一般是背包中的0-1背包问题。

因此，我把这个问题称作 Hello World，这跟我们学习一门新的编程语言十分相似。它很经典，又极具代表性，能很好地展示动态规划思想，对于你掌握动态规划面试题来说，也十分有帮助。

在“初识动态规划”模块中，相信你已经对动态规划问题有了一个比较全面的认识和了解。今天，就让我们用一用前面所学的解题思路，其实就是把总结出来的套路，套用在0-1背包问题上，看看能不能解决这道题。

那在开始前呢，我还是先提出一个简单的问题，那就是：**为什么将它称作0-1背包问题，0-1代表什么？**你不妨带着这个小问题，来学习今天的内容。

## 0-1 背包问题

我们先来看看0-1背包问题的描述。

问题：给你一个可放总重量为 $W$ 的背包和 $N$ 个物品，对每个物品，有重量 $w$ 和价值 $v$ 两个属性，那么第 $i$ 个物品的重量为 $w\[i]$，价值为 $v\[i]$。现在让你用这个背包装物品，问最多能装的价值是多少？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/d6/25/a2b77f1d.jpg" width="30px"><span>浅语清风</span> 👍（10） 💬（1）<div>课程难度越来越大了，对于对于初学者来说看一遍是根本不够的，要反复学习，不断积累，编程实践。我一定要攻克动态规划的难关！</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/47/e4/17cb3df1.jpg" width="30px"><span>BBQ</span> 👍（4） 💬（1）<div>感谢老师的细心讲解，怎么感觉越写越简单了呢。 😀
把空间复杂度优化了一下，用一个一维数组，倒着走，就不会产生重复计算了。

    def lastStoneWeightII(self, stones: List[int]) -&gt; int:
        total = sum(stones)
        size = (total)&#47;&#47;2+1 #这个要注意，如果容量要达到size，大小要是size + 1

        dp = [0] * size

        for i in range(len(stones)):
            j = size - 1
            while j &gt;= stones[i]:
                dp[j] = max(dp[j], dp[j-stones[i]] + stones[i])
                j-= 1
        return total - dp[-1] - dp[-1]</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/b0/a9b77a1e.jpg" width="30px"><span>冬风向左吹</span> 👍（2） 💬（4）<div>没太理解这里：dp[tn-1][rw-w[tn]] + v[tn]。放入物品前的价值+放入特别的价值。为什么放入特别前的价值 rw-w[tn]，这里要减w[tn]呢。放入物品前的价值不就是dp[tn-1][rw]吗？</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（2） 💬（1）<div>#include &lt;iostream&gt;
#include &lt;vector&gt;
#include &lt;cmath&gt;
#include &lt;cstring&gt;

using namespace std;

int DP(const std::vector&lt;int&gt;&amp; w, const std::vector&lt;int&gt;&amp; v, int N, int W) {
  int dp[N+1][W+1];
  memset(dp, 0, sizeof(dp)); &#47;&#47; 创建备忘录

  for (int tn = 1; tn &lt; N + 1; tn++) { &#47;&#47; 遍历每一件物品
    for (int rw = 1; rw &lt; W + 1; rw++) { &#47;&#47; 背包容量有多大就还要计算多少次
      if (rw &lt; w[tn]) {
        &#47;&#47; 当背包容量小于第tn件物品重量时，只能放入前tn-1件
        dp[tn][rw] = dp[tn-1][rw];
      } else {
        &#47;&#47; 当背包容量还大于第tn件物品重量时，进一步作出决策
        dp[tn][rw] = max(dp[tn-1][rw], dp[tn-1][rw-w[tn]] + v[tn]);
      }
    }
  }

  return dp[N][W];
}

int main() {
  int N, i, sum = 0, t, part1, part2;
  vector&lt;int&gt; w, v;
  w.push_back(0);
  v.push_back(0);

  cin &gt;&gt; N;
  for (i = 1; i &lt;= N; i++) {
    cin &gt;&gt; t;
    sum += t;
    w.push_back(t);
    v.push_back(t);
  }
  part1 = DP(w, v, N, sum &#47; 2);
  part2 = sum - part1;
  cout &lt;&lt; abs(part1 - part2) &lt;&lt; endl;
}</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/70/02b627a6.jpg" width="30px"><span>coder</span> 👍（1） 💬（2）<div>关于粉碎石头（力扣上的题：1049. 最后一块石头的重量 II）的问题的思考：

1. 可以把石头分为两堆，这两堆的重量尽量均衡，才能产生最小的差值
2. 那么就相当于把所有石头的总重量除以2，作为背包的容量，然后看最大能装入多少重量的石头
3. 从而转化成背包问题
</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/dd/df/9ad77647.jpg" width="30px"><span>樟树林</span> 👍（1） 💬（4）<div>老师，关于背包问题哈，背包容量为2，物品个数为3的背包，按照你上述计算得出的结果是3，但实际结果应为6。这个问题，老师能解释一下吗？</div>2021-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/45/e8f64725.jpg" width="30px"><span>Smile</span> 👍（0） 💬（1）<div>石头碾碎问题

public int lastStoneWeightII(int[] stones) {

        int sum = 0;
        for (int i = 0; i &lt;stones.length; i++) {
            sum+=stones[i];
        }


        int N = stones.length; &#47;&#47; 个数
        int W = sum&#47;2; &#47;&#47;总重量
        int[] w = stones; &#47;&#47;重量
        int[] v = stones; &#47;&#47;价值

        int[][] dp = new int[N+1][W+1];


        &#47;&#47;初始化状态
        for (int i = 0; i &lt; N+1; i++) {
            dp[i][0]=0;
        }

        for (int i = 0; i &lt; W+1; i++) {
            dp[0][i]=0;
        }


        for (int tn = 1; tn &lt; N+1; tn++) {
            for (int rw = 1; rw &lt; W + 1; rw++) {
                if(rw&lt;w[tn-1]){
                    dp[tn][rw] = dp[tn-1][rw];
                }else{
                    dp[tn][rw] = Math.max(dp[tn-1][rw],dp[tn-1][rw-w[tn-1]]+v[tn-1]);
                }
            }
        }

        return Math.abs(sum-2*dp[N][W]);

    }</div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/45/e8f64725.jpg" width="30px"><span>Smile</span> 👍（0） 💬（1）<div>dp[tn][rw] = Math.max(dp[tn-1][rw], dp[tn-1][rw-w[tn]] + v[tn]);  这个是有问题的，w[tn]实际上是 tn+1的物品了，这个地方都是 tn-1，思路应该是对的，但是这个代码翻译是有问题的，发现评论区好多有问题
</div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/45/e8f64725.jpg" width="30px"><span>Smile</span> 👍（0） 💬（1）<div>public int max(int[] w,int[] v,int W,int N){

        &#47;&#47;第几个物体的时候的最大价值
        &#47;&#47; dp[tn][rw] 表示浏览过 tn 件商品，能装下 rw 重量的最大剩余价值
        &#47;&#47; 题目的结果就是  dp[N][W]
        &#47;&#47; rw &lt; w[tn] dp[tn][rw] = dp[tn-1][rw]
        &#47;&#47; 否则        dp[tn][rw] =  max(dp[tn-1][rw],dp[tn-1][rw-w[tn]+v[tn]])
        &#47;&#47;初始状态
        &#47;&#47; dp[tn][0] = 0 dp[0][rw] = 0;
        
        int[][] dp = new int[N][W];

        for (int i = 0; i &lt; N; i++) {
            dp[i][0]=0;
        }

        for (int i = 0; i &lt; W; i++) {
            dp[0][i]=0;
        }


        for (int tn = 1; tn &lt;= N; tn++) {
            for (int rw =1 ; rw &lt;= W; rw++) {
                if(rw&lt;w[tn]){
                    dp[tn][rw] =  dp[tn-1][rw];
                }else{
                    dp[tn][rw] = Math.max(dp[tn-1][rw],dp[tn-1][rw-w[tn]]+v[tn]);
                }
            }
        }
        return dp[N][W];
    }</div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/03/eba78e43.jpg" width="30px"><span>风清扬</span> 👍（0） 💬（2）<div>参考评论里 Roy Liang的代码，修改了下代码，添加了部分注释：

#include &lt;iostream&gt;
#include &lt;vector&gt;
#include &lt;cmath&gt;
#include &lt;cstring&gt;
#include &lt;numeric&gt;      &#47;&#47; std::accumulate

using namespace std;

int DP(const std::vector&lt;int&gt;&amp; w, const std::vector&lt;int&gt;&amp; v, int N, int W) {
  &#47;&#47;DP[i][j]，当可以选择前i(含)个物品时，背包容量为j时最大的价值
  int dp[N+1][W+1];
  memset(dp, 0, sizeof(dp)); &#47;&#47; 创建备忘录

  for (int tn = 1; tn &lt; N + 1; tn++) { &#47;&#47; 遍历每一件物品
    for (int rw = 1; rw &lt; W + 1; rw++) { &#47;&#47; 背包容量有多大就还要计算多少次
      if (rw &lt; w[tn]) {
        &#47;&#47; 当背包容量小于第tn件物品重量时，只能放入前tn-1件
        dp[tn][rw] = dp[tn-1][rw];
      } else {
        &#47;&#47; 当背包容量还大于第tn件物品重量时，进一步作出决策
        dp[tn][rw] = max(dp[tn-1][rw], dp[tn-1][rw-w[tn]] + v[tn]);
      }
    }
  }

  return dp[N][W];
}

int main() {
  int N = 6;
  &#47;&#47;粉碎石头问题转换为0-1背包，这里价值与重量相同
  vector&lt;int&gt; w = {0,1,2,1,7,9,4};
  vector&lt;int&gt; v = {0,1,2,1,7,9,4};
  &#47;&#47;计算当前所有石头的重量和
  int sum = std::accumulate(w.begin(),w.end(),0);
  
  &#47;&#47;转换为0-1背包问题，在背包容量为sum&#47;2的情况下，尽量让价值最大（重量最大）接近sum&#47;2,因此part2-part1绝对值越小
  int part1 = DP(w, v, N, sum &#47; 2);
  int part2 = sum - part1;
  cout &lt;&lt; &quot;part1:&quot;&lt;&lt;part1&lt;&lt;&quot;,part2:&quot;&lt;&lt;part2&lt;&lt;&quot;,abs:&quot;&lt;&lt;abs(part1 - part2) &lt;&lt; endl;

  return 0;
}</div>2023-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/e9/29dfa621.jpg" width="30px"><span>小灰</span> 👍（0） 💬（1）<div>       根据老师的代码，我用了 C#实现，请老师赐教，代码如下:  
       &#47;&#47;&#47; &lt;summary&gt;
        &#47;&#47;&#47; 0-1 背包问题（针对当前物品，是放入背包，还是不放入背包时的价值最大）
        &#47;&#47;&#47; &lt;&#47;summary&gt;
        &#47;&#47;&#47; &lt;returns&gt;&lt;&#47;returns&gt;
        public int KnapsackDP(int[] wtItems, int[] valItems, int total, int maxWeight)
        {
            &#47;&#47; 创建备忘录
            int[,] dpItems = new int[total + 1, maxWeight + 1];
            &#47;&#47; 初始化状态
            &#47;&#47;for (int i = 0; i &lt; N + 1; i++) { dpItems[i,0] = 0; }
            &#47;&#47;for (int j = 0; j &lt; W + 1; j++) { dpItems[0,j] = 0; }

            for (int tn = 1; tn &lt; total + 1; tn++)  &#47;&#47; 遍历每一件物品
            {

                for (int rw = 1; rw &lt; maxWeight + 1; rw++)   &#47;&#47; 背包容量有多大就还要计算多少次
                {

                    if (rw &lt; wtItems[tn])  &#47;&#47; 当背包容量小于第 tn 件物品重量时，只能放入前tn-1件
                    {

                        dpItems[tn, rw] = dpItems[tn - 1, rw];
                    }
                    else
                    {
                        &#47;&#47; 当背包容量还大于第tn件物品重量时，进一步作出决策
                        dpItems[tn, rw] = Math.Max(dpItems[tn - 1, rw], dpItems[tn - 1, rw - wtItems[tn]] + valItems[tn]);
                    }
                }
            }

            return dpItems[total, maxWeight];
        }


        [TestCaseSource(&quot;KnapsackSource&quot;)]
        public void KnapsackDPTest(int[] wtItems, int[] valItems, int total, int maxWeight, int expectedMaxVal)
        {
            var maxVal = KnapsackDP(wtItems, valItems, total, maxWeight); &#47;&#47; 输出答案
            Console.WriteLine($&quot;KnapsackDPTest,maxVal:{maxVal},expectedMaxVal:{expectedMaxVal}&quot;);
            Assert.AreEqual(expectedMaxVal, maxVal);
        }
        public static IEnumerable KnapsackSource()
        {
            yield return new TestCaseData(new int[] { 0, 3, 2, 1 }, new int[] { 0, 5, 2, 3 }, 3, 5, 8);
        }</div>2022-04-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/m7fLWyJrnwEPoIefiaxusQRh6D1Nq7PCXA8RiaxkmzdNEmFARr5q8L4qouKNaziceXia92an8hzYa5MLic6N6cNMEoQ/132" width="30px"><span>alex_lai</span> 👍（0） 💬（1）<div>dp[n,w]中的n 不是表示第几个item在还剩w空间的情况下的最优解 而是总共可以选n个item在w空间里的最优解吧？！ 我的意思n的值跟顺序无关，比如dp[1, 10] 就是选一个item给10的空间 最优是多少</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/70/02b627a6.jpg" width="30px"><span>coder</span> 👍（0） 💬（1）<div>背包基本问题，做决策部分：“如果背包容量小于当前物品价值”

应该是“小于当前物品重量”或者“小于当前物品体积”吧？</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/e1/23/717c4449.jpg" width="30px"><span>放飞风筝</span> 👍（0） 💬（1）<div>主要抓住状态参数（构建备忘录）和转移方程</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9b/24/a131714e.jpg" width="30px"><span>Alvin</span> 👍（0） 💬（1）<div>看到这里一直觉得这个思路很奇怪，为什么是先初始化状态参数，再确定状态参数。不先确定状态参数，怎么初始化？每次看老师的思路说先初始化xxx，感觉其实就已经确定了xxx是状态参数。</div>2021-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/3d/8120438b.jpg" width="30px"><span>3.141516</span> 👍（0） 💬（1）<div>这个数学方程很数学、很简洁，但是看着头疼......不如文字好理解</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f1/12/c40d07bc.jpg" width="30px"><span>pearl刘东洋</span> 👍（0） 💬（1）<div>看到这里有一个心得体会，动态规划确实是一种解决问题的思想，光看作者的代码实现其实收获会很小，而且后续也不一定能解决类似的动态规划问题，要把更多的时间和经历花在体会作者分析一个问题到动态规划的几个特点中的过程，这个是核心，容我再多看几遍，榨干作者，哈哈哈</div>2021-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/15/c5dc2b0d.jpg" width="30px"><span>James</span> 👍（0） 💬（1）<div>老师那个0-1背包的问题你说用贪心来解不能得到全局最优解，但是我想了下对于贪心来说，我每次都选择单位重量下价值最大的那个物品最终也能得到全局最优解（比如那个例子价值为3的物品重量为1，那每单位重量就值3，这个最大，我先选这个，其次是价值为5的物品，平均单位价值为1.6，我再选择这个物品，那么最终求得的价值是8），是全局最优解，不知道理解的对不对</div>2021-03-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kj8UwADicsWBicD19FFOg8BuxHBibweWibxjpNIKHSJmAsIUu7D0GfFWdWfFELc688m9icmrfThvickW9ibAddq4jD4ow/132" width="30px"><span>Geek_116dbe</span> 👍（0） 💬（1）<div>确实能通过大部分测试用例。
但是[4,3,4,3,2]这个测试用例无法通过，确实可以选出4 + 4 和 3 + 3 + 2两个和为8的序列，但是无法碰撞让其剩余值为0。
这里的问题就是碰撞过程是离散的，相同和相消是连续的，在实际操作中无法完全匹配。</div>2021-03-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eogu5icVZzlYcOv5yxLBPtFk1EicguBCAqc2eOTrE1ttlSeTsky645Nw00gu0JF9P0BYib18dJBjlmtA/132" width="30px"><span>刘帅帅</span> 👍（0） 💬（1）<div>写的是非常的棒的，特别是思考分析的过程，这种就是已经达到举重若轻的地步了。</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/79/abf66ba0.jpg" width="30px"><span>猴子请来的仁波切</span> 👍（0） 💬（1）<div>老师咨询个问题，举个极端的情况，在选取物品tn时，它的重量大于背包可容纳的重量，但它的价值非常大，目前的处理方法会漏掉物品tn
是不是输入数据需要提前做一下什么处理？</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>动态规划确实一个难啃的骨头</div>2020-11-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLHS9BjwOgkqV1NSmNRFxUC6KU0DibS75f00GhMWx4s5OYLryibaNDoJ1tZAFRaHJ7jSZXA4pNumraQ/132" width="30px"><span>Lake</span> 👍（0） 💬（1）<div>这道题真的是上来好吓唬人，本地写了几个例子能过，偶然发现LeetCode有，就贴下能AC的版本吧。
另外1−(((4−2)−(9−7))−1) 这里应该是写错了吧，应该是这样吧1−(1 - ((4−2)−(9−7))) 

class Solution {
    public int lastStoneWeightII(int[] stones) {
        int sum = 0;
        int N = stones.length;
        for(int i=0; i&lt;N; i++) {
            sum += stones[i];
        }
        
        int W = sum &#47; 2;
        int[][] dp = new int[N + 1][W + 1];
        
        for(int i=0; i&lt;N + 1; i++) dp[i][0] = 0;
        for(int j=0; j&lt;W + 1; j++) dp[0][j] = 0;
        
        for(int i=1; i&lt;N + 1; i++) {
            for(int j=1; j&lt; W + 1; j++) {
                if(j &lt; stones[i-1]) {
                    dp[i][j] = dp[i-1][j];
                } else {
                    dp[i][j] = Math.max(dp[i-1][j], dp[i-1][j-stones[i-1]] + stones[i-1]);
                }
            }
        }
        
        int maxHalfSum = dp[N][W];
        
        return sum - maxHalfSum * 2;
    }
}</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/b0/a9b77a1e.jpg" width="30px"><span>冬风向左吹</span> 👍（0） 💬（1）<div>没太理解这里：放入物品前的价值+放入物品的价值。dp[tn-1][rw-w[tn]] + v[tn]</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/25/27/0076d304.jpg" width="30px"><span>帽子狗</span> 👍（0） 💬（2）<div>如果仅剩3个石头，质量分别为a,b,c 且 a &gt; b &amp;&amp; a &gt;c。
其结果一定是abs(a - (b+c))
那么对于每个stone数组， 都可以将其拆分为3个连续子数组, 并求碎石结果。
选出最小的拆分结果。

私以为这样穷举会直观点.

dp数组二维dp[i][j] 表示从i - j 区间的子数组碎出来的结果, 0 &lt;= i &lt;= j &lt; stone.length</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/7d/b0ca572b.jpg" width="30px"><span>jefferyqjy</span> 👍（0） 💬（1）<div>建议0-1背包问题一开始的那个描述状态转移方程的伪代码各个变量是什么意思，描述可以再斟酌一下~现在tn“即已经遍历过的物品”这样的描述感觉有点拗口，也不清晰，不太容易理解</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/aa/4f038961.jpg" width="30px"><span>马东</span> 👍（0） 💬（1）<div>“”粉碎石头”，尝试求解了一下，想到了两种解法，第一种就是在数组中插入‘+’ ，‘-’ 使得数组总值最小，我记得这个leetcode有类似这个题型；第二种方法，也就是本节课中给出的解法：
    public static int rock(int[] w){

        int sum = 0;
        for (int i = 0; i &lt; w.length ; i++) {
            sum += w[i];
        }

        return sum&#47;2 - rockHelper(w,sum&#47;2,w.length -1);
    }

    private static int rockHelper(int[] w, int cap,int N){
        int[][] dp = new int[N + 1][cap + 1];


        for (int i = 1; i &lt; N+1; i++) {

            for (int j = 1; j &lt; cap+1; j++) {

                if (j &lt; w[i]){
                    dp[i][j] = dp[i-1][j];
                }else {
                    int t1 = dp[i-1][j];
                    int t2 = dp[i-1][j-w[i]];
                    if (t2 + w[i] &gt; cap){
                        dp[i][j] = dp[i-1][j];
                    }else{
                        dp[i][j] = Math.max(t1,t2+w[i]);
                    }
                }
            }

        }
        
        return dp[N][cap];
    }</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/6b/0f3876ef.jpg" width="30px"><span>iron_man</span> 👍（0） 💬（1）<div>老师讲的很透，很细，很好。对于粉碎石头的问题有一点疑惑，就是选择容量为12的背包，是不是还有石头数量的限制，不多不少只能3个石头？而0-1背包问题，对于选择的石头并没有数量限制，只要不超过石头总数和背包容量即可</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/26/4942a09e.jpg" width="30px"><span>猫头鹰爱拿铁</span> 👍（0） 💬（1）<div>尝试用递归和dp解了一下，这里有个难点就是为什么返回值是总和-dp值*2，数组可以看成[平均值-偏差，平均值+偏差]，要使得平均值+偏差-（平均值-偏差）最小也就是偏差需要最小，而dp算出来的值是最接近平均值的，所以偏差最小。
private static int min = Integer.MAX_VALUE;

    public int ans(int[] weight) {
        int n = weight.length;
        int w = 0;
        for (int i = 0; i &lt; weight.length; i++) {
            w += weight[i];
        }

        getAnsByRecursion(0, n, 0, w, weight);
        &#47;&#47;return getAnsByDP(w, n, weight);
        return min;
    }

    public void getAnsByRecursion(int k, int n, int rw, int w, int[] weight) {
        if (k == n) {
            if (Math.abs(w - rw * 2) &lt; min) {
                min = Math.abs(w - rw * 2);
            }
            return;
        }
        for (int i = k; i &lt; n; i++) {
            getAnsByRecursion(i + 1, n, rw + weight[i], w, weight);
            getAnsByRecursion(i + 1, n, rw, w, weight);
        }
    }

    public int getAnsByDP(int w, int n, int[] weight) {
        &#47;&#47;取前i个最接近w的重量
        int total = w;
        w = w &#47; 2;
        int[][] dp = new int[n + 1][w + 1];
        for (int i = 0; i &lt; w + 1; i++) {
            dp[0][i] = 0;
        }
        for (int j = 0; j &lt; n + 1; j++) {
            dp[j][0] = 0;
        }
        for (int i = 1; i &lt; n + 1; i++) {
            for (int j = 1; j &lt; w + 1; j++) {
                if (j - weight[i - 1] &gt;= 0) {
                    if (Math.abs(j - dp[i - 1][j]) &gt;
                            Math.abs(j - (dp[i - 1][j - weight[i - 1]] + weight[i - 1]))) {
                        dp[i][j] = dp[i - 1][j - weight[i - 1]] + weight[i - 1];
                        continue;
                    }
                }
                dp[i][j] = dp[i - 1][j];
            }
        }
        return total - 2 * dp[n][w];
    }</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d4/37/aa152ddb.jpg" width="30px"><span>AshinInfo</span> 👍（0） 💬（1）<div>&#47;&#47; 初始化状态    
for (int i = 0; i &lt; N + 1; i++) { dp[i][0] = 0; }    
for (int j = 0; j &lt; W + 1; j++) { dp[0][j] = 0; 
在java代码中，这两行的初始化代码可以去掉，默认都是0</div>2020-10-10</li><br/>
</ul>