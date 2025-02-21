你好，我是康杨。今天我们来重新审视一下JVM中的变量。

变量是我们操作JVM的最小单元，它在日常工作中很容易被忽略掉，而实际上它对内存管理和垃圾回收机制的影响很大。

深入地了解变量有助于我们理解强引用、弱引用和虚引用之间的区别以及对对象回收的影响，帮助我们更加灵活地使用Java内存模型，避免一些特殊情况下的内存泄漏和性能问题。而学会从不同的维度去认识变量，也是我们写出高性能的程序的基础。

## JVM中的变量

这节课我们将通过一个实际的例子去了解JVM中的变量以及变量中的类型。

### 静态类型和实际类型

```java
Food food = new Fruit();
```

作为一个变量food，它有一个静态类型和一个实际类型。静态类型是指变量最初被定义时的类型，而实际类型则是指变量所引用的对象的类型。当变量指向一个子类对象时，就有了多态的能力。让我们先看一下下面这段代码。

```java
class Food {
    public void eat() {
        System.out.println("Eat some food");
    }
}
class Fruit extends Food {
    @Override
    public void eat() {
        System.out.println("Eat some fruits");
    }
    public void peel() {
        System.out.println("Peel the fruit");
    }
}
class Main {
    public static void main(String[] args) {
        Food food = new Fruit();
        food.eat();  // 输出: Eat some fruits
        if (food instanceof Fruit) {
            Fruit fruit = (Fruit) food;
            fruit.peel();  // 输出: Peel the fruit
        }
    }
}
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（2） 💬（1）<div>感觉，声明式编程就是封装了一下命令式编程而已</div>2023-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/17/39/3274257b.jpg" width="30px"><span>ple</span> 👍（3） 💬（0）<div>这儿表达有些误解，Java8以后文中的静态变量存储在堆上。https:&#47;&#47;openjdk.org&#47;jeps&#47;122</div>2024-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/35/d5/17833946.jpg" width="30px"><span>八宝</span> 👍（0） 💬（0）<div>我们还可以从哪些视角来看待 Java 中的变量？
从线程安全的角度看，常量天生安全，那么我们用的最多的变量呢？
1.方法区创建的变量（既静态变量），并发访问时会存在线程安全问题，需要加锁来保证数据的正确性。
2.堆中创建的变量，如果不存在逃逸现象，不存在跨线程使用，不需要考虑线程安全；
涉及到多线程访问，如 HashMap 等容器的并发 put，就要加锁或改用线程安全的容器。
3.如果在栈上创建的变量，生命周期都是方法内，随着方法的执行，出栈就会被回收，不需要考虑线程安全。</div>2023-12-20</li><br/>
</ul>