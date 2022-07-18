import numpy as np
from sklearn.datasets._samples_generator import make_blobs
from sklearn.decomposition import PCA
import torch

# tensor 和 ndarry 的相互转化
# A = X.numpy() # tensor->ndarray
# B = torch.tensor(A) # ndarray->tensor

dim = 512
tensor = torch.cat((torch.load('0.th', map_location=torch.device('cpu')), torch.load('1.th', map_location=torch.device('cpu'))), dim=0) # [20000, 768]
X = tensor.numpy()
pca = PCA(n_components=dim)
pca.fit(X)
comp = pca.components_
B = torch.tensor(comp)
torch.save(B, 'pca_{}.th'.format(str(dim)))

# test
# X, _ = make_blobs(n_samples=10, n_features=8, random_state =9) # 生成10条8维的数据
# print(X.shape)
# pca = PCA(n_components=4) # 将8维降到4维
# X_transformed1 = pca.fit(X).transform(X) # pca.fit(X)-训练 + pca.transform(X)-将数据X转换成降维后的数据
# comp = pca.components_ # (n_components, n_features) 转换矩阵
# print(comp.shape)
# X_M = X - X.mean(axis=0)
# X_transformed2 = np.dot(X_M, comp.T) # 和X_transformed1数值相同