# PapiHub

PapiHub = Private API Hub = 私有API中心

<a href="https://github.com/papihubcom/papihub"><img src="https://img.shields.io/github/stars/papihubcom/papihub" alt="Stars Badge"/></a>
<a href="https://github.com/papihubcom/papihub"><img src="https://img.shields.io/github/forks/papihubcom/papihub" alt="Forks Badge"/></a>
<a href="https://github.com/papihubcom/papihub"><img src="https://img.shields.io/github/issues/papihubcom/papihub" alt="Issues Badge"/></a>
<a href="https://github.com/papihubcom/papihub/blob/main/LICENSE"><img src="https://img.shields.io/github/license/papihubcom/papihub?color=2b9348" alt="License Badge"/></a>

# 背景

当前全球BT/PT站点非常多，这些站点的技术架构大多类似，但技术非常古老。如果我们想基于这些资源站点，做一些使用场景的扩展，是找不到合适的开放接口的。本项目的初始目标，既为了解决这个痛点，自动为这些资源站点提供标准化的接口，供我们二次开发，或者DIY一些场景。

# 安装

# 使用

# 开发者调试

## 安装依赖

项目根目录安装Python依赖

```shell
pip install -r requirements.txt
```

进入前端项目目录，安装前端依赖

``` shell
cd papihub-frontend
```

```yarn install``` or ```npm install```

## 设置环境变量

变量名：WORKDIR
值为你的本地路径，项目运行时路径，此路径会存放项目的数据文件。命令行或者IDE启动，都需要设置此环境变量。

## 运行入口

Python项目的运行入口在 ```papihub/main.py```

前端项目的运行入口在 ```papihub-frontend``` 目录，使用```yarn dev``` 或 ```npm dev``` 运行项目