# winuvloop

`winuvloop` is a Python package that ensures you always use the best event loop for your platform. 
It automatically sets up `uvloop` on Linux/POSIX systems and `winloop` on Windows, optimizing performance and compatibility without extra configuration. 
By using `winuvloop`, you can streamline your development process and focus on writing your application code, knowing that the right event loop is always in place for seamless cross-platform functionality.

## Features

- **Cross-Platform Compatibility**: Automatically installs `uvloop` on POSIX systems and `winloop` on Windows.
- **Easy Integration**: Just add `winuvloop` to your `pyproject.toml` or `requirements.txt` and let it handle the rest.
- **Simplified Event Loop Setup**: No need to worry about platform-specific event loop installation and initialization.

## Installation

You can install `winuvloop` via pip:

```bash
pip install winuvloop
```

Or by adding it to your `pyproject.toml` in a Poetry-managed project:

```bash
poetry add winuvloop
```

## Usage

Simply import the package, and use it as you would uv/win loop:

```python
import winuvloop

async def my_coroutine():
   ...  # your function here

# the preferred way to use win/uv loop is with the run method
winuvloop.run(my_coroutine())
```

alternatively, you can install the loop globally:
```python
import winuvloop

# The correct event loop is now installed and ready to use.
winuvloop.install()
```

## Requirements

- Python 3.11 or higher
- `uvloop` for POSIX systems
- `winloop` for Windows systems

## Platform Support

- **POSIX (Linux, macOS)**: Installs `uvloop`
- **Windows**: Installs `winloop`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue.

## Contact

For any questions or suggestions, please contact `aviadr1@gmail.com`.
