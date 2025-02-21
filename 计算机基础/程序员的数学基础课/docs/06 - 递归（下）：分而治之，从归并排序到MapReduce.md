你好，我是黄申。

上一节，我解释了如何使用递归，来处理迭代法中比较复杂的数值计算。说到这里，你可能会问了，有些迭代法并不是简单的数值计算，而要通过迭代的过程进行一定的操作，过程更加复杂，需要考虑很多中间数据的匹配或者保存。例如我们之前介绍的用二分查找进行数据匹配，或者我们今天将要介绍的归并排序中的数据排序等等。那么，这种情况下，还可以用递归吗？具体又该如何来实现呢？

我们可以先分析一下，这些看似很复杂的问题，是否可以简化为某些更小的、更简单的子问题来解决，这是一般思路。如果可以，那就意味着我们仍然可以使用递归的核心思想，将复杂的问题逐步简化成最基本的情况来求解。因此，今天我会从归并排序开始，延伸到多台机器的并行处理，详细讲讲递归思想在“分而治之”这个领域的应用。

## 归并排序中的分治思想

首先，我们来看，如何使用递归编程解决数字的排序问题。

对一堆杂乱无序的数字，按照从小到大或者从大到小的规则进行排序，这是计算机领域非常经典，也非常流行的问题。小到Excel电子表格，大到搜索引擎，都需要对一堆数字进行排序。因此，计算机领域的前辈们研究排序问题已经很多年了，也提出了许多优秀的算法，比如归并排序、快速排序、堆排序等等。其中，归并排序和快速排序都很好地体现了分治的思想，今天我来说说其中之一的**归并排序**（merge sort）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/69/df/2dca1305.jpg" width="30px"><span>Healtheon</span> 👍（185） 💬（5）<div>老师讲的是最经典的2路归并排序算法，时间复杂度是O(NlogN)。如果将数组分解成更多组（假设分成K组），是K路归并排序算法，当然是可以的，比如K=3时，是3路归并排序，依次类推。3路归并排序是经典的归并排序（路归并排序）的变体，通过递归树方法计算等式T(n)= 3T(n&#47;3)+ O(n)可以得到3路归并排序的时间复杂度为O(NlogN)，其中logN以3为底（不方便打出，只能这样描述）。尽管3路合并排序与2路相比，时间复杂度看起来比较少，但实际上花费的时间会变得更高，因为合并功能中的比较次数会增加。类似的问题还有二分查找比三分查找更受欢迎。</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/76/9d/bfcdbdda.jpg" width="30px"><span>大悲</span> 👍（33） 💬（2）<div>思考题：
如果不是分为两组，而是多组是可行的，但是处理起来比较麻烦。虽然分组的时候，能够更快完成，但是在合并的时候需要同时比较多组中的数据，取最小的一个。当分组数量比较大的时候，在合并的时候，为了考虑效率，需要维护一个堆来取最小值。假设分为N组，分组的时间复杂度是logn(N为底), 合并的时候时间复杂度为nlogN，总的时间复杂度不变，还是nlogn。不知道理解对不对，请老师指教！</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a7/87/4f2fa359.jpg" width="30px"><span>swortect</span> 👍（25） 💬（3）<div>老师，如果要排序的数组很大，两个最大的子节点排好序之后，交给最终的机器做最后的排序依然是一堆数据放在一个机器上</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6b/85/28fc85c5.jpg" width="30px"><span>指间砂的宿命</span> 👍（13） 💬（1）<div>分成超过两个组的更多组是可行的，不过这样在递归调用时一个是有可能产生更多的中间状态数据，再一个在合并阶段，需要比较更多个分组的数据，实际上在最小粒度的时候，比较大小的就是两个数字，即便上层分成多个组，在合并的最底层依旧是从两两之间比较合并的，感觉分成多组的并没有啥优势，还带来了比较处理的复杂性</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/13/5197f8d2.jpg" width="30px"><span>永旭</span> 👍（9） 💬（1）<div>老师,你好
归并排序代码中有非空判断代码
if (a == null) a = new int[0];
if (to_sort == null) return to_sort;
什么情况下会出现数组是null??
</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/8e/7b6ea886.jpg" width="30px"><span>Joe</span> 👍（8） 💬（1）<div>分成多组归并，主要是合并比较会比较麻烦，会在合并时增加复杂度。比如比较2个数大小，只需要1次，而比较3个数大小，最多需要3次。</div>2019-01-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIEONynt1pibq4AInxllIgSz3zJrB4tiabJwibYAohfcGTvScicboZkM03Wgic4dA4H1obcyAm9nbGR4pA/132" width="30px"><span>会飞的猪</span> 👍（8） 💬（1）<div>python实现代码：
def mergeSort(list):
    if(len(list)==0):
        return 0
    if(len(list)==1):
        return list[0]
    else:
        listHalfLen=int(len(list)&#47;2)
        left=mergeSort(list[0:listHalfLen])
        right=mergeSort(list[listHalfLen:])
        data=merge(left,right)
        return data

def merge(left,right):
    mid=[]
    ai=0
    bi=0
    if(isinstance(left,int)):
        leftLen=1
        left=[left]
    else:
        leftLen=len(left)
    if(isinstance(right,int)):
        rightLen=1
        right=[right]
    else:
        rightLen = len(right)
    while(ai &lt; leftLen and bi &lt; rightLen):
        if(left[ai]&lt;right[bi]):
            mid.append(left[ai])
            ai+=1
        else:
            mid.append(right[bi])
            bi+=1
    if(ai&lt; leftLen):
        newleft=left[ai:]
        for i in newleft:
            mid.append(i)
    else:
        newright = right[bi:]
        for i in newright:
            mid.append(i)
    return mid
list=[3,8,5,9,7,1,10]
mergeSort(list)
刚学python，希望大家多多指教</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/9d/9673a0f8.jpg" width="30px"><span>叶嘉祺</span> 👍（6） 💬（1）<div>可以用数学方法证明二分归并排序是最优的应该。二分查找是可以证明的。

二分法我是这样证明的: https:&#47;&#47;ghostbody.github.io&#47;posts&#47;algorithmn&#47;prove-binary-search-is-better&#47;

对于归并排序我还在思考利用主定理进行证明。

老师可以一起看下怎么证？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/d0/ed066d6a.jpg" width="30px"><span>有品味的混球</span> 👍（6） 💬（2）<div>MapReduce 分割，映射，洗牌，归约这几个步骤没有具体的例子，就感觉不是很明白，希望这几个步骤还是用文章前半部分的排序的例子来分别举例</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/e6/83bdccda.jpg" width="30px"><span>子非</span> 👍（6） 💬（1）<div>递归层次太多了，堆栈会溢出</div>2019-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/0e/e40ce6ea.jpg" width="30px"><span>刘明</span> 👍（5） 💬（2）<div>和快排对比，虽然时间复杂度都是nlogN，但是归并排序的空间复杂度是O(n)，快排则是原地排序。不过归并排序是稳定排序，快排则不是，两种各有优势。</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（4） 💬（1）<div>茶艺师学编程


递归的“分而治之”的思想，其实在社会中能找到相应的例子。


往古老的说，在工业革命之前，西方世界的社会结构就符合递归的“分而治之”：最顶端是国王，下一层是各个贵族，贵族下面是骑士（日本是武士）。国王只管他下面的贵族，贵族的骑士他是不管的；同样的，贵族只管他下面的骑士，骑士下面的人他是不管的。就是所谓“仆人的仆人不是自己的仆人。”


就今天而言，很多单位的组织结构，其实也是这样“分而治之”。一个国家的总理管着各个省长，省长管着市长，市长管着县长——每一级组织都是上一级组织的缩小版，而且在管理上，不提倡越级管理。


当然，能把递归玩的炉火纯青的，还得属于各位程序员大神。


关于思考题，在归并排序的时候为什么每次都将原有的数组分解成两组，而不是更多组？如果分为更多组，是否可行？


那是因为，“两两比较”才是排序的最小步骤，如果分更多的组，会增加运算过程中的不确定性，甚至无法使用递归思想来实现。

</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/55/e4/7061abd5.jpg" width="30px"><span>Mr.J</span> 👍（4） 💬（1）<div>老师您好，归并这种，比如数组排序无限的对半分开，这样会不会性能反而不如对半分开到一定程度，剩下的用别的排序算法，应该有一个平衡点吧</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/f0/82281239.jpg" width="30px"><span>Ricky</span> 👍（3） 💬（1）<div>&#47;*
 * 采用分而治之思想实现数组排序, 递归为其实现技巧
 *&#47;
#include &lt;iostream&gt;

using namespace std;

void merge(int *array, int low, int mid, int high) {
    &#47;&#47; left: low ~ mid, right: mid+1 ~ high
    int size = high - low + 1;
    int *tmp = new int[size];
    int i = low, j = mid+1, k = 0;
    while (i &lt;= mid &amp;&amp; j &lt;= high) {
        if (array[i] &lt;= array[j]) {
            tmp[k++] = array[i++];
        } else {
            tmp[k++] = array[j++];
        }
    }

    &#47;&#47; the rest elements
    while (i &lt;= mid) {
        tmp[k++] = array[i++];
    }
    while (j &lt;= high) {
        tmp[k++] = array[j++];
    }

    &#47;&#47; copy the elements to original array
    for (k = 0; k &lt; size; ++k) {
        array[k+low] = tmp[k];
    }
}

void _mergeSort(int *array, int low, int high) {
    if (low &gt;= high) return;
    int mid = low + ((high-low) &gt;&gt; 1);
    _mergeSort(array, low, mid);
    _mergeSort(array, mid+1, high);
    merge(array, low, mid, high);
}

void mergeSort(int *array, int size) {
    cout &lt;&lt; &quot;*****************before**************&quot; &lt;&lt; endl;
    for (int i = 0; i &lt; size; ++i) {
        cout &lt;&lt; array[i] &lt;&lt; &quot; &quot;;
    }
    cout &lt;&lt; endl;
    _mergeSort(array, 0, size-1);
    cout &lt;&lt; &quot;*****************after**************&quot; &lt;&lt; endl;
    for (int i = 0; i &lt; size; ++i) {
        cout &lt;&lt; array[i] &lt;&lt; &quot; &quot;;
    }
    cout &lt;&lt; endl;
}

int main() {

    int array[] = {2, 3, 5, 1, 4, 9, 7, 6, 10};
    mergeSort(array, 9);

    return 0;
}
*****************before**************
2 3 5 1 4 9 7 6 10
*****************after**************
1 2 3 4 5 6 7 9 10
</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/34/04/57e42586.jpg" width="30px"><span>Geek_2426</span> 👍（2） 💬（1）<div>学到了，学到了，数学好难，又爱又恨</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/75/be/6f3ab95e.jpg" width="30px"><span>拉普达</span> 👍（2） 💬（1）<div>二分是最优的。两个数一次比较就能确定序关系。3个数需要3次，4个需要5次。N个数的情况，需要k次（2＾k≥N!）。分得越多，merge效率越低。只有N=2，merge的过程效率最高。</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6d/29/ae69a30f.jpg" width="30px"><span>méng</span> 👍（1） 💬（2）<div>js 写的代码


function guibingorder(arr) {

if (arr.length &gt; 1) {
var leftarr = [];
var rightarr = [];
var splitindex = Math.floor(arr.length &#47; 2);
leftarr = arr.slice(0, splitindex);
rightarr = arr.slice(splitindex, arr.length);

leftarr = arguments.callee(leftarr);
rightarr = arguments.callee(rightarr);

var result = [];
while (Math.max(leftarr.length, rightarr.length) &gt; 0) {
&#47;&#47;右边遍历完了 或者 左边比右边的小，则 从左边取出来
if (rightarr.length == 0 || leftarr[0] &lt; rightarr[0]) {
result.push(leftarr[0]);
leftarr.splice(0, 1);
} else {
result.push(rightarr[0]);
rightarr.splice(0, 1);
}
}

return result;
}
return arr;
}</div>2019-01-11</li><br/><li><img src="" width="30px"><span>代码世界没有爱情</span> 👍（1） 💬（1）<div># python实现
# 切分
def split_list(temp_list):
    if not isinstance(temp_list, list):
        raise TypeError
    else:
        if not temp_list:
            raise ValueError
        else:
            length = len(temp_list)
            if length == 1:
                return temp_list
            import math
            left = math.ceil(length &#47; 2)
            del math
            left_list = split_list(temp_list[:left])
            right_list = split_list(temp_list[left:])
            return merger_list(left_list, right_list)


# 归并
def merger_list(left, right):
    result = []
    while True:

        if left and right:
            left_0 = left[0]
            right_0 = right[0]
            if left_0 &gt; right_0:
                min_num = right.pop(0)
            else:
                min_num = left.pop(0)
            result.append(min_num)
        elif left:
            result.append(left.pop(0))

        elif right:
            result.append(right.pop(0))
        else:
            break
    return result


print(split_list([3, 1, 2, 7, 4, 6, 9, 9, 10, 11, 4, 5]))</div>2018-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6b/5e/b76e7a79.jpg" width="30px"><span>我心留</span> 👍（1） 💬（1）<div>老师，我觉得排序的功能应该体现在合并的那块函数中吧，所以第二个函数的功能应该是排序并合并两个数组吧，第一个函数只体现了分解的功能，所以嵌套调用时，只是对两半进行分解，而不是排序。我这样理解对吗，老师？</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/79/ea/8fe22e74.jpg" width="30px"><span>晓嘿</span> 👍（1） 💬（1）<div>老师
“归并排序通过分治的思想，把长度为 n 的数列，每次简化为两个...只需要 log2n 次归并。”
这句话，需要的归并次数是我算着是: 简化的组数：1,2^1,2^2..2^k。归并的时候，应该合并2^0+2^1+2^2+..+2^(k-1)次，也就是2^k-1次。我这么想对吗，老师。

</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/36/52/216e5a30.jpg" width="30px"><span>Y K</span> 👍（1） 💬（1）<div>JDK自带的Arrays.sort(T[] a, Comparator&lt;? super T&gt; c)底层采用的就是归并排序，归并排序相对于快排而言是一种稳定的排序。</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ef/1a/e7ebdfa8.jpg" width="30px"><span>道可</span> 👍（1） 💬（1）<div>请问老师用的是什么IDE</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>N&#47;2 可以优化为移位，N&#47;3 可能会有点麻烦</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/20/06/6ca43f2d.jpg" width="30px"><span>厚积薄发</span> 👍（0） 💬（1）<div>谢谢老师，一直看那些算法云里雾里的，看了您的长篇引导，已经可以根据理解自己写出归并排序了</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/39/c6/1e12f271.jpg" width="30px"><span>凹凸鸿</span> 👍（0） 💬（1）<div>我们假设 n=k-1 的时候，我们已经对较小的两组数进行了排序。那我们只要在 n=k 的时候，将这两组数合并起来，并且保证合并后的数组仍然是有序的就行了

这里不解啊，为什么之前的文章和这里都用假设n=k-1，然后又n=k，n代表什么，k又代表什么？？？？老师能展开讲讲吗</div>2020-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/98/9779cf40.jpg" width="30px"><span>小北</span> 👍（0） 💬（1）<div>老师，请教一个问题。针对嵌套深的递归。是不是都需要转化为非递归堆栈实现递归？我看很多数据结构算法的源码都是才用的非递归方式模拟递归，请问哪一种方式的应用多一些？</div>2020-09-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erWrGjD40JI6WTIaSLfZ9icTyuuLEpPwCicr3Fv2icy8mibHBj5icMpIGxp9UD8rLIQib1RLpXIrwKaQxOA/132" width="30px"><span>peace</span> 👍（0） 💬（1）<div>多路归并在辅导书上有出现过，这一节开始的那两个有序数组合并的过程让我明白了归并中合并这一步的原理，懂得了就算是只有两个只包含一个元素的数组合并，也是执行上述过程</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/f6/1cdb3d52.jpg" width="30px"><span>乐达</span> 👍（0） 💬（1）<div>分成更多组是可以的。但是在合并的时候会更复杂。</div>2020-03-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>如果分成n组，那么合并结果的时候就要合并n组结果，那么又产生了一个新的排序问题，所以觉得不太可取。</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/b9/73435279.jpg" width="30px"><span>学习学个屁</span> 👍（0） 💬（1）<div>分为两个组，查询效率应该比分成多个组查询效率高。
分为多组的话，三组之间需要两两比较，所花费的时间比两组对比时间要多。</div>2019-11-21</li><br/>
</ul>