import subprocess
from pathlib import Path


YELLOW = "\033[93m"
BLUE = "\033[38;2;1;173;252m"
RESET = "\033[0m"


def print_title(title, color=BLUE):
    border = "#" * (len(title) + 6)
    print()
    print(f"{color}{border}{RESET}")
    print(f"{color}## {title} ##{RESET}")
    print(f"{color}{border}{RESET}")


def check_requirements():
    print_title("Check requirements")
    requirements = ["zsh", "git", "curl"]
    satisfied = True
    for req in requirements:
        res = subprocess.run(
            f"which {req}",
            shell=True,
            capture_output=True,
            text=True,
            )
        if res.returncode != 0:
            print("❌", end="")
            satisfied = False
        else:
            print("✅", end="")
        print(req)

    if not satisfied:
        print("Please install the missing requirements and run the script again.")

    print_title("Check optional requirements")
    optional = ["tmux"]
    for opt in optional:
        res = subprocess.run(
            f"which {opt}",
            shell=True,
            capture_output=True,
            text=True,
            )
        if res.returncode != 0:
            print("❌", end="")
            satisfied = False
        else:
            print("✅", end="")
        print(req)


def try_install_oh_my_zsh():
    print_title("Install Oh My Zsh")
    subprocess.run(
        f"yes | sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\"",
        shell=True,
    )

def try_intall_zsh_plugins():
    print_title("Install Zsh plugins")
    subprocess.run(
        "git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k",
        shell=True,
    )
    subprocess.run(
        "git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions",
        shell=True,
    )
    subprocess.run(
        "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting",
        shell=True,
    )


def backup_files():
    print_title("Backup configuration files")
    home = Path.home()
    files_to_backup = [".zshrc", ".gitconfig", ".tmux.conf", ".p10k.zsh"]
    backup_dir = home / "config_backup"
    backup_dir.mkdir(exist_ok=True)

    for file_name in files_to_backup:
        file_path = home / file_name
        if file_path.exists():
            backup_path = backup_dir / file_name
            file_path.rename(backup_path)
            print(
                f"{YELLOW}{file_path}{RESET} exists. "
                f"Backed up to {YELLOW}{backup_path}{RESET}"
            )
        else:
            print(f"{YELLOW}{file_path}{RESET} does not exist, skipping backup.")


def download_config_files():
    print_title("Download configuration files")
    download_list = [
        (".zshrc", "https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/configs/.zshrc"),
        (".p10k.zsh", "https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/configs/.p10k.zsh"),
        (".tmux.conf", "https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/configs/.tmux.conf"),
    ]

    home = Path.home()
    backup_dir = home / "config_backup"

    for file_name, url in download_list:
        print("Downloading", file_name)
        file_path = home / file_name

        if file_path.exists():
            backup_path = backup_dir / file_name
            backup_dir.mkdir(exist_ok=True, parents=True)
            file_path.rename(backup_path)
            print(
                "  Found existing config file. Backup: "
                f"{YELLOW}{file_path}{RESET} -> {YELLOW}{backup_path}{RESET}"
            )
            backup = True
        else:
            backup = False

        res = subprocess.run(
            f"curl -fsSL {url} -o {file_path}",
            shell=True,
            capture_output=True,
            text=True,
        )

        if res.returncode != 0:
            print(f"  ❌Failed to download {file_name}")
            if backup:
                backup_path.rename(file_path)
                print(
                    "    Restore backup: "
                    f"{YELLOW}{backup_path}{RESET} -> {YELLOW}{file_path}{RESET}")

        else:
            print(f"  ✅Completed downloading {file_name}")


def download_and_append_config():
    print_title("Append configuration on existing one")
    download_list = [
        (".gitconfig", "https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/configs/.gitconfig"),
    ]

    home = Path.home()

    for file_name, url in download_list:
        print("Downloading", file_name)
        file_path = home / file_name

        if not file_path.exists():
            subprocess.run(
                f"touch {file_path}",
                shell=True,
            )

        res = subprocess.run(
            f"curl -fsSL {url}",
            shell=True,
            capture_output=True,
            text=True,
        )

        if res.returncode != 0:
            print(f"  ❌Failed to download {file_name}")
        else:
            with open(file_path, "a") as f:
                f.write(res.stdout)
            print(f"  ✅Appended configuration to {file_name}")


if __name__ == "__main__":
    check_requirements()
    try_install_oh_my_zsh()
    try_intall_zsh_plugins()
    download_config_files()
    download_and_append_config()

    print_title("Autosetup completed!", color=BLUE)
    print()
