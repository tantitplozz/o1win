import asyncio
import json
from typing import Any, Dict, List

import aiohttp
import yaml
from typing_extensions import TypedDict


class MessageDict(TypedDict):
    role: str
    content: str


class LLMResponse(TypedDict):
    text: str


class LLMRouter:
    def __init__(self, config_path: str):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)["llm_router"]

    async def _make_request(self, llm_name: str, prompt: str) -> Dict[str, Any]:
        if llm_name not in self.config:
            raise ValueError(f"LLM {llm_name} not found in configuration")

        llm_config = self.config[llm_name]
        url = llm_config["url"]
        method = llm_config["method"]

        headers = {}
        if "headers" in llm_config:
            headers.update(llm_config["headers"])

        if "auth" in llm_config:
            auth = aiohttp.BasicAuth(
                login=llm_config["auth"]["username"],
                password=llm_config["auth"]["password"],
            )
        else:
            auth = None

        # Prepare payload based on body format
        if llm_config["body_format"] == "openai":
            payload = {
                "model": llm_config["model"],
                "messages": [{"role": "user", "content": prompt}],
            }
        elif llm_config["body_format"] == "raw_json":
            template = llm_config["payload_template"]
            payload = {**template}
            payload["prompt"] = prompt
        elif llm_config["body_format"] == "ollama":
            template = llm_config["payload_template"]
            payload = {**template}
            payload["prompt"] = prompt

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method, url=url, headers=headers, auth=auth, json=payload
            ) as response:
                return await response.json()

    async def chat(self, llm_name: str, messages: List[MessageDict]) -> Dict[str, Any]:
        """Chat interface for OpenAI-compatible endpoints"""
        if isinstance(messages, list):
            prompt = messages[-1]["content"] if messages else ""
        else:
            prompt = str(messages)
        return await self._make_request(llm_name, prompt)

    async def prompt(self, llm_name: str, prompt: str) -> Dict[str, Any]:
        """Simple prompt interface for raw text input"""
        return await self._make_request(llm_name, prompt)


async def main():
    # สร้าง instance ของ LLMRouter
    router = LLMRouter("custom-config/llm_router.yaml")

    # ตัวอย่างการใช้งาน
    try:
        # ใช้ dolphin24b ผ่าน chat interface
        response1 = await router.chat(
            "dolphin24b", [{"role": "user", "content": "สร้างแผนธุรกิจร้านกาแฟ"}]
        )
        print(
            "Dolphin24b response:", json.dumps(response1, indent=2, ensure_ascii=False)
        )

        # ใช้ yi model ผ่าน prompt interface
        response2 = await router.prompt("yi_model", "สวัสดี")
        print(
            "\nYi model response:", json.dumps(response2, indent=2, ensure_ascii=False)
        )

        # ใช้ mythomax local ผ่าน prompt interface
        response3 = await router.prompt("mythomax_local", "เขียนสูตรโกโก้เย็นให้หน่อย")
        print(
            "\nMythomax response:", json.dumps(response3, indent=2, ensure_ascii=False)
        )

    except (aiohttp.ClientError, yaml.YAMLError, KeyError, ValueError) as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
