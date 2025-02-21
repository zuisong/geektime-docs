你好，我是王争。初二好！

为了帮你巩固所学，真正掌握数据结构和算法，我整理了数据结构和算法中，必知必会的30个代码实现，分7天发布出来，供你复习巩固所用。今天是第二篇。

和昨天一样，你可以花一点时间，来完成测验。测验完成后，你可以根据结果，回到相应章节，有针对性地进行复习。

* * *

## 关于栈、队列和递归的几个必知必会的代码实现

### 栈

- 用数组实现一个顺序栈
- 用链表实现一个链式栈
- 编程模拟实现一个浏览器的前进、后退功能

### 队列

- 用数组实现一个顺序队列
- 用链表实现一个链式队列
- 实现一个循环队列

### 递归

- 编程实现斐波那契数列求值f(n)=f(n-1)+f(n-2)
- 编程实现求阶乘n!
- 编程实现一组数据集合的全排列

## 对应的LeetCode练习题（@Smallfly 整理）

### 栈

- Valid Parentheses（有效的括号）

英文版：[https://leetcode.com/problems/valid-parentheses/](https://leetcode.com/problems/valid-parentheses/)

中文版：[https://leetcode-cn.com/problems/valid-parentheses/](https://leetcode-cn.com/problems/valid-parentheses/)

- Longest Valid Parentheses（最长有效的括号）

英文版：[https://leetcode.com/problems/longest-valid-parentheses/](https://leetcode.com/problems/longest-valid-parentheses/)
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/59/b515a473.jpg" width="30px"><span>Abner</span> 👍（0） 💬（1）<div>java实现一个循环队列
代码如下：
package queue;

public class CircularQueue {
    
    private String[] data;
    private int size;
    private int head;
    private int tail;
    
    public CircularQueue(int capacity) {
        data = new String[capacity];
        size = capacity;
        head = 0;
        tail = 0;
    }
    
    public boolean enqueue(String item) {
        if ((tail + 1) % size == head) {
            return false;
        }
        data[tail] = item;
        tail = (tail + 1) % size;
        return true;
    }

    public String dequeue() {
        if (head == tail) {
            return null;
        }
        String value = data[head];
        head = (head + 1) % size;
        return value;
    }

    public void printAll() {
        if (0 == size) {
            return ;
        }
        for (int i = head;i % size != tail;i++) {
            System.out.print(data[i] + &quot; &quot;);
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        CircularQueue circularQueue = new CircularQueue(5);
        circularQueue.enqueue(&quot;hello1&quot;);
        circularQueue.enqueue(&quot;hello2&quot;);
        circularQueue.enqueue(&quot;hello3&quot;);
        circularQueue.enqueue(&quot;hello4&quot;);
        circularQueue.dequeue();
        circularQueue.printAll();
    }
}
</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/d4/abb7bfe3.jpg" width="30px"><span>神盾局闹别扭</span> 👍（0） 💬（1）<div>全排列实现：
void Dopermute(char *pstr, char *pBegin)
{
	if (*pBegin == &#39;\0&#39;)
		printf(&quot;%s\n&quot;, pstr);

	for (char *pCur = pBegin; *pCur != &#39;\0&#39;; pCur++)
	{

		char temp = *pBegin;
		*pBegin = *pCur;
		*pCur = temp;

		Dopermute_v2(pstr, pBegin + 1);

		temp = *pBegin;
		*pBegin = *pCur;
		*pCur = temp;

	}
}
void Permute(char* pstr)
{
	if (pstr == nullptr)
		return;
	Dopermute(pstr, pstr);
}</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/88/be4fe19e.jpg" width="30px"><span>molybdenum</span> 👍（0） 💬（1）<div>老师新年好 这是我的作业

https:&#47;&#47;blog.csdn.net&#47;github_38313296&#47;article&#47;details&#47;86819684</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/90/f90903e5.jpg" width="30px"><span>菜菜</span> 👍（0） 💬（1）<div>求斐波那契数列，当然最经典的算法就是递归，但是递归的效率非常低，因为中间过车会计算大量重复的子节点。在《剑指Offer》一书中，提到了一个自下而上计算的方法。我们知道f(0)=0,f(1)=1,再计算f(2),f(3)一直到f(n)。这样，时间复杂度就是O(n)。</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/99/44378317.jpg" width="30px"><span>李皮皮皮皮皮</span> 👍（11） 💬（1）<div>基础数据结构和算法是基石，灵活运用是解题的关键。栈，队列这些数据结构说到底就是给顺序表添加约束，更便于解决某一类问题。学习中培养算法的设计思想是非常关键的。而且思想是可以通用的。之前读《暗时间》一书，收获颇深。书中介绍之正推反推我在做程序题时竟出奇的好用。</div>2019-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/59/b515a473.jpg" width="30px"><span>Abner</span> 👍（3） 💬（0）<div>java用数组实现一个顺序栈
代码如下：
package stack;

public class ArrayStack {

    private String[] data;
    private int count;
    private int size;

    public ArrayStack(int n) {
        this.data = new String[n];
        this.count = 0;
        this.size = n;
    }
    
    public boolean push(String value) {
        if (count == size) {
            return false;
        } else {
            data[count] = value;
            count++;
            return true;
        }
    }

    public String pop() {
        if (count == 0) {
            return null;
        } else {
            count--;
            return data[count];
        }
    }
}
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/59/b515a473.jpg" width="30px"><span>Abner</span> 👍（2） 💬（0）<div>java用递归实现斐波那契数列
代码如下：
package recursion;

public class Fib {

    public long calFib(long n) {
        if (n == 0 || n == 1) {
            return 1;
        } else {
            return calFib(n - 1) + calFib(n - 2);
        }
    }
    
    public static void main(String[] args) {
        Fib fib = new Fib();
        long result = fib.calFib(5);
        System.out.println(result);
    }
}
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/59/b515a473.jpg" width="30px"><span>Abner</span> 👍（2） 💬（0）<div>java用递归实现求解n!
代码如下：
package recursion;

public class Fac {

    public long calFac(long n) {
        if (n == 0) {
            return 1;
        } 
        return calFac(n - 1) * n;
    }

    public static void main(String[] args) {
        Fac fac = new Fac();
        long result = fac.calFac(10);
        System.out.println(result);
    }
}</div>2019-02-11</li><br/><li><img src="" width="30px"><span>kai</span> 👍（2） 💬（0）<div>1. 编程实现斐波那契数列求值 f(n)=f(n-1)+f(n-2）
public class Fibonacci {
    public static int fib(int n) {
        if (n &lt;= 0) {
            return 0;
        }
        if (n == 1) {
            return 1;
        }

        return  fib(n-1) + fib(n-2);
    }
}

2. Climbing Stairs（爬楼梯）
public class ClimbStairs {
    public int climbFloor(int n) {
        if (n == 1 || n == 2) {
            return n;
        }

        return climbFloor(n - 1) + climbFloor(n - 2);
    }

    public int climbFloorIter(int n) {
        if (n == 1 || n == 2) {
            return n;
        }

        int jump1 = 1;
        int jump2 = 2;
        int jumpN = 0;

        for (int i = 3; i &lt;= n; i++) {
            jumpN = jump1 + jump2;

            jump1 = jump2;
            jump2 = jumpN;
        }

        return jumpN;
    }
}

3. Sliding Window Maximum（滑动窗口最大值)
import java.util.ArrayList;
import java.util.LinkedList;

public class MaxNumOfSlidingWindow {
    public ArrayList&lt;Integer&gt; maxInWindows(int [] num, int size)
    {
        ArrayList&lt;Integer&gt; res = new ArrayList&lt;&gt;();

        if (num == null || num.length &lt;= 0 || size &lt;= 0 || size &gt; num.length) {
            return res;
        }

        LinkedList&lt;Integer&gt; qMax = new LinkedList&lt;&gt;();  &#47;&#47; 双端队列：左端更新max,右端添加数据

        int left = 0;

        for (int right = 0; right &lt; num.length; right++) {
            &#47;&#47; 更新右端数据
            while (!qMax.isEmpty() &amp;&amp; num[qMax.peekLast()] &lt;= num[right]) {
                qMax.pollLast();
            }

            qMax.addLast(right);

            &#47;&#47; 更新max：如果max的索引不在窗口内,则更新
            if (qMax.peekFirst() == right - size) {
                qMax.pollFirst();
            }

            &#47;&#47; 待窗口达到size，输出max
            if (right &gt;= size-1) {
                res.add(num[qMax.peekFirst()]);
                left++;
            }
        }

        return res;
    }
}</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/59/b515a473.jpg" width="30px"><span>Abner</span> 👍（1） 💬（0）<div>java用链表实现一个链式栈
代码如下：
package stack;

public class LinkedStack {
    
    private Node top = null;
    
    public static class Node {
        
        private String data;
        private Node next;
        
        public Node(String data, Node next) {
            this.data = data;
            this.next = next;
        }
        
        public String getData() {
            return data;
        }
    }
    
    public void push(String item) {
        Node newNode = new Node(item, null);
        if (top == null) {
            top = newNode;
        } else {
            newNode.next = top;
            top = newNode;
        }
    }
    
    public String pop() {
        if (top == null) {
            return null;
        }
        String value = top.data;
        top = top.next;
        return value;
    }
    
    public void printAll() {
        Node pNode = top;
        while (pNode != null) {
            System.out.print(pNode.data + &quot; &quot;);
            pNode = pNode.next;
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        LinkedStack linkedStack = new LinkedStack();
        linkedStack.push(&quot;haha&quot;);
        linkedStack.push(&quot;nihao&quot;);
        linkedStack.printAll();
    }
}
</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/59/b515a473.jpg" width="30px"><span>Abner</span> 👍（1） 💬（0）<div>java用数组实现一个顺序队列
代码如下：
package queue;

public class ArrayQueue {
    
    private String[] data;
    private int size;
    private int head;
    private int tail;
    
    public ArrayQueue(int capacity) {
        data = new String[capacity];
        size = capacity;
        head = 0;
        tail = 0;
    }
    
    public boolean enqueue(String value) {
        if (tail == size) {
            return false;
        }
        data[tail] = value;
        tail++;
        return true;
    }

    public String dequeue() {
        if (tail == 0) {
            return null;
        }
        String value = data[head];
        head++;
        return value;
    }
}
</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/64/7403c694.jpg" width="30px"><span>ALAN</span> 👍（1） 💬（0）<div>import java.util.Arrays;

&#47;**
 * 
 *Stack 1 solution
 *&#47;
public class StackArray {

	public Object[] arr = new Object[10];
	public int count;

	public void push(Object ele) {
		if (count == arr.length) { &#47;&#47; expand size
			arr = Arrays.copyOf(arr, arr.length * 2);
		}
		arr[count] = ele;
		count++;
	}

	public Object pop() {
		if (count == 0)
			return null;
		if (count &lt; arr.length &#47; 2) {
			arr = Arrays.copyOf(arr, arr.length &#47; 2);
		}
		return arr[--count];

	}
}

&#47;**
 * 
 *Stack 2 solution
 *&#47;
class StackLinked {
	Node head;
	Node tail;

	public void push(Object ele) {

		if (head == null) {
			head = new Node(ele);
			tail = head;
		} else {
			Node node = new Node(ele);
			tail.next = node;
			node.prev = tail;
			tail = node;
		}
	}

	public Object pop() {
		if (tail == null)
			return null;
		Node node = tail;
		if (tail == head) {
			head = null;
			tail = null;
		} else
			tail = tail.prev;
		return node;

	}
}
class Node {
	Node prev;
	Node next;
	Object value;

	public Node(Object ele) {
		value = ele;
	}
}</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f4/26b95f0b.jpg" width="30px"><span>TryTs</span> 👍（1） 💬（0）<div>之前有个类似的题，走楼梯，装苹果，就是把苹果装入盘子，可以分为有一个盘子为空（递归），和全部装满没有空的情况，找出状态方程，递归就可以列出来了。我觉得最关键是要列出状态方程，之前老师类似于说的不需要关注特别细节，不要想把每一步都要想明白，快速排序与递归排序之类的算法，之前总是想把很细节的弄懂，却发现理解有困难。</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>滑动窗口最大值
public static void main(String[] args) {

        PriorityQueue&lt;Integer[]&gt; queue = new PriorityQueue(3, new Comparator&lt;Integer[]&gt;() {
            @Override
            public int compare(Integer[] o1, Integer[] o2) {
                if (o1[0] == o2[0]) {
                    return o2[1] - o1[1];
                }
                return o2[0] - o1[0];
            }
        });

        int[] nums = new int[]{7, 3, -1, -3, 5, 3, 6, 7};
        for (int i = 0; i &lt; 3; i++) {
            queue.add(new Integer[]{nums[i], i});
        }

        int[] ret = new int[nums.length - 3 + 1];
        ret[0] = queue.peek()[0];
        for (int i = 3; i &lt; nums.length; i++) {
            queue.add(new Integer[]{nums[i], i});
            if (queue.peek()[1] &lt; i - 3 + 1) {
                queue.poll();
            }
            ret[i - 3 + 1] = queue.peek()[0];
        }

        System.out.println(ret);


    }</div>2023-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>双端队列
    static class MyCircularDeque {
        private int[] elements;
        &#47;&#47;获得双端队列的最后rear一个元素

        private int rear, front;
        &#47;&#47;内容个数
        private int capacity;

       

        public boolean insertFront(int value) {
            if (elements.length == capacity) {
                return false;
            }
            if (capacity == 0) {
                rear = front = 0;
            } else {
                front = front - 1;
                if (front &lt; 0) {
                    front += elements.length;
                }
            }
            elements[front] = value;
            capacity++;
            return true;
        }

        public boolean insertLast(int value) {
            if (elements.length == capacity) {
                return false;
            }
            if (capacity == 0) {
                rear = front = 0;
            } else {
                rear = (rear + 1) % elements.length;
            }
            elements[rear] = value;
            capacity++;
            return true;
        }

        public boolean deleteFront() {
            if (capacity == 0) {
                return false;
            }
            int idx = front;
            front = front + 1;
            if (front &gt; elements.length) {
                front = 0;
            }
            elements[idx] = -1;
            capacity--;
            return true;
        }

        public boolean deleteLast() {
            if (capacity == 0) {
                return false;
            }
            int idx = rear;
            rear = rear - 1;
            elements[idx] = -1;
            capacity--;
            return true;
        }

        public int getFront() {
            if (front != -1) {
                return elements[front];
            }
            return -1;
        }

        public int getRear() {
            if (rear != -1) {
                return elements[rear];
            }
            return -1;
        }
    }</div>2023-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>逆波兰表达式
public static void main(String[] args) {

        List&lt;String&gt; str = new ArrayList&lt;&gt;();
        &#47;&#47;&quot;10&quot;,&quot;6&quot;,&quot;9&quot;,&quot;3&quot;,&quot;+&quot;,&quot;-11&quot;,&quot;*&quot;,&quot;&#47;&quot;,&quot;*&quot;,&quot;17&quot;,&quot;+&quot;,&quot;5&quot;,&quot;+
        str.add(&quot;10&quot;);
        str.add(&quot;6&quot;);
        str.add(&quot;9&quot;);
        str.add(&quot;3&quot;);
        str.add(&quot;+&quot;);
        str.add(&quot;-11&quot;);
        str.add(&quot;*&quot;);
        str.add(&quot;&#47;&quot;);
        str.add(&quot;*&quot;);
        str.add(&quot;17&quot;);
        str.add(&quot;+&quot;);
        str.add(&quot;5&quot;);
        str.add(&quot;+&quot;);



        Stack&lt;String&gt; stack = new Stack();
        for (int i = 0; i &lt; str.size(); i++) {
            if (!str.get(i).equals(&quot;+&quot;) &amp;&amp;
                    !str.get(i).equals(&quot;-&quot;) &amp;&amp;
                    !str.get(i).equals(&quot;*&quot;) &amp;&amp;
                    !str.get(i).equals(&quot;&#47;&quot;)) {
                stack.push(str.get(i));
            } else {
                String pop = stack.pop();
                int old = Integer.parseInt(pop);
                int newV = Integer.parseInt(stack.pop());
                int value = 0;
                if (str.get(i).equals(&quot;+&quot;)) {
                    value = old + newV;
                } else if (str.get(i).equals(&quot;-&quot;)) {
                    value = newV - old;
                } else if (str.get(i).equals(&quot;*&quot;)) {
                    value = old * newV;
                } else if (str.get(i).equals(&quot;&#47;&quot;)) {
                    value = newV &#47; old;
                }
                stack.push(String.valueOf(value));
            }
        }

        System.out.println(stack.pop());


    }</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>最长有效挎号
public static void main(String[] args) {

        String s = &quot;&quot;;
        Stack&lt;Integer&gt; stack = new Stack&lt;&gt;();
        int[] arr = new int[s.length()];
        for (int i = 0; i &lt; s.length(); i++) {
            if (s.charAt(i) == &#39;(&#39;) {
                stack.add(i);
            } else {
                if (!stack.isEmpty()) {
                    Integer pop = stack.pop();
                    arr[pop] = 1;
                    arr[i] = 1;
                }
            }
        }
        int max = 0;
        int curr = 0;
        for (int i = 0; i &lt; arr.length; i++) {
            if (arr[i] == 1) {
                curr++;
                max = Math.max(curr, max);
            } else {
                curr = 0;
            }
        }
        System.out.println(max);

    }</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>有效的挎号
public static void main(String[] args) {

        String s = &quot;((((&quot;;
        if (s.length() % 2 != 0) {
            System.out.println(false);
            return;
        }
        Stack&lt;Character&gt; stack = new Stack();
        for (int i = 0; i &lt; s.length(); i++) {
            char c = s.charAt(i);
            if (c == &#39;]&#39; || c == &#39;}&#39; || c == &#39;)&#39;) {
                Character pop = stack.pop();
                if ((c == &#39;]&#39; &amp;&amp; pop != &#39;[&#39;) || (c == &#39;}&#39; &amp;&amp; pop != &#39;{&#39;) || (c == &#39;)&#39; &amp;&amp; pop != &#39;(&#39;)) {
                    System.out.println(false);
                    break;
                }
            } else {
                stack.add(c);
            }
        }
        System.out.println(stack.isEmpty());

    }</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>有效的挎号
public static void main(String[] args) {

        String s = &quot;()[][}&quot;;
        if (s.length() % 2 != 0) {
            System.out.println(false);
            return;
        }
        Stack&lt;Character&gt; stack = new Stack();
        for (int i = 0; i &lt; s.length(); i++) {
            char c = s.charAt(i);
            if (c == &#39;]&#39; || c == &#39;}&#39; || c == &#39;)&#39;) {
                Character pop = stack.pop();
                if ((c == &#39;]&#39; &amp;&amp; pop != &#39;[&#39;) || (c == &#39;}&#39; &amp;&amp; pop != &#39;{&#39;) || (c == &#39;)&#39; &amp;&amp; pop != &#39;(&#39;)) {
                    System.out.println(false);
                    break;
                }
            } else {
                stack.add(c);
            }
        }
        System.out.println(true);

    }</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/45/2c/1916cf2f.jpg" width="30px"><span>风行者</span> 👍（0） 💬（0）<div>递归写法的话简单加一层缓存就可以有很大的性能提升了，不用动态规划也可以做
class Solution:
    cache = {}
    def climbStairs(self, n: int) -&gt; int:
        if self.cache.__contains__(n):
            return self.cache[n]
        else:
            self.cache[n]=(self.climbStairs(n-2)+self.climbStairs(n-1) if n&gt;2 else n)
            return self.cache[n]</div>2021-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8a/19/a54761af.jpg" width="30px"><span>何沛</span> 👍（0） 💬（0）<div>用数组实现一个顺序队列
&#47;**
 * @author hepei
 * @date 2020&#47;1&#47;3 17:12
 **&#47;
public class ArrayQueue {

    private int[] data;
    private int head;
    private int tail;

    public ArrayQueue(int[] data) {
        this.data = data;
    }

    
    public void enqueue(int v) {
        if (tail == data.length &amp;&amp; head == 0) {
            return;
        }
        if (tail == data.length &amp;&amp; head &gt; 0) {
            for (int i = 0; i &lt; tail - head; i++) {
                data[i] = data[i + head];
            }
            tail = tail - head;
            head = 0;
        }
        data[tail] = v;
        tail++;
    }

    public int dequeue() {
        if (tail == 0||head==tail) {
            return -1;
        }
        int r = data[head];
        head++;
        return r;
    }

    public void display() {
        for (int i = head; i &lt; tail; i++) {
            System.out.print( data[i] + &quot; &quot; );
        }
    }

    public static void main(String[] args) {
        ArrayQueue queue = new ArrayQueue( new int[5] );
        queue.enqueue( 1 );
        queue.enqueue( 2 );
        queue.enqueue( 3 );
        queue.enqueue( 4 );
        queue.enqueue( 5 );
        queue.dequeue();
        queue.dequeue();
        queue.dequeue();
        queue.dequeue();
        queue.enqueue( 6 );
        queue.enqueue( 7 );
        queue.display();
    }

}</div>2020-01-03</li><br/><li><img src="" width="30px"><span>Hxz</span> 👍（0） 💬（0）<div>我用js写的题解都放在了https:&#47;&#47;github.com&#47;abchexuzheng&#47;algorithm-for-js这里，前端学算法的小伙伴们可以看看一起学习下哈</div>2019-10-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLlztvlBgajZMEph8AvkP2pfoqNCGtYSalIKgrCbCg0MWDZJgJwqVRfWA6cgIoZicL6dKibfK0zjsWg/132" width="30px"><span>Geek_18b741</span> 👍（0） 💬（0）<div>再做Climbing Stairs这个题目的时候，提交了两个版本的代码。理论上来说内存应该是有区别的，但是LeetCode给的结果，内存大小却没有什么区别。请帮忙看看。
&#47;**
     * 动态规划
     * @param n
     * @return
     *&#47;
    public int climbStairsV3(int n) {
        if(n==1) return 1;
        int[] dp = new int[n+1];
        dp[1]=1;
        dp[2]=2;
        for(int i=3;i&lt;=n;i++){
            dp[i]=dp[i-1]+dp[i-2];
        }
        return dp[n];
    }

    &#47;**
     * 节省内存的动态规划，但实际LeetCode反馈出来的内存并不少
     * @param n
     * @return
     *&#47;
    public int climbStairsV4(int n) {
        if(n==1) return 1;
        int num1 =1;
        int num2 =2;
        int num3=0;
        for(int i=3;i&lt;=n;i++){
            num3=num1+num2;
            num1=num2;
            num2=num3;
        }
        return num2;
    }</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/29/d9/4358d6fb.jpg" width="30px"><span>猫猫</span> 👍（0） 💬（0）<div>全排列js 
&#47;&#47;9.一组数据集合的全排列 回溯（暴力枚举）
let count = 1

function permutation(nums, result = []) {
  if (nums.length == 0) {
    console.log(`${count}:${result}`)
    count++
    return
  }
  for (let i = 0; i &lt; nums.length; i++) {
    permutation(nums.filter((value, index) =&gt; index != i), [...result, nums[i]])
  }
}</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/10/275ae749.jpg" width="30px"><span>懒猫</span> 👍（0） 💬（0）<div>练完打卡</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/fd/035f4c94.jpg" width="30px"><span>欢乐小熊</span> 👍（0） 💬（0）<div>有意思, 递归的 LeeCode 题目, 使用简单粗暴的回溯法并没有办法通过, 还是得使用动态规划求解</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#一组数据集合的全排列
def f(start , b):
    a = list(b)
    if start==len(a):
        print(b)
    else:
        for i in range(start , len(a)):
            a[start] , a[i] = a[i] , a[start]
            c = tuple(a)
            f(start+1 , c)
            a[start] , a[i] = a[i] , a[start]</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#实现快速排序、归并排序
#---------快排(三数取中)---------
def QuickSort():
    array = Array(10000)
    qsort(0 , len(array)-1 , array)
    return array
def qsort(start , end , array):
    if start &lt; end:
        key = partation(array , start , end)
        qsort(start , key-1 , array)
        qsort(key+1 , end , array)
def swap(array , start , end):
    temp = array[start]
    array[start] = array[end]
    array[end] = temp
def change(array , start , mid , end):
    if array[start] &gt; array[mid]:
        swap(array , start , mid)
    if array[start]&gt;array[end]:
        swap(array , start , end)
    if array[mid] &gt; array[end]:
        swap(array , mid , end)
    swap(array , mid , start)
def partation(array , start , end):
    #mid = int((start+end)&#47;2)
    #change(array , start , mid , end)
    temp = array[start]
    while start &lt; end :
        while start&lt;end and array[end]&lt;=temp:
            end-=1
        swap(array , start , end)
        while start&lt;end and array[start]&gt;=temp:
            start+=1
        swap(array , start , end)
    return start
#---------------归并------------
def merge(a , b):
    c = []
    i = 0
    j = 0
    while i&lt;len(a) and j&lt;len(b):
        if a[i] &gt; b[j]:
            c.append(a[i])
            i+=1
        else:
            c.append(b[j])
            j+=1
    if i&gt;=len(a):
        for k in range(j , len(b)):
            c.append(b[k])
    if j&gt;=len(b):
        for k in range(i , len(a)):
            c.append(a[k])
    return c
def devide(array):
    if len(array) == 1:
        return array
    else:
        mid = int((0 + len(array)) &#47; 2)
        leftArray = devide(array[0:mid])
        rightArray = devide(array[mid:len(array)])
        return merge(leftArray , rightArray)
def mergesort():
    array = Array(100)
    m = devide(array)
    return m</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#冒泡、选择、插入排序
import random
import time
def Array(n):
    a = []
    for i in range(n):
        a.append(random.randint(0 , n))
    return a
#插入排序
def insert():
    array = Array(100)
    time_start=time.time()
    for i in range(1 , len(array)):
        for j in range(i , 0 , -1):
            if array[j] &gt; array[j-1]:
                temp = array[j]
                array[j] = array[j-1]
                array[j-1] = temp
            else:
                break
    time_end=time.time()
    print(array)
    print(&#39;totally cost&#39;,time_end-time_start)
def select():
    array = Array(100)
    time_start=time.time()
    for i in range(len(array)):
        for j in range(i+1 , len(array)):
            if array[j] &gt; array[i]:
                temp = array[j]
                array[j] = array[i]
                array[i] = temp
    time_end=time.time()
    print(array)
    print(&#39;totally cost&#39;,time_end-time_start)
def bubble():
    array = Array(100)
    time_start=time.time()
    for i in range(len(array)-1 , 0 , -1):
        flag = False
        for j in range(i):
            if array[j] &gt; array[j+1]:
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp
                flag = True
        if not flag:
            break
    time_end=time.time()
    print(array)
    print(&#39;totally cost&#39;,time_end-time_start)</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>&#47;&#47;阶乘n!
def f(n):
    if(n&lt;=1):
        return 1
    else:
        return f(n-1)*n</div>2019-02-15</li><br/>
</ul>