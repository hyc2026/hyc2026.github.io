# Huggingface Transformers

```
https://huggingface.co/course
```

## pipeline

pipeline库包括了模型本身以及必要的前处理和后处理，我们可以直接输入文本，得到最终结果。

当输入一段文本给pipeline时，其内部主要执行三个步骤：

1. 文本被预处理成模型可以识别的形式
2. 输入给模型进行预测
3. 对预测结果进行后处理

调用pipeline函数时，将会下载和缓存模型(之后调用时不用重新下载)，默认缓存路径为`~/.cache/huggingface/transformers`

### Sentiment analysis

判断一段文本是正面的还是负面的。

```python
from transformers import pipeline
classifier = pipeline("sentiment-analysis")
classifier("I've been waiting for a HuggingFace course my whole life.")
# [{'label': 'POSITIVE', 'score': 0.9598047137260437}]
classifier([
    "I've been waiting for a HuggingFace course my whole life.", 
    "I hate this so much!"
])
# [{'label': 'POSITIVE', 'score': 0.9598047137260437},
#  {'label': 'NEGATIVE', 'score': 0.9994558095932007}]
```

**zero-shot-classification**可以随意指定用于分类的标签，不必依赖于预训练模型的标签。因此该模型可以直接使用而不用微调。

```python
from transformers import pipeline
classifier = pipeline("zero-shot-classification")
classifier(
    "This is a course about the Transformers library",
    candidate_labels=["education", "politics", "business"],
)
# {'sequence': 'This is a course about the Transformers library',
#  'labels': ['education', 'business', 'politics'],
#  'scores': [0.8445963859558105, 0.111976258456707, 0.043427448719739914]}
```

### Text generation

提供一段提示，模型将会生成接下来的内容。参数`num_return_sequences`控制返回的序列数，`max_length`控制返回的最大长度。

```python
from transformers import pipeline
generator = pipeline("text-generation", model="distilgpt2")
generator(
    "In this course, we will teach you how to",
    max_length=30,
    num_return_sequences=2,
)
# [{'generated_text': 'In this course, we will teach you how to manipulate the world and '
#                     'move your mental and physical capabilities to your advantage.'},
#  {'generated_text': 'In this course, we will teach you how to become an expert and '
#                     'practice realtime, and with a hands on experience on both real '
#                     'time and real'}]
```

### Mask filling

完形填空

```python
from transformers import pipeline
unmasker = pipeline("fill-mask")
unmasker("This course will teach you all about <mask> models.", top_k=2)
# [{'sequence': 'This course will teach you all about mathematical models.',
#   'score': 0.19619831442832947,
#   'token': 30412,
#   'token_str': ' mathematical'},
#  {'sequence': 'This course will teach you all about computational models.',
#   'score': 0.04052725434303284,
#   'token': 38163,
#   'token_str': ' computational'}]
```

### Named entity recognition

命名实体识别，找出输入文本的哪些部分对应于实体，如人员、地点或组织等。

```python
from transformers import pipeline
ner = pipeline("ner", grouped_entities=True)
ner("My name is Sylvain and I work at Hugging Face in Brooklyn.")
# [{'entity_group': 'PER', 'score': 0.99816, 'word': 'Sylvain', 'start': 11, 'end': 18}, 
#  {'entity_group': 'ORG', 'score': 0.97960, 'word': 'Hugging Face', 'start': 33, 'end': 45}, 
#  {'entity_group': 'LOC', 'score': 0.99321, 'word': 'Brooklyn', 'start': 49, 'end': 57}]
```

### Question answering

```python
from transformers import pipeline
question_answerer = pipeline("question-answering")
question_answerer(
    question="Where do I work?",
    context="My name is Sylvain and I work at Hugging Face in Brooklyn"
)
# {'score': 0.6385916471481323, 'start': 33, 'end': 45, 'answer': 'Hugging Face'}
```

### Summarization

```python
from transformers import pipeline
summarizer = pipeline("summarization")
summarizer("""
    America has changed dramatically during recent years. Not only has the number of 
    graduates in traditional engineering disciplines such as mechanical, civil, 
    electrical, chemical, and aeronautical engineering declined, but in most of 
    the premier American universities engineering curricula now concentrate on 
    and encourage largely the study of engineering science. As a result, there 
    are declining offerings in engineering subjects dealing with infrastructure, 
    the environment, and related issues, and greater concentration on high 
    technology subjects, largely supporting increasingly complex scientific 
    developments. While the latter is important, it should not be at the expense 
    of more traditional engineering.

    Rapidly developing economies such as China and India, as well as other 
    industrial countries in Europe and Asia, continue to encourage and advance 
    the teaching of engineering. Both China and India, respectively, graduate 
    six and eight times as many traditional engineers as does the United States. 
    Other industrial countries at minimum maintain their output, while America 
    suffers an increasingly serious decline in the number of engineering graduates 
    and a lack of well-educated engineers.
""")
# [{'summary_text': ' America has changed dramatically during recent years . The '
#                   'number of engineering graduates in the U.S. has declined in '
#                   'traditional engineering disciplines such as mechanical, civil '
#                   ', electrical, chemical, and aeronautical engineering . Rapidly '
#                   'developing economies such as China and India, as well as other '
#                   'industrial countries in Europe and Asia, continue to encourage '
#                   'and advance engineering .'}]
```

### Translation

```python
from transformers import pipeline
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
translator("Ce cours est produit par Hugging Face.")
# [{'translation_text': 'This course is produced by Hugging Face.'}]
```

### summary

| Model           | Examples                                   | Tasks                                                        |
| --------------- | ------------------------------------------ | ------------------------------------------------------------ |
| Encoder         | ALBERT, BERT, DistilBERT, ELECTRA, RoBERTa | Sentence classification, named entity recognition, extractive question answering |
| Decoder         | CTRL, GPT, GPT-2, Transformer XL           | Text generation                                              |
| Encoder-decoder | BART, T5, Marian, mBART                    | Summarization, translation, generative question answering    |

## Tokenizer

与其他神经网络一样，Transformer模型不能直接处理原始文本，因此首先需要将文本输入转换成模型能够理解的数字形式。Tokenizer可以完成该工作，具体为：

+ 将输入文本分割成单词，子词或符号等，我们称之为token
+ 将每个token映射到一个整数
+ 添加一些额外的对模型有用的输入

```
from_pretrained() and save_pretrained() will load or save the algorithm used by the tokenizer (a bit like the architecture of the model) as well as its vocabulary (a bit like the weights of the model).
```

### 加载和保存

```python
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
# =====
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

tokenizer("Using a Transformer network is simple", return_tensors="pt")
# return_tensors：指定要返回的张量类型
# {'input_ids': [101, 7993, 170, 11303, 1200, 2443, 1110, 3014, 102],
#  'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0],
#  'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1]}
tokenizer.save_pretrained("directory_on_my_computer")
```

### 编码

编码是指将文本转化成数字，它包含两个步骤：

1. Tokenization

   将文本分割成token(words, parts of words or punctuation symbols, etc.)，使用分词器时需要指定模型的名称。

   ```python
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
   sequence = "Using a Transformer network is simple"
   tokens = tokenizer.tokenize(sequence)
   print(tokens)
   # ['Using', 'a', 'transform', '##er', 'network', 'is', 'simple']
   ```

2. From tokens to input IDs

   使用词汇表(vocabulary)进行转换。

   ```python
   ids = tokenizer.convert_tokens_to_ids(tokens)
   print(ids)
   # [7993, 170, 11303, 1200, 2443, 1110, 3014]
   ```

使用tokenizer会自动添加开始和结束标志

```python
sequence = "I've been waiting for a HuggingFace course my whole life."
model_inputs = tokenizer(sequence)
print(tokenizer.decode(model_inputs["input_ids"]))
# "[CLS] i've been waiting for a huggingface course my whole life. [SEP]"
tokens = tokenizer.tokenize(sequence)
ids = tokenizer.convert_tokens_to_ids(tokens)
print(tokenizer.decode(ids))
# "i've been waiting for a huggingface course my whole life."
```

### 解码

编码的逆运算，将数字转化成文本

```python
decoded_string = tokenizer.decode([7993, 170, 11303, 1200, 2443, 1110, 3014])
print(decoded_string)
# 'Using a Transformer network is simple'
```

### 裁剪和填充

```python
raw_inputs = [
    "I've been waiting for a HuggingFace course my whole life.", 
    "I hate this so much!",
]
inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
print(inputs)
"""{
    'input_ids': tensor([
        [  101,  1045,  1005,  2310,  2042,  3403,  2005,  1037, 17662, 12172, 2607,  2026,  2878,  2166,  1012,   102],
        [  101,  1045,  5223,  2023,  2061,  2172,   999,   102,     0,     0,     0,     0,     0,     0,     0,     0]
    ]), 
    'attention_mask': tensor([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
}"""
```

`padding=True`可以对短的句子进行填充，并自动生成attention_mask

填充的数据为`tokenizer.pad_token_id`

attention_mask是与input_ids形状完全相同的张量，用0和1填充：1表示应注意相应的token，0表示不应注意相应的token

对于Transformer模型，输入长度是有限的，一般为512或1024个token，`truncation=True`可以对超出长度的句子进行裁剪。

`max_length`用于指定paddding和truncation的长度，缺省时采用模型的默认配置。

### 句子对

在处理句子相关性任务时，不能分开输入两个句子，而是将其作为一个句子对进行输入。`token_type_ids`用于区分前后两个句子。

```python
inputs = tokenizer("This is the first sentence.", "This is the second one.")
print(inputs)
"""{ 
  'input_ids': [101, 2023, 2003, 1996, 2034, 6251, 1012, 102, 2023, 2003, 1996, 2117, 2028, 1012, 102],
  'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
  'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}"""
print(tokenizer.convert_ids_to_tokens(inputs["input_ids"]))
# ['[CLS]', 'this', 'is', 'the', 'first', 'sentence', '.', '[SEP]', 'this', 'is', 'the', 'second', 'one', '.', '[SEP]']

tokenized_dataset = tokenizer(
    raw_datasets["train"]["sentence1"],
    raw_datasets["train"]["sentence2"],
    padding=True,
    truncation=True,
)
```

## Model

`AutoModel`类可以从checkpoint实例化任何模型。

```python
from transformers import AutoModel
checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModel.from_pretrained(checkpoint)
```

### 创建一个Transformer

首先需要加载配置对象，配置中包含了构建模型需要的配置。使用`BertConfig`加载的模型中的参数是随机初始化的，使用`from_pretrained`加载训练好的模型。

#### 不同的加载方法

```python
from transformers import BertConfig, BertModel
# Building the config
config = BertConfig()
# Building the model from the config
model = BertModel(config)
# Model is randomly initialized!

model = BertModel.from_pretrained("bert-base-cased")
# This model is now initialized with all the weights of the checkpoint
```

#### 保存方法

```python
model.save_pretrained("directory_on_my_computer")
```

这个方法保存两个文件：

+ `config.json`包含构建模型需要的属性，以及一些元数据如checkpoint的来源和保存时Transformers的版本等。
+ `pytorch_model.bin`包含模型权重

### 使用Transformer模型进行推理

使用tensors作为模型输入

```python
import torch
sequences = ["Hello!", "Cool.", "Nice!"]
encoded_sequences = [
  [ 101, 7592,  999,  102],
  [ 101, 4658, 1012,  102],
  [ 101, 3835,  999,  102]
]
model_inputs = torch.tensor(encoded_sequences)
output = model(model_inputs)
```

## From tokenizer to model

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
sequences = [
  "I've been waiting for a HuggingFace course my whole life.",
  "So have I!"
]
tokens = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")
output = model(**tokens)
```

Transformers包括许多不同的结构，每一个都针对一个具体任务。

- `*Model` (retrieve the hidden states)
- `*ForCausalLM`
- `*ForMaskedLM`
- `*ForMultipleChoice`
- `*ForQuestionAnswering`
- `*ForSequenceClassification`
- `*ForTokenClassification`
- and others

## Processing the data

### 训练模型

```python
import torch
from transformers import AdamW, AutoTokenizer, AutoModelForSequenceClassification

checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
sequences = [
    "I've been waiting for a HuggingFace course my whole life.",
    "This course is amazing!",
]
batch = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")
batch["labels"] = torch.tensor([1, 1])

optimizer = AdamW(model.parameters())
loss = model(**batch).loss
loss.backward()
optimizer.step()
```

### 从Hub上加载数据集

datasets库可以从Hub上下载和缓存数据集，默认缓存路径为`~/.cache/huggingface/dataset`

```python
from datasets import load_dataset
raw_datasets = load_dataset("glue", "mrpc")
print(raw_datasets)
"""DatasetDict({
    train: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 3668
    })
    validation: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 408
    })
    test: Dataset({
        features: ['sentence1', 'sentence2', 'label', 'idx'],
        num_rows: 1725
    })
})"""
raw_train_dataset = raw_datasets["train"]
print(raw_train_dataset[0])
"""{'idx': 0,
 'label': 1,
 'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
 'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .'}"""
print(raw_train_dataset.features)
"""{'sentence1': Value(dtype='string', id=None),
 'sentence2': Value(dtype='string', id=None),
 'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
 'idx': Value(dtype='int32', id=None)}"""
```

### 预处理数据集

我们不能对数据集中的数据直接使用`tokenizer`方法，因为该方法会将数据全部加载进内存。因此使用`Dataset.map`方法将数据生成数据集，该方法的第一个参数为一个函数，在map时可以对数据集中的每个元素使用该函数。

```python
def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
print(tokenized_datasets)
"""DatasetDict({
    train: Dataset({
        features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
        num_rows: 3668
    })
    validation: Dataset({
        features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
        num_rows: 408
    })
    test: Dataset({
        features: ['attention_mask', 'idx', 'input_ids', 'label', 'sentence1', 'sentence2', 'token_type_ids'],
        num_rows: 1725
    })
})"""
```

### 动态填充

使用`DataCollatorWithPadding`进行动态填充，参数为`tokenizer`用于获取填充信息(要使用哪个填充标记，以及模型希望填充是在输入的左侧还是右侧)

```python
from transformers import DataCollatorWithPadding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

samples = tokenized_datasets["train"][:8]
samples = {k: v for k, v in samples.items() if k not in ["idx", "sentence1", "sentence2"]}
print([len(x) for x in samples["input_ids"]])
# [50, 59, 47, 67, 59, 50, 62, 32] 最长为67
batch = data_collator(samples)
print({k: v.shape for k, v in batch.items()})
# {'attention_mask': torch.Size([8, 67]),
#  'input_ids': torch.Size([8, 67]),
#  'token_type_ids': torch.Size([8, 67]),
#  'labels': torch.Size([8])}
```

## Trainer

### 训练

`Trainer`用于微调模型，首先需要定义`TrainingArguments`类，这个类包括了训练和验证时需要使用的超参数。

```python
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding
from transformers import TrainingArguments
from transformers import AutoModelForSequenceClassification
from transformers import Trainer

raw_datasets = load_dataset("glue", "mrpc")
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
training_args = TrainingArguments(
    "test-trainer",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epoch=5,
    learning_rate=2e-5,
    weight_decay=0.01,
)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)
trainer.train()
```

开始训练后，每500步会汇报一次训练损失，但不会评价模型的好坏，因为：

1. 没有设置`evaluation_strategy`为"steps"(每`eval_steps`验证一次)或"epoch"(每个epoch验证一次)
2. 没有提供`compute_metrics`函数来评估训练结果。

### 验证

`Trainer.predict`用于获取模型的预测结果。`compute_metrics`函数需要以一个`EvalPrediction`对象(which is a named tuple with a `predictions` field and a `label_ids` field)作为输入，返回预测的内容及其结果。

```python
predictions = trainer.predict(tokenized_datasets["validation"])
print(predictions.predictions.shape, predictions.label_ids.shape)
# (408, 2) (408,)
```

`predict`函数的输出是一个命名元祖，包括三个字段：`predictions`、`label_ids`和`metrics`。`metrics`字段包括损失、计算总时间和平均时间等内容。

`load_metric`函数方便我们构造损失函数。

```python
import numpy as np
preds = np.argmax(predictions.predictions, axis=-1)
from datasets import load_metric
metric = load_metric("glue", "mrpc")
print(metric.compute(predictions=preds, references=predictions.label_ids))
# {'accuracy': 0.8578431372549019, 'f1': 0.8996539792387542}
```

现在，可以构建`compute_metrics`函数，在每个epoch后汇报训练情况。

```python
def compute_metrics(eval_preds):
    metric = load_metric("glue", "mrpc")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments("test-trainer", evaluation_strategy="epoch")
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
trainer = Trainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)
```

## A full training without Trainer

在定义定义DataLoader之前首先需要修改dataset中的一些字段。

```python
tokenized_datasets = tokenized_datasets.remove_cloumns(["idx", "sentence1", "sentence2"])
tokenized_datasets = tokenized_datasets.rename_cloumn("label", "labels")
tokenized_datasets = tokenized_datasets.with_format("torch")
print(tokenized_datasets["train"])
"""DatasetDict({
    features: ['attention_mask', 'input_ids', 'labels', token_type_ids'],
    num_rows: 3668
})"""
small_train_dataset = tokenized_datasets["train"].select(range(100))

from torch.utils.data import DataLoader
train_dataloader = DataLoader(
    tokenized_datasets["train"], shuffle=True, batch_size=8, collate_fn=data_collator
)
eval_dataloader = DataLoader(
    tokenized_datasets["validation"], batch_size=8, collate_fn=data_collator
)
for batch in train_dataloader:
    break
print({k: v.shape for k, v in batch.items()})
# {'attention_mask': torch.Size([8, 65]),
#  'input_ids': torch.Size([8, 65]),
#  'labels': torch.Size([8]),
#  'token_type_ids': torch.Size([8, 65])}
```

### 训练

```python
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification
from transformers import AdamW
from transformers import get_scheduler
import torch
from tqdm.auto import tqdm

raw_datasets = load_dataset("glue", "mrpc")
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
def tokenize_function(example):
    return tokenizer(example["sentence1"], example["sentence2"], truncation=True)
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
tokenized_datasets = tokenized_datasets.remove_cloumns(["idx", "sentence1", "sentence2"])
tokenized_datasets = tokenized_datasets.rename_cloumn("label", "labels")
tokenized_datasets = tokenized_datasets.with_format("torch")

train_dataloader = DataLoader(
    tokenized_datasets["train"], shuffle=True, batch_size=8, collate_fn=data_collator
)
eval_dataloader = DataLoader(
    tokenized_datasets["validation"], batch_size=8, collate_fn=data_collator
)

model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
optimizer = AdamW(model.parameters(), lr=5e-5)

num_epochs = 3
num_training_steps = num_epochs * len(train_dataloader)
lr_scheduler = get_scheduler(
    "linear",
    optimizer=optimizer,
    num_warmup_steps=0,
    num_training_steps=num_training_steps
)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)
progress_bar = tqdm(range(num_training_steps))

model.train()
for epoch in range(num_epochs):
    for batch in train_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        
        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
        progress_bar.update(1)
```

### 验证

```python
from datasets import load_metric

metric= load_metric("glue", "mrpc")
model.eval()
for batch in eval_dataloader:
    batch = {k: v.to(device) for k, v in batch.items()}
    with torch.no_grad():
        outputs = model(**batch)
    
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)
    metric.add_batch(predictions=predictions, references=batch["labels"])

metric.compute()
```

### 加速

使用`Accelerate`库可以在多GPU上分布式训练。

```diff
+ from accelerate import Accelerator
  from transformers import AdamW, AutoModelForSequenceClassification, get_scheduler

+ accelerator = Accelerator()

  model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
  optimizer = AdamW(model.parameters(), lr=3e-5)

- device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
- model.to(device)

+ train_dataloader, eval_dataloader, model, optimizer = accelerator.prepare(
+     train_dataloader, eval_dataloader, model, optimizer
+ )

  num_epochs = 3
  num_training_steps = num_epochs * len(train_dataloader)
  lr_scheduler = get_scheduler(
      "linear",
      optimizer=optimizer,
      num_warmup_steps=0,
      num_training_steps=num_training_steps
  )

  progress_bar = tqdm(range(num_training_steps))

  model.train()
  for epoch in range(num_epochs):
      for batch in train_dataloader:
-         batch = {k: v.to(device) for k, v in batch.items()}
          outputs = model(**batch)
          loss = outputs.loss
-         loss.backward()
+         accelerator.backward(loss)

          optimizer.step()
          lr_scheduler.step()
          optimizer.zero_grad()
          progress_bar.update(1)
```

`accelerator.prepare`将象包装在适当的容器中，以确保分布式训练按预期工作。

#### 启动加速的方法

+ 脚本方法：将所有代码放入`train.py`，运行命令`accelerate config`进行相关配置然后运行命令`accelerate launch train.py`启动训练。

+ notebook方法：

  ```python
  from accelerate import notebook_launcher
  notebook_launcher(training_function)
  ```