# Docker

## 在本地使用镜像

`docker pull` 从docker hub下载镜像

`docker images` 查看所有已下载镜像

`docker create -it --name my_container image_id /bin/bash` 创建容器(默认关闭)

+ -i 交互式命令行
+ -t 将交互式命令行绑定到一个虚拟终端上
+ /bin/bash 交互式采用shell虚拟终端

`docker ps -a` 查看已经创建的容器

`docker start -ai my_container` create创建的容器默认是关闭状态，需要用下面的命令进入

`exit` 退出容器

`docker run -dit --name=my_container image_id /bin/bash` 创建容器(默认开启)

+ -d 守护容器，容器当中的程序需要长期运行，创建一个守护容器

`docker exec -it my_container /bin/bash` 切入一个已启动的容器

`docker container stop container_id` 停止容器

`docker container kill container_id` 杀死结束进程

`docker container rm container_id` 删除容器，只能删除关闭状态的容器

## 将镜像上传到docker hub

`docker login` 登录docker hub

`docker commit container_id image_name` 把所需上传的容器变为镜像

+ container_id为需要上传的容器id

`docker tag image_name docker_user_name/xxx[:tag]` 为存在于本地的镜像打标签

+ docker_user_name为docker hub的登录名，xxx为仓库名
+ tag不指定就是latest

`docker push docker_user_name/xxx[:tag]` 上传镜像

