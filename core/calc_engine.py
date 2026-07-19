import re
import ast
import operator

class SafeMath:
    allowed_operators = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.BitXor: operator.xor,
        ast.USub: operator.neg
    }

    @staticmethod
    def eval_expr(expr):
        try:
            node = ast.parse(expr, mode='eval').body
            return str(SafeMath._eval(node))
        except Exception as e:
            return f"Error"

    @staticmethod
    def _eval(node):
        if isinstance(node, ast.Constant): # For Python 3.8+
            return node.value
        elif isinstance(node, ast.Num): # For older Python
            return node.n
        elif isinstance(node, ast.BinOp):
            return SafeMath.allowed_operators[type(node.op)](SafeMath._eval(node.left), SafeMath._eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return SafeMath.allowed_operators[type(node.op)](SafeMath._eval(node.operand))
        else:
            raise TypeError("Unsupported")

class TokenInterceptor:
    def __init__(self, pattern=r"\[CALC?:\s*(.+?)\]"):
        self.pattern = re.compile(pattern)

    def process_static_text(self, text):
        matches = self.pattern.finditer(text)
        result_text = text
        for match in matches:
            expr = match.group(1)
            result = SafeMath.eval_expr(expr)
            result_text = result_text.replace(match.group(0), f"[RESULT: {result}]")
        return result_text

    def run_loop(self, prompt, llm_generation_func, max_iterations=3):
        iteration = 0
        current_prompt = prompt
        
        while iteration < max_iterations:
            output = llm_generation_func(current_prompt)
            match = self.pattern.search(output)
            
            if match:
                expr = match.group(1)
                calc_result = SafeMath.eval_expr(expr)
                
                current_prompt += output + f"\nSystem [Hardware Offload]: RESULT = {calc_result}\nAssistant:"
                iteration += 1
            else:
                current_prompt += output
                break
                
        return current_prompt
