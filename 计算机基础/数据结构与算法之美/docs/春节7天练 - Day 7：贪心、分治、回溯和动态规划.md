你好，我是王争。今天是节后的第一个工作日，也是我们“春节七天练”的最后一篇。

* * *

## 几种算法思想必知必会的代码实现

### 回溯

- 利用回溯算法求解八皇后问题
- 利用回溯算法求解0-1背包问题

### 分治

- 利用分治算法求一组数据的逆序对个数

### 动态规划

- 0-1背包问题
- 最小路径和（详细可看@Smallfly整理的 Minimum Path Sum）
- 编程实现莱文斯坦最短编辑距离
- 编程实现查找两个字符串的最长公共子序列
- 编程实现一个数据序列的最长递增子序列

## 对应的LeetCode练习题（@Smallfly 整理）

- Regular Expression Matching（正则表达式匹配）

英文版：[https://leetcode.com/problems/regular-expression-matching/](https://leetcode.com/problems/regular-expression-matching/)

中文版：[https://leetcode-cn.com/problems/regular-expression-matching/](https://leetcode-cn.com/problems/regular-expression-matching/)

- Minimum Path Sum（最小路径和）

英文版：[https://leetcode.com/problems/minimum-path-sum/](https://leetcode.com/problems/minimum-path-sum/)

中文版：[https://leetcode-cn.com/problems/minimum-path-sum/](https://leetcode-cn.com/problems/minimum-path-sum/)
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>kai</span> 👍（13） 💬（2）<div>听了老师的课程，第一遍的时候，只是在读，现在开始回顾：
课程相关的知识点，做了笔记：https:&#47;&#47;github.com&#47;guokaide&#47;algorithm&#47;blob&#47;master&#47;summary&#47;algorithm.md
课程涉及的题目，也在逐步总结当中：
https:&#47;&#47;github.com&#47;guokaide&#47;algorithm&#47;blob&#47;master&#47;questions&#47;questions.md

希望和大家一起进步，欢迎小伙伴们一起来讨论~
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/9f/f2eaaa8a.jpg" width="30px"><span>Richard</span> 👍（2） 💬（1）<div>老师留的题都很不错，正在刷之前没做过的LeetCode题。
参与下答对三题送课程的活动:
Day 1：
1.求众数(Python)
class Solution:
    def majorityElement(self, nums):
        return sorted(nums)[len(nums) &#47;&#47; 2]
2.缺失的第一个正数(Golang)
func firstMissingPositive(nums []int) int {
    if len(nums) == 0 {
		return 1
	}

	var arr = make([]bool, len(nums)+1)
	var idx = 1
	for i := 0; i &lt; len(nums); i++ {
		if nums[i] &gt;= 0 &amp;&amp; nums[i] &lt; len(arr) {
			arr[nums[i]] = true
		}
	}

	for i := 1; i &lt; len(arr); i++ {
		if arr[i] == false {
			idx = i
			break
		} else {
			idx = i + 1
		}
	}

	return idx
}
Day 7:
3. 买卖股票的最佳时机(Python)
class Solution:
    def maxProfit(self, prices):
        if not prices:
            return 0
        min_price = prices[0]
        res = 0
        for i in prices[1:]:
            min_price = min(min_price, i)
            if res &lt; i - min_price:
                res = i - min_price
        return res
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（1）<div>请教下老师，遇到一个问题，给多个银行账号，假如每个账号每天都有交易，这样在坐标中可以画出时间和交易金额的曲线，求哪个曲线的更平滑或波动更大，银行账号的交易额度可能相差很大，银行账号交易梳理可能多个。</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/b9/946b181d.jpg" width="30px"><span>好运连连</span> 👍（0） 💬（1）<div>老师，请教下。关于物流中转路线，应该采用哪种算法合适？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/6f/aacb013d.jpg" width="30px"><span>黄丹</span> 👍（4） 💬（0）<div>课程的最后一天，也是新年上班的第一天，感谢王老师的教育和陪伴，祝您生活开心，工作顺利。
今天的题目比前几天的都难一点，只做了三题，太累了TaT。对于动态规划和贪心总觉得很巧妙，如果想不到动态转移方程式，就很难做，但要是想到了，真的是豁然开朗。对于这一类题，还是要多锻炼，找动态转移方程式要从最后一个结果出发，去想这个结果可以由什么得到，知道之前所有结点的信息，如何推导出当前结点的信息，其实和高中学的归纳法有一点点像。 
下面给出我今天做的三题的解题思路和代码
1.	Problem 121. Best Time to Buy and Sell Stock
解题思路：这道题很久以前做的，我们可以维持两个变量 - 分别对应于最小谷值和最大利润（销售价格和最低价格之间的最大差异）的minprice 和maxprofit。
代码：https:&#47;&#47;github.com&#47;yyxd&#47;leetcode&#47;blob&#47;master&#47;src&#47;leetcode&#47;array&#47;easy&#47;Problem121.java
2.	Problem 120. Triangle
解题思路：这道题给一个由整数组成的三角形，自上而下寻找顶点到三角形边的最短的一条路径，设置一个数组A[0...n-1][0...n-1]，A[i][j]代表到达第i行第j列结点的最短路径 * DP转移方程式为：A[i][j]=min(A[i-1][j-1],A[i-1][j])+triangle[i][j] * 其中二维数组可以简化为一维数组，因为我们只需要上一行结点的信息 * 然后遍历到达最后一行的节点的路径，找到最短路径的值
代码：https:&#47;&#47;github.com&#47;yyxd&#47;leetcode&#47;blob&#47;master&#47;src&#47;leetcode&#47;dp&#47;Problem120_Triangle.java
3.	Problem 322. Coin Change
解题思路：这道题是给定具有n个不同金额的硬币（硬币个数无限）coins[0...n-1]，给一个整数amount，是否给的硬币能正好达到整数，给出能组成整数最少需要的硬币个数. 解法是设置一个数组A[0...amount],进行初始化A[0]=0;A[1...amount] = -1;保存的是当给定金额为i时，所需要的最少的硬币。 * dp转移方程式为 A[k] = 1+min(A[k-coins[0]],A[k-coins[1]],....A[k-coins[n-1]]). * 这里要注意的是判断A[k]是否有解
代码：https:&#47;&#47;github.com&#47;yyxd&#47;leetcode&#47;blob&#47;master&#47;src&#47;leetcode&#47;dp&#47;Problem322_CoinChange.java
课程完结撒花，真的学到好多，自己以后还会反复回顾的，再次感谢王争老师，还有每天负责朗读的声音好好听的修阳小哥哥。
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/99/44378317.jpg" width="30px"><span>李皮皮皮皮皮</span> 👍（3） 💬（0）<div>每天一道算法题，风雨无阻（过年偷懒不算😛）</div>2019-02-11</li><br/><li><img src="" width="30px"><span>kai</span> 👍（3） 💬（0）<div>动态规划，感觉是面试必考内容，今天跟着这些题目再来复习一遍~</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（3） 💬（0）<div>这冲刺压力有点大了😓</div>2019-02-10</li><br/><li><img src="" width="30px"><span>kai</span> 👍（2） 💬（0）<div>8皇后问题

public class EightQueen {

    private static final int QUEEN_NUMBER = 8;      &#47;&#47; 皇后个数
    private int[] columns = new int[QUEEN_NUMBER];  &#47;&#47; 每个皇后存储的列 (row, col), row天然不相等
    private int total = 0;

    public int solution() {
        queen(0);
        return total;
    }

    private void queen(int row) {
        if (row == QUEEN_NUMBER) {
            total++;
        } else {
            for (int col = 0; col != QUEEN_NUMBER; col++) {
                columns[row] = col;
                if (isPut(row)) {
                    queen(row+1);
                }
            }
        }
    }

    private boolean isPut(int row) {
         for (int i = 0; i != row; i++) {
             if (columns[row] == columns[i] || row - i == Math.abs(columns[row]-columns[i])) {
                 return false;
             }
         }
         return true;
    }

}</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（1） 💬（0）<div>买卖股票的最佳时机 go 语言实现
package main

import &quot;fmt&quot;

func maxProfit(prices []int) int {
	max := -1
	for i := 0; i &lt; len(prices); i++ {
		for j := i + 1; j &lt; len(prices); j++ {
			profit := prices[j] - prices[i]
			if profit &gt; 0 &amp;&amp; profit &gt; max {
				max = profit
			}
		}
	}

	if max == -1 {
		return 0
	}

	return max
}

func main() {
	testData1 := []int{7, 1, 5, 3, 6, 4}
	testData2 := []int{7, 6, 4, 3, 1}

	fmt.Println(maxProfit(testData1))
	fmt.Println(maxProfit(testData2))
}
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（1） 💬（0）<div>正则表达式
public boolean isMatch(String s, String p) {

    if (s == null || p == null) {
        return false;
    }
    boolean[][] dp = new boolean[s.length()+1][p.length()+1];
    dp[0][0] = true;
    for (int i = 0; i &lt; p.length(); i++) {
        if (p.charAt(i) == &#39;*&#39; &amp;&amp; dp[0][i-1]) {
            dp[0][i+1] = true;
        }
    }
    for (int i = 0 ; i &lt; s.length(); i++) {
        for (int j = 0; j &lt; p.length(); j++) {
            if (p.charAt(j) == &#39;.&#39;) {
                dp[i+1][j+1] = dp[i][j];
            }
            if (p.charAt(j) == s.charAt(i)) {
                dp[i+1][j+1] = dp[i][j];
            }
            if (p.charAt(j) == &#39;*&#39;) {
                if (p.charAt(j-1) != s.charAt(i) &amp;&amp; p.charAt(j-1) != &#39;.&#39;) {
                    dp[i+1][j+1] = dp[i+1][j-1];
                } else {
                    dp[i+1][j+1] = (dp[i+1][j] || dp[i][j+1] || dp[i+1][j-1]);
                }
            }
        }
    }
    return dp[s.length()][p.length()];
}

leetcode的排名第一的答案，搬过来了</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/66/1f8fccfb.jpg" width="30px"><span>云之崖</span> 👍（0） 💬（0）<div>1年左右断断续续，终于学完了所有章节，这些练习题大部分不看提示都能搞得定了。</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/5d/15c4817a.jpg" width="30px"><span>xxxxL</span> 👍（0） 💬（0）<div>请问这个在哪里呢（详细可看 @Smallfly 整理的 Minimum Path Sum）</div>2020-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/bc/6d5affd3.jpg" width="30px"><span>大风歌</span> 👍（0） 💬（0）<div>第一遍</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/b9/946b181d.jpg" width="30px"><span>好运连连</span> 👍（0） 💬（0）<div>老师，具体的是这样，比如物流公司，用户下单，需要根据最短路线或者最少花费来找出合适的中转路线。 比如需要送货到B城市，A城市发货，但是，很多路线，需要选最合适的路线，比如A到D中转再到E中转最后送货到B。</div>2019-07-10</li><br/><li><img src="" width="30px"><span>Nereus</span> 👍（0） 💬（0）<div>零钱兑换 - GO

func coinChange(coins []int, amount int) int {
	var dp []int = make([]int, amount+1)
	for _, record := range coins {
		if amount &gt;= record {
			dp[record] = 1
		}
	}

	for i := 1; i &lt;= amount; i++ {
		dp[i] = amount + 1
		for _, record := range coins {
			if i-record &gt;= 0 {
				dp[i] = min(dp[i-record]+1, dp[i])
			}
		}
	}

	if dp[amount] &gt; amount {
		return -1
	}

	return dp[amount]
}

func min(a, b int) int {
	if a &lt; b {
		return a
	}
	return b
}

</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>买卖股票的最佳时机 go 语言实现

func maxProfit(prices []int) int {

	max:=0
	for i:=0;i&lt;len(prices);i++{
		for j:=0;j&lt;i;j++{
			num:=prices[i]-prices[j]
			if num&gt;max{
				max=num
			}
		}
	}
	return max
}</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>零钱兑换 go语言实现
func coinChange(coins []int, amount int) int {
    if amount==0{
		return 0
	}
	if len(coins)==0 &amp;&amp; amount!=0{
		return -1
	}

	isSmall:=true
	for _,coin:=range coins{
		if coin&lt;=amount{
			isSmall=false
		}
	}
	if isSmall{
		return -1
	}
	grid:=make([]int,amount+1)


	for _,coin:=range coins{
		if coin&lt;=amount{
			grid[coin]=1
		}
		if coin==amount{
			return 1
		}
	}
	for i:=2;i&lt;amount+1;i++{
		newGrid:=make([]int,amount+1)
		for j:=1;j&lt;amount+1;j++{
			for _,coin:=range coins{
				if grid[j]==1 &amp;&amp; j+coin&lt;=amount{
					newGrid[j]=1
					newGrid[j+coin]=1
				}
			}
		}
		grid=newGrid
		if grid[amount]==1{
			return i
		}
	}
	return -1
}</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>最小路径和 go实现

func minPathSum(grid [][]int) int {
    l:=len(grid)
	w:=len(grid[0])
	sum:=make([][]int,l)
	for i:=0;i&lt;l;i++{
		sum[i]=make([]int,w)
	}
	sum[0][0]=grid[0][0]
	for i:=1;i&lt;w;i++{
		sum[0][i]=grid[0][i]+sum[0][i-1]
	}
	for j:=1;j&lt;l;j++{
		sum[j][0]=grid[j][0]+sum[j-1][0]
	}
	for i:=1;i&lt;l;i++{
		for j:=1;j&lt;w;j++{
			sum[i][j]=less(sum[i-1][j],sum[i][j-1])+grid[i][j]
		}
	}

	return sum[l-1][w-1]
}

func less(i,j int) int{
	if i&gt;j{
		return j
	}else{
		return i
	}
}</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>正则表达式匹配 go语言实现，还是看别人的提示搞出来的
func isMatch(s string, p string) bool {
    if len(p)==0{
		if len(s)==0{
			return true
		}else{
			return false
		}
	}
	if len(p)==1{
		if len(s)==1 &amp;&amp; (s[0]==p[0] || p[0]==&#39;.&#39;){
			return true
		} else {
			return false
		}
	}
	if p[1]!=&#39;*&#39;{
		if len(s)==0{
			return false
		}
		return (s[0]==p[0]||p[0]==&#39;.&#39;) &amp;&amp; isMatch(s[1:],p[1:])
	}else{
		for ;len(s)!=0 &amp;&amp; (s[0]==p[0]||p[0]==&#39;.&#39;);{
			if isMatch(s,p[2:]){
				return true
			}
			s=s[1:]
		}
		return isMatch(s,p[2:])
	}



	return true
}</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f4/26b95f0b.jpg" width="30px"><span>TryTs</span> 👍（0） 💬（0）<div>&#47;&#47;零钱兑换
#include&lt;iostream&gt;
#include&lt;algorithm&gt;
using namespace std;
int coins[10];
int amount;
int k;&#47;&#47;k代表纸币的数目
int dp[20];&#47;&#47;代表面值最大，也可以采用动态扩容的方式 
int cmax = 32767;
int coinChange(int coins[],int amount){
	for(int i = 1;i &lt;= amount;i++){
		dp[i] = cmax;
		for(int j = 0;j &lt; k;j++){
			int t = coins[j];
			if(i &gt;= t &amp;&amp; coins[i - t] != cmax){
				dp[i] = min(dp[i - t] + 1,dp[i]);
			}
		}
	}
	if(dp[amount] &lt; cmax &amp;&amp; dp[amount] &gt; 0){
		return dp[amount];
	}
	else
		return -1;
}
int main(){
	k = 0;
	while(true){
		cin&gt;&gt;k;
		for(int i = 0;i &lt; k;i++){
			cin&gt;&gt;coins[i];
		} 
		cin&gt;&gt;amount;
		cout&lt;&lt;coinChange(coins,amount)&lt;&lt;endl;
	}	
}</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f4/26b95f0b.jpg" width="30px"><span>TryTs</span> 👍（0） 💬（0）<div>回溯0-1背包问题
#include&lt;iostream&gt;
using namespace std;
int v[10] = {2,2,4,6,3};
int M;&#47;&#47;代表背包的容积 
int n;
int cmax = 0;

void f(int w,int k){
&#47;&#47;	if(w == 0){
&#47;&#47;		if(w &gt; max) max = w;
&#47;&#47;	}
	if(w == M || k == n){
		if(w &gt; cmax) cmax = w;
		return ;
	} 
	f(w,k + 1);
	if(w + v[k] &lt;= M){
		f(w + v[k],k + 1);
	}
}
int main(){
	&#47;&#47;v[] = {2,2,4,6,3};
	M = 9;
	n = 5;
	f(0,0);
	cout&lt;&lt;cmax&lt;&lt;endl;
}</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f4/26b95f0b.jpg" width="30px"><span>TryTs</span> 👍（0） 💬（0）<div>#include&lt;iostream&gt;
#include&lt;cmath&gt;
using namespace std;

int queen[100];
int sum = 0;
int n;
void Print(){
	&#47;&#47;cout&lt;&lt;&quot;ss&quot;&lt;&lt;endl;
	for(int i = 0;i &lt; n;i++){
		cout&lt;&lt;&quot;(&quot;&lt;&lt;i+1&lt;&lt;&quot;,&quot;&lt;&lt;queen[i] + 1&lt;&lt;&quot;)&quot;;
	}
	sum++;
	cout&lt;&lt;endl;
}

void Queen(int queen[],int k){
	if(k == n) {
		Print(); 
		&#47;&#47;return ;
	}
    int j = 0;
    for(int i = 0;i &lt; n;i++){
    	&#47;&#47;j = i;
    	for( j = 0;j &lt; k;j++){
    		if((queen[j] == i)||(abs(queen[j] - i) == abs(k - j)))
				break;
		}
		if(j == k){
			queen[k] = i;
			Queen(queen,k+1); 
		}
	}
}
int main(){
	cin&gt;&gt;n;
	Queen(queen,0);
	cout&lt;&lt;sum&lt;&lt;endl;
}</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（0） 💬（0）<div>第一题，把39讲的代码改了一下。。。

public class Pattern {
  private boolean matched = false;
  private char[] pattern; &#47;&#47; 正则表达式
  private int plen; &#47;&#47; 正则表达式长度

  public Pattern(char[] pattern, int plen) {
    this.pattern = pattern;
    this.plen = plen;
  }

  public boolean match(char[] text, int tlen) { &#47;&#47; 文本串及长度
    matched = false;
    if (pattern[0]=&#39;*&#39;)
           return matched;
   int i = 0;
   int j = 0;
   while (i&lt;=plen&amp;&amp;j&lt;=tlen&amp;&amp;pattern[i]!=text[j]&amp;&amp;pattern[i]!=&#39;.&#39;)
         i++;
    rmatch(0, 0, text, tlen);
    return matched;
  }

  private void rmatch(int ti, int pj, char[] text, int tlen) {
    if (matched) return; &#47;&#47; 如果已经匹配了，就不要继续递归了
    if (ti == tlen){ &#47;&#47;文本串到结尾了
      matched = true; 
      return;
    }
    if (pattern[pj] == &#39;*&#39;) { &#47;&#47; * 匹配任意个字符
      for (int k = 0; k &lt;= tlen-ti&amp;&amp;tex[ti+k]==text[ti]; ++k) {
        rmatch(ti+k, pj+1, text, tlen);
      }
    } else if (pattern[pj] == &#39;.&#39;) { &#47;&#47; . 匹配 0 个或者 1 个字符
      rmatch(ti, pj+1, text, tlen); 
      rmatch(ti+1, pj+1, text, tlen); 
    } else if (ti &lt; tlen &amp;&amp; pattern[pj] == text[ti]) { &#47;&#47; 纯字符匹配才行
      rmatch(ti+1, pj+1, text, tlen);
    }
  }
}</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（0） 💬（0）<div>感觉，明天就是专栏的最后一天</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/9d/4d705f03.jpg" width="30px"><span>C_love</span> 👍（0） 💬（0）<div>Best Time to Buy and Sell Stoc...

class Solution {
    public int maxProfit(int[] prices) {
        if (prices == null || prices.length == 0 || prices.length == 1) {
            return 0;
        }
        
        int max = 0;
        int start = 0;
        
        for (int i = 1; i &lt; prices.length; i++) {
            if (prices[i] &lt; prices[start]) {
                start = i;
            } else {
                max = Math.max(max, prices[i] - prices[start]);
            }
        }
        return max;
    }
}</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/9a/f2c0a206.jpg" width="30px"><span>ext4</span> 👍（0） 💬（0）<div>最小路径和
class Solution {
  public:
    int minPathSum(vector&lt; vector&lt;int&gt; &gt;&amp; grid) {
      int m = grid.size();
      if (m == 0) return 0;
      int n = grid[0].size();
      if (n == 0) return 0;
      int matrix[m][n];
      int accum = 0;
      for (int i = 0; i &lt; m; i++) {
        accum += grid[i][0];
        matrix[i][0] = accum;
      }
      accum = 0;
      for (int j = 0; j &lt; n; j++) {
        accum += grid[0][j];
        matrix[0][j] = accum;
      }
      for (int i = 1; i &lt; m; i++) {
        for (int j = 1; j &lt; n; j++) {
          matrix[i][j] = min(matrix[i - 1][j], matrix[i][j - 1]) + grid[i][j];
        }
      }
      return matrix[m - 1][n - 1];
    }
};
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/4c/4f645bda.jpg" width="30px"><span>Kyle Liu</span> 👍（0） 💬（0）<div>有兴趣朋友可以将思路分析提交到https:&#47;&#47;github.com&#47;kylesliu&#47;awesome-golang-leetcode，欢迎大家提issue</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/8a/ae50ecbb.jpg" width="30px"><span>幻月剑</span> 👍（0） 💬（0）<div>一刷完成，题目没有做，算是草草学了一遍，等第二遍将题目都做完</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（0） 💬（0）<div>七七八八跟着老师复习了遍算法，印象最深刻的无疑是老师结合具体的应用场景讲利用的数据结构与算法！棒棒哒</div>2019-02-11</li><br/>
</ul>