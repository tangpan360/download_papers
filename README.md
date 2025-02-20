## 简介
* 利用 doi 批量下载 pdf 文献。
* 只需要准备包含 ``Article Title`` 和 ``DOI`` 两列的 excel 即可。

***
github 地址：[https://github.com/tangpan360/download_papers](https://github.com/tangpan360/download_papers)
***
## 使用逻辑
1. 从 wos 导出含有文献名和 doi 的 excel 文件（savedrecs.xls），或自己按需要的格式整理成 excel；
2. 将 savedrecs.xls 放入文件夹 xls_folder 中；
3. 直接运行 download.py 即可。

## 图文展示具体步骤
### 1. 准备包含文献名和对应 doi 的 excel 文件
有两种方式都可以：从 wos 导出 excel 文件，或者自己按格式整理对应的 excel 文件。

**1. 方式一：从 wos 导出 excel**
* 进入 wos 网址：[https://webofscience.clarivate.cn/wos/alldb/basic-search](https://webofscience.clarivate.cn/wos/alldb/basic-search)

* 如下图，输入要搜索的文章：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1a48fbc2fa464c61b67fd46d5da19ed9.png)
* 检索之后可以选择多篇自己检索的文章如下图中的1，为了方便，我直接用这篇文章的 112 篇 references 来演示接下来的批量下载操作，如图中2所示点击 112：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5c110e01b4fb4e26bc4b553d338f3659.png)
* 全选之后如图所示，导出选中的 107 篇参考文献的 excel 文件（由于一些原因，存在一些文献不可选）： ![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/96f12de7199047488e8e8ab1a7004eaa.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/eecbe34880a84b3c831cab4ed5705701.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d54e93663d2643cba52790282e593b6a.png)
* 打开保存的 excel 文件 ``savedrecs.xls`` 可以看到包含 ``Article Title`` 和 ``DOI`` 两列（有其它列也无所谓，只要包含这两列即可）：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3fb6bb313ce34cd4b845058224bf44a5.png)
* 至此，所需要的 excel 文件准备完成。


**2. 方式二：自己按格式整理对应的 excel**
> 不从 wos 导出也可以使用，只需要有包含下面两列内容的 excel 文件即可。从 wos 导出的 excel 文件有很多列，因为包含这两列，所以导出之后直接可用。

| Article Title                                                                 | DOI         |
|-------------------------------------------------------------------------------|-----------------------|
| Construction of a synthetic Saccharomyces cerevisiae pan-genome neo-chromosome | 10.1038/s41467-022-31305-4 |
| Analysis of queuosine and 2-thio tRNA modifications by high throughput sequencing | 10.1093/nar/gkac517 |
| A multiplex platform for small RNA sequencing elucidates multifaceted tRNA stress response and translational regulation | 10.1038/s41467-022-30261-3 |
| De novo assembly and delivery to mouse cells of a 101 kb functional human gene | 10.1093/genetics/iyab038              |
| An isocaloric moderately high-fat diet extends lifespan in male rats and Drosophila | 10.1016/j.cmet.2020.12.017       |

***

### 2. 运行 downloader.py 程序执行批量下载

* 在终端输入命令执行代码：
	```bash
	python download.py
	```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d3373445c7ee4744ae65cc474f8c6f77.png)
* 则可以在 ``download_papers`` 文件夹中看到下载的文件：


![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/51eeb713dc184755bb94e6bfc5c2c91d.png)
* 同时还生成了下载日志以及下载失败需要手动下载的记录文件：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0392b5145216444486c56a137c198c1c.png)
### 3. 检查失败日志，进行手动下载
检查日志内容，对未下载成功的进行手动查询下载：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/2e958a38359f488289e8e07b28bf259c.png)

