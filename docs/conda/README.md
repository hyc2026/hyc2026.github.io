# conda

`conda env list` 列出当前已经创建的python环境

`conda create -n my_py_env python=3.6.2` 创建python环境

`conda create --prefix="D:\\my_python\\envs\\my_py_env"  python=3.6.3` 指定路径下创建python环境

`activate my_py_env` win进入环境

`source activate my_py_env` linux进入环境

`deactivate` win退出环境

`source deactivate` linux退出环境

`conda install -n my_py_env package_name` 安装包

`conda uninstall -n my_py_env package_name` 删除包

`conda remove -n my_py_env --all` 删除环境

**PackagesNotFoundError:**

+ `anaconda search -t conda packname`
+ ``conda install -c <url> packname`