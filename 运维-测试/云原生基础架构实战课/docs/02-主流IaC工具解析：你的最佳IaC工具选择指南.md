你好，我是潘野。

上一讲，我们了解了IaC的概念及其发展过程，今天我们着重分析一些重要的IaC工具。

虽然我们很容易就可以查阅相关工具的文档，但不少同学并没有了解过这些工具为什么会被设计出来，背后又涉及哪些原理。而掌握了这些，你才能掌握选择工具的思路与标准，之后应用的时候，也能在使用上更加得心应手，避免踩坑。

## IaC工具盘点

在正式盘点之前，我们需要先明确一下工具选择标准。

上一讲我们了解了基础设施即代码的概念，IaC是一种自动化基础设施管理的方法，通过代码描述和配置基础设施资源，实现**快速**、**可靠**和**可重复**的部署和管理过程。

这里面有三个关键词——快速、可靠和可重复，这也是我们选择IaC工具的一个基准线。

快速有两层含义。第一是工具易用，容易编写IaC代码；第二是工具性能好，运行速度快。

可靠是指基于同样一份Code，同一套参数构建出的产物，其最终的行为应该是一致的。

可重复则表示**定义基础设施的代码是可以被重复使用和共享，确保不同环境间的一致性和可靠性**，这样可以防止因配置偏移或缺少依赖项而导致的运行时问题。简单来说，我上线A资源用这套代码，上线B资源我还可以用这套代码。

接下来，我们看看IaC每个发展阶段有哪些主流工具。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/b5/e9/f1aa07d6.jpg" width="30px"><span>alex run</span> 👍（0） 💬（2）<div>老师，为什么说ansible是不可重复的呢？ ansible操作同一资源，如果配置有变化才会change，没变化是不会执行的</div>2024-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/4d/1b/062941b4.jpg" width="30px"><span>🐭 🐹 🐭 🐹 🐭</span> 👍（0） 💬（1）<div>老师之后会有k8s网络问题的排查讲解吗</div>2024-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a5/34/6e3e962f.jpg" width="30px"><span>yayiyaya</span> 👍（3） 💬（0）<div>思考题：
provider &quot;aws&quot; {
  region = &quot;us-east-1&quot;  
}

resource &quot;aws_instance&quot; &quot;example&quot; {
  ami           = &quot;ami-0c55b159cbfafe1f0&quot;  
  instance_type = &quot;t2.micro&quot;
  tags = {
    Name = &quot;example-instance&quot;
  }

  provisioner &quot;remote-exec&quot; {
    inline = [
      &quot;sudo yum install -y  httpd&quot;,
      &quot;sudo systemctl start httpd&quot;,
      &quot;sudo systemctl enable httpd&quot;
    ]
  }

  connection {
    type        = &quot;ssh&quot;
    user        = &quot;ec2-user&quot;
    private_key = file(&quot;~&#47;.ssh&#47;your_private_key.pem&quot;)  
    host        = self.public_ip
  }
}

resource &quot;aws_security_group&quot; &quot;http_sg&quot; {
  name        = &quot;http_sg&quot;
  description = &quot;Allow HTTP inbound traffic&quot;

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = &quot;tcp&quot;
    cidr_blocks = [&quot;0.0.0.0&#47;0&quot;]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = &quot;-1&quot;
    cidr_blocks = [&quot;0.0.0.0&#47;0&quot;]
  }
}
</div>2024-03-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Wo6BMoLTHHWTTg2y3jKIaA3TVuyxsd1a3f118GSiaymop7KHxxTkJwlxGb3qQMyBoD7t8y4lFbKVhHqhmf7Ngibw/132" width="30px"><span>二十三</span> 👍（2） 💬（2）<div>怎么感觉使用terraform 各种配置还要学习语法、还不如自己写代码封装云api接口啊？ </div>2024-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（0）<div>Terraform好像不让在中国用……</div>2024-04-13</li><br/>
</ul>