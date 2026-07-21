import sys
sys.path.insert(0, '.')
import requests
import logging
import csv

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ── We will use this free public API — no key needed
# Returns fake user data — perfect for practice
BASE_URL = "https://jsonplaceholder.typicode.com"

# ══ STEP 1: Basic GET request ══
def fetch_users():
    logging.info("Fetching users from API")
    try:
        response = requests.get(f"{BASE_URL}/users")

        # Check status code
        if response.status_code == 200:
            logging.info(f"Success — status code: {response.status_code}")
            return response.json()   # returns list of dicts
        else:
            logging.error(f"Failed — status code: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        logging.error("No internet connection")
        return []
    except requests.exceptions.Timeout:
        logging.error("Request timed out")
        return []

# ══ STEP 2: Fetch with parameters ══
def fetch_posts_by_user(user_id):
    logging.info(f"Fetching posts for user_id: {user_id}")
    try:
        response = requests.get(
            f"{BASE_URL}/posts",
            params={"userId": user_id},  # adds ?userId=1 to URL
            timeout=5                     # fail after 5 seconds
        )
        if response.status_code == 200:
            posts = response.json()
            logging.info(f"Found {len(posts)} posts for user {user_id}")
            return posts
        else:
            logging.error(f"Failed: {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        logging.error(f"Timeout fetching posts for user {user_id}")
        return []

# ══ STEP 3: Save API response to CSV ══
def save_users_to_csv(users, filename):
    logging.info(f"Saving {len(users)} users to {filename}")
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "city"])
            writer.writeheader()
            for user in users:
                writer.writerow({
                    "id":    user["id"],
                    "name":  user["name"],
                    "email": user["email"],
                    "city":  user["address"]["city"]
                })
        logging.info(f"CSV saved: {filename}")
    except Exception as e:
        logging.error(f"CSV save failed: {e}")

# ══ STEP 4: Test bad URL — error handling ══
def fetch_bad_url():
    logging.info("Testing bad URL")
    try:
        response = requests.get(
            f"{BASE_URL}/nonexistent",
            timeout=5
        )
        if response.status_code == 404:
            logging.warning(f"404 Not Found — resource does not exist")
        return []
    except Exception as e:
        logging.error(f"Request failed: {e}")
        return []

# ══ MAIN EXECUTION ══
print("=" * 60)
print("REQUESTS LIBRARY — API INGESTION DEMO")
print("=" * 60)

# Fetch all users
users = fetch_users()
print(f"\nTotal users fetched: {len(users)}")

# Print first 3 users
print("\nFirst 3 users:")
for user in users[:3]:
    print(f"  {user['id']}. {user['name']} — {user['email']}")

# Fetch posts for user 1
print("\nPosts for user 1:")
posts = fetch_posts_by_user(1)
for post in posts[:2]:
    print(f"  → {post['title'][:50]}")

# Save to CSV
save_users_to_csv(users, 'users.csv')

# Test bad URL
print("\nTesting bad URL:")
fetch_bad_url()

print("\n✅ Done — check users.csv in your week6 folder")