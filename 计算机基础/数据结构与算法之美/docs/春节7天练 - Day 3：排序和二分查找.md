你好，我是王争。初三好！

为了帮你巩固所学，真正掌握数据结构和算法，我整理了数据结构和算法中，必知必会的30个代码实现，分7天发布出来，供你复习巩固所用。今天是第三篇。

和昨天一样，你可以花一点时间，来完成测验。测验完成后，你可以根据结果，回到相应章节，有针对性地进行复习。

前两天的内容，是关于数组和链表、排序和二分查找的。如果你错过了，点击文末的“上一篇”，即可进入测试。

* * *

## 关于排序和二分查找的几个必知必会的代码实现

### 排序

- 实现归并排序、快速排序、插入排序、冒泡排序、选择排序
- 编程实现O(n)时间复杂度内找到一组数据的第K大元素

### 二分查找

- 实现一个有序数组的二分查找算法
- 实现模糊二分查找算法（比如大于等于给定值的第一个元素）

## 对应的LeetCode练习题（@Smallfly 整理）

- Sqrt(x) （x 的平方根）

英文版：[https://leetcode.com/problems/sqrtx/](https://leetcode.com/problems/sqrtx/)

中文版：[https://leetcode-cn.com/problems/sqrtx/](https://leetcode-cn.com/problems/sqrtx/)

* * *

做完题目之后，你可以点击“请朋友读”，把测试题分享给你的朋友，说不定就帮他解决了一个难题。

祝你取得好成绩！明天见！
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f4/26b95f0b.jpg" width="30px"><span>TryTs</span> 👍（6） 💬（1）<div>虽然现在有很多排序算法自己不会亲自写，但是作为算法的基础，分治，归并，冒泡等排序算法在时间复杂度，空间复杂度以及原地排序这些算法知识上的理解非常有帮助。递归分治这些算法思想在简单的算法中也能体现出来，其实更多的是思维方式的训练。</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2e/45/d4039dd3.jpg" width="30px"><span>Monster</span> 👍（1） 💬（2）<div>&#47;**
 * O(n)时间复杂度内求无序数组中第K大元素
 *&#47;
public class TopK {

    public int findTopK(int[] arr, int k) {
        return findTopK(arr, 0, arr.length - 1, k);
    }

    private int findTopK(int[] arr, int left, int right, int k) {
        if (arr.length &lt; k) {
            return -1;
        }
        int pivot = partition(arr, left, right);
        if (pivot + 1 &lt; k) {
            findTopK(arr, pivot + 1, right, k);
        } else if (pivot + 1 &gt; k) {
            findTopK(arr, left, pivot - 1, k);
        }
        return arr[pivot];
    }


    private int partition(int[] array, int left, int right) {
        int pivotValue = array[right];
        int i = left;

        &#47;&#47;小于分区点放在左边 大于分区点放在右边
        for (int j = left; j &lt; right; j++) {
            if (array[j] &lt; pivotValue) {
                int tmp = array[i];
                array[i] = array[j];
                array[j] = tmp;
                i++;
            }
        }
        &#47;&#47;与分区点交换
        int tmp = array[i];
        array[i] = array[right];
        array[right] = tmp;
        return i;
    }
}</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/9d/4d705f03.jpg" width="30px"><span>C_love</span> 👍（1） 💬（1）<div>Use Binary Search

class Solution {
    public int mySqrt(int x) {
        if (x == 0 || x == 1) {
            return x;
        }
        
        int start = 0;
        int end = (x &gt;&gt; 1) + 1;
        
        while (start + 1 &lt; end) {
            final int mid = start + ((end - start) &gt;&gt; 1);
            final int quotient = x &#47; mid;
            if (quotient == mid) {
                return mid;
            } else if (quotient &lt; mid) {
                end = mid;
            } else {
                start = mid;
            }
        }
        
        return start;
    }
}</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/9d/a2f555ba.jpg" width="30px"><span>涤生</span> 👍（0） 💬（1）<div>使用了二分法和牛顿法来解决平方根的求解问题。
二分法：
class Solution:
    def mySqrt(self, x):
        &quot;&quot;&quot;
        :type x: int
        :rtype: int
        &quot;&quot;&quot;
        if x == 1:
            return 1
        def binarysearch(l, r, x):
            while(l&lt;=r):
                mid = l + ((r-l)&gt;&gt;1)
                if abs(mid*mid-x)&lt;1:
                    return mid
                elif mid*mid &gt; x:
                    r = mid - 1
                else:
                    l = mid + 1
            return r
        return binarysearch(0, x&#47;&#47;2, x)
牛顿法：
class Solution:
    def mySqrt(self, x):
        &quot;&quot;&quot;
        :type x: int
        :rtype: int
        &quot;&quot;&quot;
        if x == 1:
            return 1
        ans = x&#47;&#47;2
        while(ans * ans - x&gt;0): # 可以是其他精度
            ans = (x &#47;&#47; ans + ans) &#47;&#47; 2
        return ans</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/99/44378317.jpg" width="30px"><span>李皮皮皮皮皮</span> 👍（13） 💬（0）<div>各种排序算法真要说起来实际中使用的最多的也就是快排了。然而各种编程语言内置的标准库都包含排序算法的实现，基本没有自己动手实现的必要。然后作为经典的算法，自己实现一遍，分析分析时间空间复杂度对自己的算法设计大有裨益。需要注意的是为了高效，在实际的实现中，多种排序算法往往是组合使用的。例如c标准库中总体上是快排，但当数据量小于一定程度，会转而使用选择或插入排序。
求平方根使用牛顿法二分逼近😄</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（5） 💬（0）<div>基本排序算法的关注点分为：
1. 时间复杂度。如n的平方（冒泡，选择，插入）；插入排序的优化希尔排序，则把复杂度降低到n的3&#47;2次方；n乘以logn(快排，归并排序，堆排序）。
2. 是否为原地排序。如，归并排序需要额外的辅助空间。
3. 算法的稳定性。稳定排序（by nature）如冒泡，插入，归并。如果把次序考虑在内，可以把其他的排序（如快排，堆排序）也实现为稳定排序。
4. 算法的实现。同为时间复杂度同为n平方的算法中，插入排序的效率更高。但是如果算法实现的不好，可能会降低算法的效率，甚至让稳定的算法变得不稳定。又如，快速排序有不同的实现方式，如三路快排可以更好的应对待排序数组中有大量重复元素的情况。堆排序可以通过自上而下的递归方式实现，也可以通过自下而上的方式实现。
5. 不同算法的特点，如对于近乎有序的数组进行排序，首选插入排序，时间复杂度近乎是n，而快速排序则退化为n平方。

二分查找，需要注意 (l+r)&#47;2可能存在越界问题。

leetcode题，用二分查找找到x*x &gt; n 且(x-1)的平方小于n的数，则n-1就是结果。或者 x的平方小于n且x+1的平方大于n,则返回x。</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/aa/32fc0d54.jpg" width="30px"><span>失火的夏天</span> 👍（4） 💬（0）<div>牛顿法或者二分逼近都可以解决平方根问题，leetcode上有些大神的思路真的很厉害，经常醍醐灌顶</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（3） 💬（0）<div>#O(n)时间复杂度时间复杂度内找到一组数据的第 n大元素
import random
import time

def Array(n):
    a = []
    for i in range(n):
        a.append(random.randint(0 , n))
    return a
def QuickSort(n):
    array = Array(100)
    if n &gt; len(array) or n &lt; 1:
        print(&quot;超出范围，找不到&quot;)
        return
    n = n-1
    a = qsort(0 , len(array)-1 , array , n)
    print(sorted(array))
    print(&quot;-----------------------------&quot;)
    print(a)

def qsort(start , end , array , n):
    if start == end:
        res = array[start]
    if start &lt; end:
        key = partation(array , start , end)
        print(start , key , end)
        if key &gt; n :
            res = qsort(start , key-1 , array , n)
        elif key &lt; n:
            res = qsort(key+1 , end , array , n)
        else:
            res = array[key]
    return res

def swap(array , start , end):
    temp = array[start]
    array[start] = array[end]
    array[end] = temp

def partation(array , start , end):
    temp = array[start]
    while start &lt; end :
        while start&lt;end and array[end]&lt;=temp:
            end-=1
        swap(array , start , end)
        while start&lt;end and array[start]&gt;=temp:
            start+=1
        swap(array , start , end)
    return start</div>2019-02-16</li><br/><li><img src="" width="30px"><span>kai</span> 👍（2） 💬（0）<div>实现模糊二分查找算法2:

public class BinarySearch {
    &#47;&#47; 3. 查找第一个大于等于给定值的元素
    public static int bsFistGE(int[] array, int target) {
        int lo = 0;
        int hi = array.length - 1;

        while (lo &lt;= hi) {
            int mid = lo + ((hi - lo) &gt;&gt; 1);

            if (array[mid] &gt;= target) {
                if (mid == 0 || array[mid-1] &lt; target) {
                    return mid;
                } else {
                    hi = mid - 1;
                }
            } else {
                lo = mid + 1;
            }
        }

        return -1;
    }

    &#47;&#47; 4. 查找最后一个小于等于给定值的元素
    public static int bsLastLE(int[] array, int target) {
        int lo = 0;
        int hi = array.length - 1;

        while (lo &lt;= hi) {
            int mid = lo + ((hi - lo) &gt;&gt; 1);

            if (array[mid] &lt;= target) {
                if (mid == hi || array[mid+1] &gt; target) {
                    return mid;
                } else {
                    lo = mid + 1;
                }
            } else {
                hi = mid - 1;
            }
        }

        return -1;
    }
}</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f4/26b95f0b.jpg" width="30px"><span>TryTs</span> 👍（1） 💬（0）<div>#include&lt;iostream&gt;
#include&lt;cmath&gt;
using namespace std;
double a = 1e-6;
double sqrt(double n){
	double low = 0.0;
	double high = n;
	
int i = 1000;

	while(i--){
		double mid = low + (high - low) &#47; 2.0; 
		&#47;&#47;cout&lt;&lt;&quot;n:&quot;&lt;&lt;n&lt;&lt;endl;
		double square = mid * mid;
		&#47;&#47;cout&lt;&lt;&quot;sq:&quot;&lt;&lt;square&lt;&lt;endl;
		&#47;&#47;cout&lt;&lt;&quot;s:&quot;&lt;&lt;abs(square - n)&lt;&lt;endl;
		if(abs(mid * mid - n) &lt; a){
			return mid;
		}
		else{

			if(square &gt; n){
				high = mid;
			} 
			else{
			    low = mid; 
			}
		}
	}
	return -2.0;
}
int main(){
	double t;
	while(true){
		cin&gt;&gt;t;
		cout&lt;&lt;sqrt(t)&lt;&lt;endl;
	}
}</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/03/ef0efcc4.jpg" width="30px"><span>EidLeung</span> 👍（1） 💬（0）<div>编程实现 O(n) 时间复杂度内找到一组数据的第 K 大元素。
这个的时间复杂路应该是n·logk吧？</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2d/59/b515a473.jpg" width="30px"><span>Abner</span> 👍（1） 💬（0）<div>java实现冒泡排序
代码如下：
package sort;

public class BubbleSort {

    public int[] bubbleSort(int[] array) {
        for (int i = 0;i &lt; array.length - 1;i++) {
            for (int j = 0;j &lt; array.length - i - 1;j++) {
                if (array[j] &gt; array[j + 1]) {
                    int temp = array[j + 1];
                    array[j + 1] = array[j];
                    array[j] = temp;
                }
            }
        }
        return array;
    }

    public static void main(String[] args) {
        int[] array = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
        BubbleSort bubbleSort = new BubbleSort();
        int[] result = bubbleSort.bubbleSort(array);
        for (int i = 0;i &lt; result.length;i++) {
            System.out.print(result[i] + &quot; &quot;);
        }
    }

}
</div>2019-02-11</li><br/><li><img src="" width="30px"><span>kai</span> 👍（1） 💬（0）<div>实现模糊二分查找算法1:

public class BinarySearch {
    
    &#47;&#47; 1. 查找第一个值等于给定值的元素
    public static int bsFirst(int[] array, int target) {
        int lo = 0;
        int hi = array.length - 1;

        while (lo &lt;= hi) {
            int mid = lo + ((hi - lo) &gt;&gt; 1);

            if (array[mid] &gt; target) {
                hi = mid - 1;
            } else if (array[mid] &lt; target) {
                lo = mid + 1;
            } else {
                if (mid == lo || array[mid-1] != array[mid]) {
                    return mid;
                } else {
                    hi = mid - 1;
                }
            }
        }

        return -1;
    }

    &#47;&#47; 2. 查找最后一个值等于给定值的元素
    public static int bsLast(int[] array, int target) {
        int lo = 0;
        int hi = array.length - 1;

        while (lo &lt;= hi) {
            int mid = lo + ((hi - lo) &gt;&gt; 1);

            if (array[mid] &gt; target) {
                hi = mid - 1;
            } else if (array[mid] &lt; target) {
                lo = mid + 1;
            } else {
                if (mid == hi || array[mid] != array[mid+1]) {
                    return mid;
                } else {
                    lo = mid + 1;
                }
            }
        }

        return -1;
    }
}</div>2019-02-11</li><br/><li><img src="" width="30px"><span>kai</span> 👍（1） 💬（0）<div>实现一个有序数组的二分查找算法:

public class BinarySearch {
    &#47;&#47; 最简单的二分查找算法：针对有序无重复元素数组
    &#47;&#47; 迭代
    public static int binarySearch(int[] array, int target) {
        if (array == null) return -1;

        int lo = 0;
        int hi = array.length-1; &#47;&#47; 始终在[lo, hi]范围内查找target

        while (lo &lt;= hi) {
            int mid = lo + ((hi - lo) &gt;&gt; 1); &#47;&#47; 这里若是 (lo + hi) &#47; 2 有可能造成整型溢出

            if (array[mid] &gt;  target) {
                hi = mid - 1;
            } else if (array[mid] &lt; target) {
                lo = mid + 1;
            } else {
                return mid;
            }
        }

        return -1;
    }

    &#47;&#47; 递归
    public static int binarySearchRecur(int[] array, int target) {
        if (array == null) return -1;
        return bs(array, target, 0, array.length-1);
    }

    private static int bs(int[] array, int target, int lo, int hi) {
        if (lo &lt;= hi) {
            int mid = lo + ((hi - lo) &gt;&gt; 1);
            if (array[mid] &gt; target) {
                return bs(array, target, lo, mid-1);
            } else if (array[mid] &lt; target) {
                return bs(array, target, mid+1, hi);
            } else {
                return mid;
            }
        }

        return -1;
    }
}</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（1） 💬（0）<div>这道题似乎可以等价于从1到x中找到一个数y，使得y*y小于等于x，且（y+1）*（y+1）大于x。那么可以从1到x逐个尝试，提高效率可以采用二分查找方法，时间复杂度为O（logx）。</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/6f/aacb013d.jpg" width="30px"><span>黄丹</span> 👍（1） 💬（0）<div>王争老师初三快乐！
这是今天两道题的解题思路和代码
1. O(n)时间内找到第K大的元素：
解题思路：利用快排中分区的思想，选择数组区间A[0...n-1]的左右一个元素A[n-1]作为pivot，对数组A[0...n-1]原地分区，这样数组就分成了三部分，A[0..p-1],A[p],A[p+1...n-1],如果p+1=k,那么A[p]就是要求解的元素，如果K&gt;p+1,则说明第K大的元素在A[p+1...n-1]这个区间，否则在A[0...p-1]这个区间，递归的查找第K大的元素
2. Sqrt(x) （x 的平方根）
解题思路：利用二分查找的思想，从1到x查找x的近似平方根
代码：
https:&#47;&#47;github.com&#47;yyxd&#47;leetcode&#47;blob&#47;master&#47;src&#47;leetcode&#47;sort&#47;Problem69_Sqrt.java</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/c2/6f225ccc.jpg" width="30px"><span>杨建斌(young)</span> 👍（0） 💬（0）<div>public static void main(String[] args) {

        int x = 243432;
        if (x &lt; 4) {
            System.out.println(1);
        }
        if (x &lt; 9) {
            System.out.println(2);
        }
        if (x &lt; 16) {
            System.out.println(3);
        }
        if (x &lt; 25) {
            System.out.println(4);
        }
        int end = x &#47; 2;
        int start = 1;
        while (start + 1 &lt; end) {
            int value = (end + start) &#47; 2;
            if (value * value &gt; x || value * value &lt; 0) {&#47;&#47;-0 溢出
                end = value;
            } else {
                start = value;
            }

        }
        System.out.println(start);

    }</div>2023-06-29</li><br/><li><img src="" width="30px"><span>Geek_86533a</span> 👍（0） 💬（0）<div>不断学习，不断练习到今天。发现自己的代码能力、思考问题的能力有了明显的进步。感谢！</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/10/275ae749.jpg" width="30px"><span>懒猫</span> 👍（0） 💬（0）<div>打卡</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#二分查找变种
import random
import time

def Array(n):
    a = []
    for i in range(n):
        a.append(random.randint(0 , n))
    return a
#查找第一个值等于给定值的元素
def find_1(n):
    array = Array(100)
    array = sorted(array)
    left = 0
    right = len(array)-1
    while left &lt;= right:
        mid = int((left+right)&#47;2)
        if array[mid] &gt; n:
            right = mid - 1
        elif array[mid] &lt; n:
            left = mid + 1
        else:
            if mid==0 or array[mid] != array[mid-1]:
                return mid
            else:
                right = mid - 1
    print(&quot;找不到&quot;)
    return -1

#查找最后一个值等于给定值的元素
def find_2(n):
    array = Array(100)
    array = sorted(array)
    left = 0
    right = len(array)-1
    while left &lt;= right:
        mid = int((left+right)&#47;2)
        if array[mid] &gt; n:
            right = mid - 1
        elif array[mid] &lt; n:
            left = mid + 1
        else:
            if mid==right or array[mid] != array[mid+1]:
                return mid
            else:
                left = mid + 1
    print(&quot;找不到&quot;)
    return -1

#查找第一个值大于等于给定值的元素
def find_3(n):
    array = Array(100)
    array = sorted(array)
    left = 0
    right = len(array)-1
    while left &lt;= right:
        mid = int((left+right)&#47;2)
        if array[mid] &gt;= n:
            if mid==0 or array[mid-1]&lt;n:
                return mid
            else:
                right = mid - 1
        else array[mid] &lt; n:
            left = mid + 1
    print(&quot;找不到&quot;)
    return -1

#查找最后一个值小于等于给定值的元素
def find_4(n):
    array = Array(100)
    array = sorted(array)
    left = 0
    right = len(array)-1
    while left &lt;= right:
        mid = int((left+right)&#47;2)
        if array[mid] &lt;= n:
            if mid==right or array[mid+1]&gt;n:
                return mid
            else:
                left = mid + 1
        else array[mid] &gt; n:
            right = mid - 1
    print(&quot;找不到&quot;)
    return -1</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/b3/25b7984c.jpg" width="30px"><span>hopeful</span> 👍（0） 💬（0）<div>#实现一个有序数组的二分查找算法
import random
import time

def Array(n):
    a = []
    for i in range(n):
        a.append(random.randint(0 , n))
    return a

def find(n):
    array = Array(100)
    array = sorted(array)
    left = 0
    right = len(array)-1
    while left &lt;= right:
        mid = int((left+right)&#47;2)
        if array[mid] &gt; n:
            right = mid - 1
        elif array[mid] &lt; n:
            left = mid + 1
        else:
            return mid
    print(&quot;找不到&quot;)
    return -1</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>x 的平方根 go 语言实现 
func mySqrt(x int) int{

	if x==0{
		return 0
	}
	min:=1
	max:=x

	for {
		mid:=min+(max-min)&#47;2
		if mid*mid==x{
			return mid
		}else if mid*mid&lt;x{
			if (mid+1)*(mid+1)&gt;x{
				return mid
			}else{
				min=mid+1
			}
		}else{
			max=mid-1
		}

	}
}</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/88/be4fe19e.jpg" width="30px"><span>molybdenum</span> 👍（0） 💬（0）<div>老师新年好~这是我的作业
https:&#47;&#47;blog.csdn.net&#47;github_38313296&#47;article&#47;details&#47;86818929</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/64/7403c694.jpg" width="30px"><span>ALAN</span> 👍（0） 💬（0）<div>	&#47;&#47; find the k-th biggest number
	public int heapsort(int[] arr, int k) {
		&#47;&#47; build minimum heap
		for (int i = 1; i &lt;= k; i++) {
			while (i &#47; 2 &gt; 0 &amp;&amp; arr[i] &lt; arr[i &#47; 2]) { &#47;&#47; 自下往上堆化
				swap(arr, i, i &#47; 2); &#47;&#47; swap() 函数作用：交换下标为 i 和 i&#47;2 的两个元素
				i = i &#47; 2;
			}
		}
		&#47;&#47; replace the heap top element with the new element and heapify
		for (int i = k; i &lt; arr.length; i++) {
			if (arr[i] &lt;= arr[1])
				continue;
			else {
				arr[1] = arr[i];
				heapify(arr, k, 1);
			}
		}
		return arr[1];
	}

	public void swap(int[] arr, int j, int k) {
		int temp = arr[j];
		arr[j] = arr[k];
		arr[k] = temp;
	}

	private void heapify(int[] a, int n, int i) { &#47;&#47; 自上往下堆化
		while (true) {
			int minPos = i;
			if (i * 2 &lt;= n &amp;&amp; a[i] &gt; a[i * 2])
				minPos = i * 2;
			if (i * 2 + 1 &lt;= n &amp;&amp; a[minPos] &gt; a[i * 2 + 1])
				minPos = i * 2 + 1;
			if (minPos == i)
				break;
			swap(a, i, minPos);
			i = minPos;
		}
	}</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/64/7403c694.jpg" width="30px"><span>ALAN</span> 👍（0） 💬（0）<div>sort answer:
&#47;&#47; guibing sort
	public int[] gbsort(int[] arr, int start, int end) {

		if (start == end)
			return new int[] { arr[start] };
		int[] l1 = gbsort(arr, start, (start + end) &#47; 2);
		int[] r1 = gbsort(arr, (start + end) &#47; 2 + 1, end);
		return merge(l1, r1);

	}

	&#47;&#47; merge
	public int[] merge(int[] a, int[] b) {
		int[] c = new int[a.length + b.length];
		int j = 0, k = 0;
		for (int i = 0; i &lt; a.length + b.length; i++) {
			if (j == a.length) {
				c[i] = b[k];
				k++;
				continue;
			} else if (k == b.length) {
				c[i] = a[j];
				j++;
				continue;

			}
			if (a[j] &lt; b[k]) {
				c[i] = a[j];
				j++;
			} else {
				c[i] = b[k];
				k++;
			}

		}

		return c;
	}

	&#47;&#47; quick sort
	public void qsort(int[] arr, int start, int end, int index) {
		&#47;&#47; compare and swap
		if (start &gt;= end)
			return;
		int j = start, k = end;
		int value = (start + end) &#47; 2;
		while (j &lt; k) {
			for (; j &lt; k; k--) {
				if (k &lt;= value)
					break;
				else if (arr[k] &lt;= arr[value]) { &#47;&#47; from small to big &gt;=
					continue;
				} else {
					&#47;&#47; swap
					int temp = arr[k];
					arr[k] = arr[value];
					arr[value] = temp;
					value = k;
					break;
				}

			}
			for (; j &lt; k; j++) {
				if (j &gt;= value)
					break;
				else if (arr[j] &gt;= arr[value]) { &#47;&#47; from small to big &lt;=
					continue;
				} else {
					&#47;&#47; swap
					int temp = arr[j];
					arr[j] = arr[value];
					arr[value] = temp;
					value = j;
					break;
				}

			}
		}

		qsort(arr, start, j, index);
		qsort(arr, k + 1, end, index);
	}


</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（0） 💬（0）<div>&#47;&#47;平方根
&#47;&#47;递归的话会栈溢出
&#47;&#47;迭代法，要处理好溢出的问题，开始以为溢出时结果是负数，实测并非如此。
    public int sqrtLoop(int x) {
        return _mySqrtLoop(x,0,x&#47;2+1);
    }
    private int _mySqrtLoop(int x, int l, int r) {
        while(l&lt;r){
            int m = l+(r-l)&#47;2;
            long tmp = (long)m * (long)m;
            if(tmp==x||(tmp&lt;x &amp;&amp; (m+1)*(m+1)&gt;x)){
                return m;
            }else if(tmp&gt;x){
                r = m - 1;
            }else{
                l = m + 1;
            }
        }
        return l;
    }
</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（0） 💬（0）<div>package com.jxyang.test.geek.day3;
&#47;&#47;数组中求第k大的元素
public class BigK {
    public static void main(String[] args) {
        int[] arr = {3,5,6,9,7,4,2,1,11,16};
        BigK bigK = new BigK();
        System.out.println(bigK.findBigK(arr,10));
    }
    private int findBigK(int[] arr, int k) {
        if(k&gt;arr.length||arr==null){
            return -1;
        }
        int m = partition(arr,0,arr.length-1,k-1);
        return arr[m];
    }
    &#47;*
        [l,r]处理数组l到r的闭区间
        [l+1,j] 小于arr[l],[j+1,i] 大于arr[l]
        循环结束，arr[l] 与 arr[j] 交换
        返回j
     *&#47;
    private int partition(int[] arr, int l, int r,int k) {
        &#47;&#47;结束条件
        if(l==r)
            return l;
        int j =l;
        for(int i=l+1;i&lt;=r;i++){
            if(arr[i]&lt;arr[l]){
                j++;
                int tmp = arr[i];
                arr[i] = arr[j];
                arr[j] = tmp;
            }else{
                continue;
            }
        }
        int tmp = arr[l];
        arr[l] = arr[j];
        arr[j] = tmp;
        while(j!=k){
            if(j&lt;k){
                j = partition(arr,j+1,r,k);
            }else{
                j = partition(arr,l,j-1,k);
            }
        }
        return k;
    }
}
</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/f6/1ef70cab.jpg" width="30px"><span>你看起来很好吃</span> 👍（0） 💬（0）<div>求平方根用python实现，基于二分查找法思想：
class Solution:
    def mySqrt(self, x: &#39;int&#39;) -&gt; &#39;int&#39;:
        if x == 0:
            return 0

        left, right = 1, x

        while True:
            mid = (left + right) &#47;&#47; 2
            if mid * mid &gt; x:
                right = mid
            else:
                if (mid + 1) * (mid +1) &gt; x:
                    return mid
                left = mid</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/9a/f2c0a206.jpg" width="30px"><span>ext4</span> 👍（0） 💬（0）<div>求平方根
class Solution {
  public:
    int mySqrt(int x) {
      if (x &lt; 2) return x;
      long p = 1, q = x;
      long mid;
      while (p &lt;= q) {
        mid = (p + q) &#47; 2;
        if (mid == x &#47; mid) {
          return mid;
        } else if (mid &lt; x &#47; mid) {
          p = mid + 1;
        } else {
          q = mid - 1;
        }
      }
      return q;
    }
};
</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（0） 💬（0）<div>sqrt go 实现
package main

import &quot;fmt&quot;

func mySqrt(x int) int {
	low := float64(0)
	high := float64(x)
	for {
		mid := low + (high-low)&#47;2
		delta := float64(0)
		if mid*mid &gt; float64(x) {
			high = mid
			delta = mid*mid - float64(x)
		} else {
			low = mid
			delta = float64(x) - mid*mid
		}
		if delta &lt; 0.01 {
			return int(mid)
		}
	}
}

func main() {
	fmt.Println(mySqrt(8))
}
</div>2019-02-07</li><br/>
</ul>