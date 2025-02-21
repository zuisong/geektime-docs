你好，我是雪飞。

要介绍 Kubernetes 技术，我们要从容器技术开始讲起。因为容器技术在云原生技术体系中具有革命性的意义，它可以将应用与底层运行环境进行解耦，让应用能以敏捷的、可扩展的、可复制的方式发布在云上，发挥出云原生的最大能力。

目前，容器技术已经成为云原生应用分发和部署的标准技术，它可以帮我们大大简化繁琐的发布部署环节，提升5~10倍的交付效率。同时，通过 Kubernetes 容器编排来部署大规模微服务应用，已经是互联网和传统行业数字化系统的标配。所以，容器技术是我们学习 Kubernetes 需要打好的第一块基石。

今天这节课，我会带你了解容器技术的相关概念，以及如何使用容器。我希望你学完这节课后能自己动手试一试，亲身体验一下容器技术带来的便捷和高效。

## **为什么要使用容器技术？**

首先问你一个问题，你有没有遇到过这种情况：在测试环境正常运行的程序，却在生产环境中出现一些意想不到的问题。产品、测试人员都找你抱怨，但你也很无奈，明明都是一样的代码、一样的环境，为什么表现出来的不一样呢？

然而定位这种问题有时需要花费大量的时间，到头来可能发现只是两个环境的硬件配置、操作系统、环境变量、依赖软件版本等存在一些细小偏差导致的。如果你对此深有感触，那么恭喜你，你已经能够理解为什么要使用容器技术了。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/28/040f6f01.jpg" width="30px"><span>Y</span> 👍（1） 💬（1）<div>docker run -d -p 80:80 httpd
</div>2024-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/86/77/e9f69816.jpg" width="30px"><span>YH</span> 👍（0） 💬（1）<div>docker id注册网页无法打开了</div>2024-07-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/AkcVibvqux0qrKFbV7skQvQfHsl96tu9HTSaromQyzf7OOSacoorSDreBNbwOdlBeOrKr3Alc1zle66wKkibrL5g/132" width="30px"><span>学生监狱</span> 👍（0） 💬（0）<div>企业级的虚拟化，不是这样的层级，它的OS层和hypervisor层是一个层，比如Vmware的Esxi</div>2024-08-13</li><br/>
</ul>