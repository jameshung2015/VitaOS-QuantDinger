import requests
import json
import os

base_url = "http://localhost:5000"
username = "quantdinger"
password = "123456"

def run():
    print(f"Logging in to {base_url}/api/auth/login...")
    resp = requests.post(f"{base_url}/api/auth/login", json={"username": username, "password": password})
    if resp.status_code != 200:
        print(f"Login failed: {resp.status_code} {resp.text}")
        return
    
    body = resp.json()
    token = body.get("data", {}).get("token")
    if not token:
        print("No token found in response")
        return
    
    print("Login successful.")
    headers = {"Authorization": f"Bearer {token}", "Accept-Language": "zh-CN"}
    url = f"{base_url}/api/global-market/monthly-key-events"
    params = {"days": 30, "force": 1}
    
    print(f"Calling {url}...")
    resp = requests.get(url, headers=headers, params=params, timeout=120)
    
    if resp.status_code != 200:
        print(f"API call failed: {resp.status_code} {resp.text}")
        return
    
    data_full = resp.json()
    data = data_full.get("data", {})
    agent = data.get("agent", {})
    items = data.get("items", [])
    
    print(f"data.agent.source_mode: {agent.get('source_mode')}")
    print(f"data.agent.skill_path: {agent.get('skill_path')}")
    print(f"data.agent.model_provider: {agent.get('model_provider')}")
    print(f"data.agent.model_name: {agent.get('model_name')}")
    print(f"items length: {len(items)}")

if __name__ == '__main__':
    run()
