你好，我是南柯。

今天我们要学习的是OpenAI在2021年提出的CLIP算法。在AI绘画的过程中，CLIP的作用是理解我们给到模型的prompt指令，将prompt指令编码为模型能理解的“语言”。

但你可能不知道，最早提出CLIP模型并不是帮助AI绘画模型理解prompt指令，而是用于连接图像和文本这两种模态。如今，随着AIGC技术的大爆发，CLIP模型又在AI绘画、多模态大模型等方向发挥了巨大价值。

这一讲，我们就一起来搞清楚CLIP这个算法背后的奥秘！只有真正理解了CLIP，你才能知道为什么prompt可以控制AI绘画生成的内容。在设计你自己的AI绘画模型的时候，便可以根据你的需求选择各种CLIP模型或者其变体模型，得到更好的绘画效果。

## 追本溯源：CLIP的提出背景

在学习CLIP之前，我们有必要先理解模态（Modality）的概念。在深度学习领域，模态可以用于描述输入数据的不同形式，比如图像、文本、音频等。不同的模态可以提供不同的特征，使模型能够从更多的角度理解和处理数据。在实践中，通过整合多种模态的信息，通常能够帮助模型获得更好的性能。

我们常说的NLP（Natural Language Processing），即自然语言处理，解决的就是文本模态的任务，比如文本问答、文本对话、文本情绪分析等任务。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/f6/d6c1a0c2.jpg" width="30px"><span>海杰</span> 👍（8） 💬（2）<div>老师我有几个问题。
1. 在SD里，CLIP的作用就是对prompt进行编码。文生图txt2img是用CLIP的文本编码器，图生图img2img用的是图像编码器，这样理解对吗？
2. 看到有些模型用CLIP skip 2，就是不用编码器的最后一层，这样设计的原理是什么？会得到更好的模型吗？
3. 外面下载的各种SD基础模型，它们用的都是同一个CLIP吗？下载的几个G的一个safetensors文件里，也包括CLIP的权重吗？</div>2023-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/85/b3/5f40f485.jpg" width="30px"><span>恨％心~</span> 👍（2） 💬（1）<div>老师好，请问下如何分别用CLIP 和OpenCLIP推断任意图片的prompt，有对应的代码示例吗？</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：动图是用什么做的？
Q2:512纬度空间，这个512也是经验值吗？
Q3：以4亿对图文数据集为例，硬件资源的需求量是个什么样子？ 比如存储空间需要多少台机器，计算需要多少台机器等。
Q4：我的笔记本电脑是惠普电脑，16G内存，不知道是否有GPU（估计有但不知道多大），这样的配置能运行老师的例子吗？</div>2023-08-08</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（0） 💬（1）<div>按着老师的代码，一次性在Colab运行成功。
第二个作业：
第一个图片，用CLIP测试，结果是：“Predicted class: cat    prob: cat 1.0, dog 0.0”； 
用OpenCLIP测试结果是：“prob: a diagram 8.51679033075925e-06, a dog 1.5743193216621876e-05, a cat 0.9999756813049316”
第二个图片，用CLIP测试，结果是：“Predicted class: dog  prob: cat 0.0, dog 1.0”
用OpenCLIP测试结果是：“prob: a diagram 8.806668120087124e-06, a dog 0.999969482421875, a cat 2.167693673982285e-05”</div>2023-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/06/81/dd72c32e.jpg" width="30px"><span>陈炜</span> 👍（0） 💬（0）<div>CLIP 的训练目标是让对应的图像、文本得到的特征向量靠近，也就是余弦距离越大越好，让不对应的图像、文本得到的特征向量远离，也就是余弦距离尽可能小。

这里的余弦距离是余弦相似度吗？
特征向量靠近，余弦距离减小，余弦相似度增大</div>2025-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/27/0b/12dee5ed.jpg" width="30px"><span>进化论</span> 👍（0） 💬（0）<div>import torch
import clip
from PIL import Image
import urllib.request
import matplotlib.pyplot as plt

# Load the CLIP model
device = &quot;cuda&quot; if torch.cuda.is_available() else &quot;cpu&quot;
model, preprocess = clip.load(&quot;ViT-B&#47;32&quot;, device=device)

# Define the target classes
target_classes = [&quot;cat&quot;, &quot;dog&quot;, &quot;owl&quot;]

# Load and preprocess the image

image_url = &quot;https:&#47;&#47;z1.ax1x.com&#47;2023&#47;10&#47;23&#47;piALRpQ.png&quot;
image_path = &quot;test_image.png&quot;
urllib.request.urlretrieve(image_url, image_path)
image = Image.open(image_path).convert(&quot;RGB&quot;)
image_input = preprocess(image).unsqueeze(0).to(device)

# Encode the image
with torch.no_grad():
    image_features = model.encode_image(image_input)
    
# Encode the target classes
text_inputs = clip.tokenize(target_classes).to(device)
with torch.no_grad():
    text_features = model.encode_text(text_inputs)
    
# Compute the similarity scores
similarity_scores = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# Get the predicted class
_, predicted_class = similarity_scores.max(dim=-1)
predicted_class = predicted_class.item()

# Print the predicted class
predicted_label = target_classes[predicted_class]

plt.imshow(image)
plt.show()
print(f&quot;Predicted class: {predicted_label}&quot;)
print(f&quot;prob: cat {similarity_scores[0][0]}, dog {similarity_scores[0][1]}, owl {similarity_scores[0][2]}&quot;)</div>2023-10-23</li><br/>
</ul>