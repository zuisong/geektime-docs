你好，我是Mike。这节课我们来学习如何使用Rust对图片中的对象进行识别。

图像识别是计算机视觉领域中的重要课题，而计算机视觉又是AI的重要组成部分，相当于AI的眼睛。目前图像识别领域使用最广泛的框架是 YOLO，现在已经迭代到了v8版本。而基于Rust机器学习框架Candle，可以方便地实现YOLOv8算法。因此，这节课我们继续使用Candle框架来实现图片的识别。

Candle框架有一个示例，演示了YOLOv8的一个简化实现。我在此基础上，将这个源码中的示例独立出来，做成了一个单独的项目，方便你学习（查看[代码地址](https://github.com/miketang84/jikeshijian/tree/master/24-candle_yolov8)）。

注：这节课的代码适用于 candle\_core v0.3 版本。

## YOLO简介

YOLO（You Only Look Once）是一种目标检测算法，它可以在一次前向传递中检测出图像中的所有物体的位置和类别。因为只需要看一次，YOLO被称为Region-free方法，相比于Region-based方法，YOLO不需要提前找到可能存在目标的区域（Region）。YOLO在2016年被提出，发表在计算机视觉顶会CVPR（Computer Vision and Pattern Recognition）上。YOLO对整个图片进行预测，并且它会一次性输出所有检测到的目标信息，包括类别和位置。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/02/78/4d40b4b2.jpg" width="30px"><span>渡鸦10086</span> 👍（2） 💬（1）<div>网页下载模型到本地后通过--models参数即可使用本地模型，比如
cargo run --release -- assets&#47;football.jpg --which m --model .&#47;model&#47;yolov8m.safetensors</div>2024-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/1a/367ebeac.jpg" width="30px"><span>Jump</span> 👍（1） 💬（1）<div>启用cuda需要在cargo.toml里面开启特性
[dependencies]
candle-core = {version= &quot;0.3.1&quot;,features=[&quot;cuda&quot;]}
candle-nn = {version= &quot;0.3.1&quot;,features=[&quot;cuda&quot;]}
candle-transformers = {version= &quot;0.3.1&quot;,features=[&quot;cuda&quot;]}</div>2024-03-23</li><br/><li><img src="" width="30px"><span>Geek_118351</span> 👍（0） 💬（1）<div>老师你好，会考虑出一个针对视频流的目标识别课程吗。</div>2024-03-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VF71Gcf2C2bjYPFCRv0TPfwhkJmT5WhtusltuaXQM0KMDibdallNFypqWV6v2FJ4bqNwzujiaF5LEDeia7JMZTTtw/132" width="30px"><span>Geek_e72251</span> 👍（0） 💬（2）<div>老师可以贴一段怎么从本地加载 yolo 模型的代码吗？实在下载不下来😮‍💨</div>2024-01-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VF71Gcf2C2bjYPFCRv0TPfwhkJmT5WhtusltuaXQM0KMDibdallNFypqWV6v2FJ4bqNwzujiaF5LEDeia7JMZTTtw/132" width="30px"><span>Geek_e72251</span> 👍（0） 💬（5）<div>Error: request error: https:&#47;&#47;huggingface.co&#47;lmz&#47;candle-yolo-v8&#47;resolve&#47;main&#47;yolov8m.safetensors: Connection Failed: Connect error: connection timed out

Caused by:
    0: https:&#47;&#47;huggingface.co&#47;lmz&#47;candle-yolo-v8&#47;resolve&#47;main&#47;yolov8m.safetensors: Connection Failed: Connect error: connection timed out
    1: connection timed out 一直下不来这个文件，可以提前下载下来然后放到项目里面吗？浏览器可以正常下载</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/03/72/666d9a55.jpg" width="30px"><span>凤  梨  🍍</span> 👍（0） 💬（2）<div>pytorch怎么转safetensors，没工具下载不了外面的模型</div>2023-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/22/403a340a.jpg" width="30px"><span>unistart</span> 👍（0） 💬（1）<div>老师，我有一个问题就是猫猫那张图执行姿势探测任务时无法正确识别，这是为什么啊？

cargo run --release -- assets&#47;cats.jpg --model candle-yolo-v8&#47;yolov8x-pose.safetensors --which x --task pose
   Compiling candle_demo_yolov8 v0.1.0 (E:\Project\rust-jikeshijian\24-candle_yolov8)
    Finished release [optimized] target(s) in 12.69s
     Running `target\release\candle_demo_yolov8.exe assets&#47;cats.jpg --model candle-yolo-v8&#47;yolov8x-pose.safetensors --which x --task pose`
Running on CPU, to run on GPU, build this example with `--features cuda`
model loaded
processing &quot;assets&#47;cats.jpg&quot;
generated predictions Tensor[dims 56, 6300; f32]
writing &quot;assets&#47;cats.pp.jpg&quot;</div>2023-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/09/3e/5021e8a1.jpg" width="30px"><span>蕨火</span> 👍（0） 💬（1）<div>同问，不联网怎么做？</div>2023-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（0） 💬（1）<div>用rust怎么训练录像资源啊？</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（0） 💬（2）<div>如果我们的电脑不联网的情况下，用yolo训练图片资源啊？</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（0） 💬（1）<div>怎么使用yolo训练图片？请老师请一下</div>2023-12-19</li><br/>
</ul>