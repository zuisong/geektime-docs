你好，我是方远。

在前面的课程中，我们已经学习了Torchvision的数据读取与常用的图像变换方法。其实，Torchvision除了帮我们封装好了常用的数据集，还为我们提供了深度学习中各种经典的网络结构以及训练好的模型，只要直接将这些经典模型的类实例化出来，就可以进行训练或使用了。

我们可以利用这些训练好的模型来实现图片分类、物体检测、视频分类等一系列应用。

今天，我们就来学习一下经典网络模型的实例化与Torchvision中其他有趣的功能。

## 常见网络模型

Torchvision中的各种经典网络结构以及训练好的模型，都放在了`torchvision.models`模块中，下面我们来看一看`torchvision.models` 具体为我们提供了什么支持，以及这些功能如何使用。

### torchvision.models模块

`torchvision.models` 模块中包含了常见网络模型结构的定义，这些网络模型可以解决以下四大类问题：图像分类、图像分割、物体检测和视频分类。图像分类、物体检测与图像分割的示意图如下图所示。

![](https://static001.geekbang.org/resource/image/42/b3/4211c2d8cd27db3e903e6125122f47b3.jpg?wh=1920x1204)

图像分类，指的是单纯把一张图片判断为某一类，例如将上图左侧第一张判断为cat。目标检测则是说，首先检测出物体的位置，还要识别出对应物体的类别。如上图中间的那张图，不仅仅要找到猫、鸭子、狗的位置，还有给出给定物体的类别信息。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="" width="30px"><span>AstrHan</span> 👍（17） 💬（2）<div>老师，微调的原理是什么啊？image net训练出来的倒数第二层应该是包含1000个类型的特征，那微调训练之后这层输出的会全部变成狗相关的特征吗？如果这样，那训练过程感觉反而会更慢啊。还是说微调训练最多的是输出层，降低倒数第二层里非狗的特征权重？</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fc/de/6e2cb960.jpg" width="30px"><span>autiplex</span> 👍（16） 💬（1）<div>
import torch
import torchvision.models as models

# 加载预训练模型
googlenet = models.googlenet(pretrained=True)

# 提取分类层的输入参数
fc_in_features = googlenet.fc.in_features
print(&quot;fc_in_features:&quot;, fc_in_features)

# 查看分类层的输出参数
fc_out_features = googlenet.fc.out_features
print(&quot;fc_out_features:&quot;, fc_out_features)

# 修改预训练模型的输出分类数(在图像分类原理中会具体介绍torch.nn.Linear)
googlenet.fc = torch.nn.Linear(fc_in_features, 10)
&#39;&#39;&#39;
输出：
fc_in_features: 1024
fc_out_features: 1000
&#39;&#39;&#39;

老师这段代码里 torch.nn.Linear里是不是应该是fc_out_features，因为不是要转换输出分类数为10么</div>2021-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/j24oyxHcpB5AMR9pMO6fITqnOFVOncnk2T1vdu1rYLfq1cN6Sj7xVrBVbCvHXUad2MpfyBcE4neBguxmjIxyiaQ/132" width="30px"><span>vcjmhg</span> 👍（6） 💬（1）<div>vgg16 = models.vgg16(pretrained=True)</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7b/1e/8bb7c7fe.jpg" width="30px"><span>..................</span> 👍（5） 💬（1）<div>老师请问这句话“tensor：类型是 Tensor 或列表，如果输入类型是 Tensor，其形状应是 (B x C x H x W)；”中的B,C,H,W分别是什么意思？实在想不明白</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（3） 💬（2）<div>老师您好，请教一个可能跟计算机视觉相关的深度学习的问题。假如一款3D的赛车类游戏，我在里面做了一系列操作，从起点开到了终点，我能否让神经网络根据我的操作和对应的录屏学会我的操作，并大致重复出来呢？这需要什么样的深度学习模型呢？</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ca/58/8b4723dc.jpg" width="30px"><span>奔跑的火龙果</span> 👍（1） 💬（1）<div>iter(tensor_dataloader)和next()分别是什么意思呢？
</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（1） 💬（1）<div>解决 AttributeError: module &#39;torchvision.models&#39; has no attribute &#39;googlenet&#39;
运行以下命令报错
googlenet = models.googlenet()
解决方法
google_net = torchvision.models.inception_v3(pretrained=True)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
&lt;ipython-input-3-0e4152b595be&gt; in &lt;module&gt;
      1 import torchvision.models as models
----&gt; 2 googlenet = models.googlenet()

AttributeError: module &#39;torchvision.models&#39; has no attribute &#39;googlenet&#39;

ref: https:&#47;&#47;stackoverflow.com&#47;questions&#47;55762706&#47;how-to-load-pretrained-googlenet-model-in-pytorch</div>2022-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/17/6b/4e089b79.jpg" width="30px"><span>度</span> 👍（1） 💬（1）<div>googlenet.fc = torch.nn.Linear(fc_in_features, 10)
print(&quot;fc_out_features:&quot;, fc_out_features)
老师，我更改后得到的输出特征数还是 fc_out_features: 1000 这个结果。请赐教！</div>2021-11-16</li><br/><li><img src="" width="30px"><span>clee</span> 👍（1） 💬（1）<div>vgg16 = models.vgg16(pretrained=True)</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cc/41/af863836.jpg" width="30px"><span>夏阳</span> 👍（1） 💬（4）<div>老师，这段段代码会报错
torchvision.utils.save_image(grid_tensor, &#39;grid.jpg&#39;)

ValueError: unknown file extension: 

搞不清楚什么状况，请帮忙指教</div>2021-10-30</li><br/><li><img src="" width="30px"><span>勿更改任何信息</span> 👍（1） 💬（1）<div>老师，代码太分散了，后期是否可以在github上统一存储呢？</div>2021-10-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/SKmvhbNe9LMPQ0ib8ZqbJEfHicUxzxCSKVXiaibn7OrmXGUFQjkesgvODymZz4kibzqOGxuRq42t3sB2ibcBIIGWRgSg/132" width="30px"><span>超人不会飞</span> 👍（1） 💬（1）<div>vgg16net=torchvision.models.vgg16(pretrained=True)</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b0/02/98f8b0ee.jpg" width="30px"><span>方华Elton</span> 👍（0） 💬（1）<div>import torch
import torchvision.models as models

# 加载预训练模型
vgg16 = models.vgg16(pretrained=True)</div>2023-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/d8/92a98fb6.jpg" width="30px"><span>逍遥思</span> 👍（0） 💬（1）<div>img_tensor, label_tensor = data_iter.next()会遇到这样一个问题：
AttributeError: &#39;_SingleProcessDataLoaderIter&#39; object has no attribute &#39;next&#39;
改为以下可解决：
img_tensor, label_tensor = next(data_iter)</div>2023-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（1）<div>思考题，也不懂 VGG 是什么，直接找文档 https:&#47;&#47;pytorch.org&#47;vision&#47;stable&#47;models&#47;generated&#47;torchvision.models.vgg16.html#torchvision.models.vgg16
---
from torchvision.models import VGG16_Weights
vgg16 = models.vgg16(weights=VGG16_Weights.DEFAULT)
---

老师的课程里，挺多名词我都看不懂，接着看吧，希望后面能豁然开朗。</div>2022-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/12/2d/aba06a9a.jpg" width="30px"><span>李泽</span> 👍（0） 💬（2）<div>googlenet.fc = torch.nn.Linear(fc_in_features, 10) 之后要如何使用它做一下测试呢？</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（1）<div>vgg16 = models.vgg16()
vgg16 = models.vgg16(pretrained=True)</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e4/5a/b61bd7f1.jpg" width="30px"><span>黄焯</span> 👍（0） 💬（1）<div>文中的当前版本应该是v1.10.0，而不是v0.10.0吧</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/c2/12d11bbd.jpg" width="30px"><span>康宁</span> 👍（1） 💬（0）<div>新版的 DataLoader 中迭代器函数 next（） 变成 __next__()</div>2023-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/5e/34/5b8ff9a1.jpg" width="30px"><span>XXXL</span> 👍（0） 💬（0）<div>为啥我调用 google net的时候它提示module &#39;torchvision.models&#39; has no attribute &#39;googlenet&#39;</div>2022-09-27</li><br/>
</ul>