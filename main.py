from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote
from ebay_oauth_token import OAuthToken

# https://ebaysearch-2333.wl.r.appspot.com

clientId = "JunhaoDe-AndrewEB-PRD-492d3cfae-fb57cd3e"
clientSecret = "PRD-92d3cfae414a-29b3-4d01-9e3f-3610"
# Create an instance of the OAuthUtility class
oauth_utility = OAuthToken(clientId, clientSecret)
# Get the application token
application_token = oauth_utility.getApplicationToken()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('./index.html')


@app.route('/showItem', methods=['GET'])
def showItem():
    itemId = request.args.get('itemId')
    print("itemId", itemId)
    print("type", type(itemId))
    headers = {"X-EBAY-API-IAF-TOKEN": oauth_utility.getApplicationToken()}
    singleItemUrl = f"https://open.api.ebay.com/shopping?callname=GetSingleItem&responseencoding=JSON&appid={clientId}&siteid=0&version=967&ItemID={itemId}&IncludeSelector=Description,Details,ItemSpecifics"
    print("url", singleItemUrl)
    response = requests.get(singleItemUrl, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # print("data: ", data)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
    item = data.get("Item", {})
    print("item:", item)

    # Extract the desired attributes
    photo_url = item.get("PictureURL", [None])[0]
    ebay_link = item.get("ViewItemURLForNaturalSearch", None)
    title = item.get("Title", None)
    sub_title = item.get("Subtitle", None)

    price_data = item.get("CurrentPrice", {})
    price = price_data.get("Value", None)
    currency = price_data.get("CurrencyID", None)
    price = f"{price} {currency}"
    print("price: ", price)

    location = item.get("Location", None)
    postal_code = item.get("PostalCode", None)
    location_combined = f"{location}, {postal_code}" if postal_code else location

    seller_data = item.get("Seller", {})
    seller = seller_data.get("UserID", None)
    print("seller: ", seller)

    # Extracting return policy
    return_accepted = item.get("ReturnPolicy", {}).get("ReturnsAccepted", None)
    return_within = item.get("ReturnPolicy", {}).get("ReturnsWithin", None)
    if return_accepted and return_within:
        return_policy = f"{return_accepted} within {return_within}"
    elif return_accepted:
        return_policy = return_accepted
    else:
        return_policy = None

    extracted_data_list = []
    if photo_url:
        extracted_data_list.append({"key": "Photo", "value": photo_url})
    if ebay_link:
        extracted_data_list.append({"key": "eBay Link", "value": ebay_link})
    if title:
        extracted_data_list.append({"key": "Title", "value": title})
    if sub_title:
        extracted_data_list.append({"key": "Subtitle", "value": sub_title})
    if price:
        extracted_data_list.append({"key": "Price", "value": price})
    if location_combined:
        extracted_data_list.append(
            {"key": "Location", "value": location_combined})
    if seller:
        extracted_data_list.append({"key": "Seller", "value": seller})
    if return_policy:
        extracted_data_list.append(
            {"key": "Return Policy(US)", "value": return_policy})

    item_specifics_data = item.get(
        "ItemSpecifics", {}).get("NameValueList", [])
    for specific in item_specifics_data:
        name = specific.get("Name", None)
        value = specific.get("Value", None)
        if name and value:
            value_to_add = value[0] if isinstance(value, list) else value
            extracted_data_list.append({"key": name, "value": value_to_add})

    return jsonify(extracted_data_list)

    # # Extracting item specifics
    # item_specifics_data = item.get("ItemSpecifics", {})
    # item_specifics = []
    # name_value_list = item_specifics_data.get("NameValueList", [])
    # for nv in name_value_list:
    #     name = nv.get("Name", None)
    #     value = nv.get("Value", [None])[0]
    #     item_specifics.append({name: value})

    # # Conditionally build extracted_data
    # extracted_data = {}
    # if photo_url:
    #     extracted_data["photoUrl"] = photo_url
    # if ebay_link:
    #     extracted_data["ebayLink"] = ebay_link
    # if title:
    #     extracted_data["title"] = title
    # if sub_title:
    #     extracted_data["subTitle"] = sub_title
    # if price:
    #     extracted_data["price"] = price
    # if location_combined:
    #     extracted_data["location"] = location_combined
    # if seller:
    #     extracted_data["seller"] = seller
    # if return_policy:
    #     extracted_data["returnPolicy"] = return_policy
    # # if item_specifics:
    # #     extracted_data["itemSpecifics"] = item_specifics

    # item_specifics_data = item.get(
    #     "ItemSpecifics", {}).get("NameValueList", [])
    # for specific in item_specifics_data:
    #     name = specific.get("Name", None)
    #     value = specific.get("Value", None)
    #     if name and value:
    #         extracted_data[name] = value[0] if isinstance(
    #             value, list) else value
    # print("extracted_data: ", extracted_data)

    # return jsonify(extracted_data)

    # # return jsonify({itemId: itemId})


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    minPrice = request.args.get('minPrice')
    maxPrice = request.args.get('maxPrice')
    conditions = request.args.getlist('condition')
    sellerOption = request.args.get('sellerOption')
    shippingOption = request.args.getlist('shippingOption')
    sortOption = request.args.get('sortOption')

    # 打印接收到的数据
    if keyword is None:
        print("No keyword received!")
    # print("Keyword:", keyword)
    print("Min Price:", minPrice)
    print("Max Price:", maxPrice)
    print("type", type(maxPrice))
    print("Conditions:", conditions)
    print("Seller Option:", sellerOption)
    print("Shipping Options:", shippingOption)
    print("Sort Option:", sortOption)

    base_url = "https://svcs.eBay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=JunhaoDe-AndrewEB-PRD-492d3cfae-fb57cd3e&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD"

    encoded_keyword = quote(keyword)
    # 添加关键字参数
    url = f"{base_url}&keywords={encoded_keyword}"
    filter_num = 0
    # 根据参数添加其他请求参数
    if minPrice != "":
        url += f"&itemFilter({filter_num}).name=MinPrice&itemFilter({filter_num}).value={minPrice}"
        filter_num += 1
    # else:
    #     url += f"&itemFilter(0).name=MinPrice&itemFilter(0).value={minPrice}"
        # print("url", url)

    if maxPrice != "":
        url += f"&itemFilter({filter_num}).name=MaxPrice&itemFilter({filter_num}).value={maxPrice}"
        filter_num += 1
    # else:
    #     url += f"&itemFilter(1).name=MaxPrice&itemFilter(1).value={}"

    # 针对 condition 的处理可能会有些复杂，因为它是一个列表
    if conditions != []:
        for idx, condition in enumerate(conditions):
            url += f"&itemFilter({filter_num}).name=Condition&itemFilter({filter_num}).value({idx})={condition}"
        filter_num += 1

    # 此处假设 sellerOption 和 sortOption 是单个值，不需要特殊处理
    print(sellerOption)
    # print("Return Accepted")
    if sellerOption == "Return Accepted":
        url += f"&itemFilter({filter_num}).name=ReturnsAcceptedOnly&itemFilter({filter_num}).value=true"
        filter_num += 1
    else:
        url += f"&itemFilter({filter_num}).name=ReturnsAcceptedOnly&itemFilter({filter_num}).value=false"
        filter_num += 1

    if "Free" in shippingOption:
        url += f"&itemFilter({filter_num}).name=FreeShippingOnly&itemFilter({filter_num}).value=true"

    # if "Expedited" in shippingOption:
    #     url += "&itemFilter(5).name=ExpeditedShippingType&itemFilter(5).value=Expedited"
    # if shippingOption:
    #     # 假设 shippingOption 也是列表，需要进行循环处理
    #     for idx, option in enumerate(shippingOption):
    #         url += f"&itemFilter(4).name=ShippingOption&itemFilter(4).value({idx})={option}"

    if sortOption:
        url += f"&sortOrder={sortOption}"

    print(url)

    # 在此处处理这些数据，例如存储到数据库或其他操作...
    # ...
    # url = "https://svcs.eBay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=JunhaoDe-AndrewEB-PRD-492d3cfae-fb57cd3e&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=harry%20potter&sortOrder=PricePlusShippingLowest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

    # print("data", data)

    findItemsAdvancedResponse = data.get("findItemsAdvancedResponse")

    items = findItemsAdvancedResponse[0].get(
        'searchResult', [{}])[0].get('item', [])
    # print("items", items)
    # 提取总条目数
    total_results = findItemsAdvancedResponse[0].get('paginationOutput', [{}])[
        0].get('totalEntries', [0])[0]
    print("total_results", total_results)
    # 确定需要检查的关键字
    keysToCheck = set([
        "galleryURL", "title", "viewItemURL", "returnsAccepted",
        "primaryCategory", "condition", "topRatedListing", "sellingStatus",
        "shippingInfo", "location"
    ])
    responseItems = []
    for item_data in items:
        if len(responseItems) == 10:
            break

        # 如果item数据中不包含所有必要的键，那么跳过它
        if not keysToCheck.issubset(item_data.keys()):
            continue
        # print("condition:", item_data["condition"]
        #       [0]["conditionDisplayName"][0])
        print("returnsAccepted:", item_data["returnsAccepted"][0])
        # 从条目数据中提取所需的信息
        itemToAdd = {
            "itemId": item_data["itemId"][0],
            "galleryURL": item_data["galleryURL"][0],
            "title": item_data["title"][0],
            "viewItemURL": item_data["viewItemURL"][0],
            "returnsAccepted": item_data["returnsAccepted"][0],
            "categoryName": item_data["primaryCategory"][0]["categoryName"][0],
            "condition": item_data["condition"][0]["conditionDisplayName"][0],
            "topRatedListing": item_data["topRatedListing"][0],
            "currentPrice": item_data["sellingStatus"][0]["convertedCurrentPrice"][0]["__value__"],
            "shippingServiceCost": item_data["shippingInfo"][0].get("shippingServiceCost", [{}])[0].get("__value__", 0.0),
            "expeditedShipping": item_data["shippingInfo"][0]["expeditedShipping"][0],
            "location": item_data["location"][0]
        }

        responseItems.append(itemToAdd)
    # print("responseItems", responseItems)
    return jsonify({
        "keyword": keyword,
        "total_results": total_results,
        "responseItems": responseItems
    })
    # items = findItemsAdvancedResponse.get('searchResult', [{}])[0].get('item', [])

    # 提取总条目数
    # total_results = findItemsAdvancedResponse.get(
    #     'paginationOutput', {}).get('totalEntries', 0)

    # print("type", type(json_data))
    # total_results_found = json_data["paginationOutput"]
    # print("total_results_found", total_results_found)
    # json_data_dict = json.loads(json_data)
    # print("json_data_dict", json_data_dict)
    # items = json_data[0].get('searchResult', [{}])[0].get('item', [])
    # for item in items:
    #     print("item:", item)

    # data['total_results'] = json_data[0].get(
    #     'paginationOutput', {}).get('totalEntries', 0)
    # print("total_results", data['total_results'])
    # data_list = []
    # for item in items:
    #     data = {}

    #     # 提取所需的数据
    #     data['image_url'] = item.get('galleryURL', '')
    #     data['title'] = item.get('title', '')
    #     data['category'] = item.get(
    #         'primaryCategory', {}).get('categoryName', '')
    #     data['product_link'] = item.get('viewItemURL', '')
    #     data['condition'] = item.get('condition', {}).get(
    #         'conditionDisplayName', '')
    #     data['price'] = f"Price: ${item.get('sellingStatus', {}).get('convertedCurrentPrice', {'__value__': '0'}).get('__value__')} (+ ${item.get('shippingInfo', {}).get('shippingServiceCost', {'__value__': '0'}).get('__value__')} for shipping)"

    #     # 检查是否为Top Rated Listing，并根据需要设置图像URL
    #     if item.get('topRatedListing', 'false') == 'true':
    #         data['top_rated_image'] = "URL_to_topRatedImage.jpg"  # 请替换为实际的图像URL
    #     # print("data", data)
    #     data_list.append(data)

    # 为了这个示例，我们只是简单地回应已接收到数据
    # return jsonify({
    #     "message": "Data received!",
    #     "data": {
    #         "keyword": keyword,
    #         "minPrice": minPrice,
    #         "maxPrice": maxPrice,
    #         "conditions": conditions,
    #         "sellerOption": sellerOption,
    #         "shippingOptions": shippingOption,
    #         "sortOption": sortOption
    #     }
    # })


if __name__ == '__main__':
    app.run(debug=True)
