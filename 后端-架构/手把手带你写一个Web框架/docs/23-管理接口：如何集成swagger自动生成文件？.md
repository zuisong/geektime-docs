你好，我是轩脉刃。

不管你是前端页面开发，还是后端服务开发，你一定经历过前后端联调的场景，前后端联调最痛苦的事情，莫过于没有完善的接口文档、没有可以调用调试的接口返回值了，所以一般都会采用形如Postman这样的第三方工具，来进行接口的调用和联调。

但是这一节课，我们要做的事情，就是为自己的Web应用集成swagger，使用swagger自动生成一个可以查看接口、可以调用执行的页面。

### swagger

说到swagger，可能有的同学还比较陌生，我来简要介绍一下。swagger框架在2009年启动，之前是Reverb公司内部开发的一个项目，他们的工程师在与第三方调试REST接口的过程中，为了解决大量的接口与文档问题，就设计了swagger这个项目。

项目最终成型的方案是，先设计一个JSON规则，开发工程师把所有服务接口按照这种规则来写成一个JSON文件，**这个JSON文件可以直接生成一个交互式UI，可以提供调用者查看、调用调试**。

swagger的应用是非常广泛的。非常多的开源项目在提供对外接口的时候都使用swagger来进行描述。比如目前最火的Kubernetes项目，每次在发布版本的时候，都会在项目根目录上，带上符合swagger规则的[JSON文件](https://github.com/kubernetes/kubernetes/blob/master/api/openapi-spec/swagger.json)，用来向使用者提供内部接口。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_62f18d</span> 👍（1） 💬（1）<div>您好，请问swagger的注释中的description.markdown怎么使用</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（0）<div>swag v1.7.9及后续版本gen.Config,需要添加 OutputTypes:   []string{&quot;yaml&quot;, &quot;json&quot;, &quot;go&quot;} , 指定生成文件的类型。</div>2024-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（0）<div>go swagger 可以换主题吗，默认主题太难用了。</div>2023-08-14</li><br/>
</ul>