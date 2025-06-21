import requests
import zstandard as zstd
import brotli
import gzip
import json

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

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Origin": "https://www.meta.ai",
#     "Referer": "https://www.meta.ai/"
# }


variables = {
    "after": "slv:WyIyMCIseyJTaWx2ZXJzdG9uZU1haW5GZWVkUmFua2VkUG9zdHNGZXRjaGVyIjoie1wiZGVsaXZlcmVkX3Bvc3RzXCI6WzY4MjQ5MTE2ODI5MDkzMiw2NzI4ODA3MTI1NzY3MzYsNjgyMzA0NDExNjQyOTQxLDY0MDc3NTk2NTc5NDE4NSw3MTgyMjk2MjQ3MDE4NTQsNjgxMzQ2ODExNzM4NzAxLDY3MzYxMjQ3MjUwNDQ5Niw2NjIxNDMzNTY5ODY2NDIsNjc3NTk4NDc1NDM3NDAzLDYyOTQ4MjM5MDI1OTQ4NSw2OTE2MzUwMTQwMjk2NDksNjE2ODQ0MjcxNTIyMzczLDcxODIyOTk3ODAzNTE1Miw2ODEzNDUwOTUwNzIyMDYsNjE0NjAwNDc1MDc5NTM4LDY3OTEyMjkyMTk1MTYyNSw2OTc0MDAwNjY3ODQ0NDAsNzI2NDczNTA3MjA3NTg4LDY2NTQ5OTgwMzMxNzQyMSw3MTk0NDMzMDEyNDcxNTMsNjQ2MDM2MTU1MjY3MDMwLDY3NzgzNTAwNTQxMzIwNCw3MzQ0MDM0NzY0MTIyMTIsNzA3MzEyOTA1Nzk0MDgyLDY3OTc1MTQ2ODU1NjM4Nyw2MzU2NTM1Mzk2Mzk2NjcsNzIwNjA5ODAxMTMwNTAzLDcyNjI4ODU4MDU2MjAwNiw3MTI3MDMzMjE5Mjc1MTEsNjgxMzYxMjk4NDAzOTE5LDcyNjc5MzAyMzg0MzQ3OCw2OTM0NDM4NjA1MTcyNjUsNjc4NDE3OTc4Njg3ODM3LDcyNjc3OTgyMzg4NDMyNTIsNjY3NzAxMzY2NDMwMzE1LDYzMTY0MjA2MzM3NTkyNCw2ODc5NjI5MTc3MzE5NzIsNjgyMzE3MDQ0OTc1MDExLDY0MDc3MTg5OTEyNzkyNSw2NzQ5MjE4MDU3MDk4MzF9LFwibnVtX29mX21ldGFfbWFuYWdlZF9wb3N0c1wiOjAsXCJpc19lbmRfb2ZfZmVlZFwiOmZhbHNlLFwiY2hyb25vbG9naWNhbF9jdXJzb3JcIjpudWxsLFwiZmVlZF9jb25maWdfaWRcIjoxLFwibnVtX29mX3Bvc3RzX2Zyb21fc2FtZV9hdXRob3JcIjp7XCI2MTMzNDkzNDE4NzE3ODJcIjo2fX1dfQ==",
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

# payload = {
#     "av": "0",
#     "__user": "0",
#     "__a": "1",
#     "__req": "j",
#     "__hs": "20259.HYP:kadabra_pkg.2.1...0",
#     "dpr": "1",
#     "__ccg": "GOOD",
#     "__rev": "1024031128",
#     "__s": "2bt5aw:yu8plb:fmd13u",
#     "__hsi": "7518117210622003552",
#     "__dyn": "7xeUmwlEnwn8K6EjBAg5S1Dxu13wFwnUW3q2ibwNw9G2S0lW4o0B-q7oc81EE2Cwwwqo6ucw5Mx612xO0Bo7O2l0Fwqo31w9O1lwlE-U2zxe2GewbS361qw82dU5O1lwmo423-0j52oS0Io5d0bS1LBwNwNweG269wr8aEfE5u3a0XEuwm85K2G0JU2FwkE",
#     "__csr": "igjNYrkhbRqVWnQBTy7i8CCaHGK9igKaKh2ayETxe7p8sgS00lMi6e1ig5q5E27w2XVaw4Fwk-fx6fwx2EGtxkawa65IgEjgm5QidyoKOw9y0YpUxpxx9Uy5o2Cw3uo12QWwAwfS0XUpw17S0m513c16xG2khy4bPw8m0aOg2WcEG8mie5O0Ow4SDxN7yYhLg5F6y4bDwkEcwG8W46oQnoy1RedwvU0BDwfy00xAkm5E9A0mGUlw4Lw5Azox5gcE2Gweq",
#     "__comet_req": "72",
#     "lsd": "AVoeE2CDptc",
#     "jazoest": "2944",
#     "__spin_r": "1024031128",
#     "__spin_b": "trunk",
#     "__spin_t": "1750448069",
#     "__jssesw": "1",
#     "__crn": "comet.kadabra.KadabraHomeRoute",
#     "fb_api_caller_class": "RelayModern",
#     "fb_api_req_friendly_name": "KadabraFeedContainerPaginationQuery",
#     "variables": json.dumps(variables),
#     "server_timestamps": "true",
#     "doc_id": "24628642286723238"
# }

payload = """av=0&__user=0&__a=1&__req=3&__hs=20260.HYP%3Akadabra_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1024058088&__s=nhxk9b%3Av1vbfj%3And9kcu&__hsi=7518296620469445162&__dyn=7xeUmwlEnwn8K6EjBAg5S1Dxu13wFwnUW3q2ibwNw9G2S0lW4o0B-q7oc81EE2Cwwwqo6ucw5Mx612xO0Bo7O2l0Fwqo31w9O1lwlE-U2zxe2GewbS361qw82dU5O1lwmo423-0j52oS0Io5d0bS1LBwNwNweG269wr8aEfE5u3a0XEuwm85K2G0JU2FwkE&__csr=h46crNdiIyO2fnGhkD-pszFeHhpuirKfDKt2ui4oO22E8GK00m6GU8o0gmAys9x27s-8k9F5Gi6k2J5941p0xw8K0wIU461ty82EAbwj3Ux7Kz282Jo7a3m085jK2y0U8eXwDw3trw3Jo1bUuhEx2VU4ilyUb0zgmw3UEC0ivimcC50qE2sAbwIpc9G4ElgaMG4XwExe6FVas9A8m8g2Ew2lWw6cw0v38gUZe0eiBx15hUaodU&__hsdp=gesmRcwx1F7yt7hA8Ah42lBDQ4Am2zjzogCXV9mu15z9UhyUfk4omxh16i18wSyo6u48lw&__hblp=1q0EKUggAwTx129V89oWFUF5wyBQV8y8KVK-iGpUkxC5EOumbwik4olg8pk222KdHAUsyomwFxWu44mGy8ggcU&__comet_req=72&lsd=AVrN-2_AsGM&jazoest=2861&__spin_r=1024058088&__spin_b=trunk&__spin_t=1750489841&__jssesw=1&__crn=comet.kadabra.KadabraHomeRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=KadabraFeedContainerPaginationQuery&variables=%7B%22after%22%3A%22slv%3AWyIyMCIseyJTaWx2ZXJzdG9uZU1haW5GZWVkUmFua2VkUG9zdHNGZXRjaGVyIjoie1wiZGVsaXZlcmVkX3Bvc3RzXCI6WzcwOTU1NDM2MjIzOTg5NCw3NDMyNzI2OTU1MjkzNzQsNjE0MjUyNzYxNzgxMjczLDY4MjI4MTY4NDk3ODU0N10sXCJudW1fb2ZfbWV0YV9tYW5hZ2VkX3Bvc3RzXCI6MCxcImlzX2VuZF9vZl9mZWVkXCI6ZmFsc2UsXCJjaHJvbm9sb2dpY2FsX2N1cnNvclwiOm51bGwsXCJmZWVkX2NvbmZpZ19pZHhcIjowLFwibnVtX29mX3Bvc3RzX2Zyb21fc2FtZV9hdXRob3JcIjp7XCI2NzM2NzA1NzU4MjgyNzNcIjoxLFwiNjk5OTUyNjA2NTI4MDUwXCI6MSxcIjU3NzcxNzg5ODc2ODA5M1wiOjEsXCI2MTMzNDkzNDE4NzE3ODJcIjoxfSxcIm51bV9vZl9wb3N0c193aXRoX3NhbWVfcHJvbXB0XCI6e319In1d%22%2C%22first%22%3A12%2C%22logged_out%22%3Atrue%2C%22__relay_internal__pv__AbraIsLoggedOutrelayprovider%22%3Atrue%2C%22__relay_internal__pv__KadabraFeedCardRemixTryItrelayprovider%22%3Atrue%2C%22__relay_internal__pv__KadabraSocialGraphrelayprovider%22%3Afalse%2C%22__relay_internal__pv__KadabraFeedImageDimensionrelayprovider%22%3A800%2C%22__relay_internal__pv__AbraArtifactsEnabledrelayprovider%22%3Atrue%2C%22__relay_internal__pv__AbraSearchInlineReferencesEnabledrelayprovider%22%3Atrue%2C%22__relay_internal__pv__AbraComposedTextWidgetsrelayprovider%22%3Atrue%2C%22__relay_internal__pv__AbraSearchReferencesHovercardEnabledrelayprovider%22%3Atrue%7D&server_timestamps=true&doc_id=24628642286723238"""


def parse_meta_feed(response):
    try:
        cleaned = response.text.lstrip("for (;;);")
        data = json.loads(cleaned)
        posts = []

        edges = data.get("data", {}).get("xfb_genai_fetch_feed", {}).get("edges", [])
        for edge in edges:
            node = edge.get("node", {})
            ai_response = node.get("body_renderer_v2", {}).get("text_contents", [{}])[0].get("text", "")
            posts.append({
                "id": node.get("id"),
                "user_query": node.get("original_prompt", {}).get("body", ""),
                "ai_response": ai_response,
                "username": node.get("genai_owner", {}).get("username", ""),
                "created": node.get("created_timestamp", ""),
            })

        return posts

    except Exception as e:
        print("Error parsing:", e)
        return []


response = requests.post(url, headers=headers, data=payload)
encoding = response.headers.get("Content-Encoding")

print("Status Code:", response.status_code)
print("Content-Encoding:", encoding)

parsed = parse_meta_feed(response)
print('this..')
print(parsed)

# try:
#     if encoding == 'zstd':
#         dctx = zstd.ZstdDecompressor()
#         decompressed = dctx.decompress(response.content)
#     elif encoding == 'br':
#         decompressed = brotli.decompress(response.content)
#     elif encoding == 'gzip':
#         decompressed = gzip.decompress(response.content)
#     else:
#         decompressed = response.content  # assume plain text

# except Exception as e:
#     print("Failed to decode or parse:", e)
#     print("Raw data preview:", response.content[:500])
