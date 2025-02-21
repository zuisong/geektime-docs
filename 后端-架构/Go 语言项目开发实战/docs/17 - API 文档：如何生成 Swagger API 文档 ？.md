你好，我是孔令飞。

作为一名开发者，我们通常讨厌编写文档，因为这是一件重复和缺乏乐趣的事情。但是在开发过程中，又有一些文档是我们必须要编写的，比如API文档。

一个企业级的Go后端项目，通常也会有个配套的前端。为了加快研发进度，通常是后端和前端并行开发，这就需要后端开发者在开发后端代码之前，先设计好API接口，提供给前端。所以在设计阶段，我们就需要生成API接口文档。

一个好的API文档，可以减少用户上手的复杂度，也意味着更容易留住用户。好的API文档也可以减少沟通成本，帮助开发者更好地理解API的调用方式，从而节省时间，提高开发效率。这时候，我们一定希望有一个工具能够帮我们自动生成API文档，解放我们的双手。Swagger就是这么一个工具，可以帮助我们**生成易于共享且具有足够描述性的API文档**。

接下来，我们就来看下，如何使用Swagger生成API文档。

## Swagger介绍

Swagger是一套围绕OpenAPI规范构建的开源工具，可以设计、构建、编写和使用REST API。Swagger包含很多工具，其中主要的Swagger工具包括：

- **Swagger编辑器：**基于浏览器的编辑器，可以在其中编写OpenAPI规范，并实时预览API文档。[https://editor.swagger.io](https://editor.swagger.io/) 就是一个Swagger编辑器，你可以尝试在其中编辑和预览API文档。
- **Swagger UI：**将OpenAPI 规范呈现为交互式API文档，并可以在浏览器中尝试API调用。
- **Swagger Codegen：**根据OpenAPI规范，生成服务器存根和客户端代码库，目前已涵盖了40多种语言。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/75/30/c5b7b15d.jpg" width="30px"><span>遇见@z</span> 👍（7） 💬（4）<div>看着好麻烦，我们公司自己写的框架通过扫描ast语法树生成openapi，代码即文档</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/53/c93b8110.jpg" width="30px"><span>daz2yy</span> 👍（7） 💬（5）<div>一点想法，在小团队里，其实也没那么规范，能简单就简单点，目前用的是 Postman 生成的文档，考虑的点：
1. 一方面程序员自己调试接口必然会用到接口调用工具，postman大家也比较熟悉；
2. 另一方面开发完之后，它能直接生成在线文档，不用重新去定义文档使用的 API 的字段、结构体等，感觉会方便很多，而且能实时同步修改（接口有变动可以同步反映到文档上，不需要二次修改 api 文档，减少人为的错误）

请教下老师对两者的看法，主要是我觉得写 swagger 接口注释这个工作比较繁琐，另外需要特意去维护它，容易出现代码改了但是文档未改的情况；或者说老师这边有什么好的实践经验。

FYI：Makefile 说明那里有个 Models 写成了 Modles</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（4） 💬（1）<div>思考题可能的好处：1. 方便和项目根路径下的帮助文档目录docs做区分；2. 路径层次清晰辨认功能；3. 方便启api文档的http服务？</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/91/b1/fb117c21.jpg" width="30px"><span>先听</span> 👍（2） 💬（2）<div>swagger可以通过扫描源码生成文档。但是后端往往需要在编码之前就提供接口文档。貌似有些矛盾</div>2021-07-21</li><br/><li><img src="" width="30px"><span>Geek_5baa01</span> 👍（1） 💬（1）<div>需求确认了后,后台首先应该写swagger 提供给前端开发, 相互不影响,   按照你这个套路, 是不是得后端开发完了在让前端搞</div>2022-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/7e/ebc28e10.jpg" width="30px"><span>NULL</span> 👍（1） 💬（1）<div>&quot;目前最新的 OpenAPI 规范是OpenAPI 3.0（也就是 Swagger 2.0 规范）&quot;

这里错了啊, 现在最新的规范是2021年2月16日发布的 OpenAPI 3.1.0, 而且 OpenAPI 3.0 != Swagger 2.0

OpenAPI有三个版本 Swagger 2.0, OpenAPI 3.0.x, OpenAPI 3.1.0
详见:
https:&#47;&#47;swagger.io&#47;blog&#47;news&#47;whats-new-in-openapi-3-0&#47;
https:&#47;&#47;www.openapis.org&#47;blog&#47;2021&#47;02&#47;16&#47;migrating-from-openapi-3-0-to-3-1-0</div>2022-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/fb/2f/ae053a45.jpg" width="30px"><span>咖梵冰雨</span> 👍（1） 💬（2）<div>这个demo运行会有跨域问题？这个本地咋解决，我gin加了中间件运行跨域好像不管用</div>2021-11-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（1） 💬（2）<div>swagger文档可以手动编写，也可以通过工具解析注释生成文档。
说明关于swagger 文档产生了2中开发模式：
1. 手动编写swagger 文档，可以通过文档生成代码
2. 先编写代码，添加swagger规范的注释，生成文档。
请问一般开发中，使用哪种swagger模式？（我看kubernetes中的api doc不是通过代码生成的）</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7b/c5/35f92dad.jpg" width="30px"><span>Jone_乔泓恺</span> 👍（0） 💬（1）<div>swagger generate 命令会找到 main 函数，然后遍历所有的源代码，解析源码中与 Swagger 相关的注释，然后自动生成 swagger.json&#47;swagger.yaml 文件；

version: v0.29.0 不适用了吧？</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/8e/62/5cb377fd.jpg" width="30px"><span>yangchnet</span> 👍（0） 💬（1）<div>请问老师怎么看待“protoc-gen-openapiv2”这个工具，使用proto文件定义了接口出入参后可以直接生成swagger文档，不用再手动去编写。是不是比文中这种去手动编写的方便一点呢。</div>2022-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（1）<div>总结：
1. 什么是 swagger? 它和OpenAPI之间是什么关系？如何编写swagger.yaml? 
2. go-swagger 是一个非常流行的工具。你可以生成swagger.yaml，检查 swagger.yaml，生成客户端代码，生成服务端代码，启动HTTP服务器访问API文档
3. diff 命令可以检查两个yaml文件的内容，从而判断出，API文档是否引入了Break Change。</div>2021-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（0） 💬（1）<div>文档版本比较多时（有的接口有3-4个版本），放在一个swagger文档下是否还需要加版本以区分呢？</div>2021-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/46/717d5cb9.jpg" width="30px"><span>惜心（伟祺）</span> 👍（15） 💬（0）<div>老师厉害 把软件工程方方面面通过一个项目讲了
相信看完这个再去看大型开源项目 比如kubernates应该会容易很多 
聚焦在论文核心实现部分就可以
知道一个大项目是怎么造出来的 包括什么 再去学自然容易多了</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/79/9b/66570110.jpg" width="30px"><span>土拨鼠</span> 👍（2） 💬（1）<div>目前前后端就是通过swagger沟通，后端在开发之前先定义好swagger的 api.json，这样前后端就可以并行开发了，而且减少了很多扯皮</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（2） 💬（2）<div>用go-swagger生成swagger格式的API文档。
API文档最大的一个痛点是更新不及时，使用自动生成工具可以降低及时更新文档的阻力，让文档实时更新变得更容易操作。使用更先进的工具，对抗人的惰性。</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/08/a1/9166c1d8.jpg" width="30px"><span>Joker</span> 👍（1） 💬（0）<div>请问老师，如何将swagger 里面的 静态资源更改为国内镜像，比如：
https:&#47;&#47;fonts.googleapis.com&#47;css</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e3/3b/3125ed1d.jpg" width="30px"><span>目标</span> 👍（0） 💬（0）<div>感觉swag更好用。不用手写。star 也更多。</div>2024-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/93/2a/08675e68.jpg" width="30px"><span>__PlasticMan</span> 👍（0） 💬（0）<div>二进制安装go-swagger 0.30.5版本生成yaml时，不能生成definitions字段，为api包的User添加注解`swagger:model`后，执行`swagger generate spec -o swagger.yaml --scan-models`命令可以生成definitions字段，但是不包含User结构体的属性信息，go-swagger的issue中也提到了这个问题（https:&#47;&#47;github.com&#47;go-swagger&#47;go-swagger&#47;issues&#47;2860），并且从另一个（https:&#47;&#47;github.com&#47;go-swagger&#47;go-swagger&#47;issues&#47;2841）issue看，这不是偶然问题。

综合答复来看，问题出现在二进制文件上，具体表现包含但不限于以下这种：
1. 0.30.5（23年6月发布）二进制安装有问题；
2. 看issue，0.30.0-0.30.2正常；
3. 使用go install编译安装0.30.5测试没有问题（也是在issue里面看维护者说的）；
综上，感觉这个项目有点不靠谱，拿golangci-lint说，在官方文档中指出不建议编译安装，但是我二进制安装后发现还是有些问题，看到老师也是源码安装的，难道这是go领域的一种奇怪约定吗？</div>2023-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e2/c7/3e1d396e.jpg" width="30px"><span>oneWalker</span> 👍（0） 💬（0）<div>通过swagger反向生成的代码后，运行swagger文档时，运行的是方向运行swagger文档，运行的是生成的项目
</div>2021-07-28</li><br/>
</ul>