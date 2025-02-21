你好，我是叶伟民。

上一节课我们所看到的对话模式返回的结果是人类语言（assistant的部分）。这会带来一个问题，就是程序不能识别这种语言，程序只能够识别结构化数据。

那什么是结构化数据呢？布尔值、整数、浮点数、数组、json等格式的数据就是结构化数据。人类语言就是非结构化数据。

除了这个问题之外，还有一个问题是AI只能返回一个结果，不能返回多个结果。而我们的MIS系统，特别是查询部分的代码，如果需要按照多个条件查询，肯定是要输入多个参数的。那么我们如何处理这种情况呢？

其实这两个问题都涉及同一个基础概念，就是让AI返回结构化数据，这也是我们今天课程的主题。

## 让AI返回结构化数据

我们由易到难，从最简单的返回布尔值开始。

### 返回布尔值

当我们需要询问大模型一个问题是对是错，例如询问大模型：**老婆饼和老婆是不是同一类东西？** 那么大模型很可能会回答：不是，老婆饼和老婆不是同一类东西。

很显然，程序（例如我们的MIS系统）是无法识别以上回答的。因此我们就需要大模型返回一个布尔值结果，这样程序才能理解。

那么如何实现呢？我们可以这样设置对话模式里面user角色的content值。

```python
messages=[
  {"role": "user", "content": f"""
  请以布尔值格式返回答案：老婆饼和老婆是不是同一类东西？  
  """},
  ]
```
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（11） 💬（1）<div>第3讲打卡~

思考题：老师课程中的示例，基本都是在Prompt去做优化，指导LLM生成特定的结构化数据，这种方式在大多数情况下没有问题，但是由于LLM生成的方式本质上是基于概率的，会存在一定的随机性，不一定会完全符合指定的结构。

为了更好地实现格式化输出，可以使用LLM的工具调用(tool-calling&#47;functiom-calling)功能，即在调用LLM的API时，传入可选择的工具列表，并详细描述工具调用参数的格式。这样LLM推理出需要调用工具时，就会生成工具调用的参数，这个参数是完全满足指定的结构(如json)的。通过这种方式，可以让LLM更加稳定地生成结构化数据。目前大多数主流的LLM都支持工具调用功能了。

我在实际的项目中实现过一个基于自然语言的SQL查询代理，就可以利用LLM的tool-calling功能，生成结构化的SQL，并实际执行获取查询结果。感兴趣的同学可以参考我的文章：https:&#47;&#47;blog.csdn.net&#47;weixin_34452850&#47;article&#47;details&#47;141677371 </div>2024-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（3） 💬（1）<div>老师请问这个json schema是否有帮助？
“Introducing Structured Outputs in the API” -- https:&#47;&#47;openai.com&#47;index&#47;introducing-structured-outputs-in-the-api&#47;</div>2024-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c5/76/e269369e.jpg" width="30px"><span>明辰</span> 👍（2） 💬（1）<div>老师我有一个问题请教
我们面对复杂问题的时候，prompt可能会写很长（尤其是增加了例子的情况），那么到线上应用的时候，也是保留完整的prompt嘛，这样把例子放到prompt里是否会增加不必要的成本</div>2024-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b2/8c/662e37fd.jpg" width="30px"><span>Luo</span> 👍（0） 💬（1）<div>我一般在提示词里使用下面的描述：
&quot;&quot;&quot;
输出的格式要求如下：
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing &quot;```json&quot; and &quot;```&quot;:
```json
{
    &quot;content&quot;: &quot;设计的阅读题内容&quot;, &#47;&#47;使用汉语,控制在250个汉字左右
    &quot;theme&quot;: &quot;&quot;,
    &quot;choices&quot;: [{  &#47;&#47;出的3选择题内容
        &quot;question&quot;: &quot;题目内容&quot; &#47;&#47;根据阅读题内容出的单选题, 使用汉字，控制在100个汉字以内
        &quot;options&quot;: [
            &quot;A_option&quot;: &quot;A选项内容&quot;, &#47;&#47;使用汉语,控制在20个汉字以内
            &quot;B_option&quot;: &quot;B选项内容&quot; &#47;&#47;使用汉语,控制在20个汉字以内
            &quot;C_option&quot;: &quot;C选项内容&quot; &#47;&#47;使用汉语,控制在20个汉字以内
            &quot;D_option&quot;: &quot;D选项内容&quot; &#47;&#47;使用汉语,控制在20个汉字以内
            &quot;correct_option&quot;: &quot;该题目的答案选项&quot; &#47;&#47;该题目的正确选项,内容为&#39;A&#39;,&#39;B&#39;,&#39;C&#39;,&#39;D&#39;中的一个
            &quot;correct_option_reason&quot;: &quot;解释答案的原因&quot; &#47;&#47;使用汉语,控制在100个汉字以内

        ]
    }],
    &quot;difficulty&quot;: &quot;设计的阅读理解的难度&quot; &#47;&#47;分&quot;容易&quot;、&quot;中等&quot;、&quot;难&quot;
}
&quot;&quot;&quot;
返回的JSON格式大概是这样的：
&quot;&quot;&quot;
{
	&quot;content&quot;: “content1”,
	&quot;theme&quot;: &quot;聚会和休闲活动&quot;,
	&quot;choices&quot;: [{
			&quot;question&quot;: &quot;小明和朋友们在哪里举行了野餐活动？&quot;,
			&quot;options&quot;: {
				&quot;A_option&quot;: &quot;电影院&quot;,
				&quot;B_option&quot;: &quot;公园&quot;,
				&quot;C_option&quot;: &quot;湖边&quot;,
				&quot;D_option&quot;: &quot;家里&quot;,
				&quot;correct_option&quot;: &quot;B&quot;,
				&quot;correct_option_reason&quot;: &quot;根据阅读内容，小明和朋友们是在公园里举行野餐。&quot;
			}
		},
		{
			&quot;question&quot;: &quot;他们野餐时享受了哪些活动？&quot;,
			&quot;options&quot;: {
				&quot;A_option&quot;: &quot;划船&quot;,
				&quot;B_option&quot;: &quot;看电影&quot;,
				&quot;C_option&quot;: &quot;品尝美食和聊天&quot;,
				&quot;D_option&quot;: &quot;参加音乐会&quot;,
				&quot;correct_option&quot;: &quot;C&quot;,
				&quot;correct_option_reason&quot;: &quot;阅读内容提到他们在野餐时品尝美食并聊天。&quot;
			}
		},
		{
			&quot;question&quot;: &quot;小明和朋友们的聚会在一天中的哪个时间段结束？&quot;,
			&quot;options&quot;: {
				&quot;A_option&quot;: &quot;中午&quot;,
				&quot;B_option&quot;: &quot;傍晚&quot;,
				&quot;C_option&quot;: &quot;晚上&quot;,
				&quot;D_option&quot;: &quot;早晨&quot;,
				&quot;correct_option&quot;: &quot;B&quot;,
				&quot;correct_option_reason&quot;: &quot;根据阅读内容，他们傍晚时分去电影院观看电影，说明聚会在傍晚结束。&quot;
			}
		}
	],
	&quot;difficulty&quot;: &quot;中等&quot;
}
&quot;&quot;&quot;</div>2024-10-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>更改 prompt</div>2024-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b2/8c/662e37fd.jpg" width="30px"><span>Luo</span> 👍（1） 💬（0）<div>我一般在提示词里使用下面的描述：
&quot;&quot;&quot;
输出的格式要求如下：
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing &quot;```json&quot; and &quot;```&quot;:
```json
{
    &quot;content&quot;: &quot;设计的阅读题内容&quot;, &#47;&#47;使用汉语,控制在250个汉字左右
    &quot;theme&quot;: &quot;&quot;,
    &quot;choices&quot;: [{  &#47;&#47;出的3选择题内容
        &quot;question&quot;: &quot;题目内容&quot; &#47;&#47;根据阅读题内容出的单选题, 使用汉字，控制在100个汉字以内
        &quot;options&quot;: [
            &quot;A_option&quot;: &quot;A选项内容&quot;, &#47;&#47;使用汉语,控制在20个汉字以内
            &quot;B_option&quot;: &quot;B选项内容&quot; &#47;&#47;使用汉语,控制在20个汉字以内
            &quot;C_option&quot;: &quot;C选项内容&quot; &#47;&#47;使用汉语,控制在20个汉字以内
            &quot;D_option&quot;: &quot;D选项内容&quot; &#47;&#47;使用汉语,控制在20个汉字以内
            &quot;correct_option&quot;: &quot;该题目的答案选项&quot; &#47;&#47;该题目的正确选项,内容为&#39;A&#39;,&#39;B&#39;,&#39;C&#39;,&#39;D&#39;中的一个
            &quot;correct_option_reason&quot;: &quot;解释答案的原因&quot; &#47;&#47;使用汉语,控制在100个汉字以内

        ]
    }],
    &quot;difficulty&quot;: &quot;设计的阅读理解的难度&quot; &#47;&#47;分&quot;容易&quot;、&quot;中等&quot;、&quot;难&quot;
}
&quot;&quot;&quot;
返回的JSON格式大概是这样的：
&quot;&quot;&quot;
{
	&quot;content&quot;: “content1”,
	&quot;theme&quot;: &quot;聚会和休闲活动&quot;,
	&quot;choices&quot;: [{
			&quot;question&quot;: &quot;小明和朋友们在哪里举行了野餐活动？&quot;,
			&quot;options&quot;: {
				&quot;A_option&quot;: &quot;电影院&quot;,
				&quot;B_option&quot;: &quot;公园&quot;,
				&quot;C_option&quot;: &quot;湖边&quot;,
				&quot;D_option&quot;: &quot;家里&quot;,
				&quot;correct_option&quot;: &quot;B&quot;,
				&quot;correct_option_reason&quot;: &quot;根据阅读内容，小明和朋友们是在公园里举行野餐。&quot;
			}
		},
		{
			&quot;question&quot;: &quot;他们野餐时享受了哪些活动？&quot;,
			&quot;options&quot;: {
				&quot;A_option&quot;: &quot;划船&quot;,
				&quot;B_option&quot;: &quot;看电影&quot;,
				&quot;C_option&quot;: &quot;品尝美食和聊天&quot;,
				&quot;D_option&quot;: &quot;参加音乐会&quot;,
				&quot;correct_option&quot;: &quot;C&quot;,
				&quot;correct_option_reason&quot;: &quot;阅读内容提到他们在野餐时品尝美食并聊天。&quot;
			}
		},
		{
			&quot;question&quot;: &quot;小明和朋友们的聚会在一天中的哪个时间段结束？&quot;,
			&quot;options&quot;: {
				&quot;A_option&quot;: &quot;中午&quot;,
				&quot;B_option&quot;: &quot;傍晚&quot;,
				&quot;C_option&quot;: &quot;晚上&quot;,
				&quot;D_option&quot;: &quot;早晨&quot;,
				&quot;correct_option&quot;: &quot;B&quot;,
				&quot;correct_option_reason&quot;: &quot;根据阅读内容，他们傍晚时分去电影院观看电影，说明聚会在傍晚结束。&quot;
			}
		}
	],
	&quot;difficulty&quot;: &quot;中等&quot;
}
&quot;&quot;&quot;</div>2024-10-15</li><br/><li><img src="" width="30px"><span>Geek_fbf3a3</span> 👍（0） 💬（0）<div>学习到了，比如：LLM的工具调用(tool-calling&#47;functiom-calling)功能，以为数据结构化是个很简单的问题，没想到还有那么多的门道</div>2024-11-05</li><br/>
</ul>