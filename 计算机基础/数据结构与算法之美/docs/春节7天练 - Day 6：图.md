你好，我是王争。初六好！

为了帮你巩固所学，真正掌握数据结构和算法，我整理了数据结构和算法中，必知必会的30个代码实现，分7天发布出来，供你复习巩固所用。今天是第六篇。

和之前一样，你可以花一点时间，来手写这些必知必会的代码。写完之后，你可以根据结果，回到相应章节，有针对性地进行复习。做到这些，相信你会有不一样的收获。

* * *

## 关于图的几个必知必会的代码实现

### 图

- 实现有向图、无向图、有权图、无权图的邻接矩阵和邻接表表示方法
- 实现图的深度优先搜索、广度优先搜索
- 实现Dijkstra算法、A\*算法
- 实现拓扑排序的Kahn算法、DFS算法

## 对应的LeetCode练习题（@Smallfly 整理）

- Number of Islands（岛屿的个数）

英文版：[https://leetcode.com/problems/number-of-islands/description/](https://leetcode.com/problems/number-of-islands/description/)

中文版：[https://leetcode-cn.com/problems/number-of-islands/description/](https://leetcode-cn.com/problems/number-of-islands/description/)

- Valid Sudoku（有效的数独）

英文版：[https://leetcode.com/problems/valid-sudoku/](https://leetcode.com/problems/valid-sudoku/)
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/27/06/7ab75a5b.jpg" width="30px"><span>色即是空</span> 👍（2） 💬（1）<div>有效数独，就是穷举遍历方法求解，跟这一节练习的图，没有什么关系啊！放这个题目的时候是怎么考虑的啊？</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/9a/f2c0a206.jpg" width="30px"><span>ext4</span> 👍（1） 💬（1）<div>有效的数独
class Solution {
  public:
    bool isValidSudoku(vector&lt; vector&lt;char&gt; &gt;&amp; board) {
      set&lt;char&gt; numset;
      for (int i = 0; i &lt; 9; i++) {
        numset.clear();
        for (int j = 0; j &lt; 9; j++) {
          char val = board[i][j];
          if (val != &#39;.&#39;) {
            if (numset.count(val) != 0) return false;
            numset.insert(val);
          }
        }
      }
      for (int j = 0; j &lt; 9; j++) {
        numset.clear();
        for (int i = 0; i &lt; 9; i++) {
          char val = board[i][j];
          if (val != &#39;.&#39;) {
            if (numset.count(val) != 0) return false;
            numset.insert(val);
          }
        }
      }
      for (int i = 0; i &lt; 3; i++) {
        for (int j = 0; j &lt; 3; j++) {
          numset.clear();
          for (int p = 0; p &lt; 3; p++) {
            for (int q = 0; q &lt; 3; q++) {
              char val = board[i * 3 + p][j * 3 + q];
              if (val != &#39;.&#39;) {
                if (numset.count(val) != 0) return false;
                numset.insert(val);
              }
            }
          }
        }
      }
      return true;
    }
};</div>2019-02-10</li><br/><li><img src="" width="30px"><span>Nereus</span> 👍（0） 💬（1）<div>
并查集—go实现
func numIslands(grid [][]byte) int {
	if len(grid) == 0 {
		return 0
	}

	N := len(grid)*len(grid[0]) + 1

	u := NewUnionSet(N)

	for i := 0; i &lt; len(grid); i ++ {
		for j := 0; j &lt; len(grid[i]); j ++ {
			if grid[i][j] == &#39;1&#39; {
				&#47;&#47; 联通下边
				if i+1 &lt; len(grid) {
					if grid[i+1][j] == &#39;1&#39; {
						u.join(i*len(grid[i])+j, (i+1)*len(grid[i])+j)
					}
				}

				&#47;&#47; 联通右边
				if j+1 &lt; len(grid[i]) {
					if grid[i][j+1] == &#39;1&#39; {
						u.join(i*len(grid[i])+j, i*len(grid[i])+j+1)
					}
				}
			} else {
				u.join(i*len(grid[i])+j, N-1)
			}
		}
	}

	return  u.counts() -1
}

type UnionSet []int

func NewUnionSet(n int) UnionSet {
	var u UnionSet
	u = make([]int, n)
	for i := 0; i &lt; len(u); i ++ {
		u[i] = i
	}
	return u

}

func (u UnionSet) find(i int) int {
	tmp := i
	for u[tmp] != tmp {
		tmp = u[tmp]
	}

	j := i
	for j != tmp {
		tt := u[j]
		u[j] = tmp
		j = tt
	}

	return tmp
}

func (u UnionSet) connected(i, j int) bool {
	return u.find(i) == u.find(j)
}

func (u UnionSet) counts() int {
	var count int
	for idx, rec := range u {
		if idx == rec {
			count++
		}
	}
	return count
}

func (u UnionSet) join(i, j int) {
	x, y := u.find(i), u.find(j)
	if x != y {
		if y &gt; x {
			u[x] = y
		} else {
			u[y] = x
		}
	}
}
</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（1）<div>Number of Islands（岛屿的个数）go语言实现，亲测通过：
func numIslands(grid [][]byte) int {

	isSearch:=make([][]int,len(grid))
	island:=0
	for i:=0;i&lt;len(isSearch);i++{
		isSearch[i]=make([]int,len(grid[0]))
	}
	for i,line:=range grid{
		for j,_:=range line{
			if isSearch[i][j]==0 &amp;&amp; grid[i][j]==&#39;1&#39;{
				Search(grid,isSearch,i,j)
				island++
			}

		}
	}
	return island
}

func Search(grid [][]byte,isSearch [][]int, i int,j int){
	if isSearch[i][j]==1{
		return
	}
	isSearch[i][j]=1
	if grid[i][j]==&#39;1&#39;{
		if i&gt;=1{
			Search(grid,isSearch,i-1,j)
		}
		if i&lt;len(grid)-1{
			Search(grid,isSearch,i+1,j)
		}
		if j&gt;=1{
			Search(grid,isSearch,i,j-1)
		}
		if j&lt;len(grid[0])-1{
			Search(grid,isSearch,i,j+1)
		}
	}else{
		return
	}
}
</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（1）<div>    岛屿数Java实现
public int numIslands(char[][] grid) {
        int m = grid.length;
        if (m == 0) return 0;
        int n = grid[0].length;
        
        int ans = 0;
        for (int y = 0; y &lt; m; ++y)
            for (int x = 0; x &lt; n; ++x)
                if (grid[y][x] == &#39;1&#39;) {
                    ++ans;
                    dfs(grid, x, y, n, m);
                }
        
        return ans;
    }
    
    private void dfs(char[][] grid, int x, int y, int n, int m) {
        if (x &lt; 0 || y &lt; 0 || x &gt;= n || y &gt;= m || grid[y][x] == &#39;0&#39;)
            return;
        grid[y][x] = &#39;0&#39;;
        dfs(grid, x + 1, y, n, m);
        dfs(grid, x - 1, y, n, m);
        dfs(grid, x, y + 1, n, m);
        dfs(grid, x, y - 1, n, m);
    }</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（0） 💬（1）<div>有效的数独 go 语言实现
package main

import (
	&quot;fmt&quot;
)

func hasRepeatedNumbers(numbers []byte) bool {
	var numbersExistFlag [9]bool
	for _, num := range numbers {
		if num == &#39;.&#39; {
			continue
		}
		index := num - &#39;0&#39; - 1
		if numbersExistFlag[index] {
			return true
		}
		numbersExistFlag[index] = true
	}
	return false
}

func isValidSudoku(board [][]byte) bool {
	sudokuSize := 9
	sudokuUnitSize := 3
	for _, line := range board {
		if hasRepeatedNumbers(line) {
			return false
		}
	}

	for columnIndex := 0; columnIndex &lt; sudokuSize; columnIndex++ {
		columnNumbers := make([]byte, 0)
		for lineIndex := 0; lineIndex &lt; sudokuSize; lineIndex++ {
			columnNumbers = append(columnNumbers, board[lineIndex][columnIndex])
		}
		if hasRepeatedNumbers(columnNumbers) {
			return false
		}
	}

	sudokuUnitCountEachLine := sudokuSize &#47; sudokuUnitSize
	for i := 0; i &lt; sudokuUnitCountEachLine; i++ {
		for j := 0; j &lt; sudokuUnitCountEachLine; j++ {
			sudokuUnitNumbers := make([]byte, 0)
			for _, line := range board[i*3 : (i+1)*3] {
				sudokuUnitNumbers = append(sudokuUnitNumbers, line[j*3:(j+1)*3]...)
			}

			if hasRepeatedNumbers(sudokuUnitNumbers) {
				return false
			}
		}
	}

	return true
}

func main() {
	testData1 := [][]byte{
		{&#39;5&#39;, &#39;3&#39;, &#39;.&#39;, &#39;.&#39;, &#39;7&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;},
		{&#39;6&#39;, &#39;.&#39;, &#39;.&#39;, &#39;1&#39;, &#39;9&#39;, &#39;5&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;},
		{&#39;.&#39;, &#39;9&#39;, &#39;8&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;6&#39;, &#39;.&#39;},
		{&#39;8&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;6&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;3&#39;},
		{&#39;4&#39;, &#39;.&#39;, &#39;.&#39;, &#39;8&#39;, &#39;.&#39;, &#39;3&#39;, &#39;.&#39;, &#39;.&#39;, &#39;1&#39;},
		{&#39;7&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;2&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;6&#39;},
		{&#39;.&#39;, &#39;6&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;2&#39;, &#39;8&#39;, &#39;.&#39;},
		{&#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;4&#39;, &#39;1&#39;, &#39;9&#39;, &#39;.&#39;, &#39;.&#39;, &#39;5&#39;},
		{&#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;.&#39;, &#39;8&#39;, &#39;.&#39;, &#39;.&#39;, &#39;7&#39;, &#39;9&#39;}}
	fmt.Println(isValidSudoku(testData1))
}</div>2019-02-10</li><br/><li><img src="" width="30px"><span>kai</span> 👍（3） 💬（0）<div>今天根据老师的课程，总结了一下图的相关知识点，然后用代码实现了一下图的相关的算法，感觉图还是要难于其他数据结构，需要接着多练习~</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/99/44378317.jpg" width="30px"><span>李皮皮皮皮皮</span> 👍（3） 💬（0）<div>图很复杂😢</div>2019-02-10</li><br/><li><img src="" width="30px"><span>kai</span> 👍（1） 💬（0）<div>实现图的深度优先搜索、广度优先搜索:

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;

public class BFSAndDFS {

    class Node {
        public int value; &#47;&#47;Node 值
        public int in;    &#47;&#47;入度：指向该节点的边有几条
		public int out;   &#47;&#47;出度：指向其他节点的边有几条
		public ArrayList&lt;Node&gt; nexts;
		public ArrayList&lt;Edge&gt; edges;

		public Node(int value) {
			this.value = value;
			this.in = 0;
			this.out = 0;
			this.nexts = new ArrayList&lt;&gt;();
			this.edges = new ArrayList&lt;&gt;();
		}
	}
	
    public static void bfs(Node node) {
        if (node == null) {
            return;
        }

        Queue&lt;Node&gt; queue = new LinkedList&lt;&gt;();
        HashSet&lt;Node&gt; set = new HashSet&lt;&gt;();
        queue.add(node);
        set.add(node);
        while (!queue.isEmpty()) {
            Node cur = queue.poll();
            System.out.print(cur.value + &quot; &quot;);
            for (Node next : cur.nexts) {
                if (!set.contains(next)) {
                    queue.add(next);
                    set.add(next);
                }
            }
        }
    }

    public static void dfs(Node node) {
        if (node == null) {
            return;
        }

        Stack&lt;Node&gt; stack = new Stack&lt;&gt;();
        HashSet&lt;Node&gt; set = new HashSet&lt;&gt;();
        stack.push(node);
        set.add(node);
        System.out.print(node.value + &quot; &quot;);
        while (!stack.isEmpty()) {
            Node cur = stack.pop();
            for (Node next : cur.nexts) {
                if (!set.contains(next)) { 
                    stack.push(cur);       
                    stack.push(next);
                    set.add(next);         
                    System.out.print(next.value + &quot; &quot;);
                    break;                
                }
            }
        }
    }
}</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（1） 💬（1）<div>1.在邻接矩阵中找出连通图个数即可。在每个顶点执行DFS或BFS，执行次数即为岛屿数，也可以使用并查集。

2. 依次考察9✖️9数独各行各列是否有重复数字（可以用9位数组统计），然后再考察每个3✖️3子矩阵是否有重复数字。都没有则成功。</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>有效数独
int[][] row = new int[10][10];
        int[][] col = new int[10][10];

        boolean retFlag = true;
        for (int i = 0; i &lt; grid.length; i += 3) {
            for (int j = 0; j &lt; grid[0].length; j += 3) {
                boolean xx = xx(row, col, grid, i, j);&#47;&#47;模块左上角第一个元素位置
                if (!xx) {
                    retFlag = false;
                    break;
                }
            }
            if (!retFlag) {
                break;
            }
        }
public static boolean xx(int[][] row, int[][] col, String[][] grid, int i, int j) {
        Map map = new HashMap();
        for (int ii = i; ii &lt; i + 3; ii++) {
            for (int jj = j; jj &lt; j + 3; jj++) {
                if (map.get(grid[ii][jj]) != null) {
                    return false;
                }
                if (!&quot;.&quot;.equals(grid[ii][jj])) {
                    map.put(grid[ii][jj], &quot;1&quot;);
                    int haveRow = row[ii][Integer.parseInt(grid[ii][jj])];
                    int haveCol = col[jj][Integer.parseInt(grid[ii][jj])];
                    if (haveCol == 1 || haveRow == 1) {
                        return false;
                    }
                    row[ii][Integer.parseInt(grid[ii][jj])] = col[jj][Integer.parseInt(grid[ii][jj])] = 1;
                }
            }
        }
        return true;
    }</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>岛屿的个数
public static void main(String[] args) {
        int[][] grid = new int[][]{
                {1, 1, 0, 0, 0},
                {1, 1, 0, 0, 0},
                {0, 0, 1, 0, 0},
                {0, 0, 0, 1, 1}
        };
        int cnt = 0;
        for (int i = 0; i &lt; grid.length; i++) {
            for (int j = 0; j &lt; grid[0].length; j++) {
                if (grid[i][j] == 1) {
                    xx(grid, i, j);
                    cnt++;
                }
            }
        }

        System.out.println(cnt);
    }

    public static void xx(int[][] grid, int i, int j) {
        if (i &lt; 0 || j &lt; 0 || i &gt;= grid.length || j &gt;= grid[0].length) {
            return;
        }
        if (grid[i][j] == 0) {
            return;
        }
        &#47;&#47;等于1
        grid[i][j] = 0;
        if (i &gt; 0) {
            xx(grid, i - 1, j);
        }
        if (j &gt; 0) {
            xx(grid, i, j - 1);
        }
        if (i &lt; grid.length - 1) {
            xx(grid, i + 1, j);
        }
        if (j &lt; grid[0].length - 1) {
            xx(grid, i, j + 1);
        }
    }</div>2023-07-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLQqlI43akVtRAwhT5nY4rWeRebSbvTFtn7quL7EoGJ1G923eL5LcHM2yBOFKvmKxyFiaSSrkG31iaw/132" width="30px"><span>Geek_97afb1</span> 👍（0） 💬（0）<div>入坑第一百天
                       -brandon</div>2022-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/9a/ef8c4644.jpg" width="30px"><span>Bax</span> 👍（0） 💬（0）<div>数独，还没测试</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/33/bcf37f50.jpg" width="30px"><span>阿甘</span> 👍（0） 💬（0）<div>class Solution {
  public int numIslands(char[][] grid) {
        int num = 0;
        for (int i = 0; i &lt; grid.length; i++) { &#47;&#47; rows
            for (int j = 0; j &lt; grid[i].length; j++) { &#47;&#47; cols
                if (grid[i][j] == &#39;1&#39;) {
                    num++;
                    dfs(grid, i, j, grid.length, grid[i].length);
                }
            }
        }
        return num;
    }

    private void dfs(char[][] grid, int i, int j, int rows, int cols) {
        if (i &lt; 0 || j &lt; 0 || i &gt;= rows || j &gt;= cols || grid[i][j] == &#39;0&#39;) {
            return;
        }
        grid[i][j] = &#39;0&#39;; &#47;&#47; visit

        dfs(grid, i - 1, j, rows, cols);
        dfs(grid, i, j - 1, rows, cols);
        dfs(grid, i + 1, j, rows, cols);
        dfs(grid, i, j + 1, rows, cols);
    }
}</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/44/8a/f877e599.jpg" width="30px"><span>yaoyue</span> 👍（0） 💬（0）<div>幸甚至哉，歌以咏志</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（0） 💬（0）<div>有效的数独确实可以用暴力匹配法解决</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>Valid Sudoku（有效的数独）go语言实现

func isValidSudoku(board [][]byte) bool {

	isValid:=true
	for i:=0;i&lt;9;i++{
		for j:=0;j&lt;9;j++{
			if board[i][j]==&#39;.&#39; {
				continue
			}else{
				if !judgeLine(board,i,j){
					return false
				}
			}
		}
	}

	return isValid
}

func judgeLine(board [][]byte,i,j int) bool{
	hash:=make(map[byte]int,9)
	for k:=0;k&lt;9;k++{
		if board[i][k]!=&#39;.&#39;{
			if hash[board[i][k]]==0{
				hash[board[i][k]]=1
			}else{
				return false
			}
		}
	}
	hash=make(map[byte]int,9)
	for k:=0;k&lt;9;k++{
		if board[k][j]!=&#39;.&#39; {
			if hash[board[k][j]]==0{
				hash[board[k][j]]=1
			}else{
				return false
			}
		}
	}
	hash=make(map[byte]int,9)
	for m:=i&#47;3*3;m&lt;i&#47;3*3+3;m++{
		for n:=j&#47;3*3;n&lt;j&#47;3*3+3;n++{
			if board[m][n]!=&#39;.&#39;{
				if hash[board[m][n]]==0{
					hash[board[m][n]]=1
				}else{
					return false
				}
			}
		}
	}
	return true

}


</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/88/be4fe19e.jpg" width="30px"><span>molybdenum</span> 👍（0） 💬（0）<div>island 我用的深搜，把所有的1探索，用visited保存访问过访问的，搜索次数便是岛屿个数</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/6f/aacb013d.jpg" width="30px"><span>黄丹</span> 👍（0） 💬（0）<div>已经初六啦，就快要到去学校的时间了，难受。
图的邻接矩阵表示法是使用一个二维数组int[0..n-1][0...n-1]来保存顶点和边的，对于无权图，1表示有边，0表示两个顶点没有变，有权图，值代表权重。
图的邻接表则是采用数组+链表的结构来表示的，数组里存的是顶点，链表存储的是边的信息，当然链表也可以换做二叉搜索树，散列表等高效查找的数据结构。
今天的两道leetcode题的解题思路和代码如下：
1.	Number of Islands （岛屿的个数）
解题思路：遍历数组，遇到1时，使用深度&#47;广度遍历，将连通的1都置为0，然后将岛屿个数加1.
代码：https:&#47;&#47;github.com&#47;yyxd&#47;leetcode&#47;blob&#47;master&#47;src&#47;leetcode&#47;graph&#47;Problem200_NumberofIslands.java
2.	Valid Sudoku  （有效的数独）
解题思路：emm，不知道为什么这道题要放在图论的专题下，我的解法就是横着一行行判断，竖着一列列的判断，然后每个3*3的子块进行判断。没有用到图的知识。
代码：https:&#47;&#47;github.com&#47;yyxd&#47;leetcode&#47;blob&#47;master&#47;src&#47;leetcode&#47;graph&#47;Problem36_ValidSudoku.java
</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（0） 💬（0）<div>基于临接表实现的联通分量求法， go 语言实现：
package graph_basics

type Components struct {
	graph   Graph
	visited []bool
	id      []int
	ccount  int
}

func InitComponents(g Graph) *Components {
	return &amp;Components{
		graph:   g,
		visited: make([]bool, g.V()),
		id:      make([]int, g.V()),
		ccount:  0,
	}
}

func (c *Components) dfs(index int) {
	c.visited[index] = true
	c.id[index] = c.ccount
	adj := c.graph.Iterator(index)
	for i := range adj {
		if !c.visited[adj[i]] {
			c.dfs(adj[i])
		}
	}
}

func (c *Components) CalculateComponents() {
	for i := 0; i &lt; c.graph.V(); i++ {
		if c.visited[i] {
			continue
		}
		c.dfs(i)
		c.ccount++
	}
}

func (c *Components) Count() int {
	return c.ccount
}

func (c *Components) IsConnected(p int, q int) bool {
	return c.id[p] == c.id[q]
}

临接表的实现：
package graph_basics

import &quot;fmt&quot;

type SparseGraph struct {
	v      int
	e      int
	direct bool
	g      [][]int
}

func InitSparseGraph(n int, direct bool) *SparseGraph {
	graph := make([][]int, n)
	return &amp;SparseGraph{
		v:      n,
		e:      0,
		direct: direct,
		g:      graph,
	}
}

func (sg *SparseGraph) V() int {
	return sg.v
}

func (sg *SparseGraph) E() int {
	return sg.e
}

func (sg *SparseGraph) AddEdge(p int, q int) {
	sg.g[p] = append(sg.g[p], q)
	if !sg.direct {
		sg.g[q] = append(sg.g[q], p)
	}

	sg.e++
}

func (sg *SparseGraph) HasEdge(p int, q int) bool {
	for i := 0; i &lt; len(sg.g[p]); i++ {
		if sg.g[p][i] == q {
			return true
		}
	}
	return false
}

func (sg *SparseGraph) Show() {
	for i := range sg.g {
		fmt.Printf(&quot;vertex %d :\t&quot;, i)
		for j := range sg.g[i] {
			fmt.Printf(&quot;%d\t&quot;, sg.g[i][j])
		}
		fmt.Println()
	}
}

func (sg *SparseGraph) Iterator(v int) []int {
	return sg.g[v]
}</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/f6/1ef70cab.jpg" width="30px"><span>你看起来很好吃</span> 👍（0） 💬（0）<div>岛屿个数python实现(广度优先搜索算法)：
def numIslands(self, grid):
    if not grid:
        return 0
        
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == &#39;1&#39;:
                self.dfs(grid, i, j)
                count += 1
    return count

def dfs(self, grid, i, j):
    if i&lt;0 or j&lt;0 or i&gt;=len(grid) or j&gt;=len(grid[0]) or grid[i][j] != &#39;1&#39;:
        return
    grid[i][j] = &#39;#&#39;
    self.dfs(grid, i+1, j)
    self.dfs(grid, i-1, j)
    self.dfs(grid, i, j+1)
    self.dfs(grid, i, j-1)</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（0） 💬（0）<div>island个数，从一个点从发，判断一个island的逻辑是如果本身点是water，那么必然不是island，如果是陆地，说明它能扩展成一个island，那么向上下左右进行扩展，然后再以扩展的陆地点又一直递归扩展，直到所有边界为0。而判断island的个数，就在此基础上去遍历所有点，并加上一个boolean[][]记录每个点是否已经被遍历或者扩展过。</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/9d/4d705f03.jpg" width="30px"><span>C_love</span> 👍（0） 💬（0）<div>Valid Sudoku

class Solution {
    public boolean isValidSudoku(char[][] board) {
        for (int row = 0; row &lt; 9; row++) {
            for (int col = 0; col &lt; 9; col++) {
                if (board[row][col] == &#39;.&#39;) continue;
                if (!isValid(board, row, col)) return false;
            }
        }
        return true;
    }
    
    private boolean isValid(char[][] board, final int row, final int col){
        char target=board[row][col];
        &#47;&#47;check rows
        for (int i = 0; i &lt; 9; i++) {
            if (i == row) continue;
            if (board[i][col] == target) return false;
        }
        
        &#47;&#47;check cols
        for (int i = 0; i &lt; 9; i++) {
            if (i == col) continue;
            if (board[row][i] == target) return false;
        }
        
        &#47;&#47;check 3*3
        int rowStart = row &#47; 3 * 3, colStart = col &#47; 3 * 3;
        for (int i = rowStart; i &lt; rowStart + 3; i++) {
            for (int j = colStart; j &lt; colStart + 3; j++) {
                if (i == row &amp;&amp; j == col) continue;
                if (board[i][j] == target) return false;
            }
        }
        
        return true;
    }
}</div>2019-02-10</li><br/>
</ul>