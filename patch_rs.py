import os
import re
import requests


def main():
    path = os.getenv('RS_FILE_PATH')
    out_path = os.getenv('RS_FILE_OUT_PATH', path)
    with open(path, 'r') as f:
        contents = f.read()

    lines = contents.splitlines()
    new_lines = []

    for line in lines:
        regex = re.compile(r'^\$\$DOC_BLOCK:([0-9a-f]+)\$\$$')
        match = regex.match(line)
        if not match:
            new_lines.append(line)
            continue
        ref = match.group(1)
        url = f'https://github.com/dnbln/nb-rs/blob/{ref}/README.md?raw=true'
        response_text = requests.get(url).text
        add_lines = False
        for response_line in response_text.splitlines():
            if add_lines:
                new_lines.append(response_line)
            else:
                if response_line == '## Usage':
                    add_lines = True
                    new_lines.append(response_line)

    with open(out_path, 'w') as f:
        f.write('\n'.join(new_lines))


if __name__ == '__main__':
    main()
