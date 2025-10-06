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
        (".zshrc", "https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/configs/zshrc"),
        (".p10k.zsh", "https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/configs/p10k.zsh"),
        (".tmux.conf", "https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/configs/tmux.conf"),
        ("opencode.json", "https://raw.githubusercontent.com/Fitree/DevEnvSetup/refs/heads/main/configs/opencode.json")
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
        (".gitconfig", "https://raw.githubusercontent.com/Fitree/dev-env-setup/refs/heads/main/configs/gitconfig"),
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

def install_opencode():
    print_title("Install Opencode")
    res = subprocess.run(
        "curl -fsSL https://opencode.ai/install | bash",
        shell=True,
        capture_output=True,
        text=True,
    )
    if res.returncode == 0:
        print("✅Opencode installation script executed successfully.")
    else:
        print("❌Opencode installation script failed to execute.")
        print(res.stderr)

    zshrc_path = Path.home() / ".zshrc"
    if zshrc_path.exists():
        res = subprocess.run(
            "echo '\n#Opencode\nexport PATH=\"$HOME/.opencode/bin:$PATH\"' >> ~/.zshrc",
            shell=True,
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            print("✅Successfully added Opencode to PATH in .zshrc.")
        else:
            print("❌Failed to add Claude to PATH in .zshrc.")
            print(res.stderr)
    else:
        print(f"⚠️ {zshrc_path} does not exist, skipping PATH modification in .zshrc.")

    cfg_path = Path.home() / ".config/opencode/opencode.json"
    if cfg_path.exists():
        print(f"⚠️ {cfg_path} already exists, skipping download.")
    else:
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_url = "https://raw.githubusercontent.com/Fitree/DevEnvSetup/refs/heads/main/configs/opencode.json"
        res = subprocess.run(
            f"curl -fsSL {cfg_url} -o {cfg_path}",
            shell=True,
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            print("✅Successfully downloaded opencode.json configuration file.")
        else:
            print("❌Failed to download opencode.json configuration file.")
            print(res.stderr)

def install_claude_code():
    print_title("Install Claude Code")
    res = subprocess.run(
        "curl -fsSL https://claude.ai/install.sh | bash",
        shell=True,
        capture_output=True,
        text=True,
    )
    if res.returncode == 0:
        print("✅Claude installation script executed successfully.")
    else:
        print("❌Claude installation script failed to execute.")
        print(res.stderr)

    zshrc_path = Path.home() / ".zshrc"
    if zshrc_path.exists():
        res = subprocess.run(
            "echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.zshrc",
            shell=True,
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            print("✅Successfully added Claude to PATH in .zshrc.")
        else:
            print("❌Failed to add Claude to PATH in .zshrc.")
            print(res.stderr)
    else:
        print(f"⚠️ {zshrc_path} does not exist, skipping PATH modification in .zshrc.")

    bashrc_path = Path.home() / ".bashrc"
    if bashrc_path.exists():
        res = subprocess.run(
            "echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.bashrc",
            shell=True,
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            print("✅Successfully added Claude to PATH in .bashrc.")
        else:
            print("❌Failed to add Claude to PATH in .bashrc.")
            print(res.stderr)
    else:
        print(f"⚠️ {bashrc_path} does not exist, skipping PATH modification in .bashrc.")


if __name__ == "__main__":
    check_requirements()
    try_install_oh_my_zsh()
    try_intall_zsh_plugins()
    download_config_files()
    download_and_append_config()
    install_claude_code()

    print_title("Autosetup completed!", color=BLUE)
    print(
        "Please restart your terminal or run 'source ~/.zshrc' "
        "(or `source ~/.bashrc`) to apply the changes."
    )
    print()
