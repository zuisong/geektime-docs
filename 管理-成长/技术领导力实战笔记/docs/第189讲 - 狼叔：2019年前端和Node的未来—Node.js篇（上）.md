你好，我是阿里巴巴前端技术专家狼叔，前两篇文章，我分享了大前端的现状和未来，接下来的两篇文章，我将会注重分享一些跟Node.js结合比较密切的点。

## Node.js

Node.js在大前端布局里意义重大，除了基本构建和Web服务外，这里我还想讲2点。首先它打破了原有的前端边界，之前应用开发只分前端和API开发。但通过引入Node.js做BFF这样的API proxy中间层，使得API开发也成了前端的工作范围，让后端同学专注于开发RPC服务，很明显这样明确的分工是极好的。其次，在前端开发过程中，有很多问题不依赖服务器端是做不到的，比如场景的性能优化，在使用React后，导致bundle过大，首屏渲染时间过长，而且存在SEO问题，这时候使用Node.js做SSR就是非常好的。当然，前端开发Node.js还是存在一些成本，要了解运维等，会略微复杂一些，不过也有解决方案，比如Servlerless就可以降级运维成本，又能完成前端开发。直白点讲，在已有Node.js拓展的边界内，降级运维成本，提高开发的灵活性，这一定会是一个大趋势。

2018 年Node.js发展的非常好，InfoQ曾翻译过一篇文章《2018 Node.js 用户调查报告显示社区仍然在快速成长》。2018 年 5 月 31 日，Node.js 基金会发布了2018 年用户调查报告，涵盖了来自 100 多个国家 1600 多名参与者的意见。报告显示，Node.js的使用量仍然在快速增长，超过¾的参与者期望在来年扩展他们的使用场景，另外和2017 年的报告相比，Node 的易学程度有了大幅提升。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erms9qcIFYZ4npgLYPu1QgxQyaXcj64ZBicNVeBRWcYUpCZ9p0BGsrEcX8heibMLCV4Gde4P9pf7PjA/132" width="30px"><span>yanger2004</span> 👍（0） 💬（0）<div>全是干货</div>2021-09-25</li><br/>
</ul>