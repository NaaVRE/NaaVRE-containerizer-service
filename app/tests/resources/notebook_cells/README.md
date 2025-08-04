Each directory contains:

- `notebook.ipynb`: notebook (input for `/extract_cell`)
- `cell.json`: cell description (expected output for `/extract_cell`, and input for `/containerize`)
- `payload_extract_cell.json`: payload for `/extract_cell`, without the notebook (it is in `notebook.ipynb`)
- `payload_containerize.json`: payload for `/containerize`, without the cell description (it is in `cell.json`)
