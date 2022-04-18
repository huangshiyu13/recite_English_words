# recite_English_words


## 简介

本库旨在生成每天需要背诵的单词并记录背诵进度。单词按照使用频率进行排序，也就是说，越靠前的单词其在文献中出现的频率越高。这样背单词，可以让人**优先掌握更常用的单词**。

## 使用方法

- 执行`python gen_voc.py`来生成当日需要背诵的单词表。打开`每次单词表.xlsx`进行单词背诵。如果该单词为熟悉单词，则在Mark那一列标记1，那么以后该单词将不会出现。可以在`python gen_voc.py`中修改`word_num_per_day`变量来指定每天需要背诵的单词数量（默认为50）。

## 文件描述

- `word_list.xlsx`: 词库文件。该单词表中一共包含24056个英文单词，并按照单词使用频率进行排序。一般来说，背完该词库全部单词，能达到英语国家当地大学生的水平。
- `u_log.txt`: 用于记录背诵进度。每次代码会根据该记录文件生成当天需要背诵的单词。当背完一遍单词，想重新背第二遍的时候，只用删除`u_log.txt`文件即可，代码便又会从头开始生成每日的单词表。
- `ignore_words.txt`: 用于被标记为熟知的单词，以便以后不再出现。每次生成新的`每次单词表.xlsx`时，会检查旧的`每次单词表.xlsx`，把旧的`每次单词表.xlsx`中标记为熟知(也就是Mark处标记为1)的单词加入`ignore_words.txt`。
- `u_log.png`: 单词背诵曲线。在执行`python gen_voc.py`的时候，检测到有`u_log.txt`文件，会自动画出单词背诵曲线。

## 更新词库文件的方法

首先，需要Windos系统上装有网易有道词典，然后把单词加入有道词典的单词本，然后以`xml`的格式导出单词本，并取名叫做`youdao.xml`，然后放入当前仓库中。

然后执行`python update_world_list.py`，便可以生成新的词库文件`word_list.xlsx`。


## More

欢迎大家提供更完整的`word_list.xlsx`，提出改进或者开发GUI界面。



## Citing recite_English_words

If you use recite_English_words in your work, please cite us:

```bibtex
@article{huangshiyu2022recite,
    title={Recite English Words},
    author={Shiyu Huang},
    year={2022},
    howpublished={\url{https://github.com/huangshiyu13/recite_English_words}},
}
```
