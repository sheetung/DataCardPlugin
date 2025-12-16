import aiohttp
import re

BASE_URL = "https://172.lot-ml.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://172.lot-ml.com',
}

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

# 省份到省会城市的映射
PROVINCE_CAPITALS = {
    "北京": "北京", "北京市": "北京",
    "天津": "天津", "天津市": "天津",
    "河北": "石家庄", "河北省": "石家庄",
    "山西": "太原", "山西省": "太原",
    "内蒙古": "呼和浩特", "内蒙古自治区": "呼和浩特",
    "辽宁": "沈阳", "辽宁省": "沈阳",
    "吉林": "长春", "吉林省": "长春",
    "黑龙江": "哈尔滨", "黑龙江省": "哈尔滨",
    "上海": "上海", "上海市": "上海",
    "江苏": "南京", "江苏省": "南京",
    "浙江": "杭州", "浙江省": "杭州",
    "安徽": "合肥", "安徽省": "合肥",
    "福建": "福州", "福建省": "福州",
    "江西": "南昌", "江西省": "南昌",
    "山东": "济南", "山东省": "济南",
    "河南": "郑州", "河南省": "郑州",
    "湖北": "武汉", "湖北省": "武汉",
    "湖南": "长沙", "湖南省": "长沙",
    "广东": "广州", "广东省": "广州",
    "广西": "南宁", "广西壮族自治区": "南宁",
    "海南": "海口", "海南省": "海口",
    "重庆": "重庆", "重庆市": "重庆",
    "四川": "成都", "四川省": "成都",
    "贵州": "贵阳", "贵州省": "贵阳",
    "云南": "昆明", "云南省": "昆明",
    "西藏": "拉萨", "西藏自治区": "拉萨",
    "陕西": "西安", "陕西省": "西安",
    "甘肃": "兰州", "甘肃省": "兰州",
    "青海": "西宁", "青海省": "西宁",
    "宁夏": "银川", "宁夏回族自治区": "银川",
    "新疆": "乌鲁木齐", "新疆维吾尔自治区": "乌鲁木齐",
    "香港": "香港", "香港特别行政区": "香港",
    "澳门": "澳门", "澳门特别行政区": "澳门",
    "台湾": "台北", "台湾省": "台北"
}


async def get_all_products(keyword, llkshop_id='3abcd2e80b9b4694'):
    # 处理运营商关键词（提取核心词，如"移动卡"→"移动"）
    core_keyword = keyword
    for op in OPERATORS:
        if op in keyword:
            core_keyword = op  # 提取运营商核心词作为匹配依据
            break

    # 判断关键词类型
    keyword_lower = keyword.lower()
    is_province = any(p.lower() == keyword_lower for p in PROVINCES)

    # 构建统一的POST表单数据
    if is_province:
        # 省份搜索
        form_data = {
            "title": keyword,
            "PriceTime": "优惠时间",
            "LiuLiang": "可用流量",
            "Tonghua": "通话时长",
            "Province": keyword,
            "City": PROVINCE_CAPITALS.get(keyword, keyword)  # 获取省会城市
        }
    else:
        # 价格或其他关键词搜索
        form_data = {
            "title": keyword,
            "PriceTime": "优惠时间",
            "LiuLiang": "可用流量",
            "Tonghua": "通话时长",
            "Province": "全部",
            "City": "全部"
        }
    # print(f'form_data={form_data}')
    # 统一使用Index2端点
    url = f"{BASE_URL}/ProductEn/Index2/{llkshop_id}"

    # 为每个请求设置Referer
    request_headers = HEADERS.copy()
    request_headers['Referer'] = f"{BASE_URL}/ProductEn/Index/{llkshop_id}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form_data, headers=request_headers) as response:
                response.raise_for_status()
                json_data = await response.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return []

    # print(f'json_data={json_data}')

    # 解析JSON响应
    all_products = []
    seen_links = set()
    seen_names = set()  # 名称去重容器

    # 从JSON中获取产品列表
    products_data = json_data.get('data', [])

    for product in products_data:
        product_name = product.get('name', '')

        # 名称模糊匹配（使用处理后的核心关键词）
        if not re.search(re.escape(core_keyword), product_name, re.I):
            continue

        # 关键去重逻辑
        if product_name in seen_names:
            continue
        seen_names.add(product_name)

        # 链接处理
        detail_link = product.get('shareUrl', '')
        if not detail_link:
            continue
        if detail_link in seen_links:
            continue
        seen_links.add(detail_link)

        all_products.append({
            "product_data": product,
            "detail_link": detail_link
        })

    return all_products

# 数据提取函数
def extract_product_data(product):
    # 从JSON对象中提取字段
    img_url = product.get('path', '')
    product_name = product.get('name', '')

    # 处理主推
    zhutui = '是' if product.get('zhutui', False) else '否'

    # 流量信息处理
    ty_liuliang = product.get('tyLiuliang', '0')
    dx_liuliang = product.get('dxLiuliang', '0')
    tonghua = product.get('tonghua', '0')

    # 适用年龄
    age1 = product.get('age1', 0)
    age2 = product.get('age2', 0)
    age_range = f"{age1}-{age2}岁" if age1 and age2 else "年龄不限"

    return {
        "md图片": f"![图片]({img_url})" if img_url else "",
        "产品名称": product_name,
        "通用流量": f"{ty_liuliang}G",
        "定向流量": f"{dx_liuliang}G",
        "通话时长": f"{tonghua}分钟",
        "适用年龄": age_range
    }

# 主函数供外部调用
async def search_data_cards(keyword="19元", llkshop_id='3abcd2e80b9b4694'):
    matched_products = await get_all_products(keyword, llkshop_id)
    results = []

    if not matched_products:
        return {
            "success": False,
            "message": f"未找到包含 '{keyword}' 的产品",
            "shop_link": f"https://172.lot-ml.com/ProductEn/Index/{llkshop_id}",
            "command_info": "流量卡< 元 > 例如：流量卡9元\n流量卡< 省 > 例如：流量卡广东",
            "results": []
        }
    else:
        # 提取并展示详细信息
        for product in matched_products:
            data = extract_product_data(product["product_data"])
            data["详情链接"] = product["detail_link"]
            results.append(data)

        return {
            "success": True,
            "total_count": len(matched_products),
            "keyword": keyword,
            "shop_link": f"https://172.lot-ml.com/ProductEn/Index/{llkshop_id}",
            "command_info": "流量卡< 元 > 例如：流量卡9元\n流量卡<省> 例如：流量卡广东",
            "results": results
        }