你好，我是朱涛。不知不觉间，咱们的课程就已经进行一半了，我们已经学完很多内容：

- 基础篇，我们学完了所有Kotlin基础语法和重要特性。
- 加餐篇，我们学习了Kotlin编程的5大编程思维：函数式思维、表达式思维、不变性思维、空安全思维、协程思维。
- 协程篇，我们也已经学完了所有基础的协程概念。

所以现在，是时候来一次阶段性的验收了。这次，我们一起来做一个**图片处理程序**，来考察一下自己对于Kotlin编程知识的理解和应用掌握情况。初始化工程的代码在这里[GitHub](https://github.com/chaxiu/ImageProcessor.git)，你可以像往常那样，将其clone下来，然后用IntelliJ打开即可。

我们仍然会分为两个版本1.0、2.0，不过，这一次要轮到你亲自动手写代码了！

## 1.0版本：处理本地图片

当你将初始化工程打开以后，你会发现“src/main/resources/images/”这个目录下有一张图片：android.png，它就是我们要处理的图片对象。

![图片](https://static001.geekbang.org/resource/image/0d/64/0de4da2977353d97631d88531feff464.png?wh=1817x704)

一般来说，我们想要处理图片，会第一时间想到Photoshop，但其实简单的图片处理任务，我们完全可以通过代码来实现，比如图片横向翻转、图片纵向翻转、图片裁切。

![图片](https://static001.geekbang.org/resource/image/45/c6/456e395f69c12b20e095959046fccac6.png?wh=1128x424)

关于图片的底层定义，Java SDK已经提供了很好的支持，我们在Kotlin代码当中可以直接使用相关的类。为了防止你对JDK不熟悉，我在初始化工程当中，已经为你做好了前期准备工作：
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/8f/d0874a01.jpg" width="30px"><span>曾帅</span> 👍（4） 💬（1）<div>git clone 之后，打开编译就报错，MultipleCompilationErrorsException 。把 gradle&#47;wrapper&#47;gradle-wrapper.properties 里面的 7.1 版本改成 7.2 之后重新编译就可以了。
有同样问题的同学可以参考一下。</div>2022-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/a7/ac23f5a6.jpg" width="30px"><span>better</span> 👍（3） 💬（1）<div>&#47;&#47; Image 添加方法，同时 去掉 pixels 的 private
fun getHorArray(x: Int): Array&lt;Color&gt; {
        return pixels[x]
}

&#47;&#47;&#47;&#47; 
fun Image.flipHorizontal(): Image {
    for (i in (0 until this.height())) {
        this.getHorArray(i).reverse()
    }
    return this
}

fun Image.flipVertical(): Image {
    this.pixels.reverse()
    return this
}

fun Image.crop(startY: Int, startX: Int, width: Int, height: Int): Image {
    return Array(width - startY) { y -&gt;
        Array(height - startX) { x -&gt;
            Color(this.getPixel(x, y).rgb)
        }
    }.let {
        Image(it)
    }
}
</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（1） 💬（1）<div>fun main() = runBlocking {
    File(BASE_PATH).mkdirs()
    downloadFile(URL, getPathFile(&quot;origin&quot;))
        .loadImage()
        .also { it.flipVertical().writeToFile(getPathFile(&quot;vertical&quot;)) }
        .also { it.flipHorizontal().writeToFile(getPathFile(&quot;horizontal&quot;)) }
        .also { it.crop(0, 0, 100, 50).writeToFile(getPathFile(&quot;crop&quot;)) }
    delay(10L)
}</div>2022-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/06/e5/51ef9735.jpg" width="30px"><span>A Lonely Cat</span> 👍（1） 💬（1）<div>图片下载功能

private val client = OkHttpClient.Builder()
    .build()

&#47;**
 * 挂起函数，以http的方式下载图片，保存到本地
 *&#47;
suspend fun downloadImage(url: String, outputFile: File): Boolean = suspendCoroutine { con -&gt;
    val request = Request.Builder()
        .url(url)
        .get()
        .build()
    client.newCall(request)
        .enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
                con.resume(false)
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    response.body?.bytes()?.let {
                        outputFile.writeBytes(it)
                    }
                    con.resume(true)
                } else {
                    con.resume(false)
                }
            }
        })
}

fun main() = runBlocking {
    val url = &quot;http:&#47;&#47;img.netbian.com&#47;file&#47;2020&#47;1202&#47;smallaaa773e8cc9729977037e80b19f955891606922519.jpg&quot;
    val file = File(&quot;${BASE_PATH}wallpaper.png&quot;)
    val success = downloadImage(url, file)
    println(&quot;Download file status is success：$success&quot;)
}</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e5/e1/a5064f88.jpg" width="30px"><span>Geek_Adr</span> 👍（0） 💬（1）<div>&#47;&#47; 先交作业，后看参考实现
&#47;&#47; 图片处理 单测Case 较难实现，偷懒写本地肉眼看

&#47;**
 * 写到本地，方便可看效果
 *&#47;
fun Image.writeJPEG(outputFile: File): Boolean =
    ImageIO.write(BufferedImage(width(), height(), BufferedImage.TYPE_INT_RGB).apply {
        repeat(height) { y -&gt;
            repeat(width) { x -&gt;
                setRGB(x, y, getPixel(y, x).rgb)
            }
        }
    }, &quot;JPEG&quot;, outputFile)

&#47;**
 * 图片裁切
 *&#47;
fun Image.crop(startY: Int, startX: Int, width: Int, height: Int): Image =
    Array(height) { y -&gt;
        Array(width) { x -&gt;
            getPixel(y + startY, x + startX)
        }
    }.let { Image(it) }

&#47;**
 * 横向翻转图片
 *&#47;
fun Image.flipHorizontal(): Image =
    Array(height()) { y -&gt;
        Array(width()) { x -&gt;
            getPixel(y, width() - x - 1)
        }
    }.let { Image(it) }

&#47;**
 * 纵向翻转图片
 *&#47;
fun Image.flipVertical(): Image =
    Array(height()) { y -&gt;
        Array(width()) { x -&gt;
            getPixel(height() - y - 1, x)
        }
    }.let { Image(it) }

&#47;**
 * 挂起函数，以http的方式下载图片，保存到本地
 *&#47;
suspend fun downloadImage(url: String, outputFile: File): Boolean =
    withContext(Dispatchers.IO) {
        OkHttpClient.Builder().build().run {
            newCall(Request.Builder().apply {
                url(url)
                get()
            }.build()).execute().run {
                if (!isSuccessful) {
                    return@run false
                }
                return@run body?.byteStream()?.source()?.let { outputFile.sink().buffer().writeAll(it) &gt; 0 } ?: false
            }
        }
    }
</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（0） 💬（1）<div>&#47;**
 * 挂起函数，以http的方式下载图片，保存到本地
 *&#47;
suspend fun downloadImage(url: String, outputFile: File) = withContext(Dispatchers.IO) {
    val client = OkHttpClient()
    val request = Request.Builder()
        .url(url)
        .build()
    val response = client
        .newCall(request)
        .execute()
    var size = 0L
    response.body?.byteStream()?.readAllBytes()?.let { bytes -&gt;
        outputFile.writeBytes(bytes)
        size = bytes.size.toLong()
    }
    if (size == response.headersContentLength()) {
        return@withContext true
    }
    return@withContext false
}

&#47;**
 * 主函数
 *&#47;
fun main() = runBlocking {
    val url = &quot;https:&#47;&#47;raw.githubusercontent.com&#47;chaxiu&#47;ImageProcessor&#47;main&#47;src&#47;main&#47;resources&#47;images&#47;android.png&quot;
    val path = &quot;.&#47;download.png&quot;

    val success = downloadImage(url, File(path))
    println(success)

    val image = loadImage(File(path))
    println(&quot;Width = ${image.width()};Height = ${image.height()}&quot;)
}

看到有同学使用 suspendCoroutine 函数处理，不知道和我这个方法比较有什么区别 👀</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1b/f9/018197f1.jpg" width="30px"><span>小江爱学术</span> 👍（0） 💬（0）<div>当然是要把第一部分和第二部分的内容结合起来啦：
首先自己创建一个获取图片的接口：
    @GetMapping(&quot;&#47;{name}&quot;, produces = [MediaType.IMAGE_JPEG_VALUE])
    fun picture(@PathVariable name: String): ByteArray {
        return pictureService.getPicture(name)
    }

然后用之前的KtCall发请求：
    @GET(&quot;&#47;picture&#47;mountain&quot;)
    fun image(): KtCall&lt;ByteArray&gt;

    suspend fun downloadImage() = runBlocking {
        val deferred = async {
            KtHttpProxy.create(ApiService::class.java)
                .image()
                .await()
        }
        println(&quot;still in progress&quot;)
        return@runBlocking deferred.await()
    }</div>2023-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/01/2885812b.jpg" width="30px"><span>Michael</span> 👍（0） 💬（0）<div>使用系统自带的 api 下载文件
suspend fun downloadImage(url: String, outputFile: File): Boolean =
    withContext(Dispatchers.IO) {
      kotlin.runCatching {
        URL(url).openStream().use {
          outputFile.writeBytes(it.readAllBytes())
        }
      }
    }.isSuccess</div>2022-06-29</li><br/>
</ul>