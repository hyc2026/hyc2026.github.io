# 机器翻译

## 多语言机器翻译

多语言神经网络机器翻译(Multilingual neural machine translation, MNMT)采用独一的模型框架，可以减少一些部署或训练开销；并且统一训练一个模型会带来一些知识的共享。

编码器-中间语-解码器模型保持原来的编码器和解码器不变，在中间插了一个中间语模块，采用固定长度和固定内存。对输入先用编码器进行编码，再经过中间语模块获得更通用的一个表示，最后采用这个表示来解码输出。

Language-aware Interlingua for Multilingual Neural Machine Translation

`p86`