你好，我是方远。

上节课我们一起学习了Tensor的基础概念，也熟悉了创建、转换、维度变换等操作，掌握了这些基础知识，你就可以做一些简单的Tensor相关的操作了。

不过，要想在实际的应用中更灵活地用好Tensor，Tensor的连接、切分等操作也是必不可少的。今天这节课，咱们就通过一些例子和图片来一块学习下。虽然这几个操作比较有难度，但只要你耐心听我讲解，然后上手练习，还是可以拿下的。

## Tensor的连接操作

在项目开发中，深度学习某一层神经元的数据可能有多个不同的来源，那么就需要将数据进行组合，这个组合的操作，我们称之为**连接**。

### cat

连接的操作函数如下。

```python
torch.cat(tensors, dim = 0, out = None)
```

cat是concatnate的意思，也就是拼接、联系的意思。该函数有两个重要的参数需要你掌握。

第一个参数是tensors，它很好理解，就是若干个我们准备进行拼接的Tensor。

第二个参数是dim，我们回忆一下Tensor的定义，Tensor的维度（秩）是有多种情况的。比如有两个3维的Tensor，可以有几种不同的拼接方式（如下图），dim参数就可以对此作出约定。

![图片](https://static001.geekbang.org/resource/image/61/3c/61bd88f3yy8d0ca07799f36540d3473c.jpg?wh=1285x862)

看到这里，你可能觉得上面画的图是三维的，看起来比较晦涩，所以咱们先从简单的二维的情况说起，我们先声明两个3x3的矩阵，代码如下：
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKyEJx6dG2dMuMz6swdfjNuw3HMoEAbtxprfdBUAyRpLFayxmwEiaYLs224LuAdwWu55ENLgsI8U4w/132" width="30px"><span>lwg0452</span> 👍（28） 💬（2）<div>更正😀
mask = torch.tensor([[1, 0, 0], [1, 1, 0], [0, 0, 1]])
B = torch.masked_select(A, mask&gt;0)</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/68/6c/5b572baa.jpg" width="30px"><span>optimus</span> 👍（4） 💬（2）<div>eye  = torch.eye(3)
torch.masked_select(A,eye&gt;0)</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/89/23/e71f180b.jpg" width="30px"><span>Geek_fc975d</span> 👍（2） 💬（1）<div>抄作业

# 手动构建了一个True&#47;False
A = torch.tensor([[4,5,7],[4,9,8],[2,3,4]])
masked_index = torch.tensor( [[True,False,False], [True,True,False], [False,False,True] ])
torch.masked_select(A, masked_index) 

#  这篇课程，个人觉得重要的几个知识点
1. index_select返回的结果和输入是一个维度，而masked_select返回一维输出
2. split获取的是原输入的视图，也就是对split的结果的操作会影响原来的数据
3. stack和cat的一个不同点在于，stack会升维，而cat不会。</div>2022-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>学习打卡</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/53/79/327ef30e.jpg" width="30px"><span>sugar</span> 👍（0） 💬（1）<div>a = torch.tensor([[4, 5, 7], [3, 9, 8], [2, 3, 4]])
mask = torch.tensor([[True, False, False], [True, True, False], [False, False, True]])
torch.masked_select(a, mask)
加油，冲哇</div>2024-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/5e/68/2fafe647.jpg" width="30px"><span>A🐴@伯乐</span> 👍（0） 💬（1）<div>import torch
A=torch.tensor([[4,5,7], [3,9,8],[2,3,4]])
B=torch.tensor([[1,0,0],[1,1,0],[1,0,0]])
C=torch.masked_select(A, A*B!=0)
print(C)</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（1）<div>这是个mask是不是就是传说中的数据打标</div>2022-05-09</li><br/><li><img src="" width="30px"><span>Geek_a95f0e</span> 👍（0） 💬（1）<div>a=tc.tensor([[4,5,7],[3,9,8],[2,3,4]])
b=tc.tensor([1,0,0,1,1,0,0,0,1],dtype=tc.bool).reshape(3,3)
c=tc.masked_select(a,b)</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/17/63887353.jpg" width="30px"><span>王骥</span> 👍（0） 💬（2）<div>input 表示待处理的 Tensor。mask 代表掩码张量，也就是满足条件的特征掩码。这里你需要注意的是，mask 须跟 input 张量有相同数量的元素数目，但形状或维度不需要相同。

老师，mask 须跟 input 张量有相同数量的元素数目，但形状或维度不需要相同 这句话该怎么理解？

  A = torch.tensor([[4, 5, 7], [3, 9, 8], [2, 3, 4]])
  B = torch.masked_select(A, torch.tensor([[1, 0, 0], [1, 1, 0], [0, 0, 1]]) &gt; 0)
  # B = torch.masked_select(A, torch.tensor([1, 0, 0, 1, 1, 0, 0, 0, 1]) &gt; 0)

我尝试下面一种就会报错。</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cd/b7/6efa2c68.jpg" width="30px"><span>李雄</span> 👍（0） 💬（2）<div>喜欢这节的内容。</div>2021-10-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/j24oyxHcpB5AMR9pMO6fITqnOFVOncnk2T1vdu1rYLfq1cN6Sj7xVrBVbCvHXUad2MpfyBcE4neBguxmjIxyiaQ/132" width="30px"><span>vcjmhg</span> 👍（0） 💬（1）<div>A = torch.tensor([[4, 5, 7], [3, 9, 8], [2, 3, 4]])
mask_matrix = torch.tensor([[1, 0, 0], [1, 1, 0], [0, 0, 1]])
B = torch.masked_select(A, mask == 1)</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e2/21/3bb82a79.jpg" width="30px"><span>栗白</span> 👍（0） 💬（1）<div>A=torch.tensor([[4,5,7], [3,9,8],[2,3,4]])
B=torch.tensor([[1,0,0],[1,1,0],[0,0,1]])
C=torch.masked_select(A,B&gt;0)</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/a3/e67d6039.jpg" width="30px"><span>narsil的梦</span> 👍（0） 💬（2）<div>练习：
    A = torch.tensor([[4, 5, 7], [3, 9, 8], [2, 3, 4]])

    # 提取出其中第一行的第一个，第二行的第一、第二个，第三行的最后一个
    B = torch.chunk(A, 3, dim=0)

    A00 = torch.index_select(B[0], 1, torch.tensor([0]))
    A1011 = torch.index_select(B[1], 1, torch.tensor([0, 1]))
    A22 = torch.index_select(B[2], 1, torch.tensor([2]))

PS：题目应该说明输出是什么格式的，要不同学们不知道做到哪一步算完事</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（7） 💬（0）<div># 手动构建了一个True&#47;False
A = torch.tensor([[4,5,7],[4,9,8],[2,3,4]])
masked_index = torch.tensor( [[True,False,False], [True,True,False], [False,False,True] ])
torch.masked_select(A, masked_index) 

#  这篇课程，个人觉得重要的几个知识点
1. index_select返回的结果和输入是一个维度，而masked_select返回一维输出
2. split获取的是原输入的视图，也就是对split的结果的操作会影响原来的数据
3. stack和cat的一个不同点在于，stack会升维，而cat不会。
</div>2021-12-08</li><br/><li><img src="" width="30px"><span>GEEKBANG_9421399</span> 👍（4） 💬（0）<div>其实如果tensor和mask的维度相同的话，直接tensor[mask]就是torch.masked_select(tensor, mask)的效果了。</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/31/bbb513ba.jpg" width="30px"><span>mtfelix</span> 👍（2） 💬（0）<div>cat不升维，stack升维。

cat就是拼接，stack是堆叠。

cat时要保证原来的tensors必须具备同样的维度个数(是一个空间的)，dim只是选择在哪个具体维度上拼接，以使得合二为一。那么，就要求除了dim指定的维度外，其他维度的大小必须是一致的。

stack时，要保证原来的tensors必须shape一致。dim只是选择在哪个维度上堆叠出未来的新维度。因此，如果原来维度数是n，那么dim选择范围就是[-n+1, n]。比如，原来是3维的，dim可以选择为-3,-2,-1,0,1,2。

</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/0e/b2/192fbab4.jpg" width="30px"><span>Difer</span> 👍（0） 💬（0）<div>方法1：
import torch.tensor as tt
list_indices = [ tt([0]), tt([0, 1]), tt([2]) ] ###手动构建各行所需要的位置
b = torch.unbind(A, 0)
torch.cat([torch.index_select(x, 0, i) for x, i in zip(b, list_indices)], 0)

方法2：
B = tt([[1, 0, 0], [1, 1, 0], [0, 0, 1]])  ###手动构建1, 0 矩阵以对应取出的位置
torch.masked_select(A, B==1)</div>2023-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1c/a2/936a8032.jpg" width="30px"><span>沈振雷</span> 👍（0） 💬（0）<div>torch.index_select(A.reshape(9),dim=0,index=torch.tensor([0,3,4,8]))</div>2023-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/30/913d008b.jpg" width="30px"><span>八点二十</span> 👍（0） 💬（0）<div>a, b, c = torch.unbind(A, dim=0)
print(torch.split(a, 1, 0)[0])
print(torch.split(b, 2, 0)[0])
print(torch.split(c, 1, 0)[2])</div>2023-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/92/7b/8c7e3e61.jpg" width="30px"><span>Monroe  He</span> 👍（0） 💬（0）<div># 方法1 直接提取
A[0,1],A[1,:2],A[2,-1]</div>2023-03-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKyEJx6dG2dMuMz6swdfjNuw3HMoEAbtxprfdBUAyRpLFayxmwEiaYLs224LuAdwWu55ENLgsI8U4w/132" width="30px"><span>lwg0452</span> 👍（0） 💬（1）<div>思考题 B = torch.masked_select(A, torch.eye(3) &gt; 0)</div>2021-10-20</li><br/>
</ul>