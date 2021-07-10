# git相关操作

`git init` 将当前目录变成git可以管理的目录(生成 .git)

`git add`、`git commit -m` 将文件添加到版本库

`git status` 查看版状态

+ 未add： untracked files(新文件)、changes not staged for commit
+ add但未commit： changes to be committed
+ committed： nothing to commit，working tree clean

![状态图](状态图.png)

`git reset --hard HEAD^ (HEAD~x)` 版本回退

`git log` 查看题解历史

`git reflog` 查看历史命令

`git checkout --file` 丢弃工作区的修改(若暂存区有提交，则撤回到暂存区，否则撤回到版本库)

`git reset HEAD <file>` 丢弃暂存区的修改

`git rm` 删除暂存区的文件

`git remote add origin git@github.com:...` 将本地仓库与远程仓库关联(若已有关联`git remote rm origin`)

`git push -u origin master` 将本地库内容推送到远程库(加了-u后，以后可以用git push代替git push origin master)

`git branch <branch name>` 创建分支

`git checkout <branch name>` 切换分支

`git checkout -b <branch name>` 创建并切换分支

`git merge <branch name>` 快速合并分支

`git branch -d <branch name>` 删除分支

git无法自动合并分支时，首先需要解决冲突，即把合并失败的文件手动编辑为我们希望的内容

`git log --graph` 查看分支合并图

`git stash save "save message"`储存当前工作现场(该操作后工作区是clean的)，执行存储时，添加备注，方便查找，只有git stash 也要可以的，但查找时不方便识别。

`git stash list` 查看stash了哪些存储

`git stash show` 显示做了哪些改动，默认show第一个存储,如果要显示其他存贮，后面加stash@{$num}，比如第二个 git stash show stash@{1}

`git stash show -p` 显示第一个存储的改动，如果想显示其他存存储，命令：git stash show stash@{$num} -p ，比如第二个：git stash show stash@{1} -p

`git stash apply` 应用某个存储,但不会把存储从存储列表中删除，默认使用第一个存储,即stash@{0}，如果要使用其他个，git stash apply stash@{$num} ， 比如第二个：git stash apply stash@{1} 

`git stash pop` 命令恢复之前缓存的工作目录，将缓存堆栈中的对应stash删除，并将对应修改应用到当前的工作目录下,默认为第一个stash,即stash@{0}，如果要应用并删除其他stash，命令：git stash pop stash@{$num} ，比如应用并删除第二个：git stash pop stash@{1}

`git stash drop stash@{\$num}` 丢弃stash@{\$num}存储，从列表中删除这个存储

`git stash clear` 删除所有缓存的stash

`git cherry-pick <commit_id>` 复制一个特定的修改提交到当前分支

**多人协作：**

`git clone` (只克隆master)

`git pull`

`git checkout -b <name> origin/<name>`

修改后提交，如果有冲突，先pull，本地合并后提交，如果pull失败，需要建立本地分支与远程分支的连接：`git branch --set-upstream-to=origin/<name> <name>`

**从github上clone某个文件夹**

```shell
# 创建一个空的本地仓库，同时将远程Git Server URL加入到Git Config文件中。
$ mkdir project_folder
$ cd project_folder
$ git init
$ git remote add -f origin <url>
# 在Config中允许使用Sparse Checkout模式
$ git config core.sparsecheckout true
# 将想Check Out的文件夹保存在.git/info/sparse-checkout
$ echo "<file_path>"  >> .git/info/sparse-checkout
$ git pull origin master
```

