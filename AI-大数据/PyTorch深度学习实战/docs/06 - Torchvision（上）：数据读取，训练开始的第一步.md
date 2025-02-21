你好，我是方远。

今天起我们进入模型训练篇的学习。如果将模型看作一辆汽车，那么它的开发过程就可以看作是一套完整的生产流程，环环相扣、缺一不可。这些环节包括**数据的读取、网络的设计、优化方法与损失函数的选择以及一些辅助的工具等**。未来你将尝试构建自己的豪华汽车，或者站在巨人的肩膀上对前人的作品进行优化。

试想一下，如果你对这些基础环节所使用的方法都不清楚，你还能很好地进行下去吗？所以通过这个模块，我们的目标是先把基础打好。通过这模块的学习，对于PyTorch都为我们提供了哪些丰富的API，你就会了然于胸了。

Torchvision 是一个和 PyTorch 配合使用的 Python 包，包含很多图像处理的工具。我们先从数据处理入手，开始PyTorch的学习的第一步。这节课我们会先介绍Torchvision的常用数据集及其读取方法，在后面的两节课里，我再带你了解常用的图像处理方法与Torchvision其它有趣的功能。

## PyTorch中的数据读取

训练开始的第一步，首先就是数据读取。PyTorch为我们提供了一种十分方便的数据读取机制，即使用Dataset类与DataLoader类的组合，来得到数据迭代器。在训练或预测时，数据迭代器能够输出每一批次所需的数据，并且对数据进行相应的预处理与数据增强操作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/SKmvhbNe9LMPQ0ib8ZqbJEfHicUxzxCSKVXiaibn7OrmXGUFQjkesgvODymZz4kibzqOGxuRq42t3sB2ibcBIIGWRgSg/132" width="30px"><span>超人不会飞</span> 👍（5） 💬（3）<div>tensor_dataloader 是一个迭代器
iter（tensor_dataloader)是一个迭代器对象

iter(tensor_dataloader).next() 是输出迭代器的下一个元素

兄弟们我这波理解到位不</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bf/51/1791ae60.jpg" width="30px"><span>JC</span> 👍（3） 💬（2）<div>国内直接下载MNIST数据集，可能会有些问题
可以通过本地下载文件，放入到某目录，然后在该目录下使用 python -m http.server 启动一个本地server
最后把 mnist.py 文件里的 mirrors 上方添加一行 http:&#47;&#47;localhost:8000&#47;MNIST&#47;</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d6/1b/b0f912fd.jpg" width="30px"><span>Spoon</span> 👍（3） 💬（5）<div>老师好， 想问下。。为啥你说是10x3 维啊 数据不是2维的吗，下面标签不是一维的吗。。。有点confuse了。。
data_tensor = torch.randn(10, 3)
target_tensor = torch.randint(2, (10,)) # 标签是0或1</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/0c/1f/fcc777e1.jpg" width="30px"><span>乐呵的hehe</span> 👍（1） 💬（1）<div>老师，您好，下面这个问题，我也有些疑惑，但是我不在微信群里，您可以在这里再解释一下吗？谢谢！
-------------------------------------------------------------------
from torch.utils.data import DataLoader

tensor_dataloader = DataLoader(dataset=my_dataset, batch_size=2, shuffle=True,
                                               num_workers=0)# 进程数, 0表示只有主进程

# 以循环形式输出
for data, target in tensor_dataloader: 
    print(data, target)

# 输出一个batch
print(&#39;One batch tensor data: &#39;, iter(tensor_dataloader).next())

输出结果：
tensor([[ 0.7989,  3.1884,  1.2282],

        [-0.6210, -0.9707,  2.5557]]) tensor([1, 0])

tensor([[-0.8162, -0.5454,  2.1312],

        [ 0.8296, -0.2082,  1.7351]]) tensor([0, 0])

tensor([[ 1.3808,  0.2034,  0.3342],

        [ 0.4650, -1.1422, -0.4364]]) tensor([1, 1])

tensor([[ 1.0286, -1.1956,  0.4743],

        [ 3.1708, -0.0568, -1.5444]]) tensor([1, 0])

tensor([[ 0.1358,  1.2954, -0.0674],

        [-0.7422, -0.2062,  2.4920]]) tensor([0, 0])

One batch tensor data:  [tensor([[ 3.1708, -0.0568, -1.5444],

        [-0.7422, -0.2062,  2.4920]]), tensor([0, 0])]

迭代器输出的tensor怎么会都不在一个batch里呢？正常情况下，不是应该输出第二个batch里的tensor嘛？</div>2022-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/89/23/e71f180b.jpg" width="30px"><span>Geek_fc975d</span> 👍（1） 💬（2）<div>为什么我只有__next__函数，而没有next()函数</div>2022-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/3c/b03ed9c2.jpg" width="30px"><span>Swaggy</span> 👍（1） 💬（1）<div>老师好，我现在遇到一个问题，就是同一份代码，我在1.9.1中运行，会因为内存不足Kill掉，我开了htop和nvidia smi查看，一开始内存就直接拉满，下边的虚拟内存提示需要两倍的内存，然后GPU只用了五分之一还会横跳到0。一共300epochs 跑到第97-98epoch就会卡住不动，内存依旧拉满，六个CPU核心恢复正常状态，之前是一直拉满，然后GPU也恢复正常占用。我反复折腾了几次最后都只能强制关机。最后，我把环境换成1.5.1的版本，顺利跑完，只用了四百多秒。因为本身就是一个很简单的lstm网络，然后在新环境中内存占用一半多点，CPU全部拉满，GPU只用了五分之一多点。我想请问老师，我这种情况是为什么，版本区别这么大的吗？我遇到类似情况应该怎么排查，是不是我写的dataset部分有问题，因为本身数据量也不大，以mb计算的，网络更是很简单。对了，电脑配置CPU是i5-9600k，六核十二线程，GPU 2070单卡，内存16g。希望老师能指点迷津，非常感谢</div>2021-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/46/3aa0cd40.jpg" width="30px"><span>peng</span> 👍（0） 💬（1）<div>老师您好，以下的例子，我调用时会报错，
# 输出一个batch
print(&#39;One batch tensor data: &#39;, iter(tensor_dataloader).next())

报错信息如下，
AttributeError                            Traceback (most recent call last)
Cell In[17], line 11
      8 for data, target in tensor_dataloader: 
      9     print(data, target)
---&gt; 11 print(&#39;One batch tensor data: &#39;, iter(tensor_dataloader).next())

AttributeError: &#39;_SingleProcessDataLoaderIter&#39; object has no attribute &#39;next&#39;
把调用改为
print(&#39;One batch tensor data: &#39;, iter(tensor_dataloader).__next__())
才可以正常运行，这个是pytorch的版本问题？</div>2024-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/fb/37/791d0f5e.jpg" width="30px"><span>Monin</span> 👍（0） 💬（3）<div>老师  你好 目前Pytorch框架跟TensorFlow相比市场应用还多吗？  目前除了这两个还有哪些深度学习框架值得关注和研究的？ </div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e0/ca/adfaa551.jpg" width="30px"><span>孙新</span> 👍（0） 💬（2）<div>display(mnist_dataset_list[0][0])  这一行没有成功，提示display错误
Traceback (most recent call last):
  File &quot;&lt;stdin&gt;&quot;, line 1, in &lt;module&gt;
NameError: name &#39;display&#39; is not defined
我用的环境有问题吗？还是说需要什么IDE才能出效果？
</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ad/2b/46b4a196.jpg" width="30px"><span>ACT</span> 👍（0） 💬（1）<div>Dataset</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（1）<div>IOPub data rate 超限 解决 

This works for me in Mac and Windows (taken from here):

1. To create a jupyter_notebook_config.py file, with all the defaults commented out, you can use the following command line:

$ jupyter notebook --generate-config

2. Open the file and search for c.NotebookApp.iopub_data_rate_limit

3. 取消注释Comment out the line c.NotebookApp.iopub_data_rate_limit = 1000000 and change it to a higher default rate. l used c.NotebookApp.iopub_data_rate_limit = 10000000

参考：
https:&#47;&#47;stackoverflow.com&#47;questions&#47;43288550&#47;iopub-data-rate-exceeded-in-jupyter-notebook-when-viewing-image
</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（1）<div>Dataset</div>2022-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/89/23/e71f180b.jpg" width="30px"><span>Geek_fc975d</span> 👍（0） 💬（1）<div>这节课收获颇丰</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/f9/3f48fd13.jpg" width="30px"><span>黑羽</span> 👍（0） 💬（1）<div>老师，如果自己有一个图片的数据集，也需要先定义dataset类来读取吗</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/5e/f9/96896116.jpg" width="30px"><span>天凉好个秋</span> 👍（0） 💬（1）<div>老师请问 迭代器输出的batch和for循环输出的batch不同的原因是设置了shuffle=True后，每次调用实例化对象后都会进行一次打乱吗？</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fc/de/6e2cb960.jpg" width="30px"><span>autiplex</span> 👍（0） 💬（1）<div>老师请问conda install torchvision -c pytorch 后面的-c pytorch代表什么</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/13/3e/d028cddd.jpg" width="30px"><span>王珎</span> 👍（0） 💬（1）<div>在PyTorch中定义数据集，应该继承 Dataset 类</div>2021-11-08</li><br/><li><img src="" width="30px"><span>clee</span> 👍（0） 💬（1）<div>你好，我在引入PIL的时候遇到一个版本问题，没找到解决办法，请问是哪儿有问题呢？
ImportError: dlopen(&#47;Users&#47;xx&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;PIL&#47;_imaging.cpython-38-darwin.so, 2): Library not loaded: @rpath&#47;libjpeg.9.dylib
  Referenced from: &#47;Users&#47;xx&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;PIL&#47;_imaging.cpython-38-darwin.so
  Reason: Incompatible library version: _imaging.cpython-38-darwin.so requires version 14.0.0 or later, but libjpeg.9.dylib provides version 12.0.0</div>2021-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e1/48/3a981e55.jpg" width="30px"><span>林于翔</span> 👍（0） 💬（4）<div>from torch.utils.data import DataLoader
tensor_dataloader = DataLoader(dataset=my_dataset, # 传入的数据集, 必须参数
                               batch_size=2,       # 输出的batch大小
                               shuffle=True,       # 是否对数据进行重新打乱；
                               num_workers=0)      # 进程数, 0表示只有主进程

# 以循环形式输出
for data, target in tensor_dataloader: 
    print(data, target)

# 输出一个batch
print(&#39;One batch tensor data: &#39;, iter(tensor_dataloader).next())


输出结果：
tensor([[ 0.7989,  3.1884,  1.2282],
        [-0.6210, -0.9707,  2.5557]]) tensor([1, 0])
tensor([[-0.8162, -0.5454,  2.1312],
        [ 0.8296, -0.2082,  1.7351]]) tensor([0, 0])
tensor([[ 1.3808,  0.2034,  0.3342],
        [ 0.4650, -1.1422, -0.4364]]) tensor([1, 1])
tensor([[ 1.0286, -1.1956,  0.4743],
        [ 3.1708, -0.0568, -1.5444]]) tensor([1, 0])
tensor([[ 0.1358,  1.2954, -0.0674],
        [-0.7422, -0.2062,  2.4920]]) tensor([0, 0])
One batch tensor data:  [tensor([[ 3.1708, -0.0568, -1.5444],
        [-0.7422, -0.2062,  2.4920]]), tensor([0, 0])]

迭代器输出的tensor怎么会都不在一个batch里呢？正常情况下，不是应该输出第二个batch里的tensor嘛？</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/da/2c/783413de.jpg" width="30px"><span>彭涛</span> 👍（0） 💬（2）<div>老师好，请问代码：
my_dataset = MyDataset(data_tensor, target_tensor)
报错：
TypeError: object.__new__() takes exactly one argument(the type to instantiate)
求解决方案，谢谢老师。</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cc/41/af863836.jpg" width="30px"><span>夏阳</span> 👍（0） 💬（1）<div>我之前提的那个问题解决了。可能是因为我用的pycharm，显示Image图片的时候，需要用 image.show()函数。display（）函数不能正常显示图片。</div>2021-10-27</li><br/><li><img src="" width="30px"><span>BirthKnight</span> 👍（0） 💬（1）<div>老师您好。我尝试了下载MNIST数据集，然后把download设置为false，root设置为MNIST 下载文件的相对路径，发现无法找到。搜了下网上资料，发现torchvision在下载之后有一系列的预处理。老师能否讲下如何直接使用原生的MNIST数据集？</div>2021-10-23</li><br/><li><img src="" width="30px"><span>Sam Wang</span> 👍（0） 💬（2）<div>为什么MyData中的两个method都用双前导和双末尾下划线？有什么约定吗还是编译不同？</div>2021-10-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/j24oyxHcpB5AMR9pMO6fITqnOFVOncnk2T1vdu1rYLfq1cN6Sj7xVrBVbCvHXUad2MpfyBcE4neBguxmjIxyiaQ/132" width="30px"><span>vcjmhg</span> 👍（0） 💬（1）<div>应该继承torch.utils.data.Dataset类</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fc/ca/c1b8d9ca.jpg" width="30px"><span>IUniverse</span> 👍（0） 💬（1）<div>要继承Dataset类</div>2021-10-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKyEJx6dG2dMuMz6swdfjNuw3HMoEAbtxprfdBUAyRpLFayxmwEiaYLs224LuAdwWu55ENLgsI8U4w/132" width="30px"><span>lwg0452</span> 👍（0） 💬（1）<div>torch.utils.data.Dataset类</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bf/51/1791ae60.jpg" width="30px"><span>JC</span> 👍（4） 💬（0）<div>国内直接下载MNIST数据集，可能会有些问题
可以通过本地下载文件，放入到某目录，然后在该目录下使用 python -m http.server 启动一个本地server
最后把 mnist.py 文件里的 mirrors 上方添加一行 http:&#47;&#47;localhost:8000&#47;MNIST&#47;</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>继承dataset</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/58/b3/abb3256b.jpg" width="30px"><span>枫树_6177003</span> 👍（0） 💬（0）<div>Dataset</div>2023-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（0）<div>PIL Image Module
The Image module provides a class with the same name which is used to represent a PIL image. The module also provides a number of factory functions, including functions to load images from files, and to create new images.

Examples
Open, rotate, and display an image (using the default viewer)
The following script loads an image, rotates it 45 degrees, and displays it using an external viewer (usually xv on Unix, and the Paint program on Windows).

from PIL import Image
with Image.open(&quot;hopper.jpg&quot;) as im:
    im.rotate(45).show()
</div>2022-07-29</li><br/>
</ul>