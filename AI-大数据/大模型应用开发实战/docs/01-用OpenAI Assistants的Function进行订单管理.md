你好，我是黄佳。

从今天开始，我们开始大模型应用开发实战的启程篇。最简单的大模型应用开发工具应该就是OpenAI Assistants。不过虽然简单，但是它的功能超级强大。所以，在启程篇中我们先把这个工具讲透。（注意，在2024年四月中旬，OpenAI 发布了Assistants的Beta v2版本，我们的课程基于v2版本。）

先说说本课的学习目标，主要有两个：

1. 完全掌握到底什么是OpenAI Assistants，怎么使用它。
2. 通过 Assistants提供的Function，把自然语言问答自动地转换成函数调用的元数据，并能够动态地选择合适的函数进行调用。其中，什么是函数调用的元数据，什么是动态调用，也许有一点难理解，不怕，学完本课就会清晰。

另外，这节课我会带你完成一个**订单管理功能**，只根据用户的对话，给他计算购物篮里面订单商品的总金额。

## OpenAI 的 Assistants 工具其实是个不错的 Agent

吴恩达老师在他最新的演讲中，大谈特谈AI Agent，而且给出了下面四种Agent设计模式。

![图片](https://static001.geekbang.org/resource/image/c3/a5/c387871a9d18302e64a81c56924987a5.png?wh=2154x1135)

这四种Agent实现模式分别是：

1. 反思（Reflection）：Agent通过交互学习和反思来优化决策。
2. 工具使用（Tool use）：Agent 在这个模式下能调用多种工具来完成任务。
3. 规划（Planning）：在规划模式中，Agent 需要规划出一系列行动步骤来达到目标。
4. 多Agent协作（Multiagent collaboration）：涉及多个Agent之间的协作。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLFvhaPbJ1sBZqr8GQRVDiaxsicukAETVzjqmBRba2WqibbmX3NmoPIkaNEnBvyaWobyCjGN0FJgGnKQ/132" width="30px"><span>Geek_9948a5</span> 👍（2） 💬（1）<div>这里的Assistant 本质是不是就是一个agent？
就像老师之前的langchain课程中所讲，我们也可以基于langchain+react框架 搭建一个具备调用外部工具的agent。
那么Assistant 和基于langchain搭建的agent的主要区别是什么呢？</div>2024-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f6/af/17886a09.jpg" width="30px"><span>Jay</span> 👍（1） 💬（1）<div>能提供完成的代码吗 ，，你提供的代码片段跑不起来</div>2024-05-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（1） 💬（1）<div>除了计算订单总额之外，还可以实现以下两个函数：

1. `apply_discount(order_total, discount_percentage)`: 该函数用于计算订单总额中的折扣金额。用户可以提供订单总额和折扣百分比，函数会返回应用折扣后的订单总额。

```python
def apply_discount(order_total, discount_percentage):
    discount_amount = order_total * discount_percentage &#47; 100
    discounted_total = order_total - discount_amount
    return discounted_total
```

2. `calculate_shipping_cost(order_weight, shipping_rate)`: 这个函数用于计算订单的运输成本。用户可以提供订单的重量和每磅运输费用，函数将返回订单的运输总成本。

```python
def calculate_shipping_cost(order_weight, shipping_rate):
    shipping_cost = order_weight * shipping_rate
    return shipping_cost
```

通过这两个新的函数，可以更全面地处理网上商店的订单相关功能。在具体对话中，根据用户的需求，我会自动选择调用合适的函数来满足用户的要求。</div>2024-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（0） 💬（1）<div>佳哥好，让大模型从一组函数中选择一个，并精确地指定每个参数，是否有适用的边界？什么时候该选择大模型模糊调用，什么时候该选择传统编程实现精确调用？如果大模型调用函数失败，除了给定一个默认函数，有什么方法能调优调用函数的手段吗，让不成功变得成功。</div>2024-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/1f/8e9ee163.jpg" width="30px"><span>良记</span> 👍（0） 💬（1）<div>Assistant 是怎么知道要调用服务的地址的？一开始的function就定义了函数的元数据，那么实现这个function的服务位置又应该在哪里配置？</div>2024-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（3）<div>1. 请问完整的代码在哪里？
我在执行时，有一定几率出现异常：
    function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
    AttributeError: &#39;NoneType&#39; object has no attribute &#39;submit_tool_outputs&#39;
通过 print(run.status) 打印状态，发现是complete而不是required_action...
这和api的limit有关系么(我没有调用很频繁)？亦或者和网络有关？在什么情况下会直接得到一个complete的状态？

2. 想找python sdk的详细文档请问哪里有？官网上大篇幅的都是restful api的文档</div>2024-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/21/a33cc944.jpg" width="30px"><span>熊出没</span> 👍（0） 💬（1）<div>创建Assistants时模型选择只有gpt-3.5-turbo-16k、gpt-3.5-turbo-0125、gpt-3.5-turbo、CHAT这几个选择 和老师的不一样 为什么
</div>2024-05-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTICAILuSqtnARmMmomT7ic85ITviaiaJlowficJ4XH1pkh1syt1EFtOTvrMht2yOWxlW710AicaAf1EXEg/132" width="30px"><span>yision97</span> 👍（0） 💬（2）<div>各位使用的什么支付方案啊，我的卡被封了</div>2024-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/f4/86/21ea3970.jpg" width="30px"><span>界元</span> 👍（0） 💬（4）<div>学习完了，对于order_total = globals()[function_name](**arguments_dict)的function_name怎么来的不太理解，为什么不是calculate_order_total？</div>2024-05-22</li><br/><li><img src="" width="30px"><span>Geek_7593a0</span> 👍（0） 💬（8）<div>问，这样的场景用ai对比传统方案的优势在哪里</div>2024-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（3）<div>感觉提示不写清楚的话，chatgpt在选择是否调用tools、以及调用哪个tool上还有点随缘。所以才会有强制使用某个tool或function的选项来兜底</div>2024-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/5c/c9/f1b053f2.jpg" width="30px"><span>Family mission</span> 👍（0） 💬（0）<div>如何进入交流群啊，分享下链接或二维码</div>2025-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/e9/f43781b3.jpg" width="30px"><span>Sandy</span> 👍（0） 💬（0）<div>在run Cart_Price_Finally.py 脚本中 出现items的中文名称乱码 这样结果也就不正确。怎么解决？</div>2024-07-16</li><br/>
</ul>