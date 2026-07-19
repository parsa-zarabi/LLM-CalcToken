# LLM-CalcToken 🚀

An ultra-lightweight middleware for Small/Large Language Models to offload mathematical processing directly to the system's hardware CPU.

## The Problem
LLMs (especially smaller models) waste tokens, consume heavy GPU/NPU compute, and often hallucinate when doing math token-by-token.

## The Solution
By teaching your LLM to output `[CALC: 2 + 2]` or `[CAL: 2 + 2]`, **LLM-CalcToken** intercepts the generation, calculates the math using Python's ultra-fast built-in AST (Abstract Syntax Tree), and injects the result back into the prompt without executing arbitrary/unsafe code.

## Quick Start
```bash
git clone https://github.com/YOUR_USERNAME/LLM-CalcToken.git
cd LLM-CalcToken
python examples/run_inference.py
```

## Features
- **Zero Dependencies:** Core engine uses native Python libraries (`re`, `ast`).
- **100% Safe Execution:** Math is parsed via AST trees, avoiding the security risks of Python's `eval()`.
- **Plug & Play:** Wrap it around any Hugging Face, OpenAI, or local LLM generation loop.
