# (PoC) In a production environment, integrate this into your actual inference pipeline.

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.calc_engine import TokenInterceptor


def mock_llm(prompt):
    if "[Hardware Offload]" not in prompt:
        return " The calculation is heavy. I will offload it to CPU: [CALC: 452 * 18]"
    else:
        return " As calculated by the hardware, the process is complete."

if __name__ == "__main__":
    interceptor = TokenInterceptor()
    
    print("Test 1: Static Text Parsing")
    raw_text = "AI output string with [CALC: 1024 / 8] and [CAL: 2**10]"
    print("Original:", raw_text)
    print("Processed:", interceptor.process_static_text(raw_text))
    
    print("\n Test 2: Agentic LLM Loop")
    system_prompt = "User: What is 452 * 18?\nAssistant:"
    final_context = interceptor.run_loop(system_prompt, mock_llm)
    print(final_context)
