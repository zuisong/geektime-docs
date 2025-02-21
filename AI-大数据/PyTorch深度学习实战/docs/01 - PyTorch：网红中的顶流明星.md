你好，我是方远。

从这节课开始，我们正式进入PyTorch基础篇的学习。

在基础篇中，我们带你了解PyTorch的发展趋势与框架安装方法，然后重点为你讲解NumPy和 Tensor的常用知识点。

掌握这些基础知识与技巧，能够让你使用 PyTorch 框架的时候更高效，也是从头开始学习机器学习与深度学习迈出的第一步。磨刀不误砍柴工，所以通过这个模块，我们的目标是做好学习的准备工作。

今天这节课，我们先从PyTorch的安装和常用编程工具说起，先让你对PyTorch用到的语言、工具、技术做到心里有数，以便更好地开启后面的学习之旅。

## PyTorch登场

为什么选择 PyTorch 框架，我在开篇词就已经说过了。从19年起，无论是学术界还是工程界 PyTorch 已经霸占了半壁江山，可以说 PyTorch 已经是现阶段的主流框架了。

这里的Py我们不陌生，它就是Python，那Torch是什么？从字面翻译过来是一个“火炬”。

![图片](https://static001.geekbang.org/resource/image/8b/8d/8b83b03c5e25886e1c6fe5aed8572e8d.png?wh=480x141)

什么是火炬呢？其实这跟TensorFlow中的Tensor是一个意思，我们可以把它看成是**能在GPU中计算的矩阵**。

那PyTorch框架具体是怎么用的呢？说白了就是一个计算的工具。借助它，我们就能用计算机完成复杂的计算流程。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/2f/8a/82d25d7a.jpg" width="30px"><span>bbbbbbbbbb</span> 👍（7） 💬（2）<div>请问没有显卡，可以有什么不用买显卡的解决方案吗</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/d1/0e/c0554a72.jpg" width="30px"><span>悠闲不自得</span> 👍（6） 💬（1）<div>请问老师，这个没有视频吗？</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/3c/b03ed9c2.jpg" width="30px"><span>Swaggy</span> 👍（4） 💬（1）<div>老师可以讲一点网络训练技巧吗，比如如何应对循环神经网络梯度弥散的意思。</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/8d/70/b0047299.jpg" width="30px"><span>Zeurd</span> 👍（2） 💬（1）<div>老师好，要是用的是A卡就没办法了只能用cpu对么</div>2022-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJTqcBC6lVDsQE7f1Tr5elKibRfJv7v3RRok4Q6DyBxjFvlPNngWgWyVqZHLD60ibzicMtTxLZjZy2tw/132" width="30px"><span>Geek_ce0dd6</span> 👍（1） 💬（1）<div>老师请教几个神经网络训练模型的问题，假设我需要训练一个识别猫的模型，我准备了3000张猫的图片

问题1：3000张猫的图片意味着有3000个猫的模型吗？这里我的想法是因为每个照片不一样所以每个照片都是一个模型都有单独的权重值

问题2：每张猫的图片训练完它的权重值怎么保存

问题3：假设问题1成立那么训练完成之后，输入测试照片的时候，它是如何匹配模型的呢？

问题4：如果问题1不成立，训练的3000张照片只会存在一个模型，那么输入测试照片的时候他是会如何找到匹配的权重值得呢？

</div>2023-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e3/4d/60826050.jpg" width="30px"><span>🌟</span> 👍（1） 💬（1）<div>
torch.cuda.is_available()后直接到下一行了，没反应是怎么回事呀？</div>2022-09-04</li><br/><li><img src="" width="30px"><span>zhbr001</span> 👍（1） 💬（1）<div>项目的工具是什么</div>2022-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4e/84/394b64d2.jpg" width="30px"><span>张昊</span> 👍（1） 💬（1）<div>昨天看到pytorch支持Mac M1的芯片了，马上装了一个，从头来学习。</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/89/23/e71f180b.jpg" width="30px"><span>Geek_fc975d</span> 👍（1） 💬（2）<div>很喜欢老师的图文方式</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/17/6b/4e089b79.jpg" width="30px"><span>度</span> 👍（1） 💬（4）<div>老师，你好。我在新建一个 Python 的 Notebook时，“New”下拉菜单，并没有“Python 3”选项，而是Python 3（ipykernel）,点击后出现创建错误。特想请教是为什么？谢谢</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/c6/772f9b74.jpg" width="30px"><span>guang384</span> 👍（1） 💬（1）<div>期待更新</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（1）<div>第一课学习打卡，PyTorch环境已经安装成功</div>2023-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/27/791d0f5e.jpg" width="30px"><span>小林子</span> 👍（0） 💬（1）<div>老师你好，我想问一下cudnn有必要装吗</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/de/25/44662eb8.jpg" width="30px"><span>Miss</span> 👍（0） 💬（2）<div>老师你好，我手上只有mac，一开始用mac学习，后面换成win系统可以吗？</div>2022-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/b6/e91a693f.jpg" width="30px"><span>曾小福气</span> 👍（0） 💬（1）<div>请问下老师，如果直接用pip install torch==1.9.0安装的是cpu还是gpu的版本呀？还是两者都有？</div>2022-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/03/f2c008fc.jpg" width="30px"><span>明远</span> 👍（0） 💬（1）<div>编辑器中可以把 vs code 算上。vs code 能够良好的支持 Jupyter Notebook 格式，也能交互式执行。</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/dc/d4/9616384f.jpg" width="30px"><span>Mr.Lin</span> 👍（0） 💬（2）<div>在Jupyter notebook 中输入import torch
torch._version_
显示module &#39;torch&#39; has no attribute &#39;_version_&#39;怎么回事啊？</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f3/d7/ae84f9b8.jpg" width="30px"><span>李柠檬🍋</span> 👍（0） 💬（1）<div>老师你好我按照步骤下载了cuda10.2和cuDNN并配置了环境变量之后为什么执行torch.cuda.is_available()指令之后仍然显示False呢 报错CUDA driver initialization failed, you might not have a CUDA gpu.我的显卡是1050的 需要卸载cuda重新安装吗 如果重装的话需要怎么操作呢</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f3/d7/ae84f9b8.jpg" width="30px"><span>李柠檬🍋</span> 👍（0） 💬（1）<div>你好老师我想问一下按照您给出的代码下载的pytorch 那么cuda应该选择10版本还是11版本呢</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/07/b6/e213fc11.jpg" width="30px"><span>她の他</span> 👍（0） 💬（1）<div>老师您好，下载CUAD工具包是下载local版本还是network版本的，因为文件大小差距有点大，不知如何选择。</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/cb/7c004188.jpg" width="30px"><span>和你一起搬砖的胡大爷</span> 👍（0） 💬（2）<div>Windows 11可以直接docker中，wsl2的backend，使用GPU，装完docker和nvdocker后，可以跑pytorch的容器，不需要额外安装cuda运行时</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/31/f1/1ff57b9d.jpg" width="30px"><span>徐富献</span> 👍（0） 💬（1）<div>老师你好，想问下推荐使用anaconda进行安装的方式吗？</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e3/d7/d7b3505f.jpg" width="30px"><span>官</span> 👍（0） 💬（1）<div>vscode+jupyter notebook 这个搭配也挺好用的，相比默认的notebook感觉调试方便一些，自己之前经常用sklearn包做一些简单任务的时候受益匪浅</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/5f/ea25d673.jpg" width="30px"><span>西红柿牛男</span> 👍（0） 💬（1）<div>jupyter安装完如何打开？好像没讲，网页地址在哪里找？</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b5/10/6165c67d.jpg" width="30px"><span>破绽</span> 👍（0） 💬（1）<div>打卡第一天~从从安装开始~</div>2021-10-13</li><br/><li><img src="" width="30px"><span>人间失格</span> 👍（0） 💬（1）<div>希望老师更新快一点，学习可以连贯些。</div>2021-10-12</li><br/><li><img src="" width="30px"><span>fengzhiyu_sh</span> 👍（0） 💬（1）<div>能推荐一本市面的pytorch书配套学习么？ 谢谢</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/2c/b27eefc5.jpg" width="30px"><span>Abcd</span> 👍（0） 💬（2）<div>AMD显卡可以用吗</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cc/41/af863836.jpg" width="30px"><span>夏阳</span> 👍（0） 💬（1）<div>催更催更~</div>2021-10-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epJHlrZ1pcs2sxHpxW6EaDmUq8sMD85vm3hskWVn2LmlcUI84tARViam4vAuS0uVibpFq1uRAABff6g/132" width="30px"><span>hbuelgr</span> 👍（0） 💬（1）<div>直接入手。</div>2021-10-11</li><br/>
</ul>