# Pytorch

## tensor

| Data type               | dtype                              | CPU tensor           | GPU tensor                |
| ----------------------- | ---------------------------------- | -------------------- | ------------------------- |
| 32-bit floating point   | `tourch.float32` or `torch.float`  | `torch.FloatTensor`  | `torch.cuda.FloatTensor`  |
| 64-bit floating point   | `tourch.float64` or `torch.double` | `torch.DoubleTensor` | `torch.cuda.DoubleTensor` |
| 16-bit floating point   | `tourch.float16` or `torch.half`   | `torch.HalfTensor`   | `torch.cuda.HalfTensor`   |
| 8-bit integer(unsigned) | `tourch.uint8`                     | `torch.ByteTensor`   | `torch.cuda.ByteTensor`   |
| 8-bit integer(signed)   | `tourch.int8`                      | `torch.CharTensor`   | `torch.cuda.CharTensor`   |
| 16-bit integer(signed)  | `tourch.int16` or `torch.short`    | `torch.ShortTensor`  | `torch.cuda.ShortTensor`  |
| 32-bit integer(signed)  | `tourch.int32` or `torch.int`      | `torch.IntTensor`    | `torch.cuda.IntTensor`    |
| 64-bit integer(signed)  | `tourch.int64` or `torch.long`     | `torch.LongTensor`   | `torch.cuda.LongTensor`   |

### 标量

```python
torch.tensor(1.)
a = torch.tensor(1.3)
a.shape # torch.Size([])
len(a.shape) # 0
a.size() # torch.Size([])
```

### 向量

```python
# 一维向量
torch.tensor([1.1]) # tensor([1.1000])
torch.tensor([1.1, 2.2]) # tensor([1.1000, 2.2000])
torch.FloatTensor(1) # 随机初始化一个向量
data = np.ones(2)
a = torch.from_numpy(data) # tensor([1, 1], dtype=torch.float64)
a.shape # # torch.Size([2])
# 二维向量
a = torch.randn(2, 3)
a.shape # torch.Size([2, 3])
a.size(1) a.shape[1] # 3
a.numel() # 2*3=6 number of element
a.dim() # 2
```

### 初始化

```python
a = torch.rand(3, 3) # [0, 1]均匀分布
torch.rand_like(a) # 生成与a相同形状
torch.randint(1, 10, [3, 3]) # 参数为：[1, 10)内整数，形状为[3, 3]
torch.randn(3, 3) # 正态分布
torch.full([2, 3], 7) # [[7, 7, 7], [7, 7, 7]]
torch.arange(0, 10, 2) # 0, 2, 4, 6, 8
a = torch.normal(mean=torch.full([10], 0), std=torch.arange(1, 0, -0.1)) # 自定义正态分布，mean[i]和std[i]是a[i]的均值和方差
torch.linespace(0, 10, steps=4) # tensor([ 0.0000, 5.0000, 10.0000])
torch.logspace(0, -1, steps=2) # tensor([ 1.0000, 0.1000])
a = torch.ones(3, 3)
torch.zeros_like(a)
torch.eye(3, 4)
```

### 索引与切片

```python
a.shape # 4, 3, 28, 28
a.index_select(0, torch.tensor([0, 2])) # 对dim=0维度采样索引0和2
a[...].shape # 4, 3, 28, 28
a[0, ...].shape # 3, 28, 28
a[:, 1, ...].shape # 4, 28, 28
a[..., 2].shape # 4, 3, 28, 2
# masked_select
mask = a.ge(0.5)
torch.masked_select(x, mask)
```

### 变换

```python
# view 大小不变的前提下随意调整形状
a = torch.rand(4, 1, 28, 28)
a.view(4, 28*28)
a.unsqueeze(0).shape # 1, 4, 1, 28, 28
a.unsqueeze(-1).shape # 4, 1, 28, 28, 1
a.unsqueeze(4).shape # 4, 1, 28, 28, 1
a.unsqueeze(-4).shape # 4, 1, 1, 28, 28
a.unsqueeze(-5).shape # 1, 4, 1, 28, 28
# 只有维度是1才能被squeeze
b = torch.rand(1, 32, 1, 1)
b.squeeze().shape # 32 不提供维数挤压掉所有1
b.squeeze(0).shape # 32, 1, 1
b.squeeze(-1).shape # 1, 32, 1
b.squeeze(1).shape # 1, 32, 1, 1
b.squeeze(-4).shape # 32, 1, 1
# expand和repeat都是扩展维度，expand只是改变理解方式，在有必要时才复制数据，repeat直接复制数据
b.expand(4, 32, 14, 14) # 4, 32, 14, 14 expand只能对1进行扩展，括号中的参数时最终的扩展结果
b.expand(4, 32, -1, -1)
b.repeat(4, 1, 14, 14) # 4, 32, 14, 14 repeat括号中的参数时重复的次数
a.t() # 只能对二维矩阵进行转置
a.transpose(1, 3).contiguous().view(4, 3*32*32).view(4, 32, 32, 3).transpose(1, 3) # 对1和3维度进行交换
a.permute(0, 2, 3, 1) # 4, 32, 32, 3 在内部调用transpose起到交换的作用
```

### 拼接与拆分

```python
a = torch.rand(4, 32, 8)
b = torch.rand(5, 32, 8)
torch.cat([a, b], dim=0).shape # 9, 32, 8
c = torch.rand(4, 32, 8)
torch.stack([a, b], dim=1) # 4, 2, 32, 8 新建一个维度
torch.split([3, 1], dim=0) # 3, 32, 8; 1, 32, 8 具体指定每段长度
torch.split(2, dim=0) # 2, 32, 8; 2, 32, 8 同一长度
torch.chunk(2, dim=2) # 4, 32, 4; 4, 32, 4 参数为分成的个数
```

### 基本运算

```python
torch.add(a, b) # a+b
torch.sub(a, b) # a-b
torch.mul(a, b) # a*b
torch.div(a, b) # a/b
torch.mm(a, b) # 只能处理二维矩阵
torch.matmul(a, b) # a@b 只处理最后两维
a = torch.full([2, 2], 3)
a.pow(2) # a**2
a.sqrt() # a**(0.5)
torch.exp(a) # e^a
torch.log(a) # ln(a)
a = torch.tensor(3.14)
a.floor() # 3
a.ceil() # 4
a.trunc() # 3 整数部分
a.frac() # 0.1400 小数部分
a.round() # 3 四舍五入
a.clamp(min) # a中小于min的全部替换为min
a.clamp(min, max) # 大于max的全部替换为max
```

### 统计属性

```python
a.norm(1, dim=1) # 对维度为1的求1范数
a.min() # 返回结果及其索引
a.max()
a.mean()
a.prod()
a.sum()
a.argmax() # 可以指定维度
a.argmin()
a.topk(3, dim=1, largest=False)
a.kthvalue(8, dim=1) # 第8小
# 大小比较 > >= < <= != ==
torch.eq(a, b) # 逐元素比较，返回每个比较结果，结果的size与参数相同
torch.equal(a, b) # 返回True或False
```

### 高级用法

```python
c = torch.where(condition, x, y) # c[i] = (condition[i])?x[i]:y[i]
torch.gather(input, dim, index, out=None)
# out[i, j] = input[index[i, j], j] # dim=0
# out[i, j] = input[i, index[i, j]] # dim=1
```

