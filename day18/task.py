# 同步版本
def process_urls(urls):
    results = []
    for url in urls:
        data = fetch(url)  # 模拟网络请求
        processed = process(data)
        results.append(processed)
    return results

# TODO: 改写为异步版本
