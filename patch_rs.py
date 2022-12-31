import os
import requests


def patch_line(line: str) -> str:
    if line.startswith("```rs") or line.startswith("```rust"):
        return "```rust, noplaypen"
    return line


def main():
    path = os.getenv('RS_FILE_PATH')
    out_path = os.getenv('RS_FILE_OUT_PATH', path)
    commit_sha_file = os.getenv('RS_COMMIT_SHA_FILE')
    with open(path, 'r') as f:
        contents = f.read()

    with open(commit_sha_file, 'r') as f:
        commit_sha = f.read().strip()

    lines = contents.splitlines()
    new_lines = []

    for line in lines:
        if line != "$$DOC_BLOCK$$":
            new_lines.append(line)
            continue
        url = f'https://github.com/dnbln/nb-rs/blob/{commit_sha}/README.md?raw=true'
        response_text = requests.get(url).text
        add_lines = False
        for response_line in response_text.splitlines():
            if add_lines:
                new_lines.append(patch_line(response_line))
            else:
                if response_line == '## Usage':
                    add_lines = True
                    new_lines.append(patch_line(response_line))

    with open(out_path, 'w') as f:
        f.write('\n'.join(new_lines))


if __name__ == '__main__':
    main()
