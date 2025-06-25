from llm_guard.base import deepseek_modify

def main():
    print(deepseek_modify('<think><think></think></think>123'))

if __name__ == '__main__':
    main()