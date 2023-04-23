import os
import vim
import openai

WINDOW_NAME="GptPyNvim"

# OPENAIのAPIキーを環境変数から取得し設定
if 'OPENAI_API_KEY' in os.environ:
    openai.api_key = os.environ['OPENAI_API_KEY']
else:
    print('環境変数OPENAI_API_KEYが設定されていません。')


def open_new_window():
    # 既存のウインドウを探し、あればそこに移動する
    for window in vim.windows:
        if os.path.basename(window.buffer.name) == WINDOW_NAME:
            vim.current.window = window
            break

    else:
        # 新しくバッファを作成する
        vim.command(f"new {WINDOW_NAME}")
        vim.command("normal! ggVGd") 

        # {BUFFER_NAME}のバッファを読み取り専用にする
        vim.command("setlocal buftype=nofile")


def main():
    try:

        # 矩形選択された行を取得
        start_row, start_col = vim.eval("getpos(\"'<\")[1:2]")
        end_row, end_col = vim.eval("getpos(\"'>\")[1:2]")
        contents = []
        for row in range(int(start_row), int(end_row) + 1):
            line = vim.eval(f"getline({row})")
            contents += [line[int(start_col) - 1 : int(end_col) - 1]]
    
        selected_text = "\\n".join(contents).strip()
    
        # GPT-3による解説コメントの生成
        if selected_text.startswith("#"):
            prompt = f"Based on the following description, write a Python code snippet that implements the described functionality: \n{selected_text}"
    
        elif selected_text.startswith("def"):
            prompt = f"Generate a detailed docstring for the following Python function, describing its purpose, parameters, and return value and find bugs: \n{selected_text}"
        else:
            raise Exception("Error: Selected text must start with # or def.")
    
        response = openai.Completion.create(engine="text-davinci-003",
                                            prompt=prompt,
                                            max_tokens=1000,
                                            n=1, stop=None,
                                            temperature=0.5)
    
        # コメントを取得
        text = response.choices[0].text.strip()
    
        # 新規にウインドウを開く
        open_new_window()
        vim.current.buffer[:] = text.splitlines()
    
    except Exception as e:
        print(f"Error: {str(e)}\n")
