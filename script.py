from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import zstandard as zstd
# import brotli
# import gzip
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
url = "https://www.meta.ai/api/graphql/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.meta.ai",
    "Referer": "https://www.meta.ai/",
    "Sec-Ch-Prefers-Color-Scheme": "dark",
    "Sec-Ch-Ua": '"Chromium";v="137", "Not/A)Brand";v="24", "Google Chrome";v="137"',
    "Sec-Ch-Ua-Full-Version-List": '"Chromium";v="137.0.7151.104", "Not/A)Brand";v="24.0.0.0", "Google Chrome";v="137.0.7151.104"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Ch-Ua-Platform-Version": '"19.0.0"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Asbd-Id": "359341",
    "X-Fb-Friendly-Name": "KadabraFeedContainerPaginationQuery",
    "X-Fb-Lsd": "AVoeE2CDptc",
    "Cookie": "datr=ALZVaD6CLkRttIqWUyD2FXhc; abra_csrf=zq0bqskUSA-ELyZUsxvw_S; wd=1528x238"
}

def get_payload(after_cursor=None):
    variables = {
        "after": after_cursor or "",  # Use provided cursor or empty for first page
        "first": 12,
        "logged_out": True,
        "__relay_internal__pv__AbraIsLoggedOutrelayprovider": True,
        "__relay_internal__pv__KadabraFeedCardRemixTryItrelayprovider": True,
        "__relay_internal__pv__KadabraFeedImageDimensionrelayprovider": 800,
        "__relay_internal__pv__AbraArtifactsEnabledrelayprovider": True,
        "__relay_internal__pv__AbraSearchInlineReferencesEnabledrelayprovider": True,
        "__relay_internal__pv__AbraComposedTextWidgetsrelayprovider": True,
        "__relay_internal__pv__AbraSearchReferencesHovercardEnabledrelayprovider": True
    }
    return f"""av=0&__user=0&__a=1&__req=3&__hs=20260.HYP%3Akadabra_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1024058088&__s=nhxk9b%3Av1vbfj%3And9kcu&__hsi=7518296620469445162&__dyn=7xeUmwlEnwn8K6EjBAg5S1Dxu13wFwnUW3q2ibwNw9G2S0lW4o0B-q7oc81EE2Cwwwqo6ucw5Mx612xO0Bo7O2l0Fwqo31w9O1lwlE-U2zxe2GewbS361qw82dU5O1lwmo423-0j52oS0Io5d0bS1LBwNwNweG269wr8aEfE5u3a0XEuwm85K2G0JU2FwkE&__csr=h46crNdiIyO2fnGhkD-pszFeHhpuirKfDKt2ui4oO22E8GK00m6GU8o0gmAys9x27s-8k9F5Gi6k2J5941p0xw8K0wIU461ty82EAbwj3Ux7Kz282Jo7a3m085jK2y0U8eXwDw3trw3Jo1bUuhEx2VU4ilyUb0zgmw3UEC0ivimcC50qE2sAbwIpc9G4ElgaMG4XwExe6FVas9A8m8g2Ew2lWw6cw0v38gUZe0eiBx15hUaodU&__hsdp=gesmRcwx1F7yt7hA8Ah42lBDQ4Am2zjzogCXV9mu15z9UhyUfk4omxh16i18wSyo6u48lw&__hblp=1q0EKUggAwTx129V89oWFUF5wyBQV8y8KVK-iGpUkxC5EOumbwik4olg8pk222KdHAUsyomwFxWu44mGy8ggcU&__comet_req=72&lsd=AVrN-2_AsGM&jazoest=2861&__spin_r=1024058088&__spin_b=trunk&__spin_t={int(time.time())}&__jssesw=1&__crn=comet.kadabra.KadabraHomeRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=KadabraFeedContainerPaginationQuery&variables={json.dumps(variables)}&server_timestamps=true&doc_id=24628642286723238"""


def parse_meta_feed(response):
    try:
        cleaned = response.text.lstrip("for (;;);")
        print(f"Raw response (first 200 chars): {cleaned[:200]}")  # Debug log
        data = json.loads(cleaned)
        posts = []
        feed = data.get("data", {}).get("xfb_genai_fetch_feed", {})
        edges = feed.get("edges", [])
        page_info = feed.get("page_info", {})
        has_next_page = page_info.get("has_next_page", False)
        end_cursor = page_info.get("end_cursor")

        for edge in edges:
            node = edge.get("node", {})
            ai_response = node.get("body_renderer_v2", {}).get("text_contents", [{}])[0].get("text", "")
            posts.append({
                "id": node.get("id"),
                "user_query": node.get("original_prompt", {}).get("body", ""),
                "ai_response": ai_response,
                "username": node.get("genai_owner", {}).get("username", ""),
                "created": node.get("created_timestamp", "")
            })
        return posts, has_next_page, end_cursor, None
    except Exception as e:
        return [], False, None, str(e)

def filter_posts(posts, keyword):
    if not keyword:
        return posts
    keyword = keyword.lower()
    return [
        post for post in posts
        if keyword in post["user_query"].lower()
    ]

@app.route("/scrape", methods=["POST"])
def scrape_posts():
    try:
        data = request.get_json(silent=True) or {}
        keyword = data.get("keyword")
        after_cursor = data.get("after_cursor")
        
        response = requests.post(url, headers=headers, data=get_payload(after_cursor))
        
        print(f"Status code: {response.status_code}")
        # print(response.text)  # Debug log
        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Request failed with status {response.status_code}: {response.text[:200]}",
            }), response.status_code
        
        posts, has_next_page, end_cursor, error = parse_meta_feed(response)
        if error:
            return jsonify({
                "status": "error",
                "message": f"Parsing error: {error}",
            }), 500
        
        # Apply keyword filtering
        filtered_posts = filter_posts(posts, keyword)
        
        return jsonify({
            "status": "success",
            "posts": filtered_posts,
            "count": len(filtered_posts),
            "page_info": {
                "has_next_page": has_next_page,
                "end_cursor": end_cursor
            }
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
        }), 500

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Meta Scraper API is running"})

if __name__ == "__main__":
    # Get port from environment variable (Render sets PORT)
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 to accept external connections
    app.run(host="0.0.0.0", port=port, debug=False)