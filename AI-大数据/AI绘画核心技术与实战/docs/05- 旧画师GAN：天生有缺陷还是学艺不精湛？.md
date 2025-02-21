你好，我是南柯。

今天开始，我们正式进入AI绘画理论阶段的学习。我会带你理解图像生成模型背后的算法原理，掌握AI绘画主流算法方案背后通用的算法模块，并带你从零到一训练一个扩散模型。

基于扩散模型的AI绘画技术是我们这门课的主题，但其实在22年以前，GAN才是业界公认的AI绘画技术首选。在老一辈的AI画图中，GAN（生成对抗网络）可以说是唯一的选择。相信你也在各种社交软件上见到过各种变小孩、变老、性别变换的视觉特效，这类效果通常就是靠GAN完成的。

然而，随着22年DALL-E 2、Stable Diffusion的推出，扩散模型技术逐渐成为了AI绘画的主流技术。无论是绘画细节的精致度还是内容的多样性，扩散模型似乎都要优于GAN。

即便如此，对于入门AI绘画知识体系而言，GAN仍然是绕不开的话题，值得我们深入了解。因为搞懂了GAN的长处和短板，才能理解后来扩散模型解决了GAN的哪些痛点。而且今天我们要学的各种算法模型，也是面试中常常会问到的。

在正式探索基于扩散模型的AI绘画技术之前，我们用这一讲来重温旧画师GAN，探讨GAN如何从兴起到高光，并简要回顾GAN发展史上那些里程碑式的技术。

## GAN的起源

下面我放了两张例子。第一个例子是张大千模仿石涛的画作，第二个例子是贝特莱奇14岁时仿照毕加索的画作。假如你是艺术鉴赏家，能否发现这些仿作的破绽呢？
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/3e/90/c86ec4ca.jpg" width="30px"><span>Chengfei.Xu</span> 👍（1） 💬（1）<div>GAN的原理总结：

生成对抗网络（GAN）由两个部分组成：生成器（Generator）与判别器（Discriminator），它们在模型训练的过程中会持续更新和对抗，最终达到平衡

生成器的任务是根据输入的随机噪声，生成看起来像真实样本的新数据
判别器的任务是辨别给定的真实数据是真样本还是生成器生成的伪造样本（它会收到一组真实数据和一组生成数据）

在训练过程中，生成器和判别器互相对抗。生成器试图生成更逼真的样本来迷惑判别器，而判别器则努力辨别出生成器生成的伪造样本。它们之间会不断重复这个过程，持续更新自己的参数，达到相互改进和提升


而随着训练的进行，生成器和判别器逐渐“学会”了“博弈”，最终会达到一个平衡状态，即生成器的样本会越来越逼真，判别器识别的准确率也会越来越高。通过这种对抗式的训练方式，GAN可以生成非常逼真的数据，使用场景有图像合成、图像修复、图像风格转换等等。</div>2023-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/58/f8/8b9bb574.jpg" width="30px"><span>Wiliam</span> 👍（0） 💬（1）<div>老师请教一下：
1. GAN 的局限性主要表现在训练不稳定性、生成图像模糊、难以评估和控制生成质量等问题，那么GigaGAN具体是解决了哪个问题呢？
2. 抛开GAN的劣势，相比Diffusion，GAN有什么优点吗？有考虑过GAN的优点与Diffusion的优点强强联合吗？</div>2023-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/21/c3/bb900ed2.jpg" width="30px"><span>xixi</span> 👍（0） 💬（1）<div>giga读错了</div>2023-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7d/d0/48c13a76.jpg" width="30px"><span>xingliang</span> 👍（0） 💬（1）<div>BigGAN：BigGAN 是为了实现高分辨率、高质量的图像生成而设计的。它的特点是在模型中引入了大量的参数，利用更大的批次大小和更多的特征通道。这样可以实现高分辨率且内容丰富的图像生成。但同时，由于模型的复杂性，它需要大量的计算资源和时间来训练。

StarGAN：不同于其他 GANs 专注于单一领域或任务，StarGAN 能够在多个领域之间进行图像转换，例如，它可以在一个模型中实现人脸属性（如头发颜色、性别等）的多种转换。StarGAN 的核心是使用一个共同的生成器和判别器，以及域标签，使其可以对多个域进行学习和转换。

Progressive GAN (逐步增长的 GAN，也被称为 PGGAN)：Progressive GAN 的主要特点是它从低分辨率开始训练，然后逐渐添加更多的层来增加分辨率。这种逐步的方法使得模型在初期的训练更稳定，并且能够逐渐适应更高分辨率的图像。这使得模型能够生成高质量且高分辨率的图像。</div>2023-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9f/f6/7431e82e.jpg" width="30px"><span>xueerfei007</span> 👍（0） 💬（2）<div>一口气看完，催更</div>2023-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（1）<div>这句：下面我放了两张例子。第一个例子是张大千模仿石涛的画作，第二个例子是贝特莱奇 14 岁时仿照毕加索的画作。假如你是艺术鉴赏家，能否发现这些仿作的破绽呢？

所以破绽是什么？（到这里，我还没往下看，想先提问一下）</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：GAN有具体产品吗？
扩散模型有具体产品，比如SD，GAN有具体产品吗？
Q2：GAN的生成器加随机噪声，请问有非随机噪声吗？
Q3：模型的训练一般用什么语言？
Q4：GAN或webUI能制作技术文档上的图吗？比如写一个技术文档，上面有数据链应用图等，可以制作这一类的技术图片吗？</div>2023-07-26</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（5） 💬（0）<div>看不懂伪代码。将代码复制给极客的&quot;AI学习助手“，回答如下：
这段代码是一个用于训练生成对抗网络（GAN）的循环。下面是对代码的逐行分析：

for epoch in range(num_epochs):：外层循环，用于控制训练的轮数。

for batch_data in data_loader:：内层循环，用于遍历训练数据集中的每个批次。

real_images = batch_data.to(device)：将真实图像数据移动到指定的设备（如GPU）上。

z = torch.randn(batch_size, latent_dim).to(device)：从标准正态分布中生成一组随机噪声向量z，并将其移动到指定的设备上。

fake_images = generator(z).detach()：使用生成器网络（generator）和随机噪声z生成一组假图像，并将其与生成器的参数的计算图分离。

d_loss_real = discriminator(real_images)：将真实图像输入判别器网络（discriminator）中，计算真实图像的判别器损失。

d_loss_fake = discriminator(fake_images)：将假图像输入判别器网络中，计算假图像的判别器损失。

d_loss = -(torch.mean(d_loss_real) - torch.mean(d_loss_fake))：计算判别器的总损失，这里使用了最大化判别器对真实图像的预测概率和最小化判别器对假图像的预测概率的策略。

discriminator.zero_grad()：清除判别器的梯度。

d_loss.backward()：反向传播，计算判别器的梯度。

discriminator_optimizer.step()：更新判别器的参数，使用优化器进行梯度下降。

z = torch.randn(batch_size, latent_dim).to(device)：重新生成一组随机噪声向量z，并将其移动到指定的设备上。

fake_images = generator(z)：使用生成器网络和新的随机噪声z生成一组新的假图像。

g_loss = -torch.mean(discriminator(fake_images))：计算生成器的损失，这里使用了最大化判别器对假图像的预测概率的策略。

generator.zero_grad()：清除生成器的梯度。

g_loss.backward()：反向传播，计算生成器的梯度。

generator_optimizer.step()：更新生成器的参数，使用优化器进行梯度下降。

这段代码的作用是通过交替地训练判别器和生成器，使生成器能够生成逼真的假图像，同时判别器能够准确地区分真实图像和假图像。</div>2023-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/d0/82/791d0f5e.jpg" width="30px"><span>大将</span> 👍（0） 💬（0）<div>最大化真实图像的损失（d_loss_real）和最小化生成图像的损失（d_loss_fake），个人感觉这个描述并不准确，最大化和最小化容易引起歧义</div>2024-02-06</li><br/><li><img src="" width="30px"><span>Geek_0bac2d</span> 👍（0） 💬（0）<div>AI生成的代码解释
for epoch in range(num_epochs):
    for batch_data in data_loader:
        # 更新判别器
        real_images = batch_data.to(device)  # 获取真实图像数据
        z = torch.randn(batch_size, latent_dim).to(device)  # 生成随机噪声向量
        fake_images = generator(z).detach()  # 通过生成器生成假图像，并将其与生成器的梯度计算图分离

        d_loss_real = discriminator(real_images)  # 判别器对真实图像的判别结果
        d_loss_fake = discriminator(fake_images)  # 判别器对假图像的判别结果

        # 判别器损失
        d_loss = -(torch.mean(d_loss_real) - torch.mean(d_loss_fake))  # 计算判别器的损失

        discriminator.zero_grad()  # 清空判别器的梯度
        d_loss.backward()  # 反向传播计算判别器的梯度
        discriminator_optimizer.step()  # 利用优化器更新判别器的参数

        # 更新生成器
        z = torch.randn(batch_size, latent_dim).to(device)  # 生成新的随机噪声向量
        fake_images = generator(z)  # 通过生成器生成新的假图像

        g_loss = -torch.mean(discriminator(fake_images))  # 判别器对新的假图像的判别结果作为生成器的损失

        generator.zero_grad()  # 清空生成器的梯度
        g_loss.backward()  # 反向传播计算生成器的梯度
        generator_optimizer.step()  # 利用优化器更新生成器的参数
</div>2023-07-30</li><br/>
</ul>