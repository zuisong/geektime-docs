上一节我讲了冒泡排序、插入排序、选择排序这三种排序算法，它们的时间复杂度都是O(n2)，比较高，适合小规模数据的排序。今天，我讲两种时间复杂度为O(nlogn)的排序算法，**归并排序**和**快速排序**。这两种排序算法适合大规模的数据排序，比上一节讲的那三种排序算法要更常用。

归并排序和快速排序都用到了分治思想，非常巧妙。我们可以借鉴这个思想，来解决非排序的问题，比如：**如何在O(n)的时间复杂度内查找一个无序数组中的第K大元素？** 这就要用到我们今天要讲的内容。

## 归并排序的原理

我们先来看**归并排序**（Merge Sort）。

归并排序的核心思想还是蛮简单的。如果要排序一个数组，我们先把数组从中间分成前后两部分，然后对前后两部分分别排序，再将排好序的两部分合并在一起，这样整个数组就都有序了。

![](https://static001.geekbang.org/resource/image/db/2b/db7f892d3355ef74da9cd64aa926dc2b.jpg?wh=1142%2A914)

归并排序使用的就是**分治思想**。分治，顾名思义，就是分而治之，将一个大问题分解成小的子问题来解决。小的子问题解决了，大问题也就解决了。

从我刚才的描述，你有没有感觉到，分治思想跟我们前面讲的递归思想很像。是的，分治算法一般都是用递归来实现的。**分治是一种解决问题的处理思想，递归是一种编程技巧**，这两者并不冲突。分治算法的思想我后面会有专门的一节来讲，现在不展开讨论，我们今天的重点还是排序算法。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（337） 💬（12）<div>每次从各个文件中取一条数据，在内存中根据数据时间戳构建一个最小堆，然后每次把最小值给写入新文件，同时将最小值来自的那个文件再出来一个数据，加入到最小堆中。这个空间复杂度为常数，但没能很好利用1g内存，而且磁盘单个读取比较慢，所以考虑每次读取一批数据，没了再从磁盘中取，时间复杂度还是一样O(n)。</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/c1/aa9cde77.jpg" width="30px"><span>Light Lin</span> 👍（587） 💬（24）<div>伪代码反而看得费劲，可能还是对代码不够敏感吧</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/4d/a3237b34.jpg" width="30px"><span>李建辉</span> 👍（516） 💬（60）<div>先构建十条io流，分别指向十个文件，每条io流读取对应文件的第一条数据，然后比较时间戳，选择出时间戳最小的那条数据，将其写入一个新的文件，然后指向该时间戳的io流读取下一行数据，然后继续刚才的操作，比较选出最小的时间戳数据，写入新文件，io流读取下一行数据，以此类推，完成文件的合并， 这种处理方式，日志文件有n个数据就要比较n次，每次比较选出一条数据来写入，时间复杂度是O（n），空间复杂度是O（1）,几乎不占用内存，这是我想出的认为最好的操作了，希望老师指出最佳的做法！！！</div>2018-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/f0/1f86793d.jpg" width="30px"><span>sherry</span> 👍（84） 💬（8）<div>还是觉得伪代码更好，理解思路然后可以写成自己写练练手，看完代码后就没啥想写的欲望了。</div>2018-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4a/a2/37640e95.jpg" width="30px"><span>大汉</span> 👍（75） 💬（9）<div>我是一个笨的人，一节课要看很多遍，但是我知道，只要比聪明的人多看几遍，就也会达到同样的效果</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/63/f5988a98.jpg" width="30px"><span>斗米担米</span> 👍（43） 💬（3）<div>当 T(n&#47;2^k)=T(1) 时，也就是 n&#47;2^k=1
这个为什么会等于T(1)啊</div>2018-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/86/3be94807.jpg" width="30px"><span>angel😇txy🤓</span> 👍（32） 💬（6）<div>大家都说快排的伪代码不好理解，我用JAVA翻译了一下，实测通过，老师给个置顶哈。private static void quickSortC(int[] a, int p, int r) {
        if (p &gt;= r) {
            return;
        }
        int q = partition(a, p, r);
        quickSortC(a, p, q - 1);
        quickSortC(a, q + 1, r);
    }
    
    public static int partition(int[] a, int start, int end) {
        int pivot = a[end];
        int i = start;
        for (int j = start; j &lt; end; j++) {
            if (a[j] &lt; pivot) {
                swap(a, i, j);
                i = i + 1;
            }
        }
        swap(a, i, end);
        return i;
    }</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/bb/c488d5db.jpg" width="30px"><span>刘远通</span> 👍（17） 💬（1）<div>老师 这个地方我没看懂...
“第一次分区查找，我们需要对大小为 n 的数组执行分区操作，需要遍历 n 个元素。第二次分区查找，我们只需要对大小为 n&#47;2 的数组执行分区操作，需要遍历 n&#47;2 个元素。依次类推，分区遍历元素的个数分别为、n&#47;2、n&#47;4、n&#47;8、n&#47;16.……直到区间缩小为 1。”
这里讨论的是最平均的情况吗？ 最坏的情况可以n,n-1,...,1啊</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/78/f5/915d5442.jpg" width="30px"><span>xr</span> 👍（15） 💬（3）<div>你可能会说，我有个很笨的办法，每次取数组中的最小值，将其移动到数组的最前面，然后在剩下的数组中继续找最小值，以此类推，执行 K 次，找到的数据不就是第 K 大元素了吗？

应该是每次取数组中的最“大”值放到前面吧，因为找的是第k大元素？</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/7b/47be4ead.jpg" width="30px"><span>趁风卷</span> 👍（6） 💬（2）<div>快排的partition函数的空间复杂度是O(1)，但整个排序过程是递归的，最多会有O(logn)个函数放在栈里。这一部分不算空间复杂度么？</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/88/5e/e9a8417d.jpg" width="30px"><span>꧁花间一壶酒꧂</span> 👍（5） 💬（1）<div>这节看着有点懵</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/50/d476ed6c.jpg" width="30px"><span>Mr.Panda</span> 👍（5） 💬（3）<div>自己本地实现归并排序后，觉得归并排序终止条件p==r就可以了，没必要大于等于，因为p只存在小于等于r的情况，请作者指导下，我是不是哪里没考虑到？</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/a7/d379ca4f.jpg" width="30px"><span>jon</span> 👍（5） 💬（2）<div>归并时间复杂度推导时当 T(n&#47;2^k)=T(1) 时。  这里没看懂能解释一下吗</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/02/bc5ea779.jpg" width="30px"><span>Liam</span> 👍（4） 💬（2）<div>归并排序真的不能原地吗？</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cc/33/19f150d9.jpg" width="30px"><span>城</span> 👍（4） 💬（2）<div>快排的伪代码写的过于简单，能否按照面试级别给我们写个实例代码呢</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/36/2e/376a3551.jpg" width="30px"><span>ano</span> 👍（3） 💬（2）<div>伪代码里的 :=  是什么意思啊？

partition(A, p, r) {
  pivot := A[r]
  i := p
  for j := p to r-1 do {
    if A[j] &lt; pivot {
      swap A[i] with A[j]
      i := i+1
    }
  }
  swap A[i] with A[r]
  return i
</div>2020-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（3） 💬（2）<div>请问老师，终止条件啥时候会出现大于号的情况？（终止条件：p &gt;= r）</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/43/7b4a11cc.jpg" width="30px"><span>梦总被尿憋醒</span> 👍（3） 💬（1）<div>分区找第K大元素用排序吗？</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c4/ab/6ff34df1.jpg" width="30px"><span>Senal</span> 👍（2） 💬（3）<div>@Test
    public void test(){

        int[] a = {7,2,28,5,3,38,9,11,57,25,18,21,51,34,23};
&#47;&#47;        int[] a = getIntArray();
        quick(a, 0 , a.length-1);
        System.out.println(Arrays.toString(a));
    }



    private int[] quick(int[] a, int p, int r){

        if(p&gt;=r) {
           return a;
        } else {
            int q = sort(a, p ,r);
            quick(a, p ,q-1);
            return quick(a, q+1, r);
        }
    }

    private int sort(int[] a, int p, int r){
        int end = a[r];
        int i = p;
        for (int j = p; j &lt; r ;j++){
            if (a[j] &lt; end){
                int temp = a[i];
                a[i] = a[j];
                a[j] = temp;
                i++;
            }
        }
        int temp = a[i];
        a[i] = a[r];
        a[r] = temp;
        return i;
    }
这个是我写的快排java实现，如果有问题也希望老师可以指出，还有就是不太明白文章末尾，为什么第一次分区是n，第二次是2&#47;n，明明最后一个数的分区并不能等分，为什么每次都是乘以1&#47;2？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（1）<div>老师，讲的思路都基本看懂了，想问个小白的问题哈，就是数组[p,...r]如果取中间位置值q，假如像[0,..10]数组个数为11个，那么q值是(0+10)&#47;2=5吧？而[0,..9,]数组个数为10个，q值是(0+9)&#47;2=4吧？</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c0/5c/087abb7f.jpg" width="30px"><span>风</span> 👍（1） 💬（1）<div>老师能不能把这篇文章的伪代码改为代码,看着理解起来挺费劲</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4f/17/2185685f.jpg" width="30px"><span>Zhangxuesong</span> 👍（1） 💬（1）<div>当下标从 p 到 q 和从 q+1 到 r 这两个子数组都排好序之后，我们再将两个有序的子数组合并在一起，这样下标从 p 到 r 之间的数据&quot;就也&quot;  -&gt;  &quot;也就&quot;  排好序了。</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e0/20/003190c1.jpg" width="30px"><span>康斯坦丁</span> 👍（1） 💬（1）<div>T(n&#47;2^k)=T(1)
这个推导过程，可以再详细说一下嘛</div>2019-02-25</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLmBgic9UlGySyG377pCVzNnbgsGttrKTCFztunJlBTDS32oTyHsJjAFJJsYJyhk9cNE5OZeGKWJ6Q/132" width="30px"><span>beiliu</span> 👍（1） 💬（3）<div>老师，我想问一个问题，为什么快排是不稳定的，如果我们每次都取最后一个做分区点，然后0到n-1，当遍历到的数据小于等于分区点数据时就进行交换，遍历完之后再改变分区点的位置，我觉得这样快排是稳定的呀</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/5d/3a75c20b.jpg" width="30px"><span>Geek_bd6gy9</span> 👍（1） 💬（1）<div>相比之前的三个排序算法理解起来比较困难，还得琢磨琢磨......</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/37/11/dc26e43e.jpg" width="30px"><span>头像不好看</span> 👍（0） 💬（1）<div> 归并排序最后将临时数组中的值赋给原来的数组的循环语句中，i的限制条件为什么是r-p，不能是a.length-1

for (i = 0; i &lt;= r-p; ++i) {
      a[p+i] = tmp[i];
    }
  }</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d4/47/0deb44d6.jpg" width="30px"><span>技术小生</span> 👍（0） 💬（1）<div>这是不是使用归并排序的并的过程</div>2019-10-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKvgSccCBPlzUo1SvJoAXuSMmTtGA9zQA9I4HmwIsm6tpDic1iao6YRppkTBibQXcLaGO5icUtxqqDWzA/132" width="30px"><span>mrkou47</span> 👍（0） 💬（1）<div>“你可能会说，我有个很笨的办法，每次取数组中的最小值，将其移动到数组的最前面，然后在剩下的数组中继续找最小值，以此类推，执行 K 次，找到的数据不就是第 K 大元素了吗？” 这个对吗。。我傻了，如果找 [1,2,3,4,5,6] 中第2大元素，不是5么？执行2次，不是求出的是3吗？？</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/64/0f/12b1b224.jpg" width="30px"><span>Mercury</span> 👍（0） 💬（1）<div>我觉得可不可以将一个文件中的时间段分为3段，放入3个新文件（或者时间不均匀的话分为更多发段）然后，再取一个文件到内存里按顺序依次插入对应时间段的文件中。以此类推，这样是不是可以提高效率呢</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/57/2d92cf9a.jpg" width="30px"><span>姜川</span> 👍（0） 💬（2）<div>有疑问，查找第K大的那个是不是用了二分查找的思想，但前提是先排好序，但无序序列排序最快也达不到O（n）呀</div>2019-10-14</li><br/>
</ul>