你好，我是黄鸿波。

在前面的课程中，我们已经对推荐系统的基本架构以及各个模块有了一个比较清晰的认识，也能够自己动手处理在推荐系统中用到的各种数据和简单的画像系统了。通过上一章的学习，我们也能够使用一些简单的基于规则的方法找到用户喜欢的内容。有了这些储备，从本章起，我们就可以开始搭建一个简单的推荐系统服务了。

这节课我们先来用Flask搭建一个简单的推荐服务。我们会深入地认识Flask，学习如何使用Flask框架来搭建一个简单的Web服务。我们会用它提供一个POST接口，再用相应的工具进行调用。

## **我们可以用Flask来做什么**

要搭建一个推荐系统，我们首先要对Web服务有一个简单的了解。

我们上线一个推荐系统，最终的目的就是给到用户访问，所以我们首先需要一个载体，比如网页、App等。这些载体会通过Web服务调用服务端提供的接口，然后服务端再去请求模型，并根据输入的特征将模型的结果返回并进行组装，拿到相应的推荐数据后再返回给用户，形成一个完整的流程。

我们可以发现，Web服务在整个推荐系统中起到了一个承上启下的作用，它相当于是用户与推荐系统的一个中间件，而这个中间件对于一个完整的企业级推荐系统来说是至关重要的。所以，**对于现阶段的我们来说，最重要的一件事就是搭建一套Web服务。**
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/EaBxhibOicZe9L7z2icbU4W462l543drFWYqibqczTicj4Msyb2g9pDSGmFTiafW9jibwib7jG6hpAdPMcCowdCiaxHaOdA/132" width="30px"><span>Geek_ccc0fd</span> 👍（4） 💬（1）<div>直接request.get_json()就可以了，不需要get_data再json.loads一遍：

@app.route(&#39;&#47;sum&#39;, methods=[&quot;POST&quot;])
def sum():
    try:
        if request.method == &quot;POST&quot;:
            req_json = request.get_json()
            a = req_json[&#39;a&#39;]
            b = req_json[&#39;b&#39;]
            return jsonify({&#39;code&#39;: 200, &#39;msg&#39;: &#39;请求成功&#39;, &#39;data&#39;: a+b})
    except:
        return jsonify({&#39;code&#39;: &#39;500&#39;, &#39;msg&#39;: &#39;error&#39;})</div>2023-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/1d/10/a73d63ba.jpg" width="30px"><span>欢少の不忘初心</span> 👍（0） 💬（1）<div>最近刚学了Go，拿Go来练练手。老师Go语言  Gin框架也可以吧</div>2023-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>python适合用来开发中型、大型网站吗？ Python是不是难以处理高并发？</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/43/03/51f377fb.jpg" width="30px"><span>海欧</span> 👍（0） 💬（1）<div>这个flask结合docker可以做到多大的并发，有什么实现技巧吗</div>2023-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/f3/791d0f5e.jpg" width="30px"><span>一叶浮萍</span> 👍（0） 💬（1）<div>老师, 一般公司高并发的请求都是后端统一来处理的, 他们调用推荐系统的话一般是grpc吗, 还是其他什么方式?</div>2023-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（2） 💬（0）<div>Github作业地址：https:&#47;&#47;github.com&#47;gacdu&#47;recommendation-service</div>2023-05-17</li><br/>
</ul>