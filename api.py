from flask import Flask, request
import telegram
import os
import json
import random
import time
import threading

app = Flask(__name__)

# টেলিগ্রাম বট টোকেন এবং বট ইনিশিয়ালাইজ করা
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

# অ্যাডমিন আইডি (যাকে অ্যাডমিন প্যানেল দেখানো হবে)
ADMIN_ID = os.getenv("7402603360")

# ডেটা সংরক্ষণের জন্য JSON ফাইলের নাম
DATA_FILE = "data.json"

# কয়েন মাইনিং স্ট্যাটাস এবং ইউজারের কয়েন ট্র্যাক করার জন্য ডেটা স্ট্রাকচার
users = {}

# JSON ফাইল থেকে ইউজারের ডেটা লোড করা
def load_data():
    global users
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = {}

# ইউজারের ডেটা JSON ফাইলে সেভ করা
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f)

# টেলিগ্রাম থেকে আসা আপডেট হ্যান্ডল করা
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = str(update.message.chat_id)
    message_text = update.message.text

    # যদি নতুন ইউজার হয়, তাহলে ডেটা তৈরি করুন
    if chat_id not in users:
        users[chat_id] = {"coins": 0, "tasks": 0}
        save_data()

    # স্টার্ট কমান্ড হ্যান্ডলিং
    if message_text == "/start":
        bot.send_message(chat_id=chat_id, text=f"👋 Welcome! You have {users[chat_id]['coins']} coins.\n"
                                               f"Use /mine to mine coins, /tasks to complete tasks, /refer to refer others.")
    # মাইনিং কমান্ড হ্যান্ডলিং
    elif message_text == "/mine":
        bot.send_message(chat_id=chat_id, text="⚙️ Initiating fake coin mining...")
        threading.Thread(target=mine_coins, args=(chat_id,)).start()

    # টাস্ক কমান্ড হ্যান্ডলিং
    elif message_text == "/tasks":
        users[chat_id]["tasks"] += 1
        task_reward = random.randint(5, 15)
        users[chat_id]["coins"] += task_reward
        save_data()
        bot.send_message(chat_id=chat_id, text=f"✅ Task completed! You earned {task_reward} coins.\n"
                                               f"Total coins: {users[chat_id]['coins']} coins.\n"
                                               f"Total tasks completed: {users[chat_id]['tasks']}.")

    # রেফারেল লিংক
    elif message_text == "/refer":
        refer_link = f"http://t.me/@crypto_network_bot?start={chat_id}"
        bot.send_message(chat_id=chat_id, text=f"👥 Refer others to get coins! Share this link:\n{refer_link}")

    # অ্যাডমিন প্যানেল
    elif message_text == "/admin" and chat_id == ADMIN_ID:
        total_users = len(users)
        total_coins = sum(user["coins"] for user in users.values())
        total_tasks = sum(user["tasks"] for user in users.values())

        bot.send_message(chat_id=chat_id, text=(f"📊 Admin Panel:\n\n"
                                                f"Total Users: {total_users}\n"
                                                f"Total Coins Mined: {total_coins}\n"
                                                f"Total Tasks Completed: {total_tasks}"))
    return 'ok'

# মাইনিং প্রক্রিয়া
def mine_coins(chat_id):
    for i in range(10):  # ১০ ধাপে মাইনিং দেখাবে
        progress = random.randint(1, 10)
        users[chat_id]["coins"] += progress
        save_data()
        bot.send_message(chat_id=chat_id, text=f"💻 Mining... {progress} coins mined. Total: {users[chat_id]['coins']} coins.")
        time.sleep(2)
    bot.send_message(chat_id=chat_id, text=f"✅ Mining completed! You have {users[chat_id]['coins']} fake coins now.")

# Flask অ্যাপ রান করা
if __name__ == "__main__":
    load_data()
    app.run()