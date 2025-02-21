在上节课中，我们一起学习了NumPy的主要使用方法和技巧，有了NumPy我们可以很好地处理各种类型的数据。而在深度学习中，数据的组织则更进一步，从数据的组织，到模型内部的参数，都是通过一种叫做**张量**的数据结构进行表示和处理。

今天我们就来一块儿了解一下张量（Tensor），学习一下Tensor的常用操作。

## 什么是Tensor

Tensor是深度学习框架中极为基础的概念，也是PyTroch、TensorFlow中最重要的知识点之一，它是一种数据的存储和处理结构。

回忆一下我们目前知道的几种数据表示：

1. 标量，也称Scalar，是一个只有大小，没有方向的量，比如1.8、e、10等。
2. 向量，也称Vector，是一个有大小也有方向的量，比如(1,2,3,4)等。
3. 矩阵，也称Matrix，是多个向量合并在一起得到的量，比如\[(1,2,3),(4,5,6)]等。

为了帮助你更好理解标量、向量和矩阵，我特意准备了一张示意图，你可以结合图片理解。  
![](https://static001.geekbang.org/resource/image/a8/85/a85883cc14171ff5361346dd65776085.jpg?wh=1920x1090)

不难发现，几种数据表示其实都是有着联系的，标量可以组合成向量，向量可以组合成矩阵。那么，我们可否将它们看作是一种数据形式呢？

答案是可以的，这种统一的数据形式，在PyTorch中我们称之为**张量(Tensor)**。从标量、向量和矩阵的关系来看，你可能会觉得它们就是不同**“维度”**的Tensor，这个说法对，也不全对。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（39） 💬（2）<div>通过查阅文档，torch.Tensor是默认tensor类型的torch.FloatTensor别名,  可以直接从给定数据中创建出FloatTensor的tensor， 而torch.tensor是创建会根据输入的数据类型判断。 也就是说，如果我传入的是int类型，那么torch.Tensor输出的是FloatTensor数据格式，而torch.tensor输出的torch.int32</div>2021-12-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/j24oyxHcpB5AMR9pMO6fITqnOFVOncnk2T1vdu1rYLfq1cN6Sj7xVrBVbCvHXUad2MpfyBcE4neBguxmjIxyiaQ/132" width="30px"><span>vcjmhg</span> 👍（10） 💬（1）<div>torch.Tensor() 是Tensor类的构造方法，通过构造方法创建Tensor对象的实例；torch.tensor()则是Tensor类内部的一个方法，方法的返回值是Tensor类型</div>2021-10-18</li><br/><li><img src="" width="30px"><span>Sam Wang</span> 👍（4） 💬（3）<div>Squeeze 和unsqueeze我的理解是他们只是减少或增加了1维，但其实并未增加或者减少数据。因为数据数量没变 (多乘1而已，数量不变)</div>2021-10-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dQQR8nfd3k8zO9Z7TjOxSuRb3z6QH9Y7hGZibPuganp8Xspic2LPAIYggKafsP98U46Lc3X1BQ4qw9ROxLZXP4WA/132" width="30px"><span>Geek_86b454</span> 👍（3） 💬（2）<div>新创建出来的tensor是CPU tensor还是GPU tensor呢</div>2021-12-13</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/EibfOEBg0ZtchzGLBtRrpjG4MPxm3GqyU7rR4gPCL9NTwoOqh0RLXCBOQYrP48LLB1FqIwicDgKm3iaK1jcuzuibAg/132" width="30px"><span>celerychen</span> 👍（2） 💬（2）<div>x.view(4, 4) 元素个数仍然是16个，和之前的一样，内存怎么就变成不连续的呢，能否解释一下？谢谢老师！</div>2022-07-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoibQLsjsrjiasFUaPdjib95Jk4y3ZMD6zXyEud7bCvibrjrPia3RCib0zTD7MahQJ41icOicIWXfbq8JpnGQ/132" width="30px"><span>步比天下</span> 👍（1） 💬（1）<div>老师您好，感觉最后一个例子有些不太理想，有些同学可能会搞不清新的一维是在哪个位置插入的，能不能再换个例子啊</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/86/c0/34b56a24.jpg" width="30px"><span>梦之吃吃</span> 👍（0） 💬（1）<div>调用torch.Tensor构造的tensor默认类型是单精度浮点数类型，调用torch.tensor构造的tensor根据原始数据类型生成对应的tensor数据类型</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/d0/2a/316a4932.jpg" width="30px"><span>站着睡觉的树</span> 👍（0） 💬（1）<div>老师，请问 获取形状的代码中，a=torch.zeros(2, 3, 5) ，这是一个2行，3列，深度为5的张量吗？我看您的配图，表示的是2列，3行，深度为5的张量。 也就是说，张量的0维，指的是有多少列，张量的1维指的是有多少行，张量的2维指的是有层（深度），我的理解对吗？</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/99/4bdadfd3.jpg" width="30px"><span>Chloe</span> 👍（0） 💬（1）<div>请问老师能不能讲讲为什么squeeze 只能增减维度的大小为 1 的维度呢？</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/8a/ec29ca4a.jpg" width="30px"><span>马克图布</span> 👍（0） 💬（1）<div>老师，关于 Tensor 内存不连续的问题，使用 contiguous() 函数也可以解决吧？还是说使用 reshape() 有些什么其他优势呢？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cd/b7/6efa2c68.jpg" width="30px"><span>李雄</span> 👍（0） 💬（3）<div>这里我们新建了一个维度为[2, 1, 3]的 Tensor，然后在第 2 维度插入一个数据，这样就得到了一个[2,1,1,3]大小的 tensor。
应该是在第2维度上插入一个维度，这样说是不是更准确些。因为x.numel() == y.numel()的返回值是True</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fc/ca/c1b8d9ca.jpg" width="30px"><span>IUniverse</span> 👍（0） 💬（1）<div>两者都可以用于生成张量，但一个是类（torch.FloatTensor()的别名），而另外一个是函数。</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（1）<div>torch.Tensor()是Python类，是默认张量类型torch.FloatTensor()的别名，而torch.tensor()是Python函数。</div>2021-10-18</li><br/><li><img src="" width="30px"><span>Geek_1509a8</span> 👍（0） 💬（0）<div>torch.Tensor()通过data创建张量的实例，此时没有对data做拷贝，更改数据同时会更改张量;而torch.tensor()是一个创建张量的函数，会对数据做拷贝，更改数据不会对张量有影响。</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/61/b1/1261c177.jpg" width="30px"><span>胖胖虎</span> 👍（0） 💬（0）<div>PyTorch&#39;s tensor (lowercase &quot;t&quot;) and Tensor (capital &quot;T&quot;) both refer to the same fundamental data structure in PyTorch, which is a multi-dimensional array. The difference between the two is that tensor is a function used to create a new tensor from an existing data source, while Tensor is a class used to represent a tensor object.

The tensor function is used to create a new tensor from an existing data source such as a list or a NumPy array. For example, the following code creates a tensor using the tensor function:
```python
import torch

data = [1, 2, 3, 4, 5]
tensor = torch.tensor(data)
```
On the other hand, the Tensor class is used to create a new tensor object with specified properties such as size and data type. For example, the following code creates a tensor using the Tensor class:
```python
import torch

tensor = torch.Tensor(2, 3)
```
In general, it is recommended to use the tensor function to create new tensors from existing data sources, and to use the Tensor class to create new empty tensors with specific properties. However, both tensor and Tensor can be used interchangeably depending on the use case.
</div>2023-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/31/bbb513ba.jpg" width="30px"><span>mtfelix</span> 👍（0） 💬（2）<div>NumPy 不能用于 GPU 加速，Tensor 则可以。

---- 老师能给详细说说嘛？</div>2022-08-25</li><br/><li><img src="" width="30px"><span>AstrHan</span> 👍（0） 💬（2）<div>为什么我运行a = torch.Tensor(1)；b = a.item()的时候，b的数值不是1，而且每次运行的结果都不相同。会得到1.0或者0.0或者很接近0的数或者一个随机的浮点数。</div>2021-10-26</li><br/>
</ul>