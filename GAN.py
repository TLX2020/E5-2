# 导入必要的库
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# 定义超参数
batch_size = 128 # 批次大小
latent_dim = 100 # 隐空间维度
num_epochs = 20 # 训练轮数
lr = 0.0002 # 学习率
beta1 = 0.5 # Adam优化器的参数

# 定义数据集和数据加载器
transform = transforms.Compose([
    transforms.ToTensor(), # 将图像转换为张量，并归一化到[0,1]
    transforms.Normalize((0.5,), (0.5,)) # 将图像标准化到[-1,1]
])

dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform) # 加载MNIST数据集
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True) # 定义数据加载器

# 定义生成器网络
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            # 输入一个随机向量，经过一个全连接层，输出一个7*7*256的特征图
            nn.Linear(latent_dim, 7*7*256),
            nn.BatchNorm1d(7*7*256),
            nn.ReLU(True),
            # 将特征图变形为7*7*256的张量，方便后续卷积操作
            nn.Unflatten(1, (256, 7, 7)),
            # 使用转置卷积层，将特征图上采样为14*14*128的张量
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            # 使用转置卷积层，将特征图上采样为28*28*64的张量
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            # 使用转置卷积层，将特征图上采样为28*28*1的张量，即生成的图像
            nn.ConvTranspose2d(64, 1, kernel_size=3, stride=1, padding=1),
            nn.Tanh() # 使用tanh激活函数，将输出限制在[-1,1]之间
        )

    def forward(self, x):
        return self.main(x)

# 定义判别器网络
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            # 输入一个28*28*1的图像，经过一个卷积层，输出一个14*14*64的特征图
            nn.Conv2d(1, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2), # 使用leaky relu激活函数，避免梯度消失问题
            # 经过一个卷积层，输出一个7*7*128的特征图
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            # 将特征图变形为一个向量，方便后续全连接操作
            nn.Flatten(),
            # 经过一个全连接层，输出一个标量，表示判别器对输入图像的判断结果（真或假）
            nn.Linear(7*7*128, 1),
            nn.Sigmoid() # 使用sigmoid激激活函数，将输出限制在[0,1]之间
        )

    def forward(self, x):
        return self.main(x)

# 创建生成器和判别器对象
generator = Generator()
discriminator = Discriminator()

# 定义损失函数，使用二元交叉熵损失
criterion = nn.BCELoss()

# 定义优化器，使用Adam优化器
optimizer_G = optim.Adam(generator.parameters(), lr=lr, betas=(beta1, 0.999))
optimizer_D = optim.Adam(discriminator.parameters(), lr=lr, betas=(beta1, 0.999))

# 定义真假标签
real_label = 1
fake_label = 0

# 开始训练
for epoch in range(num_epochs):
    # 遍历数据集
    for i, (data, _) in enumerate(dataloader):
        # 获取真实图像和对应的批次大小
        real_images = data
        b_size = real_images.size(0)

        # 更新判别器参数
        optimizer_D.zero_grad() # 清空梯度

        # 计算判别器对真实图像的输出和损失
        output_real = discriminator(real_images).view(-1)
        label_real = torch.full((b_size,), real_label) # 创建真实标签
         # 计算判别器对生成图像的输出和损失
        noise = torch.randn(b_size, latent_dim) # 创建随机噪声向量
        fake_images = generator(noise) # 生成假图像
        output_fake = discriminator(fake_images.detach()).view(-1) # 计算判别器的输出，注意要使用detach方法，避免影响生成器的梯度
        label_fake = torch.full((b_size,), fake_label) # 创建假标签

        # 计算判别器的总损失和梯度，并更新参数
        loss_D = loss_real + loss_fake # 计算总损失
        loss_D.backward() # 计算梯度
        optimizer_D.step() # 更新参数

        # 更新生成器参数
        optimizer_G.zero_grad() # 清空梯度

        # 计算生成器的损失，即判别器对生成图像的输出与真实标签之间的损失
        output_fake = discriminator(fake_images).view(-1) # 重新计算判别器的输出，这次不使用detach方法，因为要更新生成器的梯度
        label_real = torch.full((b_size,), real_label) # 创建真实标签，注意这里是真实标签，因为生成器希望判别器将生成图像判断为真
        loss_G = criterion(output_fake, label_real) # 计算损失

        # 计算生成器的梯度，并更新参数
        loss_G.backward() # 计算梯度
        optimizer_G.step() # 更新参数

        # 打印训练信息
        if i % 100 == 0:
            print(f'Epoch {epoch}, Batch {i}, Loss_D: {loss_D.item():.4f}, Loss_G: {loss_G.item():.4f}')

    # 每个epoch结束后，保存并显示一些生成图像
    with torch.no_grad():
        noise = torch.randn(16, latent_dim) # 创建随机噪声向量
        fake_images = generator(noise) # 生成假图像
        fake_images = fake_images * 0.5 + 0.5 # 将图像从[-1,1]转换到[0,1]
        plt.figure(figsize=(4,4)) # 创建画布
        for j in range(16):
            plt.subplot(4,4,j+1) # 创建子图
            plt.imshow(fake_images[j][0], cmap='gray') # 显示图像
            plt.axis('off') # 关闭坐标轴
        plt.savefig(f'fake_images_epoch_{epoch}.png') # 保存图像
        plt.show() # 显示图像