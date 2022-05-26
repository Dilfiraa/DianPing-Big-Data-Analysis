from selenium import webdriver
from time import sleep
import random
import csv
import codecs


def get_shop_data(list_item):

    shop_name = list_item.find_element_by_class_name("item-shop-name").text

    if "." in list_item.find_element_by_class_name("item-comment").text:
        shop_star = list_item.find_element_by_class_name("seed-star_wrap").find_element_by_xpath("div[2]").text
    else:
        shop_star = '0'

    if len(list_item.find_elements_by_class_name("item-comment-price")) > 1:
        shop_comment = list_item.find_elements_by_class_name("item-comment-price")[0].text
        shop_price = list_item.find_elements_by_class_name("item-comment-price")[1].text
    elif len(list_item.find_elements_by_class_name("item-comment-price")) == 1:
        shop_comment = list_item.find_elements_by_class_name("item-comment-price")[0].text
        shop_price = ''
    else:
        shop_comment = '0'
        shop_price = ''

    shop_region = list_item.find_element_by_class_name("item-info-region")
    shop_category = list_item.find_element_by_class_name("item-category-name")
    shop_tag = list_item.find_elements_by_class_name("tag-item")

    # 处理部分数据 存入info中
    info = [shop_name, shop_star, shop_comment.strip('条'), shop_price.strip('￥').strip('/人'),
            shop_region.text, shop_category.text, '', '', '', '', '', '', '', '', '']

    # 处理tag字段的数据 存入info中
    index = 6
    for tag in shop_tag:
        info[index] = tag.text
        index += 1

    return info


# 打开网页
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://m.dianping.com/tianjin/ch10/r55")
sleep(5)

# csv文件的格式
headers = ["shop_name", "shop_star", "shop_comment", "shop_price", "shop_region", "shop_category", "tag1", "tag2",
            "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9"]
file_name = driver.title.split('】')[0].strip('【') + '.csv'

data = []
shop_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

with codecs.open(file_name, 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    number = 1
    page = 1
    while scrolling:
        list_items = driver.find_elements_by_class_name("list-item.border-bottom-new")
        for list_item in list_items[-20:]:
            shop_info = get_shop_data(list_item)
            if shop_info:
                shop_id = ''.join(shop_info)
                if shop_id not in shop_ids:
                    shop_ids.add(shop_id)
                    data.append(shop_info)
                    writer.writerow(shop_info)
                    print('爬取第 ', number, ' 店鋪的数据\t', shop_info)
                    number += 1


        scroll_attempt = 0
        while True:
            # check scroll position
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            print('********************* ', page, ' *********************')
            page += 1
            sleep(2 + random.randrange(2))
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1
                print('################### ', scroll_attempt, ' ###################')

                # end of scroll region
                if scroll_attempt >= 10:
                    scrolling = False
                    break
                else:
                    sleep(3 + random.randrange(3))  # attempt another scroll
                    break
            else:
                last_position = curr_position
                break




