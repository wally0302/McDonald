import os
import json
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="你是一名餐飲評論家，專門根據提供的數據進行餐廳的詳細評估。你的任務是根據使用者的需求，從給定的評論資料中找出最符合使用者偏好的餐廳，並提供詳盡的分析與建議。評論資料包括環境、食物、速度、店員態度等面向的評價。請用繁體中文 (zh-tw) 回應。",
)

chat_session = model.start_chat(
    history=[]
)

# 讀取 JSON 檔案
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"找不到檔案：{file_path}")
        return None
    except json.JSONDecodeError:
        print(f"檔案格式錯誤：{file_path}")
        return None

# 設定 JSON 檔案路徑
json_file_path = "restaurant.json"  # 修改為你的 JSON 檔案路徑
review_data = load_json_data(json_file_path)

if review_data:
    print("成功讀取評論資料。")
else:
    print("無法讀取評論資料，請檢查檔案路徑或格式。")
    exit()

print("Bot: Hello, how can I help you?")
print()

while True:
    # 使用者輸入具體需求
    user_input = input("You (請描述對餐廳的需求，例如：環境乾淨、食物美味): ")
    print()

    # 生成模型查詢
    query = f"""
    我提供了一份 JSON 資料作為餐廳評論的數據來源：
    {json.dumps(review_data, ensure_ascii=False, indent=2)}

    使用者的需求是：{user_input}

    請基於評論數據與使用者的需求，完成以下分析：
    - 找出一間最符合使用者需求的餐廳，並推薦給使用者。
    - 提供該餐廳的簡短分析，包括優點與缺點。
    - 請用條理清晰的方式回應，並以繁體中文呈現結果。
    """
    
    response = chat_session.send_message(query)

    # 顯示生成的回應
    model_response = response.text
    print(f"Bot: {model_response}")
    print()

    # 更新聊天歷史
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})