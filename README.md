# FolderMaker

**FolderMaker** is a free and open-source Python library that creates complete project folder and file structures from a text tree copied from AI assistant.

Instead of manually creating every folder and file, paste the AI-generated structure into a `.txt` file and run one Python command. FolderForge will create the full structure automatically.

## Features

- Creates folders and files from an AI-generated text tree
- Supports nested folders and files
- Understands tree symbols such as `│`, `├──`, and `└──`
- Supports Windows paths such as `D:\MY_AGENT\`
- Detects folders with trailing `\` or `/`
- Detects files such as `main.py`, `README.md`, and `Modelfile`
- Creates empty folders such as `logs\`, `workspace\`, and `venv\`
- Includes a dry-run mode to preview the result
- No external dependencies
- MIT licensed

## Installation

### Install from source

1. Download or clone this repository.

```powershell
git clone [https://github.com/Anni95-bot/foldermaker.git]
cd foldermaker
```

2. Install the library:

```powershell
pip install foldermaker.
```
### 1. Create a structure file

Create a file named `structure.txt`.

Paste your AI-generated folder tree into it exactly as shown by the AI assistant.

Example:

```text
D:\MY_AGENT\
│
├── Modelfile
├── main.py
├── config\
│   └── settings.py
│
├── core\
│   ├── ollama_client.py
│   ├── agent.py
│   ├── planner.py
│   └── tool_executor.py
│
├── tools\
│   ├── web_search.py
│   ├── browser.py
│   ├── file_manager.py
│   └── code_executor.py
│
├── memory\
│   ├── database.py
│   ├── long_term_memory.py
│   └── feedback.py
│
├── knowledge\
│   └── document_reader.py
│
├── task_manager\
│   └── queue.py
│
├── logs\
├── generated_tools\
├── workspace\
└── venv\
```

### 2. Create a Python runner file

Create a file named `main.py`:

```python
import foldermaker

folderforge.build(
    structure_file="structure.txt",
    output_dir=r"D:\MY_AGENT"
)
```

### 3. Run the script

```powershell
python main.py
```

FolderMaker will create this structure:

```text
D:\MY_AGENT\
├── Modelfile
├── main.py
├── config\settings.py
├── core\ollama_client.py
├── core\agent.py
├── core\planner.py
├── core\tool_executor.py
├── tools\web_search.py
├── tools\browser.py
├── tools\file_manager.py
├── tools\code_executor.py
├── memory\database.py
├── memory\long_term_memory.py
├── memory\feedback.py
├── knowledge\document_reader.py
├── task_manager\queue.py
├── logs\
├── generated_tools\
├── workspace\
└── venv\
```

## Command-Line Usage

After installing FolderForge, you can also use it from the terminal:

```powershell
foldermaker structure.txt -o D:\MY_AGENT
```

To preview what will be created without creating anything:

```powershell
foldermaker structure.txt -o D:\MY_AGENT --dry-run
```

## Python API

### Create from a `.txt` file

```python
import foldermaker

folderforge.build(
    structure_file="structure.txt",
    output_dir=r"D:\MY_AGENT"
)
```

### Create from tree text directly

```python
import foldermaker

tree = """
D:\MY_AGENT\
│
├── main.py
├── config\
│   └── settings.py
├── core\
│   ├── agent.py
│   └── planner.py
"""

foldermaker.build_from_text(
    tree_text=tree,
    output_dir=r"D:\MY_AGENT"
)
```

### Preview without creating files

```python
import foldermaker

folderforge.build(
    structure_file="structure.txt",
    output_dir=r"D:\MY_AGENT",
    dry_run=True
)
```

## Folder and File Detection

FolderForge uses these rules:

| Example | Created as | Reason |
|---|---|---|
| `config\` | Folder | Ends with `\` |
| `tools/` | Folder | Ends with `/` |
| `main.py` | File | Has a file extension |
| `README.md` | File | Has a file extension |
| `Modelfile` | File | Has no children |
| `logs\` | Folder | Ends with `\` |
| `core` | Folder | Has child files or folders |

## Supported Tree Formats

FolderForge supports common AI-generated tree formats, including:

```text
project/
├── main.py
├── config/
│   └── settings.py
└── core/
    ├── agent.py
    └── planner.py
```

And Windows-style trees:

```text
D:\MY_AGENT\
│
├── main.py
├── config\
│   └── settings.py
└── core\
    ├── agent.py
    └── planner.py
```

## Project Structure

```text
folderforge/
├── folderforge/
│   ├── __init__.py
│   ├── parser.py
│   └── builder.py
├── structure.txt
├── generate_project.py
├── README.md
├── LICENSE
└── pyproject.toml
```

## Safety Notes

- FolderMaker creates empty files only; it does not generate file contents.
- Existing files are not overwritten.
- Existing folders are reused safely.
- Use `dry_run=True` first if you are unsure where the structure will be created.

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Add examples or tests if possible
5. Submit a pull request

## License

This project is released under the MIT License. See the [`LICENSE`](LICENSE) file for details.
