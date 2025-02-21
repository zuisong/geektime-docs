你好，我是Mike。

今天我们继续用Slint做一个小项目。这个项目的目标是为我们[第 24 讲](https://time.geekbang.org/column/article/734943)实现的用YOLOv8从图片中识别出对象及姿势的小应用提供一个GUI界面。

这个GUI程序非常实用，可以以一种真观对比的形式让你看到对原始图片经过AI加工后的效果。比如像下面这样：

![图片](https://static001.geekbang.org/resource/image/ab/a4/ab5aebed249dc410328a4cee8305e6a4.png?wh=1825x1029)

## 原理解析

根据我们上节课学到的知识及第24讲里的操作流程，我们的实现应该分成4步。

1. 选择一张图片，加载显示在界面左边。
2. 点击 “Detect Objects”或 “Detect Poses”。
3. 经过YOLOv8引擎计算和标注，生成一张新的图片。
4. 在界面右边加载这张新图片。

下面让我们开始动手操作。

注：这节课的代码适用于 Slint v1.3 版本。

## 分步骤实现

### 创建项目

我们还是使用官方提供的Slint模板来创建，先下载模板。

```plain
cargo generate --git https://github.com/slint-ui/slint-rust-template --name slint-yolov8-demo
cd slint-yolov8-demo
```

运行 `cargo run` 测试一下。

### 设计界面

这个应用其实不复杂，你可以这样来分解这个界面。

![](https://static001.geekbang.org/resource/image/a7/a3/a7c4ecbf59ce56f727581577e65984a3.jpg?wh=1754x1156)

1. 从上到下使用一个 VerticalBox，分成三部分：Model说明、图片显示区、按钮区。
2. 图片显示区使用一个 HorizontalBox，分成三部分：左边图片显示区、中间分隔线、右边图片显示区。图片使用 Image 基础元素来显示。
3. 按钮区，使用HorizontalBox排列三个按钮：选择图片、探测对象、探测姿势，并且左对齐。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VF71Gcf2C2bjYPFCRv0TPfwhkJmT5WhtusltuaXQM0KMDibdallNFypqWV6v2FJ4bqNwzujiaF5LEDeia7JMZTTtw/132" width="30px"><span>Geek_e72251</span> 👍（0） 💬（1）<div>老师，怎么给组件添加鼠标右键菜单选项啊？看文档好像没这个功能。</div>2023-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/73/93/abb7bfe3.jpg" width="30px"><span>Marco</span> 👍（0） 💬（1）<div>老师，用slint如何实现多窗口呢。例如在主窗口点击某个按钮，弹出一个新的窗口</div>2023-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（0） 💬（2）<div>老师，用slint怎么实现浏览pdf文件啊？</div>2023-12-22</li><br/>
</ul>