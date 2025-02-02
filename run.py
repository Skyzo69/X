import requests
import threading
import time
import random
import json

# Load file data (bisa kosong)
def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"⚠️ File {filename} tidak ditemukan, lanjut tanpa file ini.")
        return []

# Headers dasar (X.com API)
def get_headers(auth_token):
    return {
        "authority": "x.com",
        "accept": "*/*",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "cookie": f"auth_token={auth_token}"
    }

# Debugging response
def debug_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        json_data = response.json()
        print(f"Response JSON: {json.dumps(json_data, indent=2)}")
        return json_data
    except json.JSONDecodeError:
        print("⚠️ ERROR: Response bukan JSON atau kosong!")
        return None  # Return None jika gagal parse JSON

# Like Tweet
def like_tweet(auth_token, tweet_id):
    url = "https://x.com/i/api/1.1/like/create.json"
    payload = {"tweet_id": tweet_id}
    response = requests.post(url, json=payload, headers=get_headers(auth_token))
    return debug_response(response)

# Retweet Tweet
def retweet_tweet(auth_token, tweet_id):
    url = f"https://x.com/i/api/1.1/statuses/retweet/{tweet_id}.json"
    payload = {"id": tweet_id}
    response = requests.post(url, json=payload, headers=get_headers(auth_token))
    return debug_response(response)

# Comment Tweet (jika ada)
def comment_tweet(auth_token, tweet_id, text):
    url = "https://x.com/i/api/1.1/statuses/update.json"
    payload = {"status": text, "in_reply_to_status_id": tweet_id}
    response = requests.post(url, json=payload, headers=get_headers(auth_token))
    return debug_response(response)

# Follow User (jika ada target)
def follow_user(auth_token, user_id):
    url = "https://x.com/i/api/1.1/friendships/create.json"
    payload = {"user_id": user_id, "follow": "true"}
    response = requests.post(url, json=payload, headers=get_headers(auth_token))
    return debug_response(response)

# Fungsi utama untuk eksekusi tiap akun
def process_account(index, auth_token, tweet_id, comment, follow_id):
    try:
        print(f"[{index+1}] Akun memproses Tweet {tweet_id}...")

        like_response = like_tweet(auth_token, tweet_id)
        print(f"[{index+1}] Like: {like_response}")

        retweet_response = retweet_tweet(auth_token, tweet_id)
        print(f"[{index+1}] Retweet: {retweet_response}")

        if comment:
            comment_response = comment_tweet(auth_token, tweet_id, comment)
            print(f"[{index+1}] Comment: {comment_response}")

        if follow_id:
            follow_response = follow_user(auth_token, follow_id)
            print(f"[{index+1}] Follow: {follow_response}")

    except Exception as e:
        print(f"[{index+1}] ❌ Error: {e}")

# Load data
auth_tokens = load_file("cookie.txt")
tweet_ids = load_file("tweetid.txt")
comments = load_file("comment.txt")
follow_ids = load_file("follow.txt")

# Pastikan jumlah akun, tweet, comment, dan follow sesuai (bisa kosong)
max_len = max(len(auth_tokens), len(tweet_ids), len(comments), len(follow_ids))
auth_tokens += [""] * (max_len - len(auth_tokens))
tweet_ids += [""] * (max_len - len(tweet_ids))
comments += [""] * (max_len - len(comments))
follow_ids += [""] * (max_len - len(follow_ids))

# Atur jeda minimal & maksimal antar akun (dalam detik)
MIN_DELAY = 60  # 1 menit
MAX_DELAY = 120  # 2 menit

# Jalankan semua akun dengan jeda acak
for i in range(max_len):
    if auth_tokens[i] and tweet_ids[i]:  # Pastikan ada akun & Tweet ID
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"[{i+1}] Akun akan dieksekusi dalam {delay // 60} menit...")
        time.sleep(delay)  # Tunggu sebelum eksekusi
        
        process_account(i, auth_tokens[i], tweet_ids[i], comments[i], follow_ids[i])

print("✅ Semua akun selesai dieksekusi.")
