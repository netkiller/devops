# 禅道集成

## 已存在项目

```bash
    curl -s https://raw.githubusercontent.com/netkiller/devops/master/share/git/hooks/commit-msg -o .git/hooks/commit-msg
    chmod +x .git/hooks/commit-msg
    pip3 install requests
```

## 配置模版目录

```bash
    mkdir -p ~/workspace/template/hooks
    curl -s https://raw.githubusercontent.com/netkiller/devops/master/share/git/hooks/commit-msg -o ~/workspace/template/hooks/commit-msg
    git config --global init.templatedir ~/workspace/template/
```

## Windows 系统


1. 安装 Python 

    下载地址，安装到 C:\Python 目录下

    https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe

    Window 11 也可以使用 Winget 安装

    winget install python

    安装完成之后安装依赖包

    pip3 install requests
        
1. 已存在项目安装 Script

    ```powershell
    powershell curl -o .git/hooks/commit-msg https://raw.githubusercontent.com/netkiller/devops/master/share/git/hooks/commit-msg 
    ```

1. 设置模板

    ```powershell
    mkdir c:\workspace\template\hooks
    powershell curl -o c:\workspace\template\hooks\commit-msg https://raw.githubusercontent.com/netkiller/devops/master/share/git/hooks/commit-msg 
    git config --global init.templatedir c:\workspace\template
    git config -l
    ```

## 使用方法

    代码提交时，提交信息这样写：

    BUG 1234

    如果本次提交代码修复了多个 BUG 这样写：

    BUG 123 456 789

    如果是需求，这样写：
    
    TASK 123
