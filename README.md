## 极客时间文档

极客时间 markdown & pdf 文档

----

* 看 markdown文档，推荐: https://github.com/uaxe/geektime-docs 🌟🌟🌟
* 看 pdf文档，推荐: https://github.com/uaxe/geektime-pdfs 🌟🌟🌟
* 看 音视频，推荐: https://github.com/zkep/my-geektime 🌟🌟🌟🌟🌟

### [全文搜索](https://github.com/uaxe/geektime-docs/blob/master/fultext-search/README.md)
感谢 [KonghaYao](https://github.com/KonghaYao) 全文搜索功能

###  markdown 在线文档

 * [github](https://uaxe.github.io/geektime-docs/) 
 * [netlify](https://geektime-docs.netlify.app/)  

> tips: 在线文档支持 PC 浏览器，也支持移动端浏览器

### 本地部署

#### docker方式
> 该方式实现了服务端代理请求图片，解决裂图，放心使用
```shell
docker run -d -p 8091:8091 --restart always  --name geektime-docs  zkep/geektime-docs
```
浏览器访问：<http://127.0.0.1:8091/>

#### 源码方式
```shell
git clone --single-branch --branch master --depth 1 https://github.com/uaxe/geektime-docs.git

pip install mkdocs-material

cd geektime-docs/后端-架构/说透中台/

mkdocs serve
```

浏览器访问：<http://127.0.0.1:8000/>


#### 本项目markdown文档全部由 [my-geektime](https://github.com/zkep/my-geektime) 生成




#### 贡献代码
欢迎提交PR，修复错误或添加新的文档

欢迎提交Issue，报告错误或建议改进

感谢所有贡献者，以下是他们的名单
[zkep](https://github.com/zkep)
[yywmrz](https://github.com/yywmrz)
[KonghaYao](https://github.com/KonghaYao)
[lrh3321](https://github.com/lrh3321)
[zhyjor](https://github.com/zhyjor)

   





