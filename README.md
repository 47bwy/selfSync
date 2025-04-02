# 47bwy 的学习之路


### 本电子书制作和写作方式
使用 mkdocs 和 markdown 构建，vim 编写，使用  Python-Markdown-Math 完成数学公式。
markdown 语法参考：http://xianbai.me/learn-md/article/about/readme.html

安装依赖：
```sh
requirements.txt

使用 pipenv 安装
```

编写并查看：
```sh
mkdocs serve     # 修改自动刷新浏览器，浏览器打开 http://localhost:8000 访问
# 数学公式参考 https://www.zybuluo.com/codeep/note/163962
# 图片最好压缩再放到仓库(不过不建议放非文本文件)
mkdocs gh-deploy    # 部署到自己的 github pages, 如果是 readthedocs 会自动触发构建
```

### 访问:

[https://47bwy.readthedocs.io/en/latest/](https://47bwy.readthedocs.io/en/latest/)

[https://47bwy.github.io/selfSync/](https://47bwy.github.io/selfSync/)
