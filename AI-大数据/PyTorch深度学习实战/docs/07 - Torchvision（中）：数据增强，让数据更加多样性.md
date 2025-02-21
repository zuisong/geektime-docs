你好，我是方远。

上一节课，我们一同迈出了训练开始的第一步——数据读取，初步认识了Torchvision，学习了如何利用Torchvision读取数据。不过仅仅将数据集中的图片读取出来是不够的，在训练的过程中，神经网络模型接收的数据类型是Tensor，而不是PIL对象，因此我们还需要对数据进行预处理操作，比如图像格式的转换。

与此同时，加载后的图像数据可能还需要进行一系列图像变换与增强操作，例如裁切边框、调整图像比例和大小、标准化等，以便模型能够更好地学习到数据的特征。这些操作都可以使用`torchvision.transforms`工具完成。

今天我们就来学习一下，利用Torchvision如何进行数据预处理操作，如何进行图像变换与增强。

## 图像处理工具之torchvision.transforms

Torchvision库中的`torchvision.transforms`包中提供了常用的图像操作，包括对Tensor 及PIL Image对象的操作，例如随机切割、旋转、数据类型转换等等。

按照`torchvision.transforms` 的功能，大致分为以下几类：数据类型转换、对PIL.Image 和 Tensor进行变化和变换的组合。下面我们依次来学习这些类别中的操作。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/45/64/ab1fada2.jpg" width="30px"><span>上岸吧，Adagio</span> 👍（9） 💬（1）<div>老师您好，请问

img1 = transforms.ToTensor()(img)
img2 = transforms.ToPILImage()(img1)

是怎么使用的呢？
transforms.ToTensor是一个类，为什么不把img当做参数传给这个类做初始化呢？
transforms.ToTensor()是创建一个对象吗？为什么后面又直接传入了(img)参数呢？
不太懂这一块的细节，请老师帮忙解答下~
</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3a/d2/cbd2c882.jpg" width="30px"><span>Yuhan</span> 👍（9） 💬（5）<div>老师您好，感觉应该注明一下display函数的来源，是Ipython.display 里面的display函数吗？</div>2021-10-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/j24oyxHcpB5AMR9pMO6fITqnOFVOncnk2T1vdu1rYLfq1cN6Sj7xVrBVbCvHXUad2MpfyBcE4neBguxmjIxyiaQ/132" width="30px"><span>vcjmhg</span> 👍（7） 💬（1）<div>Torchvision 中 transforms 模块的作用：封装了常用的图像操作，例随机切割、旋转、数据类型转换、tensor 与 numpy 和 PIL Image 的互换等。</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/62/09/7fd0634a.jpg" width="30px"><span>汤火火火</span> 👍（4） 💬（3）<div>老师您好，我想问一下，在训练时对图像做了标准化，那测试的时候需要对测试图像做标准化吗？</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/5e/f9/96896116.jpg" width="30px"><span>天凉好个秋</span> 👍（3） 💬（1）<div>老师你好，在使用 Resize 的时候，出现以下 warning:

UserWarning: Argument interpolation should be of type InterpolationMode instead of int. Please, use InterpolationMode enum.

在之前的回答中给的解决方案的第二条：将Image.BICUBIC 替换为InterpolationMode.BICUBIC，这个是在哪儿替换?transforms.py的源代码中也没有相关代码</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（2） 💬（1）<div>Torchvision 中 transforms 模块的作用图像数据的预处理。怎么标准化，这些标准化参数是如何确定的类？</div>2022-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/5b/5b/1804b22f.jpg" width="30px"><span>问鼎苍穹</span> 👍（1） 💬（1）<div>老师您好，transforms是只能对图像的tensor数据进行处理是吧，对于表格类型的数据是不能进行数据增强的操作是吗，如果要对表格类型的数据进行数据增强应该如何操作呢</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/8c/c4/9fbe78cf.jpg" width="30px"><span>快快🔥</span> 👍（1） 💬（1）<div>老师，我想问下，在transform.dataset()中进行transforms的转换操作，是会将原图像数据覆盖掉吗，还是产生新的转换后的数据。</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/67/743128f7.jpg" width="30px"><span>书木子谢明</span> 👍（0） 💬（1）<div>老师您好，标准化用到的均值、标准差需要提前通过图片计算出来吗？还是根据经验拍一个数据？</div>2024-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（1）<div>transform可以进行图片与tensor的数据转类型转换，还可以进行旋转，裁剪，缩放等操作，与datasets搭配使用时，可以在加载数据的过程中，完成数据的增强操作。</div>2023-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/ad/6ee2b7cb.jpg" width="30px"><span>Jacob.C</span> 👍（0） 💬（1）<div>方远老师好，像FiveCrop这样一个样本变多个样本的变换，dataset加载的时候，标签如何跟着变多呢？不然会对不齐呀。</div>2023-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/5c/f4/70270989.jpg" width="30px"><span>🐰</span> 👍（0） 💬（1）<div>老师好，我想问一下，我在运行时最后结果不显示图片只显示标签是为什么呢？</div>2022-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（1）<div>加上逗号解决：too many indices for tensor of dimension 0
The problem is that the mean and std have to be sequences (e.g., tuples), therefore you should add a comma after the values:


# 定义一个transform
my_transform = transforms.Compose([transforms.ToTensor(),
                                   transforms.Normalize((0.5,), (0.5,))

ref: https:&#47;&#47;stackoverflow.com&#47;questions&#47;56745486&#47;pytorch-dataloader-indexerror-too-many-indices-for-tensor-of-dimension-0</div>2022-07-29</li><br/><li><img src="" width="30px"><span>Geek_b454ca</span> 👍（0） 💬（1）<div>老师您好，Torchvision中有transform这些可以对数据进行标准化的函数，如果不是要处理图像数据，在pytorch中是不是也有类似的对数据进行标准化等transform操作的函数呢？</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/5d/3f/ad1fed4a.jpg" width="30px"><span>黑暗骑士</span> 👍（0） 💬（1）<div>老师您好，
这节课我们对于数据本身进行了一系列操作，请问相应的标签如何处理呢？是不是会自动匹配？</div>2022-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（0） 💬（2）<div>老师您好，对于torchvision提供的datasets, 可以应用我们定义的transforms.Compose, 在读取时同时做数据变换。 那么对于我们自己的图像数据集，是不是只能定义一个函数，一边读取成tensor，然后一边处理？</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/8a/ec29ca4a.jpg" width="30px"><span>马克图布</span> 👍（0） 💬（1）<div>老师，在使用 Resize 的时候，出现以下 warning:

UserWarning: Argument interpolation should be of type InterpolationMode instead of int. Please, use InterpolationMode enum.

这个是可以直接忽略的吗？</div>2021-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e2/21/3bb82a79.jpg" width="30px"><span>栗白</span> 👍（0） 💬（1）<div>是图像的预处理操作。</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/e9/d131dd81.jpg" width="30px"><span>Mamba</span> 👍（0） 💬（0）<div>torchvision.transform  ——  对预处理的图像进行各种变换</div>2024-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b0/02/98f8b0ee.jpg" width="30px"><span>方华Elton</span> 👍（0） 💬（0）<div>torchvision.transforms
提供了多种图像预处理和增强的方法；包括裁剪、旋转、缩放、颜色等变化，通常用于数据增强和准备训练数据集。</div>2023-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（0）<div>老师，请教 执行报错
my_transform = transforms.Compose([transforms.ToTensor(),
                                   transforms.Normalize((0.5), (0.5))
                                  ])
mnist_dataset = datasets.MNIST(root=&#39;.&#47;data&#39;,
                               train=False,
                               transform=my_transform,
                               target_transform=None,
                               download=True)
item = mnist_dataset.__getitem__(0)
print(type(item[0]))

---------
IndexError                                Traceback (most recent call last)
&lt;ipython-input-1-bc3a8de1cbd4&gt; in &lt;module&gt;
     14 
     15 # 查看变换后的数据类型
---&gt; 16 item = mnist_dataset.__getitem__(0)
     17 print(type(item[0]))

~&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;torchvision&#47;datasets&#47;mnist.py in __getitem__(self, index)
     93 
     94         if self.transform is not None:
---&gt; 95             img = self.transform(img)
     96 
     97         if self.target_transform is not None:

~&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;torchvision&#47;transforms&#47;transforms.py in __call__(self, img)
     58     def __call__(self, img):
     59         for t in self.transforms:
---&gt; 60             img = t(img)
     61         return img
     62 

~&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;torchvision&#47;transforms&#47;transforms.py in __call__(self, tensor)
    161             Tensor: Normalized Tensor image.
    162         &quot;&quot;&quot;
--&gt; 163         return F.normalize(tensor, self.mean, self.std, self.inplace)
    164 
    165     def __repr__(self):

~&#47;opt&#47;anaconda3&#47;lib&#47;python3.8&#47;site-packages&#47;torchvision&#47;transforms&#47;functional.py in normalize(tensor, mean, std, inplace)
    206     mean = torch.tensor(mean, dtype=torch.float32)
    207     std = torch.tensor(std, dtype=torch.float32)
--&gt; 208     tensor.sub_(mean[:, None, None]).div_(std[:, None, None])
    209     return tensor
    210 

IndexError: too many indices for tensor of dimension 0
</div>2022-07-29</li><br/>
</ul>