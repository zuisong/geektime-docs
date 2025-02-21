你好，我是康杨，今天我们来聊聊JVM中的反射机制。

在有反射之前，JVM对我们来说就像是一个黑盒。我们与它的交互，仅仅是在编译期之前，我们遵照Java语法写了一段程序，之后JVM如何编译，运行期如何执行我们不得而知，也和我们无关。这就像我们进入一家饭店 ，服务员递给我们一份菜单，我们能做的就是照着菜单去点菜，对于普通的消费者，一份精美菜单已经足够了。

就像下面这段代码 ，我们不需要做任何事情，构造器不用传入任何参数，就能得到一份蘸酱小黄瓜。

```java
// 蘸酱小黄瓜
public class DippedSauceCucumbers {
    private String  mainIngredient = "黄瓜";
    private String  dippingSauce = "豆瓣酱";
    private String  menu ="";
 
    public DippedSauceCucumbers() {
        setMenu();
    }
    // 设置菜单
    private void  setMenu() {
        menu = "蘸酱小黄瓜{" +
                "mainIngredient='" + mainIngredient + '\'' +
                ", dippingSauce='" + dippingSauce + '\'' +
                '}';
    }
    // 打印菜单
    public void printMenu(){
         System.out.printf(menu);
    }
    public static void main(String[] args) throws  Exception {
        DippedSauceCucumbers dippedSauceCucumbers = new DippedSauceCucumbers();
        dippedSauceCucumbers.printMenu();
    }
}
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（3）<div>获取 Class 对象的三种方式，其动态性不断降低，没太理解。既然拿到了 Class 对象这把钥匙，不管哪种方式拿到，其本质不都一样吗，后面想怎么玩就怎么玩。我是不是角度理解错了。</div>2023-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/6a/7f858f1f.jpg" width="30px"><span>白不吃</span> 👍（3） 💬（0）<div>深度差点意思</div>2023-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/aa/5c/d2c1c7ce.jpg" width="30px"><span>^_^</span> 👍（2） 💬（0）<div>1，获取一个 class 对象不同方式的差异点
    1）， 对象的getClass()方法获取的Class对象是针对具体的对象的，而.class语法和Class.forName()方法获取的Class对象是针对类本身的。
    2），使用对象的getClass()方法获取的Class对象是在运行时动态获取的，而使用.class语法和Class.forName()方法获取的Class对象是在编译时就确定的。
    3），使用.class语法和Class.forName()方法获取的Class对象可以在没有实例化对象的情况下使用，而对象的getClass()方法需要有一个实例化对象才能调用。
2,如何通过反射机制获取某个类以及它继承的类的所有公有字段
public class MyClass {
    public int publicField;
    private int privateField;
    protected int protectedField;

    public static void main(String[] args) {
        try {
            &#47;&#47; 获取类的Class对象
            Class&lt;?&gt; clazz = MyClass.class;

            &#47;&#47; 获取类的所有公有字段
            Field[] fields = clazz.getFields();

            &#47;&#47; 遍历字段数组并处理字段
            for (Field field : fields) {
                &#47;&#47; 输出字段的名称和类型
                System.out.println(&quot;Field name: &quot; + field.getName());
                System.out.println(&quot;Field type: &quot; + field.getType());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（0）<div>第一个问题：Class.forName静态方法一般用于加载驱动或者判断类是否存在的情况，.class必须事先知道有这个类，object.getClass必须要有类实例对象。
第二个问题：clazz.getFields();&#47;&#47;获取当前类及其父类的所有公有字段。clazz.getDeclaredFields();&#47;&#47;取私有字段或受保护的字段和公共字段。
</div>2023-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（0）<div>Q1：最简单程序，只是打印一个“hello”字符串；此程序的运行，会有哪些类加载器参与？ 以及加载顺序？
Q2：JAVA的“动态性”，除了反射，还有其他的吗？</div>2023-09-06</li><br/>
</ul>