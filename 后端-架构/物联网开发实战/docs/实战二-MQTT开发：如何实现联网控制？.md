你好，我是郭朝斌。

在上一节中，我们基于平头哥RVB2601开发板完成了智能电灯硬件的搭建和嵌入式应用的开发，但是打造一款物联网设备，我们还需要将硬件接入物联网平台。接下来，我就来讲解一下RVB2601开发板通过MQTT协议接入阿里云生活物联网平台的流程及方法。

在开始本节内容的阅读之前，你可以重新打开[第17讲](https://time.geekbang.org/column/article/322528)，了解一下Python语言的实现代码。对比着本节的C语言代码，你将会对程序开发有更深入的理解。

## 生活物联网平台的准备工作

阿里云生活物联网平台，又称为飞燕平台，是面向消费级产品的物联网开放平台。它具备完整的、面向家居物联网场景的功能定义，可以非常方便地完成智能设备的物联网接入工作。

接下来，我们就在这个平台上完成智能灯的联网控制实验。

### 创建项目和产品

首先，登录[生活物联网平台](https://living.aliyun.com)，我们进行第一个项目的创建。项目的名称，我们可以填写“智能电灯”。对于项目类型，你可以根据产品需求来决定，因为我们不计划接入天猫精灵生态，所以这里选择“自有品牌项目”。

![](https://static001.geekbang.org/resource/image/e8/1c/e8c304c43ed2yyd0ac86c8b1ca50ff1c.png?wh=1014x754)

接着，我们为这个“智能电灯”项目创建一个新产品“Led\_1”。

![](https://static001.geekbang.org/resource/image/15/be/15fac49fc02321208fc2c7e7f08d13be.png?wh=1858x554)

产品的参数可以这样设置：

- 所属品类，选择“电工照明”–&gt;“灯”。
- 节点设备，选择“设备”。是否接入网关，选择“否”。
- 连网方式，选择“WiFi”。
- 数据格式，选择“ICA标准数据格式（Alink JSON）”。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（1） 💬（0）<div>static函数仅可以在本文件中使用，不是static的函数除了能够在本文件中使用，还能在其他文件中使用</div>2022-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ae/e8/d01b90c3.jpg" width="30px"><span>种花家</span> 👍（0） 💬（1）<div>老师，reb2601 咋么实现4G&#47;5G联网，以及不在同一wifi 下手机控制灯呢？</div>2022-04-27</li><br/>
</ul>