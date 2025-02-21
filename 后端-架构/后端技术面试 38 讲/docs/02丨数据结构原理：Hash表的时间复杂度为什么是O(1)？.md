大概十年前，我在阿里巴巴工作的时候，曾经和另一个面试官一起进行一场技术面试，面试过程中我问了一个问题：**Hash表的时间复杂度为什么是O(1)**？候选人没有回答上来。面试结束后我和另一个面试官有了分歧，我觉得这个问题没有回答上来是不可接受的。而他则觉得，这个问题有一点难度，回答不上来不说明什么。

因为有了这次争执，后来这个问题成了我面试时的必考题。此后十年间，我用这个问题面试了大约上千人，这些面试经历让我更加坚定了一个想法：这个问题就是候选人技术水平的一个分水岭，是证明一个技术人员是否具有必备专业技能和技术悟性的一个门槛。这个槛过不去是不可接受的。

为什么呢？我很难相信，如果基本的数据结构没有掌握好，如何能开发好一个稍微复杂一点的程序？

要了解Hash表，需要先从数组说起。

## 数组

数组是最常用的数据结构，创建数组必须要内存中一块**连续**的空间，并且数组中必须存放**相同**的数据类型。比如我们创建一个长度为10，数据类型为整型的数组，在内存中的地址是从1000开始，那么它在内存中的存储格式如下。

![](https://static001.geekbang.org/resource/image/c9/71/c98f1f08afacdb9754e6d18c1d7e0471.png?wh=600%2A860)  
由于每个整型数据占据4个字节的内存空间，因此整个数组的内存空间地址是1000～1039，根据这个，我们就可以轻易算出数组中每个数据的内存下标地址。利用这个特性，我们只要知道了数组下标，也就是数据在数组中的位置，比如下标2，就可以计算得到这个数据在内存中的位置1008，从而对这个位置的数据241进行快速读写访问，时间复杂度为O(1)。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/41/40/5489dae0.jpg" width="30px"><span>_funyoo_</span> 👍（78） 💬（31）<div>说说我的思考：
方法1：在遍历链表1，看该结点是否在2中存在，若存在，即为合并。
遍历的方法：①两个for嵌套 ②根据1建立hash表，遍历2时在1中查找

方法2：计算两个链表的长度，谁长谁先“往前走”，待长链表未查看长度等于短链表是，两两元素比较，遍历完未出现相同时，则没有合并

方法3：直接比较两个链表的最后一个元素，相等即合并</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6b/b9/9b0630b1.jpg" width="30px"><span>Geek_9c3134</span> 👍（57） 💬（7）<div>老师 你这问题我问了别人  发现只回答到了数组下标  没有人讲到内存  还说我的问题太简单了</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/ec/0c24c4f5.jpg" width="30px"><span>breezeQian</span> 👍（13） 💬（3）<div>步骤一：将长度短的链表的元素构造成哈希表，key是指针，value是节点值。
步骤二：遍历较长链表找出合并的节点</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3c/d4/f42afcda.jpg" width="30px"><span>晶晶</span> 👍（8） 💬（2）<div>是我听过的课程里面觉得最让我思路清晰的课程~所以先打卡沙发一下☺</div>2019-11-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Yofo8cTYBLlos9KXpEQW3YBgu2WN8bDIOBUKiciar7mFY4fxJz1Dz6reHRCy9icN3YAd7lqnpT4QReGvibYZS8VpnQ/132" width="30px"><span>Geek_ac779f</span> 👍（7） 💬（2）<div>老师，为什么有些数据结构的内存空间不要求是连续的？都是连续的内存空间不好吗。既然连续和不连续的内存空间都可以实现这些数据结构，使用不连续的内存空间实现有什么好处呢，利用率更高吗。为什么利用率更高呢，不都是以字节为基本单位吗</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/87/46d7e1c2.jpg" width="30px"><span>Better me</span> 👍（2） 💬（2）<div>老师，文中这段话“想在 b 和 c 之间插入一个元素 x，只需要将 b 指向 c 的指针修改为指向 x，然后将 x 的指针指向 c 就可以了”感觉反过来说更合理一些，如果按以上顺序代码实现会出现指针丢失内存泄漏的情况吧。</div>2019-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b7/00/12149f4e.jpg" width="30px"><span>郭刚</span> 👍（2） 💬（2）<div>类似Oracle中的hash join的算法</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/18/6e44e6e0.jpg" width="30px"><span>恺撒之剑</span> 👍（1） 💬（1）<div>课程中的数组示意图，长度为10的整数数组，地址从1000开始，下标为9的数组对应的起始地址应该为1036，而不是1039</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6a/03/cb597311.jpg" width="30px"><span>远心</span> 👍（1） 💬（2）<div>实现了同时遍历两个单向链表的方法，欢迎拍砖：https:&#47;&#47;github.com&#47;Huan-Rong&#47;geektime-backend-technology-basics&#47;blob&#47;master&#47;sources&#47;2-the-time-complexity-of-hash-table&#47;src&#47;main&#47;java&#47;site&#47;blbc&#47;MergeDetect.java</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7c/03/2941dea7.jpg" width="30px"><span>幸福来敲门</span> 👍（1） 💬（3）<div>由于每个整型数据占据 4 个字节的内存空间，因此整个数组的内存空间地址是 0x1000～0x1039，根据这个，我们就可以轻易算出数组中每个数据的内存下标地址。利用这个特性，我们只要知道了数组下标，也就是数据在数组中的位置，比如下标 2，就可以计算得到这个数据在内存中的位置 0x1008。

请问这个内存16进制地址是怎么得出来的？ 0x1000～0x1039 

</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（1） 💬（2）<div>基于单向链表的特性，  为链一的地址建立hash  然后便利链表2  存在就返回，指到null 了就没有合并。

下面写伪码实现 手机上输入的，就不整理了
p1  = &amp;p1_head
while  p1
hsets[p1] =*p1
p1 = *p1 箭头 
next

p2 = &amp;p2_head
while(p2)
if  isset hsets  p2   return   
p2  = *p2 箭头next
</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/78/74/b04ee2af.jpg" width="30px"><span>杨光</span> 👍（0） 💬（1）<div>刚刚做过这题，C语言实现

&#47;**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 *&#47;
struct ListNode *getIntersectionNode(struct ListNode *headA, struct ListNode *headB) {
    if(headA == NULL || headB == NULL) return NULL;
    struct ListNode *pA = headA, *pB = headB;
    while(pA != pB) {
        pA = pA == NULL ? headB : pA-&gt;next;
        pB = pB == NULL ? headA : pB-&gt;next;
    }
    return pA;
}</div>2020-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c4/f3/92f654f1.jpg" width="30px"><span>Bug? Feature!</span> 👍（19） 💬（0）<div>思路特别清晰，但是都是点到为止呀，感觉差点啥，哈哈，可能后面的文章会具体介绍，更加详细。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d9/52/73351eab.jpg" width="30px"><span>　扬帆丶启航　</span> 👍（18） 💬（4）<div>计算两个链表的长度，用长的链表减去短的链表，计算出差值，长的链表先向后移动差值的个数，然后两个链表再同时移动，判断一下个节点的地址是否相同。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/75/02b4366a.jpg" width="30px"><span>乘坐Tornado的线程魔法师</span> 👍（8） 💬（1）<div>思考题：第一步：分别遍历针对两个链表A、B（先不考虑长度差）。第二步：如果A链表先走到了末尾那么把A链表的指针指向B链表的第一个节点，继续遍历B链表；B链表的原始指针继续做遍历不变，走到末尾后，将B链表的指针指向A链表的第一个节点，继续遍历A链表。第三步：两个链表继续做遍历，如果分别指向的节点数值（地址）相同，那么这两个链表就是合并链表，这个节点就为合并的第一个节点。

思想：通过指针的变换指向，很好滴解决的长度差的问题。消除两个链表的长度差带来的影响，</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/85/b1/fe357d1a.jpg" width="30px"><span>Anne</span> 👍（3） 💬（0）<div>暴力法：双重循环，针对链表1的每个元素，对链表2的每个元素进行遍历，比较是否相等，第一个相等的元素就是相交点
使用栈：将两个链表的元素分别放入2个栈中，分别弹出栈顶元素，进行比较，如果栈顶元素相同则相交，相交之后第一个不相同元素的前一个元素就是相交点
判断两个链表的长度：如果长度不同，比如一个是n，一个m，较长的链表先走n-m步，然后两个链表一起遍历，相同的元素即为交点。如果长度相同，一起遍历。</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（2） 💬（0）<div>看到题目，我也回答不上来，为什么 Hash 表的访问时间复杂度是 O(1)，后来看了专栏才知道（想起来），Hash 表的底层实现其实是数组。然后老师在留言里面提到的 Hash 表高阶问题，更是问的我一头大汗。

即使是简单的数据结构，也能问出来好问题。

课后思考题，单向链表合并，其实是 LeetCode 的 160 题，Intersection of Two Linked Lists。

官方给出了三个解题思路：

1. Brute Force 暴力解法，双重循环遍历两个链表，时间复杂度 O(mn)，空间复杂度 O(1)
2. Hash Table 哈希表，将一个链表转为 Hash 表，然后遍历另一个链表，时间复杂度 O(m+n)，空间复杂度 O(m) 或 O(n)
3. Two Pointers 双指针，同时遍历两个链表，遍历到一条链表终点之后，续到另一条链表头部，比较两个指针，如果相等，则为交点

因为这一篇以 Hash 表为题，所以第二个解法比较容易想到。

public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        &#47;&#47; boundary check
        if (headA == null || headB == null) {
            return null;
        }
        ListNode pA = headA;
        ListNode pB = headB;
        &#47;&#47; if a &amp; b have different len,
        &#47;&#47; then we will stop the loop after second iteration
        while (pA != pB) {
            &#47;&#47; for the end of first iteration,
            &#47;&#47; we just reset the pointer to the head of another linkedlist
            pA = pA == null ? headB : pA.next;
            pB = pB == null ? headA : pB.next;
        }
        return pA;
    }
}</div>2020-09-20</li><br/><li><img src="" width="30px"><span>王杰</span> 👍（2） 💬（1）<div>其实这个问题可以归纳为两链表是否具有相同的元素地址。具体：两层for循环，查找相同的指针地址</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/77/0c593044.jpg" width="30px"><span>碧雪天虹</span> 👍（1） 💬（0）<div>把两个链表都入栈, 然后从栈顶开始同时出栈, 如果某一轮出栈两个元素不同, 那么前一轮的就是x元素</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/d1/209abdd6.jpg" width="30px"><span>小狼</span> 👍（1） 💬（0）<div>“但是正因为链表是不连续存储的，所以在链表中插入或者删除一个数据是非常容易的，只要找到要插入（删除）的位置，修改链表指针就可以了” 这句话的归因“但是正因为链表是不连续存储的”不严谨，插入或者删除一个数据非常容易并不是因为链表是不连续存储的，而是因为本质上链表指针的设计，有了这些指针，即便链表的存储是连续的，也丝毫不影响插入或者删除一个数据的快捷性，也即链表中插入或删除数据方便跟链表的存储分配是否连续没有因果关系</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/55/198c6104.jpg" width="30px"><span>小伟</span> 👍（1） 💬（0）<div>之前只给了伪代码，感觉不过瘾，同时也验证自己的思路是否正确，就实现了下，请老师和同学拍砖。
https:&#47;&#47;github.com&#47;ToddSAP&#47;Geektime&#47;blob&#47;master&#47;src&#47;backendinterview38&#47;course2&#47;LinkedListMergedTest.java</div>2020-02-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq36dSapVA92lPpicBALBsecgwN1uIJQUfqwa6eTz2BuibebH11W4DAmeJeV5aedBY2KIcKLMTIl67A/132" width="30px"><span>小烽</span> 👍（1） 💬（1）<div>我的思考去下：能想到的就是遍历，结合前面几位的方法，做个比较。假设长度分别为m和n，m大。
方法一：先去遍历m 链表到m-n,然后同时遍历两个链表，比较大小，时间复杂度是O(m)

方法二：取一条链表的值放入hash 表，另一个链表进行遍历，在没有hash 冲突的情况下，时间复杂度应该是O(m+n)

方法三：从链表末端开始比较，时间复杂度应该也是O(m+n)

不知道理解的对不对。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/77/13/a424f771.jpg" width="30px"><span>小太白52度</span> 👍（1） 💬（1）<div>1.将两个单链表顺序颠倒，即由尾指向头；
2.将两个新链表由头开始一一比较，直到两个元素不想等；
3.若第一元素即不等，则两个链表不合并，否则最后一个相等元素即为合并处的元素。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/1d/4e193dae.jpg" width="30px"><span>Geek_60eace</span> 👍（1） 💬（0）<div>获取2个列表的所有指针，进行交集运算，抛出第一个指针就是开始合并的地方</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/4c/46c43cce.jpg" width="30px"><span>小祺</span> 👍（1） 💬（0）<div>0x1000～0x1036写成了0x1000～0x1039</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/f2/d5/d5417f4e.jpg" width="30px"><span>就是那个刘涛</span> 👍（0） 💬（0）<div>思考题：
我会用一个while循环来实现。设置两个指针分别只想两个链表的头，比较两个节点，谁小则指针右移，直到节点值相等，返回合并的节点。时间复杂度为O(n)</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f7/4c/9efa9ece.jpg" width="30px"><span>李凯</span> 👍（0） 💬（0）<div>提供一个思路，遍历两个链表，分别压入二个栈。看栈顶元素是否相同。如果是，那么就发生了合并。接着，同时做出栈操作，一直到出栈的元素不相等为止，最后那个相同的元素就是x。</div>2023-03-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/62QVu6oNeyYib4Ch8oaWuoiboQdweTDC45wOeic6ib3ShJ9DfibpggtKmvnUX2gSKIUrNtKUkqaEeqhVU377sSadRRA/132" width="30px"><span>王兵</span> 👍（0） 💬（0）<div>在顺序表的基础上增加操作限制有什么好处呢？

链表访问栈顶的时间复杂度降到了 O(1)，数组 Push|Pop 栈顶的时间复杂度也降到了 O(1)，皆大欢喜。
不过基于数组的栈在内存使用方面会优秀一点，因为可以连续存储。基于链表的栈在扩容方面会优秀一点，因为动态分配内存比较容易。</div>2022-12-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/NeRCyul5wpibzQ9gXY8J9icHnDm3JOoW9Lr1NNxok2ZfcXQrK2ECe7J9GARdziaUspicTNbgJzx3pYoYbtyYBfGkWg/132" width="30px"><span>风清扬</span> 👍（0） 💬（0）<div>整合评论区两位的留言：
暴力法：双重循环，针对链表1的每个元素，对链表2的每个元素进行遍历，比较是否相等，第一个相等的元素就是相交点；
使用hash：对其中一个链表建立hash表，遍历另一个链表时在hash表中查找，若存在则为合并且第一个发现存在的元素即为相交点；
使用栈：将两个链表的元素分别放入2个栈中，分别弹出栈顶元素，进行比较，如果栈顶元素相同则相交，相交之后第一个不相同元素的前一个元素就是相交点
判断两个链表的长度：如果长度不同，比如一个是n，一个m，较长的链表先走n-m步，然后两个链表一起遍历，相同的元素即为交点。如果长度相同，一起遍历。</div>2022-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b8/21/f692bdb0.jpg" width="30px"><span>路在哪</span> 👍（0） 💬（0）<div>思考题：创建一个hashmap，先遍历a链表，把每个节点放到hashmap中，然后遍历b链表，判断hashmap中有没有b中的节点，这样应该行吧</div>2022-09-22</li><br/>
</ul>