import json

def convert_reviews(reviews_data, new_name):
  """
  將原有評論資料轉換成新的 JSON 格式。

  Args:
    reviews_data: 原有評論資料的列表。
    new_name: 新的 name 欄位值。

  Returns:
    轉換後的 JSON 資料。
  """

  new_reviews = []
  for review in reviews_data:
    new_review = {"name": new_name, "review": review["review"]}
    new_reviews.append(new_review)

  return new_reviews

# 載入原始 JSON 資料 (請替換為你的檔案路徑)
with open(r'C:\Users\yen\Desktop\my_code\ccClub期末專案\reviews.json', 'r', encoding='utf-8') as f:
  original_data = json.load(f)

# 將資料轉換成新的格式
new_data = convert_reviews(original_data, "麥當勞新竹經國店")

# 將轉換後的資料寫入新的 JSON 檔案
with open('new_reviews.json', 'w', encoding='utf-8') as f:
  json.dump(new_data, f, ensure_ascii=False, indent=4)