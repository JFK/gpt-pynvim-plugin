import os
try:
    import vim
except ImportError:
    from tests.mock_vim import vim
import openai

WINDOW_NAME = "GptPyNvim"

if 'OPENAI_API_KEY' in os.environ:
    openai.api_key = os.environ['OPENAI_API_KEY']
else:
    print("Error: OPENAI_API_KEY is not set.")


def open_new_window():
    for window in vim.windows:
        if os.path.basename(window.buffer.name) == WINDOW_NAME:
            vim.current.window = window
            break

    else:
        vim.command(f"new {WINDOW_NAME}")
        vim.command("normal! ggVGd")
        vim.command("setlocal buftype=nofile")


def main():
    try:
        start_row, start_col = vim.eval("getpos(\"'<\")[1:2]")
        end_row, end_col = vim.eval("getpos(\"'>\")[1:2]")
        contents = []
        for row in range(int(start_row), int(end_row) + 1):
            line = vim.eval(f"getline({row})")
            contents += [line[int(start_col) - 1: int(end_col) - 1]]

        selected_text = "\\n".join(contents).strip()

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

        text = response.choices[0].text.strip()

        open_new_window()
        vim.current.buffer[:] = text.splitlines()

    except Exception as e:
        print(f"Error: {str(e)}\n")
