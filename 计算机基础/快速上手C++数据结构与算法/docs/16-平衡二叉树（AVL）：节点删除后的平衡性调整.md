你好，我是王健伟。

上节课我们了解了什么是平衡二叉树，也详细讲解了插入一个新的节点后如何保持该树仍旧是一颗平衡二叉树。本节课我将继续与你分享在删除一个平衡二叉树中的节点后如何保持平衡的话题。

平衡二叉树删除某个节点的操作与二叉查找树删除某个节点的操作非常类似，但删除操作同样会使平衡二叉树失去平衡性。一旦因为删除某个节点导致平衡二叉树失衡，那么也要通过旋转使其恢复为平衡二叉树。删除操作的平衡性调整的实现代码有一定的复杂性，请你认真学习。我们先从删除过程的操作步骤开始说起。

## 删除过程的三个步骤

具体的删除过程可以分为三个主要步骤。

**步骤一，在平衡二叉树中查找要删除的节点。**

**步骤二，针对所要删除的节点的子节点个数不同，分别处理几类情况。**

- 要删除的节点是叶子节点，则直接把该节点删除并将指向该被删除节点的父节点的相应孩子指针设置为空。
- 要删除的节点有左子树或右子树（单分支节点），则把该节点删除并更新指向该被删除节点的父节点的相应孩子指针，让该指针指向要删除节点的非空的子节点（节点替换）。
- 要删除的节点左子树和右子树都不为空，则这里存在三种情况：找到这个要删除节点的左子树的最右下节点，也可以找这个要删除节点右子树的最左下节点；将该节点的值替换到要删除的节点上；把刚刚找到的那个最右下节点删除。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELibhkZWN1BqDCeTKJdtu0UfbHNQ1KnjmOE4Zsy05nEyUKQ5AjTdh29iaGFAoXk2ic6juxI2Gxr294LzzUfIDI9YRgPCbfY84PKp9RuXXqFGibLCw/132" width="30px"><span>Geek_845395</span> 👍（0） 💬（0）<div>老师您好，您的67——73行的代码

if (parent != nullptr) { 
if (parent-&gt;leftChild == ptmp) 
     parent-&gt;leftChild = ptmp-&gt;leftChild; 
else 
    parent-&gt;rightChild = ptmp-&gt;leftChild; }

我有点疑惑，while循环里，parent = q, q = q-&gt;rightChild, 那么q一定是parent节点的右孩子呀，把q赋值给ptmp后， 为什么会出现parent-&gt;leftChild == ptmp的情况呢？  我觉得应该直接改成if (parent != nullptr) {
	parent-&gt;rightChild = ptmp-&gt;leftChild;
}</div>2024-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0c/a5/0bbfd5e7.jpg" width="30px"><span>Tiger</span> 👍（0） 💬（0）<div>老师您好，在处理被删除节点既有左子树又有右子树的情况时，您的代码的第67至第73行的ifelse语句是不是应该改为
if(parent != nullptr)
{
         if(parent-&gt;leftChild == ptmp)
         {
                 q = ptmp-&gt;leftChild;
                 parent-&gt;leftChild = q;
         }
         else
         {
                 q = ptmp-&gt;leftChild;
                 parent-&gt;rightChild = q;
         }
}</div>2023-07-23</li><br/>
</ul>