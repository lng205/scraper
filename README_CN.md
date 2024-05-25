# StackOverflow 爬虫

这是一个通用的网页爬虫框架，用于从 StackOverflow 网站提取问题和答案。它使用 BeautifulSoup 库来解析 HTML 并提取所需的信息。

## 安装

1. 克隆仓库：
   ```bash
   git clone <repository-url>
   ```
2. 安装所需的包：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 步骤1：爬取

第一步是爬取网页并将其本地保存，以避免多次请求网站而被封禁。

#### 获取初始 Cookie

1. 访问 StackOverflow 网站并登录。
2. 访问目标页面并使用浏览器开发者工具（F12）检查网络请求。
3. 从浏览器中提取请求的 Cookie 和头信息。

   一种提取 Cookie 的方法：
   ![Cookies 提取](image/cookies.png)
   - 将 cURL 命令粘贴到 [curlconverter.com/python](https://curlconverter.com/python/)
   - 将 Cookie 保存到 `scrape.py` 文件中的 `initial_cookies` 变量中。

#### 爬取问题

1. 取消注释 `scrape.py` 文件中的以下行：
   ```python
   scrape_questions(initial_cookies, headers, range(1, 200), 'pytorch')
   ```
   - `range` 指定要爬取的页面范围。
   - `'pytorch'` 是要搜索的查询。

2. 运行爬虫：
   ```bash
   python scrape.py
   ```

3. 爬取的数据将保存在 `pages` 文件夹中。

#### 爬取内容

1. 取消注释 `scrape.py` 文件中的以下行：
   ```python
   scrape_contents(initial_cookies, headers)
   ```

#### 处理封禁

- 如果程序打印"ip blocked"消息，请使用代理更改 IP 地址。
- 如果遇到验证码，请手动更新 Cookie 和头信息。

### 步骤2：解析

第二步是解析并提取保存的响应中的所需信息。

1. 运行解析器：
   ```bash
   python parse.py
   ```

2. 解析的数据将存储在 SQL 数据库中，以便进一步分析。

### 步骤3：导出

1. 运行导出器：
   ```bash
   python export.py
   ```

### 推荐的开始流程

1. 爬取前 10 页的问题
2. 解析问题并将其保存到数据库
3. 爬取问题的内容
4. 解析内容并将其保存到数据库
5. 将解析的数据导出到 CSV 文件中以便访问和分享