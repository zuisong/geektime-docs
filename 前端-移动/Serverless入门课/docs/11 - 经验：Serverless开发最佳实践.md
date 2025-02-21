你好，我是秦粤。上节课，我们了解了利用K8s集群的迁移和扩展能力，可以解决云服务商锁定的问题。我们还横向对比了各大云服务商的特点和优势，纵向梳理了云服务商提供的各种服务能力。最后我们可以看到，利用Knative提供的Container Serverless能力，我们可以任意迁移部署我们的应用架构，选择适合我们的云服务商。

但同时我们也发现，FaaS相对于Knative，反而是我们的瓶颈，我们无法平滑地迁移FaaS的函数。云服务商大力发展FaaS，其实部分原因也是看中了FaaS新建立起来的Vendor-lock，因此目前各大运营商都在拼FaaS的体验和生态建设。

那这节课，我们就来看看FaaS是如何解除云服务商锁定的吧。但在正式开始之前呢，我们先得了解一些FaaS的使用场景，以免一些同学误会，要是你的实践是为了Serverless而去Serverless，那就不好了，我们还是应该从技术应用的角度出发。

## FaaS场景

我从[\[第5课\]](https://time.geekbang.org/column/article/229905) 开始就在讲FaaS和BaaS的底层实现原理Container Serverless，是希望通过底层实现原理，帮助你更好地掌握Serverless的思想。但在日常工作中，使用Serverless，只需要借助云服务商提供的Serverless化的FaaS和BaaS服务就可以了。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（2）<div>今天的例子部署的比较顺利.
只修改了f.yml和src&#47;config&#47;config.default.ts.

使用npm install安装依赖后
`f invoke -p`就可以本地调试了
`f deploy`就可以部署上阿里云了

这次部署后,只有一个函数,但是代码中的函数却都可以成功调用.
应该是`aggregation`的功劳吧.

-------
之前尝试&lt;阿里云开发平台&gt;时,自动生成过一个项目,也是跟老师这次的代码结构类似,也是有f.yml文件.
好像就是用的`Midway FaaS`框架

不过这次想用它部署老师的项目就遇到了问题.
编辑器会提示:VS Code 的 tsserver 已被其他应用程序(例如运行异常的病毒检测工具)删除。请重新安装 VS Code。
我也不会修,暂时在钉钉群中询问了也没有答复.

------
老师这一会node.js,一会TypeScript的,作为后端开发的我,比较懵.
只会简单的部署,代码不会改也不会调.
</div>2020-05-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJnj0bL0YdiawRe9rauOCiczLlPuM9JdmJhFzGNMq4ILic4FGOzGfibZHLcfiblYMPA8AevjVpETYlTTHg/132" width="30px"><span>Geek_a7fcb9</span> 👍（0） 💬（1）<div>老师，看完了您的文章。有2个问题想请教一下。
问题一：
【k8s主要是对容器的编排，knative是一种基于k8s的serverless平台的实现，相比较于k8s提供了灰度发布、自动扩缩容之类的功能。】请问这样理解对吗？
-------------------------------------------------------------------------
问题二：
【Serverless 有多种实现方法，比如：Serverless Framework，Malagu，Midway FaaS。上边三者类似knative可以帮助我们搭建serverless平台。而“阿里云开发平台”是已经搭建好的serverless平台。】请问这样理解对吗</div>2021-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/17/0bb45a21.jpg" width="30px"><span>peter</span> 👍（2） 💬（0）<div>挺好的，不错！</div>2020-05-18</li><br/>
</ul>