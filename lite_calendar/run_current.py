import os
import sys
from pathlib import Path
import subprocess


def main():
    if len(sys.argv) < 2:
        print('Usage: run_current.py <relative_path_to_py_file_from_project_root>')
        sys.exit(1)

    project_root = Path(__file__).parent.parent.resolve()
    # sys.path.insert(0, str(project_root))  # Эту строку можно оставить, но subprocess свой sys.path не видит

    file_path = (project_root / sys.argv[1]).resolve()
    print(f'project_root = {project_root}')
    print(f'file_path = {file_path}')

    relative_path = file_path.relative_to(project_root)

    module_name = str(relative_path.with_suffix('')).replace('\\', '.').replace('/', '.')
    print(f'▶ Запуск модуля: {module_name}')

    python_executable = Path(sys.executable).parent / sys.executable
    cmd = [python_executable, '-m', module_name]

    # Добавляем cwd=project_root, чтобы subprocess запускался из корня проекта
    result = subprocess.run(cmd, cwd=str(project_root))

    if result.returncode != 0:
        print(f'Ошибка запуска модуля {module_name}, код выхода: {result.returncode}')
        sys.exit(result.returncode)


if __name__ == '__main__':
    main()