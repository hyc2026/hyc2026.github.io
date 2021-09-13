# 支持向量机(Support Vector Machines)

支持向量机(support vector machines, SVM)是一种定义在特征空间上的间隔最大的线性分类器，学习算法是求解凸二次规划的最优化算法。

## 线性可分支持向量机与硬间隔最大化

### 线性可分支持向量机

给定一个特征空间上的训练数据集：
$$
\mathbb{X}=\{(\pmb x^{(1)},y^{(1)}),(\pmb x^{(2)},y^{(2)}),...,(\pmb x^{(N)},y^{(N)})\}
$$
其中，$\pmb x^{(i)}\in X=\mathbb{R}^n$​，$y^{(i)}\in Y=\{1,-1\}$​。

学习的目标是在特征空间中找到一个分离超平面，能将实例分到不同的类。通过间隔最大化或等价地求解相应的凸二次规划问题，学习得到的分离超平面对应于方程为
$$
\pmb W^*\cdot \pmb x+\pmb b^*=0 \tag{1}
$$
以及相应的分类决策函数
$$
f(x)={\rm {sign}}(\pmb W^*\cdot \pmb x+\pmb b^*) \tag{2}
$$
超平面将特征空间划分为两部分，法向量$\pmb W$​​指向的一侧为正类，另一侧为负类。

### 函数间隔和几何间隔

超平面$(\pmb W,\pmb b)$​关于样本点$(\pmb x^{(i)},y^{(i)})$​​​的**函数间隔(functional margin)**为：
$$
\hat \gamma^{(i)}=y^{(i)}(\pmb W\cdot\pmb x^{(i)}+\pmb b) \tag{3}
$$
超平面$(\pmb W,\pmb b)$关于训数据集$\mathbb{X}$​的​函数间隔为：
$$
\hat \gamma={\rm min}_{i=1,...,N}\ \hat \gamma^{(i)} \tag{4}
$$
函数间隔可以表示分类预测的正确性及确信度，但如果成倍增加$\pmb W$和$\pmb b$​就能在不改变超平面的前提下增加函数空间，因此需要增加规范化约束$||\pmb W||=1$​​，使得间隔确定，此时的函数间隔变成了**几何间隔(geometric margin)**：
$$
\gamma^{(i)}=y^{(i)}(\frac{\pmb W}{||\pmb W||}\cdot\pmb x^{(i)}+\frac{\pmb b}{||\pmb W||}) \tag{5}
$$
超平面$(\pmb W,\pmb b)$关于训数据集$\mathbb{X}$的几何间隔为：
$$
\gamma={\rm min}_{i=1,...,N}\ \gamma^{(i)} \tag{6}
$$

### 间隔最大化

支持向量机的基本想法是求解能够正确划分训练数据集并且几何间隔最大的分离超平面，这意味着以充分大的确信度队训练数据进行分类

#### 1. 最大间隔分离超平面

该问题可抽象为约束最优化问题：
$$
{\rm{max}}_{\pmb W,\pmb b}\quad\gamma\tag{7}
$$
$$
{\rm{s.t.}}\quad y^{(i)}(\frac{\pmb W}{||\pmb W||}\cdot\pmb x^{(i)}+\frac{\pmb b}{||\pmb W||})\ge\gamma,i=1,...,N\tag{8}
$$

考虑到几何间隔与函数间隔的关系$\gamma=\frac{\hat\gamma}{||\pmb W||}$，该问题可改写为：

$$
{\rm{max}}_{\pmb W,\pmb b}\quad\frac{\hat\gamma}{||\pmb W||}\tag{9}
$$
$$
{\rm{s.t.}}\quad y^{(i)}(\pmb W\cdot\pmb x^{(i)}+\pmb b)\ge\hat\gamma,i=1,...,N\tag{10}
$$

又因为函数间隔的取值不影响最优化问题的解，因此令$\hat\gamma=1$，且最大化$\frac{1}{||\pmb W||}$和最小化$\frac{1}{2}||\pmb W||^2$等价，因此线性可分支持向量机学习的最优化问题最终转化成一个**凸二次规划(convex quadratic programming)**问题：
$$
{\rm{min}}_{\pmb W,\pmb b}\quad\frac{1}{2}||\pmb W||^2\tag{11}
$$

$$
{\rm{s.t.}}\quad y^{(i)}(\pmb W\cdot\pmb x^{(i)}+\pmb b)-1\ge0,i=1,...,N\tag{12}
$$

求解该问题即可得到最大间隔分离超平面和分类决策函数。

为了求解线性可分支持向量机的最优化问题，将它作为原始最优化问题，应用拉格朗日对偶性，通过求解对偶问题(dual problem)得到原始问题(primal problem)的最优解，这就是线性可分支持向量机的对偶算法(dual algorithm)。这样做的优点：1. 对偶问题往往更易求解；2. 自然引入核函数，进而推广到非线性分类问题。

首先构建拉格朗日函数(Lagrange function)，对(14)的每一个不等式约束引进拉格朗日乘子(Lagrange multiplier)$\alpha_i$，定义拉格朗日函数：
$$
L(\pmb W,\pmb b,\pmb\alpha)=\frac12||\pmb W||^2-\sum_{i=1}^N\alpha_iy^{(i)}(\pmb W\cdot\pmb x^{(i)}+\pmb b)+\sum_{i=1}^N\alpha_i\tag{13}
$$
其中$\pmb\alpha=(\alpha_1,\alpha_2,...\alpha_N)^\top$​为拉格朗日乘子向量。

根据拉格朗日对偶性，原始问题的对偶问题是极大极小问题：
$$
{\rm{max}}_{\pmb\alpha}{\rm{min}}_{\pmb W,\pmb b}L(\pmb W,\pmb b,\pmb\alpha)
$$

1. 求${\rm{min}}_{\pmb W,\pmb b}L(\pmb W,\pmb b,\pmb\alpha)$​

   分别对$\pmb W,\pmb b$求偏导并令其等于0。
   $$
   \nabla_{\pmb W}L(\pmb W,\pmb b,\pmb\alpha)=\pmb W-\sum_{i=1}^N\alpha_iy^{(i)}\pmb x^{(i)}=0\\
   \nabla_{\pmb b}L(\pmb W,\pmb b,\pmb\alpha)=\sum_{i=1}^N\alpha_iy^{(i)}=0\tag{14}
   $$
   将(14)带入(13)：
   $$
   L(\pmb W,\pmb b,\pmb\alpha)=\frac12\sum_{i=1}^N\sum_{j=1}^N\alpha_i\alpha_jy^{(i)}y^{(j)}(\pmb x^{(i)}\cdot\pmb x^{(j)})-\sum_{i=1}^N\alpha_iy^{(i)}((\sum_{j=1}^N\alpha_jy^{(j)}\pmb x^{(j)})\cdot\pmb x^{(i)}+\pmb b)+\sum_{i=1}^N\alpha_i\\=-\frac12\sum_{i=1}^N\sum_{j=1}^N\alpha_i\alpha_jy^{(i)}y^{(j)}(\pmb x^{(i)}\cdot\pmb x^{(j)})+\sum_{i=1}^N\alpha_i
   $$
   即 ${\rm{min}}_{\pmb W,\pmb b}L(\pmb W,\pmb b,\pmb\alpha)=-\frac12\sum_{i=1}^N\sum_{j=1}^N\alpha_i\alpha_jy^{(i)}y^{(j)}(\pmb x^{(i)}\cdot\pmb x^{(j)})+\sum_{i=1}^N\alpha_i$

2. 求${\rm{min}}_{\pmb W,\pmb b}L(\pmb W,\pmb b,\pmb\alpha)$对$\pmb\alpha$的极大

   将极大转换成极小问题：
   $$
   {\rm{min}}_{\pmb\alpha}\quad\frac12\sum_{i=1}^N\sum_{j=1}^N\alpha_i\alpha_jy^{(i)}y^{(j)}(\pmb x^{(i)}\cdot\pmb x^{(j)})-\sum_{i=1}^N\alpha_i\tag{15}
   $$

   $$
   {\rm{s.t.}}\quad \sum_{i=1}^N\alpha_iy^{(i)}=0\tag{16}
   $$

   $$
   \alpha_i\ge0,i=1,2,...,N\tag{17}
   $$

   求得最优解$\alpha^*=(\alpha^*_1,\alpha^*_2,...,\alpha^*_N)^\top$，$\pmb W^*=\sum_{i=1}^N\alpha_i^*y^{(i)}\pmb x^{(i)}$，选择一个$\alpha^*$的正分量$\alpha^*_j$，$\pmb b^*=y^{(i)}-\sum_{i=1}^N\alpha_i^*y^{(i)}(\pmb x^{(i)}\cdot\pmb x^{(j)})$。分离超平面$\pmb W^*\cdot\pmb x^{(i)}+\pmb b^*=0$，分类决策函数$f(x)={\rm {sign}}(\pmb W^*\cdot \pmb x+\pmb b^*)$。​

#### 2. 支持向量和间隔边界

训练数据集的样本点中与分离超平面距离最近的样本点的实例称为**支持向量(support vector)**，支持向量是使约束条件(12)等号成立的点。存在使$y^{(i)}=\pm1$的两个支持向量$H_1,H_2$。它们之间的距离称为**间隔(margin)**，间隔大小为$\frac2{||\pmb W||}$，$H_1,H_2$​称为间隔边界。

决定分离超平面时只有支持向量起作用，移动支持向量将改变所求解，因此该模型称为支持向量机。支持向量一般很少，所以支持向量机由很少的重要的训练样本决定。

训练数据集中对应于$\alpha^*_i>0$​的样本点的实例称为**支持向量(support vector)**。

## 线性支持向量机与软间隔最大化

### 线性支持向量机

线性可分的支持向量机学习方法对线性不可分训练数据是不适用的，通常情况，线性不可分数据中有一些特异点(outlier)，将这些特异点除去后，剩下大部分的样本点组成的集合是线性可分的。线性不可分意味着某些样本点不满足(12)，因此对每个样本点引入一个松弛变量$\xi_i\ge0$​，约束条件变为$$​​，同时对于每个松弛变量支付一个代价。因此线性不可分的线性支持向量机的学习问题变成如下凸二次规划(convex quadratic programming)问题：
$$
{\rm min}_{\pmb W,\pmb b,\pmb\xi}\quad\frac12||\pmb W||^2+C\sum_{i=1}^N\xi_i\tag{18}
$$

$$
{\rm s.t.}\quad y^{(i)}(\pmb W\cdot\pmb x^{(i)}+\pmb b)\ge1-\xi_i,i=1,2,...,N\tag{19}
$$

$$
\xi_i\ge0,i=1,2,...,N\tag{20}
$$

