import requests
from bs4 import BeautifulSoup
import os
import threading
import pandas as pd
import re
from queue import Queue


# 清理文件名中的非法字符
def clean_filename(title):
    illegal_chars = r'[\\/:*?"<>|]'
    return re.sub(illegal_chars, '', title)


# 下载文献的函数
def download_paper(doi_title_queue, success_log, error_log, failed_dois, sci_hub_domains, head, download_folder):
    while not doi_title_queue.empty():
        doi, title = doi_title_queue.get()  # 从队列中获取 DOI 和标题

        if not doi:  # 如果 DOI 为空
            error_log.append(f"{title}\t没有 DOI。\n")  # 记录没有 DOI 的文献
            failed_dois.append((title, 'No DOI'))  # 将没有 DOI 的文献标题和说明记录到 failed_dois 中
            doi_title_queue.task_done()  # 任务完成
            continue  # 跳过这篇文献

        download_url = None
        for domain in sci_hub_domains:
            url = domain + doi + "#"
            try:
                r = requests.get(url, headers=head, timeout=15)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")

                if soup.iframe is None and soup.embed:
                    download_url = "https:" + soup.embed.attrs.get("src", "")
                elif soup.iframe:
                    download_url = soup.iframe.attrs.get("src", "")

                if download_url:
                    print(f"{doi}\t正在下载\n下载链接为\t" + download_url)
                    download_r = requests.get(download_url, headers=head, timeout=15)
                    download_r.raise_for_status()

                    file_name = clean_filename(title) + ".pdf"
                    file_path = os.path.join(download_folder, file_name)
                    with open(file_path, "wb+") as temp:
                        temp.write(download_r.content)

                    success_log.append(f"{doi}\t下载成功.\n")
                    print(f"{doi}\t文献下载成功.\n")
                    break

            except requests.exceptions.RequestException as e:
                error_log.append(f"{doi}\t下载失败! 错误信息: {str(e)}\n")
                continue

        if not download_url:
            error_log.append(f"{doi}\t下载失败! 无法从任何Sci-Hub域名获取文献.\n")
            failed_dois.append((title, doi))  # 将失败的文献标题和 DOI 记录到 failed_dois 中
        doi_title_queue.task_done()


def main():
    # 配置变量
    xls_file = './xls_folder/savedrecs.xls'
    download_folder = './download_papers/'
    sci_hub_domains = [
        "https://www.sci-hub.ren/",
        "https://sci-hub.hk/",
        "https://sci-hub.se/",
        "https://sci-hub.st/",
        "https://sci-hub.la/",
        "https://sci-hub.cat/",
        "https://sci-hub.ee/",
        "https://www.tesble.com/"
    ]
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    num_threads = 5

    # 创建保存下载文件的文件夹
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # 读取Excel文件
    df = pd.read_excel(xls_file)

    # 提取DOI列和文献标题列
    doi_list = df['DOI'].dropna().tolist()
    titles = df['Article Title'].dropna().tolist()

    # 创建一个线程安全的队列
    doi_title_queue = Queue()

    # 将 DOI 和标题一一对应地放入队列中
    for doi, title in zip(doi_list, titles):
        doi_title_queue.put((doi, title))

    # 成功与失败的记录
    success_log = []
    error_log = []
    failed_dois = []  # 使用列表来存储失败的 DOI 和文献标题

    # 启动多线程下载文献
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=download_paper, args=(
        doi_title_queue, success_log, error_log, failed_dois, sci_hub_domains, head, download_folder))
        threads.append(t)

    # 启动所有线程
    for t in threads:
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    # 记录成功和失败的日志
    with open(os.path.join("./download_log.txt"), "w", encoding="utf-8") as log_file:
        log_file.write("成功下载的DOI：\n")
        log_file.writelines(success_log)
        log_file.write("\n下载失败的DOI：\n")
        log_file.writelines(error_log)

    # 输出下载失败的文献（包括没有 DOI 的文献）
    with open(os.path.join("./failed_dois.txt"), "w", encoding="utf-8") as failed_file:
        failed_file.write("以下DOI下载失败，请手动检查资源：\n")
        for title, doi in failed_dois:
            if doi == 'No DOI':
                failed_file.write(f"{title}\t没有 DOI\n")  # 没有 DOI 的文献
            else:
                failed_file.write(f"{title}\t{doi}\n")  # 有 DOI 但下载失败的文献

    print("所有任务完成！")


# 确保脚本只有在作为主程序运行时才执行下载操作
if __name__ == '__main__':
    main()
