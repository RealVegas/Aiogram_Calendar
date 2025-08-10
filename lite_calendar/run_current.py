import sys
from pathlib import Path
import subprocess


def main():
    if len(sys.argv) < 2:
        print('Usage: run_current.py <relative_path_to_py_file_from_project_root>')
        sys.exit(1)

    project_root = Path(__file__).parent.parent.resolve()

    file_path = (project_root / sys.argv[1]).resolve()
    print(f'project_root : {project_root}')
    print(f'file_path : {file_path}\n')

    relative_path = file_path.relative_to(project_root)

    module_name = str(relative_path.with_suffix('')).replace('\\', '.').replace('/', '.')
    print(f'▶ Запуск модуля: {file_path.name}')

    # if module_name in sys.modules:
    #     print(f'Удаляю модуль {module_name} из памяти')
    #     del sys.modules[module_name]

    python_exe = Path(sys.executable)
    cmd = [python_exe, '-m', module_name]

    # Добавляем cwd=project_root, чтобы subprocess запускался из корня проекта
    result = subprocess.run(cmd, cwd=str(project_root))

    if result.returncode != 0:
        print(f'Ошибка запуска модуля {module_name}, код выхода: {result.returncode}')
        sys.exit(result.returncode)


if __name__ == '__main__':
    main()