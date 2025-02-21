你好，我是南柯。

上一讲我们已经学习了ControlNet的算法原理，也了解了它在AI绘画中强大的控制能力。今天我们一起来完成ControlNet的实战任务。

在这一讲中，我们将通过写代码的方式使用ControlNet，一起完成后面这三个任务。

1. 认识官方已经发布的ControlNet模型以及社区传播的第三方ControlNet模型。
2. 实现ControlNet论文中的控图生成任务，掌握ControlNet的基础能力。
3. 探索ControlNet的趣味生成功能，包括图像风格化、二维码生成、创意文字和线稿上色。

掌握了这些技巧，你也一定能够发挥创意，做出很多结构鲜明的作品。让我们开始吧！

## 模型获取

在Hugging Face上，我们不光可以获取到海量AI绘画基础模型，还能找到各种开发者训练的ControlNet模型。正式使用之前，我们先来认识下这些模型。

### 官方发布的模型

首先是ControlNet论文作者在ControlNet1.0和1.1中发布的22个模型。

ControlNet1.0的8个模型可以通过后面这个 [Hugging Face链接](https://huggingface.co/lllyasviel/ControlNet/tree/main/models)获取。我们可以看到ControlNet1.0各个模型的命名规则，以第一行的 “control\_sd15\_canny.pth” 为例，sd15表示用于训练这个ControlNet的基础模型是SD1.5，Canny便是ControlNet的控制条件是Canny算子，也就是提取原始图像的边缘。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（4） 💬（1）<div>包括ControlNet 在内的AI绘画工具越来越多，但AI绘画结果需要人工抽取结果的痛点依在。

现在AI 绘画的流程如下:
1. 先有个想画的想法，
2. 根据这个想法编出个prompt 输给AI 绘画工具，
3. AI绘画工具生成多张图片比如说4张供人参考，
4. 人们再依据上面步骤1中的想象，从出的4张图里面选出合意的，如不甚满意，就继续上面的步骤2改变prompt，然后再执行步骤3，让AI重新绘图，这过程可能会进行好几轮，比较费时。

那么问题来了，有没有什么方法让上面的过程自动化? 

计算机的优势就是不知疲惫，虽然有时也宕机罢工，但总体来说比人能干。如果能将上面成图+判断的过程先交给计算机进行5轮，然后再由人类对出图给出评估，效率会提高很多，图的质量也会更高。

解决上面痛点的思考之一是设计一个质量控制层 QualityControlNet，这个可训练的质量控制层应包含下面的一些功能:
1. 有对图像质量评估的量化指标，可选艺术，技术，美学等几个方面做为评估参量，指标可调可变，
2. 有对正反prompt修正反馈的能力，
3. 要修正的图像+新的更改要求可以自动返回低维隐藏层，并启动重绘过程，
4. 能自动求解最佳重绘参数，最佳去噪步骤等参量。

达到上面要求中的一个或几个，对质量控制层 QualityControlNet 的一些想法，大家补充。</div>2023-09-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/lJR3Ba9EuTLRSry9sajEeRcvfwuiaPDr41KicHYGxcsXnRcTxaTp3OHq24AebUR9MS016zSEmqAyws5iaQiaj5TDdQ/132" width="30px"><span>Geek_cbcfc8</span> 👍（1） 💬（1）<div>腾讯发布了一个adapter https:&#47;&#47;github.com&#47;tencent-ailab&#47;IP-Adapter
可以实现根据一张图抽取人脸，风格，服装等特征，用于image to image </div>2023-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：彩票上面的数字，只有一个数字，其他的看不到了，不知道是被雨淋了还是被撕掉了。用WebUI可以恢复吗？或者其他某个模型？
Q2：controlNet或其他模型可以创作名片吗？ </div>2023-09-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/lJR3Ba9EuTLRSry9sajEeRcvfwuiaPDr41KicHYGxcsXnRcTxaTp3OHq24AebUR9MS016zSEmqAyws5iaQiaj5TDdQ/132" width="30px"><span>Geek_cbcfc8</span> 👍（0） 💬（1）<div>老师你好，controlnet xl版本已经出来了，能加餐一个的换装任务吗，把一些知识点串一下
1、训练衣服或人物的lora模型
2、基于controlnet进行衣服或模特的更换
可应用到电商一键换装，或者帮组情侣实现AI婚纱摄影</div>2023-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fd/dc/8c394a51.jpg" width="30px"><span>刘蕾</span> 👍（0） 💬（0）<div>老师您好，这节课里面的蒙娜丽莎的那个例子，免费的CoLab资源是不是跑不了？ 价值SDXL（stable-diffusion-xl-base-1.0）的那句，跑了1个多小时还没跑完。</div>2024-01-07</li><br/>
</ul>