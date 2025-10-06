from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin

BASE_URL = "https://172.lot-ml.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# 国内省份列表（包含全称和简称）
PROVINCES = [
    "北京市", "北京", "天津市", "天津", "河北省", "河北", "山西省", "山西",
    "内蒙古自治区", "内蒙古", "辽宁省", "辽宁", "吉林省", "吉林", "黑龙江省", "黑龙江",
    "上海市", "上海", "江苏省", "江苏", "浙江省", "浙江", "安徽省", "安徽",
    "福建省", "福建", "江西省", "江西", "山东省", "山东", "河南省", "河南",
    "湖北省", "湖北", "湖南省", "湖南", "广东省", "广东", "广西壮族自治区", "广西",
    "海南省", "海南", "重庆市", "重庆", "四川省", "四川", "贵州省", "贵州",
    "云南省", "云南", "西藏自治区", "西藏", "陕西省", "陕西", "甘肃省", "甘肃",
    "青海省", "青海", "宁夏回族自治区", "宁夏", "新疆维吾尔自治区", "新疆",
    "香港特别行政区", "香港", "澳门特别行政区", "澳门", "台湾省", "台湾"
]

# 运营商关键词（核心匹配词）
OPERATORS = ["移动", "联通", "广电"]


def get_all_products(keyword, llkshop_id='3abcd2e80b9b4694'):
    # 处理运营商关键词（提取核心词，如"移动卡"→"移动"）
    core_keyword = keyword
    for op in OPERATORS:
        if op in keyword:
            core_keyword = op  # 提取运营商核心词作为匹配依据
            break
    
    # 判断关键词类型并选择对应的页面路径
    is_number = bool(re.search(r'\d', keyword))
    keyword_lower = keyword.lower()
    is_province = any(p.lower() == keyword_lower for p in PROVINCES)
    
    # 根据关键词类型和llkshop_id动态构建路径
    if is_province:
        path = f"/producten/tyindex/{llkshop_id}"
    else:
        path = f"/ProductEn/Index/{llkshop_id}"
    
    try:
        response = requests.get(urljoin(BASE_URL, path), headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"请求失败: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    all_products = []
    seen_links = set()
    seen_names = set()  # 名称去重容器
    
    # 精确锁定产品列表（根据实际页面结构调整选择器）
    product_containers = soup.select('div.new_lst')
    
    for container in product_containers:
        for li in container.select('ul.fa > li'):
            h1 = li.find('h1')
            if not h1:
                continue
            
            # 名称模糊匹配（使用处理后的核心关键词）
            product_name = h1.get_text(strip=True)
            # 对运营商关键词进行宽松匹配，只要产品名包含核心运营商名称即可
            if not re.search(re.escape(core_keyword), product_name, re.I):
                continue
            
            # 关键去重逻辑
            if product_name in seen_names:
                continue
            seen_names.add(product_name)
            
            # 链接处理
            a_tag = li.find('a')
            if not a_tag or not a_tag.get('href'):
                continue
            detail_link = urljoin(BASE_URL, a_tag['href'])
            if detail_link in seen_links:
                continue
            seen_links.add(detail_link)
            
            all_products.append({
                "element": li,
                "detail_link": detail_link
            })
    
    return all_products

# 数据提取函数
def extract_product_data(product_li):
    # 提取基础信息
    img_tag = product_li.find('dt').find('img')
    product_name = product_li.find('h1').get_text(strip=True)
    
    # 处理主推/年龄/领取人数
    b1_div = product_li.find('div', class_='b1')
    zhutui = '是' if b1_div.find('span', class_='zhutui') else '否'
    age_span = b1_div.find('span', class_='xl')
    receive_span = b1_div.find('span', class_='yr')
    
    # 流量信息处理
    flow_data = {"通用流量": "0G", "定向流量": "0G", "通话时长": "0分钟", "适用年龄": "年龄不限"}
    b2_div = product_li.find('div', class_='b2')
    if b2_div:
        for span in b2_div.find_all('span'):
            text = span.get_text(strip=True)
            if '通用流量' in text:
                flow_data['通用流量'] = text.split()[-1]
            elif '定向流量' in text:
                flow_data['定向流量'] = text.split()[-1]
            elif '通话时长' in text:
                flow_data['通话时长'] = text.split()[-1]
    b1_div = product_li.find('div', class_='b1')
    if b1_div:
        xl_span = b1_div.find('span', class_='xl')
        if xl_span:
            flow_data['适用年龄'] = xl_span.get_text(strip=True)
    return {
        "md图片":f"![图片]({urljoin(BASE_URL, img_tag['src']) if img_tag else None})",
        "产品名称": product_name,
        **flow_data
    }

# 主函数供外部调用
def search_data_cards(keyword="19元", llkshop_id='3abcd2e80b9b4694'):
    matched_products = get_all_products(keyword, llkshop_id)
    results = []
    
    if not matched_products:
        return {
            "success": False,
            "message": f"未找到包含 '{keyword}' 的产品",
            "shop_link": f"https://172.lot-ml.com/ProductEn/Index/{llkshop_id}",
            "command_info": "流量卡< $元 > 例如：流量卡9元\n流量卡< 省 > 例如：流量卡广东",
            "results": []
        }
    else:
        # 提取并展示详细信息
        for product in matched_products:
            data = extract_product_data(product["element"])
            data["详情链接"] = product["detail_link"]
            results.append(data)
        
        return {
            "success": True,
            "total_count": len(matched_products),
            "keyword": keyword,
            "shop_link": f"https://172.lot-ml.com/ProductEn/Index/{llkshop_id}",
            "command_info": "流量卡<$元> 例如：流量卡9元\n流量卡<省> 例如：流量卡广东",
            "results": results
        }