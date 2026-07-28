"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
"""

import ast
import json
import os
import re
import sys
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import TOOL_SCHEMAS, execute_tool
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()

# Thứ tự tham số vị trí của mỗi tool, suy ra từ TOOL_SCHEMAS của Role 2
# (dùng để map Action: tool[val1, val2] -> {"param1": val1, "param2": val2})
_TOOL_PARAM_ORDER = {
    schema["function"]["name"]: list(schema["function"]["parameters"]["properties"].keys())
    for schema in TOOL_SCHEMAS
}

def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    
    # Fallback kiểm tra nếu file ở thư mục hiện tại
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
        
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider):
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: {CHATBOT_BASELINE_PROMPT.strip()}")
    
    # Gọi LLM Provider thực hiện sinh câu trả lời
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")


def _extract_bracket_content(text: str, open_bracket_index: int):
    """Lấy nội dung bên trong cặp ngoặc [] cân bằng, hỗ trợ list/dict lồng nhau."""
    depth = 0
    for i in range(open_bracket_index, len(text)):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                return text[open_bracket_index + 1:i]
    return None


def parse_action(response: str):
    """
    Trích xuất tên tool và tham số (dict) từ dòng 'Action: ten_cong_cu[tham_so]'.
    Hỗ trợ cả tham số vị trí (get_course_details["CS101"]) lẫn key=value
    (search_courses[keyword="Python", max_fee=2000000]), map tham số vị trí
    theo đúng thứ tự khai báo trong TOOL_SCHEMAS của Role 2.
    """
    match = re.search(r"Action:\s*(\w+)\s*(\[)", response)
    if not match:
        return None, None

    tool_name = match.group(1).strip()
    raw_args = _extract_bracket_content(response, match.start(2))
    if raw_args is None:
        return tool_name, None

    raw_args = raw_args.strip()
    if not raw_args:
        return tool_name, {}

    try:
        call_node = ast.parse(f"_({raw_args})", mode="eval").body
    except SyntaxError:
        return tool_name, None

    arguments = {}
    param_names = _TOOL_PARAM_ORDER.get(tool_name, [])

    for index, arg_node in enumerate(call_node.args):
        if index >= len(param_names):
            break
        arguments[param_names[index]] = ast.literal_eval(arg_node)

    for kw in call_node.keywords:
        arguments[kw.arg] = ast.literal_eval(kw.value)

    return tool_name, arguments


def run_react_agent(user_query: str, provider):
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) có Guardrails.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    transcript = f"Câu hỏi của người dùng: {user_query}\n"
    step = 0

    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")

        response = provider.generate(transcript, system_prompt=REACT_SYSTEM_PROMPT)
        print(response.strip())
        transcript += response + "\n"

        if "Final Answer:" in response:
            break

        tool_name, arguments = parse_action(response)
        if tool_name is None or arguments is None:
            print("🛡️ GUARDRAIL: Không phát hiện Action hợp lệ trong phản hồi, ngắt lặp an toàn.")
            break

        observation = execute_tool(tool_name, arguments)
        print(f"👁️ Observation: {observation}")
        transcript += f"Observation: {observation}\n"
    else:
        print(f"🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("==================================================")
    
    # Khởi tạo Multi-Provider LLM Adapter (Đọc từ biến môi trường LLM_PROVIDER)
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
    
    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")
    
    # Chạy thử câu test số 3
    sample_query = tests[2]["question"]
    
    print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
    run_baseline_chatbot(sample_query, provider)
    
    print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT ---")
    run_react_agent(sample_query, provider)
