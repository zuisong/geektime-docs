你好，我是王争。春节假期进入尾声了。你现在是否已经准备返回工作岗位了呢？今天更新的是测试题的第五篇，我们继续来复习。

* * *

## 关于二叉树和堆的7个必知必会的代码实现

### 二叉树

- 实现一个二叉查找树，并且支持插入、删除、查找操作
- 实现查找二叉查找树中某个节点的后继、前驱节点
- 实现二叉树前、中、后序以及按层遍历

### 堆

- 实现一个小顶堆、大顶堆、优先级队列
- 实现堆排序
- 利用优先级队列合并K个有序数组
- 求一组动态数据集合的最大Top K

## 对应的LeetCode练习题（@Smallfly 整理）

- Invert Binary Tree（翻转二叉树）

英文版：[https://leetcode.com/problems/invert-binary-tree/](https://leetcode.com/problems/invert-binary-tree/)

中文版：[https://leetcode-cn.com/problems/invert-binary-tree/](https://leetcode-cn.com/problems/invert-binary-tree/)

- Maximum Depth of Binary Tree（二叉树的最大深度）

英文版：[https://leetcode.com/problems/maximum-depth-of-binary-tree/](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

中文版：[https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/](https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/)
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/aa/32fc0d54.jpg" width="30px"><span>失火的夏天</span> 👍（4） 💬（1）<div>&#47;&#47; 翻转二叉树
public TreeNode invertTree(TreeNode root) {
        if(root == null){
			return root;
		}
		TreeNode node = root;
		Queue&lt;TreeNode&gt; queue = new LinkedList&lt;&gt;();
		queue.add(node);
		while(!queue.isEmpty()){
			node = queue.poll();
			TreeNode tempNode = node.left;
			node.left = node.right;
			node.right = tempNode;
			if(node.left != null){
				queue.offer(node.left);
			}
			if(node.right != null){
				queue.offer(node.right);
			}
		}
        return root;
    }
&#47;&#47; 二叉树的最大深度
public int maxDepth(TreeNode root) {
        if(root == null) return 0;
        return Math.max(maxDepth(root.left), maxDepth(root.right))+1;   
    }
&#47;&#47; 验证二叉查找树
public boolean isValidBST(TreeNode root) {
        if (root == null) {
			return true;
		}
		Stack&lt;TreeNode&gt; stack = new Stack&lt;&gt;();
		TreeNode node = root;
		TreeNode preNode = null;
		while(node != null || !stack.isEmpty()){
			stack.push(node);
			node = node.left;
			while(node == null &amp;&amp; !stack.isEmpty()){
				node = stack.pop();
				if(preNode != null){
					if(preNode.val &gt;= node.val){
						return false;
					}
				}
				preNode = node;
				node = node.right;
			}
		}
        return true;
    }
&#47;&#47; 路径总和
public boolean hasPathSum(TreeNode root, int sum) {
        if (root == null) {
            return false;
        }
        return hasPathSum(root, root.val, sum);
    }

    public boolean hasPathSum(TreeNode root, int tmp, int sum) {
        if (root == null) {
            return false;
        }
        if (root.left == null &amp;&amp; root.right == null) {
            return tmp == sum;
        }
        if (root.left == null) {
            return hasPathSum(root.right, root.right.val + tmp, sum);
        }
        if (root.right == null) {
            return hasPathSum(root.left, root.left.val + tmp, sum);
        }
        return hasPathSum(root.left, root.left.val + tmp, sum) ||
                hasPathSum(root.right, root.right.val + tmp, sum);
    }</div>2019-02-09</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/QBySItkygOZskp8mt8kgglaFib73hTCsBBd06krzqqnNfWYg1auPVy1W5rJw9d6f7gqYKiaZnflUEH2iaZLAvfVvw/132" width="30px"><span>啵啵啵</span> 👍（0） 💬（1）<div>作者可以提供pdf版的课程资料吗，不然我觉得不值，因为不能大量复制，不能形成书面笔记，毕竟我付费了。</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（0） 💬（1）<div>Golang max depth
&#47;**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 *&#47;
func maxDepth(root *TreeNode) int {
    
    if root == nil {
        return 0
    }
         
    if root.Left == nil &amp;&amp; root.Right == nil {
         return 1
    }
        
    return int(math.Max(float64(maxDepth(root.Left)), float64(maxDepth(root.Right)))) + 1
    
}</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/6f/aacb013d.jpg" width="30px"><span>黄丹</span> 👍（0） 💬（1）<div>王争老师新年的第五天快乐！
放上今天LeetCode四题的代码和思路
解题思路：对于树，这个结构很特殊，树是由根节点，根节点的左子树，根节点的右子树组成的，定义的时候就是一个递归的定义。因此在解决与树相关的问题的时候，经常会用到递归。今天的四题都不例外。
翻转二叉树：就是递归的让节点的左子树指向右子树，右子树指向左子树。
二叉树的最大深度：当前深度=1+Max(左子树深度，右子树深度)，递归的结束条件为节点为null，或者是一个叶节点。
验证二叉查找树：一颗树是二叉查找树必须满足：当前的节点&gt;=左子树&amp;&amp;当前的节点&lt;=右子树，左子树是二叉查找树，右子树是二叉查找树，也是递归的定义。
路径总和：遍历树的路径，看是否和为sum值（树的遍历也是递归的哦）
四道题的代码在：https:&#47;&#47;github.com&#47;yyxd&#47;leetcode&#47;tree&#47;master&#47;src&#47;leetcode&#47;tree
</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/99/44378317.jpg" width="30px"><span>李皮皮皮皮皮</span> 👍（20） 💬（0）<div>平衡树的各种操作太烧脑了，左旋右旋，红黑树就更别提了。过段时间就忘。😢</div>2019-02-09</li><br/><li><img src="" width="30px"><span>kai</span> 👍（5） 💬（0）<div>树的前中后序遍历-递归实现：

public class TreeTraversal {

    public static class Node {
        public int value;
        public Node left;
        public Node right;

        public Node(int value) {
            this.value = value;
        }
    }

    &#47;&#47; 二叉树的递归遍历
    public static void preOrderRecursive(Node head) {
        if (head == null) {
            return;
        }

        System.out.print(head.value + &quot; &quot;);
        preOrderRecursive(head.left);
        preOrderRecursive(head.right);
    }

    public static void inOrderRecursive(Node head) {
        if (head == null) {
            return;
        }

        inOrderRecursive(head.left);
        System.out.print(head.value + &quot; &quot;);
        inOrderRecursive(head.right);
    }

    public static void postOrderRecursive(Node head) {
        if (head == null) {
            return;
        }

        postOrderRecursive(head.left);
        postOrderRecursive(head.right);
        System.out.print(head.value + &quot; &quot;);
    }

}
</div>2019-02-11</li><br/><li><img src="" width="30px"><span>kai</span> 👍（2） 💬（0）<div>树的前中后序遍历-非递归实现：
import java.util.Stack;


public class TreeTraversal {
    public static class Node {
        public int value;
        public Node left;
        public Node right;
        public Node(int value) {
            this.value = value;
        }
    }
    &#47;&#47; 二叉树的非递归遍历
    public static void preOrder(Node head) {
        System.out.print(&quot;pre-order: &quot;);
        if (head == null) {
            return;
        }
        Stack&lt;Node&gt; s = new Stack&lt;&gt;();
        s.push(head);
        while (!s.isEmpty()) {
            head = s.pop();
            System.out.print(head.value + &quot; &quot;);
            if (head.right != null) {
                s.push(head.right);
            }

            if (head.left != null) {
                s.push(head.left);
            }
        }
        System.out.println();
    }

    public static void inOrder(Node head) {
        System.out.print(&quot;in-order: &quot;);
        if (head == null) {
            return;
        }
        Stack&lt;Node&gt; s = new Stack&lt;&gt;();
        while (!s.isEmpty() || head != null) {
            if (head != null) {
                s.push(head);
                head = head.left;
            } else {
                head = s.pop();
                System.out.print(head.value + &quot; &quot;);
                head = head.right;
            }
        }
        System.out.println();
    }

    public static void postOrder(Node head) {
        System.out.print(&quot;pos-order: &quot;);
        if (head == null) {
            return;
        }

        Stack&lt;Node&gt; tmp = new Stack&lt;&gt;();
        Stack&lt;Node&gt; s = new Stack&lt;&gt;();

        tmp.push(head);
        while(!tmp.isEmpty()) {
            head = tmp.pop();
            s.push(head);

            if (head.left != null) {
                tmp.push(head.left);
            }

            if (head.right != null) {
                tmp.push(head.right);
            }
        }

        while (!s.isEmpty()) {
            System.out.print(s.pop().value + &quot; &quot;);
        }

        System.out.println();
    }
}
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/2b/9db9406b.jpg" width="30px"><span>星夜</span> 👍（1） 💬（0）<div>二叉查找树节点删除逻辑，不知道对不对：
    public boolean removeNode(int val) {
        if (null == root) {
            return false;
        }

        if (root.val == val) {
            &#47;&#47; 根节点
            root = replace(root);
        } else {
            Node parent = findParent(val);
            if (null == parent) {
                return false;
            }
            if (parent.left.val == val) {
                parent.left = replace(parent.left);
            } else if (parent.right.val == val) {
                parent.right = replace(parent.right);
            }
        }
        return true;
    }

    private Node replace(Node cur) {
        Node res = null;
        if (cur.left != null &amp;&amp; cur.right != null) {
            res = cur.left;
            res.left = replace(cur.left);
            res.right = cur.right;
        } else if (cur.left != null) {
            res = cur.left;
        } else if (cur.right != null) {
            return cur.right;
        }
        &#47;&#47; 置空
        cur.left = null;
        cur.right = null;
        return res;
    }</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/59/b515a473.jpg" width="30px"><span>Abner</span> 👍（1） 💬（0）<div>java实现二叉树前序、中序、后序和层次遍历
代码如下：
package tree;

import java.util.LinkedList;
import java.util.Queue;

public class BinaryTree {
    
    private Node root = null;
    
    public static class Node {
        
        private String data;
        private Node left;
        private Node right;
        
        public Node(String data, Node left, Node right) {
            this.data = data;
            this.left = left;
            this.right = right;
        }
    }
    
    public void preOrder(Node root) {
        if (null == root) {
            return ;
        }
        System.out.print(root.data + &quot; &quot;);
        preOrder(root.left);
        preOrder(root.right);
    }
    
    public void inOrder(Node root) {
        if (null == root) {
            return ;
        }
        inOrder(root.left);
        System.out.print(root.data + &quot; &quot;);
        inOrder(root.right);
    }
    
    public void postOrder(Node root) {
        if (null == root) {
            return ;
        }
        postOrder(root.left);
        postOrder(root.right);
        System.out.print(root.data + &quot; &quot;);
    }
    
    public void traverseByLayer(Node root) {
        if (null == root) {
            return ;
        }
        Queue&lt;Node&gt; queue = new LinkedList&lt;Node&gt;();
        queue.add(root);
        while (!queue.isEmpty()) {
            Node pNode = queue.peek();
            System.out.print(pNode.data + &quot; &quot;);
            queue.poll();
            if (root.left != null) {
                queue.add(root.left);
            }
            if (root.right != null) {
                queue.add(root.right);
            }
        }
    }
}
</div>2019-02-14</li><br/><li><img src="" width="30px"><span>kai</span> 👍（1） 💬（0）<div>今天看了一下这一节的题目，发现校招面试的时候都考过，今天又刷了一下，总结了一波，相应的知识点也总结了一下~</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（1） 💬（0）<div>今天的题目很适合递归实现，当然递归公式离代码实现还是存在一定距离。
1.翻转二叉树（T）｛
当T为Null时则返回；
翻转二叉树（T的左子树）；
翻转二叉树（T的右子树）；
若T不为叶节点，则交换T的左右子树位置；
｝

2.最大深度（T）｛
当T为Null时，return 0；
return Max（最大深度（T左子树）+1，最大深度（T右子树）+1）；
｝
函数返回值即为最大深度。

3.验证二叉查找树（T，&amp;最大值，&amp;最小值）｛
当T为Null时，return true；
当T为叶节点时，最小值=最大值=当前节点，返回true；
左最大值=左最小值=T的值；
验证二叉查找树（T的左子树，&amp;左最大值，&amp;左最小值）；
右最大值=右最小值=T的值；
验证（T的右子树，&amp;右最大值，&amp;右最小值）；
T的值小于等于右最小值，并且大于等于左最大值时，最大值=右最大值，最小值=左最小值，之后返回true，否则返回false并结束。
｝
函数最终返回true则验证成功。

4.计算路径和（T，sum）｛
若T为Null返回false；
若T是叶节点，如果sum+T的值=目标值则返回true并结束，否则返回false；
计算路径和（T的左子树，sum+T的值）；
计算路径和（T的右子树，sum+T的值）；
｝
计算路径和（T，0）返回true时则存在于目标值相同的路径之和；</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（1） 💬（0）<div>二叉树的最大深度 go 语言实现
&#47;**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 *&#47;
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }
    
    leftDepth :=0
    rightDepth :=0
    if root.Left != nil {
        leftDepth = maxDepth(root.Left)
    }
    
    if root.Right != nil {
        rightDepth = maxDepth(root.Right)
    }
    
    if leftDepth &gt;= rightDepth {
        return leftDepth + 1
    } else {
        return rightDepth + 1
    }
}</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>路径总和
private static boolean deep(TreeNode treeNode, int targetSum, int curr) {
        if (treeNode == null &amp;&amp; curr == targetSum) {
            return true;
        }
        if (treeNode == null) {
            return false;
        }
        if (curr &gt;= targetSum) {
            return false;
        }
        return deep(treeNode.left, targetSum, curr + treeNode.val) || deep(treeNode.right, targetSum, curr + treeNode.val);
    }</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>验证二叉查找树
private static boolean deep(TreeNode treeNode) {
        if (treeNode == null) {
            return true;
        }
        int val = treeNode.val;
        if (treeNode.left != null &amp;&amp; treeNode.left.val &gt; val) {
            return false;
        }
        if (treeNode.right != null &amp;&amp; treeNode.right.val &lt; val) {
            return false;
        }
        return deep(treeNode.left) &amp;&amp; deep(treeNode.right);
    }</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>最大深度
private static int deep(TreeNode treeNode, int dep) {
        if (treeNode == null) {
            return dep;
        }
        return Math.max(deep(treeNode.left, dep + 1), deep(treeNode.right, dep + 1));
    }</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>翻转二叉树
    public static void main(String[] args) {
        TreeNode treeNode = new TreeNode(4);
        treeNode.left = new TreeNode(2);
        treeNode.left.left = new TreeNode(1);
        treeNode.left.right = new TreeNode(3);

        treeNode.right = new TreeNode(7);
        treeNode.right.left = new TreeNode(6);
        treeNode.right.right = new TreeNode(9);

        xx(treeNode);

        System.out.println(treeNode);

    }

    private static void xx(TreeNode treeNode) {
        if (treeNode == null) {
            return;
        }
        TreeNode left = treeNode.left;
        treeNode.left = treeNode.right;
        treeNode.right = left;
        xx(treeNode.left);
        xx(treeNode.right);
    }</div>2023-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/66/1f8fccfb.jpg" width="30px"><span>云之崖</span> 👍（0） 💬（0）<div>现在复习，基本上10分钟之类，能手写搞定堆排序，基本一次就过。还有二叉树的删除操作，现在想明白了原理，间隔再久的时间，纸上画一画，写起来也不会有什么困难。</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ec/0f/555aa881.jpg" width="30px"><span>jianhuang_zou</span> 👍（0） 💬（0）<div>迭代是逐渐逼近，用新值覆盖旧值，直到满足条件后结束，不保存中间值，空间利用率高。
递归是将一个问题分解为若干相对小一点的问题，遇到递归出口再原路返回，因此必须保存相关的中间值，这些中间值压入栈保存，问题规模较大时会占用大量内存。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ec/0f/555aa881.jpg" width="30px"><span>jianhuang_zou</span> 👍（0） 💬（0）<div> 二叉树的两种解法，一下解释为中序遍历，将代码调整顺序，可得到前序和后序遍历结果（转）
# # 递归法
        # if root is None:
        #     return[]
        # return self.inorderTraversal(root.left)\
        #     +[root.val]\
        #         +self.inorderTraversal(root.right)
        # 迭代法
        result=[]
        stack=[(1,root)]
        while stack:
            go_deeper,node=stack.pop()
            if node is None:
                continue
            if go_deeper:
                #左右结点还需深化
                stack.append((1,node.right))
                stack.append((0,node))
                stack.append((1,node.left))
            else:
                result.append(node.val)
        return result</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/10/275ae749.jpg" width="30px"><span>懒猫</span> 👍（0） 💬（0）<div>打卡</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/e0/33521e13.jpg" width="30px"><span>DigDeeply</span> 👍（0） 💬（0）<div>https:&#47;&#47;github.com&#47;DigDeeply&#47;data-structures-learning&#47;blob&#47;0e14f4f69d1f3d45c3d16820cb771f6c242898e4&#47;57-5-binary_tree&#47;binary_tree.go

用数组实现的二叉查找树，支持增删查。</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#验证二叉搜索树
def isValidBST(self, root: TreeNode) -&gt; bool:
        def inorderTraversal(root): 
            if root == None:
                return []
            res = []
            res += inorderTraversal(root.left)
            res.append(root.val)
            res += inorderTraversal(root.right)
            return res
 
        res = inorderTraversal(root)
        if res != sorted(list(set(res))): return False
        return True
</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#实现小顶堆
def makeSmallHeap(array):
    for i in range(int(len(array)&#47;2) , -1 , -1):
        makeHeap(array , i , len(array))
def makeHeap(array , i ,N):
    while 2*i+1 &lt; N:
        child = 2*i+1
        if child != N-1 and array[child] &gt; array[child+1]:
            child+=1
        if array[child] &lt; array[i]:
            temp = array[child]
            array[child] = array[i]
            array[i] = temp
            i = child
        else:
            break</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#实现大顶堆
def makeBigHeap(array):
    for i in range(int(len(array)&#47;2) , -1 , -1):
        makeHeap(array , i , len(array))
def makeHeap(array , i ,N):
    while 2*i+1 &lt; N:
        child = 2*i+1
        if child != N-1 and array[child] &lt; array[child+1]:
            child+=1
        if array[child] &gt; array[i]:
            temp = array[child]
            array[child] = array[i]
            array[i] = temp
            i = child
        else:
            break</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#堆排序
import random
import time

def Array(n):
    a = []
    for i in range(n):
        a.append(random.randint(0 , n))
    return a

def makeHeap(array , i ,N):
    while 2*i+1 &lt; N:
        child = 2*i+1
        if child != N-1 and array[child] &lt; array[child+1]:
            child+=1
        if array[child] &gt; array[i]:
            temp = array[child]
            array[child] = array[i]
            array[i] = temp
            i = child
        else:
            break
def heapSort():
    array = Array(100)
    for i in range(int(len(array)&#47;2) , -1 , -1):
        makeHeap(array , i , len(array))
    for i in range(len(array)-1 , -1 , -1):
        temp = array[0]
        array[0] = array[i]
        array[i] = temp
        makeHeap(array , 0 , i)
    print(array)</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/fd/035f4c94.jpg" width="30px"><span>欢乐小熊</span> 👍（0） 💬（0）<div>路径总和: 使用回溯法, 遍历每一条 root-&gt;leaf 的路线是否满足在和为 sum, 可以使用减枝操作

二叉树深度 = 左右子树中深度最大者 + 1

验证二叉搜索树: 
1. 遍历每一个结点, 若都满足, 当前结点大于左子树中的最大值, 小于右子树中的最小值, 则说明为二叉搜索树
2. 中序遍历二叉搜索树, 若序列递增, 则说明为二叉搜索树</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#二叉树前中后序及层次遍历非递归版本
class Tree:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

#----前序----
def preOrder(Tree T):
    if T is None:
        return []
    list1 = []
    list2 = []
    list1.append(T)
    while len(list1) &gt; 0:
        t = list1.pop()
        list2.append(t)
        if t.right not None:
            list1.append(t.right)
        if t.left not None:
            list1.append(t.left)
    return list2

#----中序----
def inOrder(Tree T):
    if T is None:
        return []
    list1 = []
    list2 = []
    while T or len(list1)&gt;0 :
        if T :
            list1.append(T)
            T = T.left
        else:
            T = list1.pop()
            list2.append(T)
            T = T.right
    return list2

#----后序----
def postOrder(Tree T):
    if T is None:
        return []
    list1 = []
    list2 = []
    list1.append(T)
    while len(list1)&gt;0 :
        t = list1.pop()
        list2.append(t)
        if t.left not None:
            list1.append(t.left)
        if t.right not None:
            list1.append(t.right)
    return list2[::-1]

#----层次-----
def levelOrder():
    if T is None:
        return []
    list1 = []
    list2 = []
    list1.append(T)
    while len(list1)&gt;0 :
        t = list1[0]
        del list1[0]
        list2.append(t)
        if t.left not None:
            list1.append(t.left)
        if t.right not None:
            list1.append(t.right)
    return list2
</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>Path Sum（路径总和）go 语言实现
func hasPathSum(root *TreeNode, sum int) bool {

	if root==nil{
		return false
	}
	if root.Left==nil &amp;&amp; root.Right==nil{
		if root.Val==sum{
			return true
		}else{
			return false
		}

	}
	left:=false
	if root.Left!=nil{
		left=hasPathSum(root.Left,sum-root.Val)
	}
	right:=false
	if root.Right!=nil{
		right=hasPathSum(root.Right,sum-root.Val)
	}
	return left || right
}</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>Validate Binary Search Tree（验证二叉查找数） go语言实现

func isValidBST(root *TreeNode) bool {

	if root==nil{
		return true
	}
	less:=true
	more:=true
	if root.Left!=nil{
		less=JudgeLess(root.Left,root.Val)
	}
	if root.Right!=nil{
		more=JudgeMore(root.Right,root.Val)
	}
	if ! (less &amp;&amp; more){
		return false
	}else{
		return isValidBST(root.Left) &amp;&amp; isValidBST(root.Right)
	}
}

func JudgeLess(root *TreeNode,num int) bool{

	if root.Val&gt;=num{
		return false
	}
	if root.Left!=nil &amp;&amp; root.Right!=nil{
		return JudgeLess(root.Left,num) &amp;&amp; JudgeLess(root.Right,num)
	}else if root.Left!=nil{
		return JudgeLess(root.Left,num)
	}else if root.Right!=nil{
		return JudgeLess(root.Right,num)
	}else{
		return true
	}
}

func JudgeMore(root *TreeNode,num int) bool{
	if root.Val&lt;=num{
		return false
	}
	if root.Left!=nil &amp;&amp; root.Right!=nil{
		return JudgeMore(root.Left,num) &amp;&amp; JudgeMore(root.Right,num)
	}else if root.Left!=nil{
		return JudgeMore(root.Left,num)
	}else if root.Right!=nil{
		return JudgeMore(root.Right,num)
	}else{
		return true
	}
}
</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>Invert Binary Tree（翻转二叉树） go 语言实现
func invertTree(root *TreeNode) *TreeNode {
	if root==nil{
		return root
	}
	temp:=root.Left
	root.Left=root.Right
	root.Right=temp
	invertTree(root.Left)
	invertTree(root.Right)
	return root
}</div>2019-02-14</li><br/>
</ul>