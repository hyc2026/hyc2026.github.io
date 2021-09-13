https://blog.csdn.net/qq_42185634/article/details/102914406

## 数学符号

### 数和数组

+ $a$​ 标量(整数或实数)
+ $\pmb{a}$​ 向量
+ $\pmb{A}$​​ 矩阵​
  + $\pmb{I}_n$ n行n列的单位矩阵
  + $\pmb{I}$ 维度蕴含于上下文的单位矩阵
+ $\pmb {\mathsf{A}}$​​ 张量​
+ ${\rm a}$​​​ 标量随机变量
+ $\pmb{\rm a}$​​​ 向量随机变量
+ $\pmb{\rm A}$​​​​ 矩阵随机变量
+ $\pmb{e}^{(i)}$​​​ 标准基向量，索引$i$​处值为1 $[0, ..., 0, 1, 0, ..., 0]$
+ ${\rm diag}(\pmb{a})$​ 对角方阵

### 集合和图

+ $\mathbb{A}$ 集合
+ $\mathbb{R}$​ 实数集
+ $\{0,1,...,n\}$ 整数集​
+ $[a,b)$​ 区间
+ $\mathbb{A}\setminus\mathbb{B}$​ 差集
+ $\mathcal{G}$​ 图

+ $Pa_\mathcal{G}({\rm x}_i)$ 图$\mathcal{G}$中${\rm x}_i$的父节点

### 索引

+ $a_i$ 向量$\pmb{a}$的第$i$个元素
+ $A_{i,j}$ 矩阵${\pmb A}$的$i,j$元素
+ ${\pmb A}_{i,:}$ 矩阵${\pmb A}$的第$i$列
+ ${\rm a}_i$ 随机向量$\pmb{\rm a}$的第$i$个元素

### 线性代数中的操作

+ ${\pmb A}^\top$ ${\pmb A}$的转置

+ ${\pmb A}^+$ ${\pmb A}$的Moore-Penrose伪逆
+ ${\pmb A}\odot{\pmb B}$ ${\pmb A}$和${\pmb B}$的逐元素乘积(Hadamard乘积)
+ ${\rm det}(\pmb A)$ ${\pmb A}$的行列式

### 微积分

+ $\frac{dy}{dx}$ $y$关于$x$的导数
+ $\frac{\partial y}{\partial x}$ $y$关于$x$的偏导
+ $\nabla_xy$ $y$关于$x$的偏导
+ $\nabla_{\pmb X}y$ $y$关于$\pmb X$矩阵导数
+ $\nabla_{\pmb{\mathsf{X}}}y$ $y$关于$\pmb{\mathsf{X}}$求导后的张量
+ $\frac{\partial f}{\partial {\pmb x}}$ $f$：$\mathbb{R}^n\to\mathbb{R}^m$的$\rm{Jacobian}$矩阵$\pmb J\in\mathbb{R}^{m\times n}$
+ $\nabla_x^2f(\pmb x)$​​ or ${\pmb H}(f)(\pmb x)$​​ $f$在点​$\pmb x$处的$\rm{Hessian}$​矩阵​
+ $\int f(\pmb x)d\pmb x$ $\pmb x$整个域上的定积分
+ $\int_{\mathbb{S}} f(\pmb x)d\pmb x$ 集合$\mathbb{S}$上关$\pmb x$于的定积分

### 概率和信息论

+ ${\rm a}\bot{\rm b}$ a和b相互独立的随机变量
+ ${\rm a}\bot{\rm b}|\rm c$​ 给的c后条件独立
+ $P(\rm a)$​ 离散变量上的概率分布
+ $p(\rm a)$ 连续变量上的概率分布
+ ${\rm a}\sim P$​ 具有分布$P$的随机变量a​
+ $\mathbb{E}_{{\rm x}\sim P}[f(x)]$​​​ or $\mathbb{E}f(x)$​ ​$f(x)$​​关于$P(x)$​的期望
+ ${\rm Var}(f(x))$ $f(x)$ 在分布$P(x)$下的方差
+ ${\rm Cov}(f(x),g(x))$ $f(x)$和$g(x)$在分布$P(x)$下的协方差
+ $H(\rm x)$ 随机变量的$\rm x$的香农熵​
+ $D_{\rm KL}(P||Q)$​ $P$和$Q$的KL散度
+ $\mathcal{N}(\pmb x;\pmb \mu; \pmb \Sigma)$​​ 均值为$\pmb \mu$​​协方差为$\Sigma$​​，$\pmb x$​上的高斯分布​

### 函数

+ $f:\mathbb{A}\to\mathbb{B}$ 定义域为$\mathbb{A}$值域为$\mathbb{B}$的函数$f$
+ $f\circ g$ $f$和$g$的组合
+ $f(\pmb x;\pmb \theta)$ 由$\pmb \theta$参数化，关于$\pmb x$的函数
+ ${\rm log}\ x$​ 自然对数
+ $\sigma(x)$ Logistics sigmoid，$\frac{1}{1+{\rm{exp}}(-x)}$
+ $\zeta(x)$​​​​ Softplus，${\rm {log}}(1+{\rm {exp}}(x))$​
+ $||\pmb x||_p$​ $\pmb x$的$L^p$范数
+ $||\pmb x||$​ $\pmb x$​的$L^2$​范数
+ $x^+$​ $x$的正数部分
+ ${\pmb 1}_{\rm {condition}}$​​ 如果条件为真则为1，否则为0

### 数据集和分布

+ $p_{\rm {data}}$​ 数据生成分布
+ $\hat p_{\rm {data}}$​ 由训练集定义的经验分布
+ $\mathbb{X}$​ 训练样本的集合
+ ${\pmb x}^{(i)}$​ 数据集的第$i$个样本
+ $y^{(i)}$ or ${\pmb y}^{(i)}$ 监督学习中与${\pmb x}^{(i)}$​关联的目标
+ $\pmb X$ $m\times n$的矩阵，其中行${\pmb X}_{i,:}$为输入样本${\pmb x}^{(i)}$



$\mathbb{AaBbCcDdEFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXXYyZz}$
$\mathbf{AaBbCcDdEFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXXYyZz}$
$\mathtt{AaBbCcDdEFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXXYyZz}$
$\mathrm{AaBbCcDdEFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXXYyZz}$
$\mathsf{AaBbCcDdEFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXXYyZz}$
$\mathcal{AaBbCcDdEFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXXYyZz}$
$\mathscr{AaBbCcDdEFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXXYyZz}$
$\mathfrak{AaBbCcDdEFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXXYyZz}$