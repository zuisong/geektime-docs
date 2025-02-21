你好，我是康杨。

今天我们一起站在对象创建的视角，看看JVM为我们提供了哪些能力，还有怎么更好的应用这些能力。我们也会聊一下，创建对象需要考虑的因素以及对象创建对对象回收的影响。

首先我们从一个实际的场景开始，假设你是某一个在线阅读网站的程序员，老板安排了一个任务，需要统计在线图书被阅读的次数。你决定采用面向对象的思想来设计，所以第一步你先设计了一个Book对象，它有四个属性，分别是这本书的编号、书名、图书的简介以及这本书被阅读的次数。

```java
public class Book {
    private Long    no;  // 图书的编号
    private String  name = “ default Name ”; //书名
    private String  desc; //图书的简介
    private Long    readedCnt; // 这本书被读的次数
    public Book() {
    }
    public Book(Long no, String name, String desc, Long readedCnt) {
        this.no = no;
        this.name = name;
        this.desc = desc;
        this.readedCnt = readedCnt;
    }
    public Long getNo() {
        return no;
    }
    public String getName() {
        return name;
    }
    public String getDesc() {
        return desc;
    }
    public Long getReadedCnt() {
        return readedCnt;
    }
}
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（1） 💬（1）<div>请教老师一个问题，开启或者关闭对象指针压缩，对象指针和Class指针是不是应该同步开启或关闭压缩。文中举的例子压缩指针的时候是12字节头部+16字节实例数据。未压缩指针的是不是应该16字节头部+32字节实例数据？</div>2023-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（1） 💬（0）<div>优化点：
1、静态工厂方法，通过静态方法返回对象实例，相比于直接调用构造函数，静态工厂方法可以提供更多的灵活性和优化空间。（例：静态工厂方法中使用对象池或缓存来重用对象，避免重复创建）
2、使用对象池或缓存：对于频繁创建和销毁的对象，可以考虑使用对象池或缓存来重用对象，避免重复创建和垃圾回收的开销。（Apache Commons Pool）
3、使用不可变对象，不可变对象是指其状态在创建后不可更改的对象，可以避免线程安全性问题和复制对象的开销。
4、懒初始化，推迟对象初始化的时机，使用的时候初始化。
解耦：
1、工厂模式
2、依赖注入</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/b6/27412d76.jpg" width="30px"><span>sc</span> 👍（0） 💬（0）<div>讲的真清晰</div>2023-09-18</li><br/>
</ul>