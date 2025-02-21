你好，我是大圣。上一讲我们仔细分析了Vue中虚拟DOM如何执行的，整体流程就是树形结构的diff计算，但是在diff的计算过程中，如何高效计算虚拟DOM属性的变化，以及如何更新数组的子元素，需要一些算法知识的补充。

给你提前划个重点，今天我们将讲到如何使用位运算来实现Vue中的按需更新，让静态的节点可以越过虚拟DOM的计算逻辑，并且使用计算最长递增子序列的方式，来实现队伍的高效排序。我们会剖析Vue框架源码，结合对应的LeetCode题，帮助你掌握算法的核心原理和实现。

## 位运算

前面也复习了，在执行diff之前，要根据需要判断每个虚拟DOM节点有哪些属性需要计算，因为无论响应式数据怎么变化，静态的属性和节点都不会发生变化。

所以我们看每个节点diff的时候会做什么，在renderer.ts代码文件中就可以看到代码，主要就是通过虚拟DOM节点的patchFlag树形判断是否需要更新节点。

**方法就是使用&amp;操作符来判断操作的类型**，比如patchFlag &amp; PatchFlags.CLASS来判断当前元素的class是否需要计算diff；shapeFlag &amp; ShapeFlags.ELEMENT来判断当前虚拟DOM是HTML元素还是Component组件。这个“&amp;”其实就是位运算的按位与。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTITZ8d25icGgFSPInPRfxTE8ryvAibVtKI6G16WoV9D1cC5uXpqHviay7mKSTTxoU7WfguNjRjvXGxLw/132" width="30px"><span>Geek_ec138d</span> 👍（1） 💬（1）<div>大圣老师，全景图的里的newIndexOldIndexMap的长度和值好像不对。。。。</div>2022-01-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqrm1J6MVvFibtUorUn88kfpIVQKI615tzicJZiceBbW4WjiaETzqjtGFTK49EL5lqWPqIDibjCyuEMgzQ/132" width="30px"><span>xzq</span> 👍（0） 💬（1）<div>&#47;&#47; 获取最长递增子序列之后这一步是干啥的，。， 太难理解了 
&#47;&#47; 还有一个就是为啥要获取最长递增子序列       
if (j &lt; 0 || i !== increasingNewIndexSequence[j]) {
            &#47;&#47; insertBefore(nextChild, anchor)
            &#47;&#47; 移动到锚点的前面(这个锚点的意思可以理解为插入到所有已处理节点的后面, 或者所有未处理节点的前面) 
            move(nextChild, container, anchor, MoveType.REORDER)
          } else {
            j--
          }</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0a/1d/269a15c3.jpg" width="30px"><span>Kim Yin</span> 👍（5） 💬（0）<div>感觉 newIndexOldIndexMap 不太对</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/0d/cd/791d0f5e.jpg" width="30px"><span>Mr_shaojun</span> 👍（1） 💬（0）<div>太费脑子了</div>2022-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/20/45/6c8bb3aa.jpg" width="30px"><span>小花（fa）</span> 👍（1） 💬（0）<div>newIndexOldIndexMap=[0,3,6,5,0,3]的值没看懂, 然后图中 老序列 h b f d c计算后的最长子序列是多少呢</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/31/5b8800fb.jpg" width="30px"><span>微扰理论</span> 👍（1） 💬（0）<div>厉害呀 感觉是讲虚拟dom比较清晰的一篇文章了～</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（1） 💬（0）<div>思考题
后端用户权限的设计，采用了位运算，前端也需要位运算解析</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/0d/21bf48eb.jpg" width="30px"><span>NULL</span> 👍（0） 💬（1）<div>刚补完算法差不多搞懂LIS后，一转到这个结尾……可是太仓促了，以及评论大家都在质疑尾图里的MAP，作者说去确认可并没有个明确结果，多年未改——
是对的，毋庸置疑呢（只是最后讲得仓促稀烂让所有人搞不懂）？
还是就不对，可就懒得、忘了改呢（反正也没几个人看）？</div>2024-01-09</li><br/>
</ul>