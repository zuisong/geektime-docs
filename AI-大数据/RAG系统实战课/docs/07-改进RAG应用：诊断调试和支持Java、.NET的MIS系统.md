你好，我是叶伟民。

上一节课我们完成了实战案例1的代码。然而这只是个demo，如果要支持更多的用例，支持更多的模块，我们需要添加更多选项序号和提示。

但是这又会引起一个新问题，用户在用我们系统的时候，你并没有在旁边看着，你怎么知道如何添加这些内容呢？你又怎么知道如何改进呢？

这就是我们今天要讨论的主题——诊断与调试。我们先开始第一步，查看用户的提问。

## 查看用户的提问

前面我们已经把对话记录保存在数据库里面了。现在，我们只需要在管理员界面添加相关模块就可以查看它们了。

### 启用管理员界面

首先，我们需要启用管理员界面。

我们打开**实战案例1\\改造前\\mysite\\urls.py** 文件。然后把第7行的注释取消掉。

```python
from django.contrib import admin
from django.urls import include, path

app_name = "home"
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
]
```

然后重新运行，打开浏览器，导航到 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)。将会出现以下界面。  
![](https://static001.geekbang.org/resource/image/af/5e/af5e0cf631fa0218145081yyae66f25e.jpg?wh=1990x715)
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3b/d0/e5/0a3ee17c.jpg" width="30px"><span>kevin</span> 👍（1） 💬（1）<div>本章节讲了如何用自然语言替代以往的查询操作，从而达到节省操作时间提升工作效率，优化用户体验。但是为什么很多工具APP，比如美团订酒店为何没有采用这种方式呢，还是继续使用原来按键的方式。是不是由于比较复杂的操作，通过语音说出来，AI再去理解很容易出错不到位，很容易导致查询不准确。如果一个MIS的查询条件很多，或者保存记录很多字段，AI万一哪个字段搞错了，这种问题要如何解决呢？</div>2024-10-19</li><br/><li><img src="" width="30px"><span>Geek_fbf3a3</span> 👍（0） 💬（0）<div>打卡：除字典外另外一个方式，就是让把数据库字典输入大模型，让大模型来转换中文-&gt;英文查询</div>2024-11-24</li><br/><li><img src="" width="30px"><span>Geek_fbf3a3</span> 👍（0） 💬（0）<div>学习打卡：可以增加一个字典表（从配置文件获取），将中文转换为英文</div>2024-11-06</li><br/>
</ul>