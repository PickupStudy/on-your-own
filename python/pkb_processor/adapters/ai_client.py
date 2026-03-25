import os


def summarize_note(title: str, content: str) -> str:
    import httpx
    api_key = os.getenv("AI_API_KEY")
    model = os.getenv("AI_MODEL")
    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

    if not api_key or not model:
        return f"[fallback] {title}: missing AI_API_KEY or AI_MODEL"

    prompt = (
        "请对下面的学习笔记进行结构化总结，输出简洁中文，包含："
        "1) 主题 2) 核心要点 3) 后续行动建议。\n\n"
        f"标题：{title}\n内容：\n{content[:6000]}"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是个人知识库助手，擅长学习总结。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    with httpx.Client(timeout=60.0) as client:
        resp = client.post(f"{base_url}/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
