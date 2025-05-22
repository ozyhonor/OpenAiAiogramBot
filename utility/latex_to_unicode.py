import re
import unicodeit
import asyncio
from menu.texts import ChatGptTexts

def latex_array_to_unicode(text):
    # Находим все блоки \begin{array}{...} ... \end{array}
    pattern = re.compile(
        r'(.*?)\\begin\{array\}\{([^\}]*)\}(.*?)\\end\{array\}',
        re.DOTALL
    )

    def array_replacer(match):
        before = match.group(1).rstrip()
        colspec = match.group(2)
        body = match.group(3)
        # Удаляем лишние пробелы и пустые строки
        lines = [line.strip() for line in body.strip().split('\\\\') if line.strip()]
        # Разбиваем строки на элементы
        matrix = [re.split(r'\s*&\s*', line) for line in lines]
        n = len(matrix)
        if n == 0:
            return before
        # Определяем ширину столбцов для выравнивания
        cols = max(len(row) for row in matrix)
        col_widths = [
            max(len(row[i]) if i < len(row) else 0 for row in matrix)
            for i in range(cols)
        ]
        # Формируем строки
        result = []
        for i, row in enumerate(matrix):
            row_str = ' '.join(
                (row[j] if j < len(row) else '').rjust(col_widths[j])
                for j in range(cols)
            )
            if i == 0:
                result.append('⎛ ' + row_str + ' ⎞')
            elif i == n - 1:
                result.append('⎝ ' + row_str + ' ⎠')
            else:
                result.append('⎜ ' + row_str + ' ⎟')
        # Если перед матрицей что-то есть (например, H =), то ставим матрицу с новой строки
        if before:
            return before + '\n' + '\n'.join(result)
        else:
            return '\n'.join(result)

    # Убираем \left( и \right) вокруг массива, если есть
    text = re.sub(r'\\left\(\s*', '', text)
    text = re.sub(r'\s*\\right\)', '', text)

    # Заменяем все матрицы
    return pattern.sub(array_replacer, text)
def latex_matrix_to_unicode(text):
    # Находим все блоки \begin{pmatrix} ... \end{pmatrix}
    pattern = re.compile(
        r'(.*?)\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',
        re.DOTALL
    )

    def matrix_replacer(match):
        before = match.group(1).rstrip()
        body = match.group(2)
        # Удаляем лишние пробелы и пустые строки
        lines = [line.strip() for line in body.strip().split('\\\\') if line.strip()]
        # Разбиваем строки на элементы
        matrix = [re.split(r'\s*&\s*', line) for line in lines]
        # Формируем юникод-матрицу
        n = len(matrix)
        if n == 0:
            return before
        # Определяем ширину столбцов для выравнивания
        cols = max(len(row) for row in matrix)
        col_widths = [
            max(len(row[i]) if i < len(row) else 0 for row in matrix)
            for i in range(cols)
        ]
        # Формируем строки
        result = []
        for i, row in enumerate(matrix):
            row_str = ' '.join(
                (row[j] if j < len(row) else '').rjust(col_widths[j])
                for j in range(cols)
            )
            if i == 0:
                result.append('⎛ ' + row_str + ' ⎞')
            elif i == n - 1:
                result.append('⎝ ' + row_str + ' ⎠')
            else:
                result.append('⎜ ' + row_str + ' ⎟')
        # Если перед матрицей что-то есть (например, G =), то ставим матрицу с новой строки
        if before:
            return before + '\n' + '\n'.join(result)
        else:
            return '\n'.join(result)

    # Заменяем все матрицы
    return pattern.sub(matrix_replacer, text)


async def convert_latex_to_unicode(latex_text):
    # Шаблон для поиска блоков кода
    code_block_pattern = re.compile(r'```(.*?)```', re.DOTALL)

    # Извлекаем блоки кода
    code_blocks = code_block_pattern.findall(latex_text)

    # Заменяем блоки кода на временные маркеры
    markers = [f'CODE=BLOCK={i}' for i in range(len(code_blocks))]
    for i, code_block in enumerate(code_blocks):
        latex_text = latex_text.replace(f'```{code_block}```', markers[i])

    # Выполняем преобразования на остальной части текста
    latex_text = latex_matrix_to_unicode(latex_text)
    latex_text = latex_array_to_unicode(latex_text)
    def process_text(text):
        text = re.sub(r'\\\[(.*?)\\\]', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'\\\((.*?)\\\)', r'\1', text)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Заменим ** на «...»
        text = text.replace('*', '⋅')  # Заменим * на ⋅
        text = re.sub(r'\\pmod\{(.*?)\}', r'mod \1', text)
        text = re.sub(r'\\bmod\{(.*?)\}', r'mod \1', text)
        text = text.replace(r'\mod', 'mod')
        text = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'⟮\1 ÷ \2⟯', text)
        text = re.sub(r'\\left(.*?)\\right', r'\1', text)
        text = re.sub(r'\\boxed\{([^}]*)\}', r'⎡\1⎤', text)
        text = text.replace(r'\ldots', '...')
        text = text.replace(r'^+', '+')
        text = text.replace(r'^⋅', '⋅')

        def bold_replacement(match):
            text = match.group(1)
            return ''.join(
                chr(ord(c) + 0x1D400 - ord('A')) if 'A' <= c <= 'Z' else
                chr(ord(c) + 0x1D41A - ord('a')) if 'a' <= c <= 'z' else c
                for c in text
            )

        # Преобразование текста в жирный
        text = re.sub(r'\\text\{(.*?)\}', bold_replacement, text)
        return text
    def replace_subscript(match):
        base = match.group(1)
        subs = match.group(2)
        return base + ''.join(ChatGptTexts.subscript_map.get(c, c) for c in subs)

    pattern = re.compile(r'\b([a-zA-Z])_([a-zA-Z0-9]+)\b')

    latex_text=(re.sub(pattern, replace_subscript, latex_text))
    latex_text = re.sub(r'(\w+)_+(\w+)', lambda m: m.group(0).replace('_', '＿'), latex_text)
    latex_text = re.sub(r'(?<=\w)_(?=\w{3,})', '＿', latex_text)  # Заменить _ на ＿ только для слов длиной 3 и более

    latex_text = latex_text.replace(r'\xrightarrow', '→')

    latex_text = process_text(latex_text)
    latex_text = await asyncio.to_thread(unicodeit.replace, latex_text)

    latex_text = latex_text.replace('`', '’')  # Заменим обратную кавычку на правую одинарную
    latex_text = re.sub(r'\\binom\{(.*?)\}\{(.*?)\}', r'⟮\1, \2⟯', latex_text)
    for i, code_block in enumerate(code_blocks):
        latex_text = latex_text.replace(markers[i], f'```{code_block}```')

    return latex_text

