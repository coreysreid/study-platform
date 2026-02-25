from django.db import migrations


def seed_flashcards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('study', 'Course')
    Topic = apps.get_model('study', 'Topic')
    Flashcard = apps.get_model('study', 'Flashcard')

    system_user = User.objects.filter(username='system').first()
    if not system_user:
        return

    course = Course.objects.filter(
        name='Linux Fundamentals (LFCA)', created_by=system_user
    ).first()
    if not course:
        return

    topics = {t.name: t for t in Topic.objects.filter(course=course)}

    def add_cards(topic_name, cards):
        topic = topics.get(topic_name)
        if not topic or Flashcard.objects.filter(topic=topic).exists():
            return
        for card in cards:
            Flashcard.objects.create(topic=topic, **card)

    # -------------------------------------------------------------------------
    # 1. Linux Basics & CLI
    # -------------------------------------------------------------------------
    add_cards('Linux Basics & CLI', [
        {
            'question': 'What is the Linux kernel?',
            'answer': 'The kernel is the core of the Linux OS: it manages hardware resources (CPU, memory, I/O), provides system calls for programs, and handles process scheduling, memory management, device drivers, and networking.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between a shell and a terminal emulator?',
            'answer': 'A shell (bash, zsh, fish) is the command interpreter that processes commands. A terminal emulator (GNOME Terminal, xterm, Konsole) is the GUI application that provides a text window and connects to the shell. You interact with the shell through the terminal.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What do the following ls flags do: -l, -a, -h, -R?',
            'answer': '-l: long listing (permissions, owner, size, date). -a: show all including hidden files (starting with .). -h: human-readable file sizes (K, M, G). -R: recursive listing of subdirectories.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain the Linux directory hierarchy: /, /bin, /etc, /home, /var, /tmp, /usr.',
            'answer': '/: root of the filesystem. /bin: essential user binaries (ls, cp). /etc: system configuration files. /home: user home directories. /var: variable data (logs, spool). /tmp: temporary files (cleared on reboot). /usr: user programs, libraries, documentation.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What command finds the absolute path to an executable?',
            'answer': 'which <command> returns the path of the first executable found in $PATH. whereis also shows man pages and sources. type shows if it\'s built-in, aliased, or external.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe the three standard I/O streams in Linux.',
            'answer': 'stdin (fd 0): standard input — defaults to keyboard. stdout (fd 1): standard output — defaults to terminal. stderr (fd 2): standard error output — defaults to terminal. Redirection: > (redirect stdout), 2> (redirect stderr), < (redirect stdin), >> (append).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a pipe (|) in Linux and give an example?',
            'answer': 'A pipe connects stdout of one command to stdin of another. Example: ps aux | grep nginx — lists all processes and filters for lines containing "nginx". Pipes enable powerful command composition.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you get help for a Linux command?',
            'answer': 'man <command>: comprehensive manual page. <command> --help: brief usage summary. info <command>: GNU info documentation (more detailed). apropos <keyword>: search man page descriptions.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between absolute and relative paths?',
            'answer': 'Absolute path: starts from root /. E.g. /home/user/docs/file.txt. Relative path: relative to current directory. E.g. docs/file.txt or ../other_dir. . = current dir, .. = parent dir.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you search for text in files from the command line?',
            'answer': 'grep "pattern" file: search a file. grep -r "pattern" dir/: recursive search. grep -i: case-insensitive. grep -n: show line numbers. grep -v: invert match (lines not matching). grep -E: extended regex. Example: grep -rn "TODO" /home/user/code/',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 2. File System & Permissions
    # -------------------------------------------------------------------------
    add_cards('File System & Permissions', [
        {
            'question': 'Explain the Linux permission model: read, write, execute for owner, group, other.',
            'answer': 'Each file has 9 permission bits: rwxrwxrwx = owner(rwx) group(rwx) other(rwx). r=read(4), w=write(2), x=execute(1). chmod 755 = rwxr-xr-x (owner: all; group/other: read+execute). Directories: x means enter.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you change file permissions and ownership?',
            'answer': 'chmod: change permissions. chmod 644 file, chmod u+x file, chmod -R 755 dir/. chown: change owner. chown user:group file, chown -R user:group dir/. chgrp: change group only.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is umask and how does it affect new file permissions?',
            'answer': 'umask subtracts permissions from the default (files: 666, dirs: 777). umask 022: files created as 644 (666-022), dirs as 755 (777-022). View with: umask. Set with: umask 027.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a hard link vs a symbolic (soft) link?',
            'answer': 'Hard link: another directory entry pointing to the same inode. File not deleted until all hard links are removed. Cannot cross filesystems. Symbolic link (symlink): a file containing a path to another file. Can cross filesystems; can be broken (dangling). ln file link (hard); ln -s target link (symlink).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What do SUID, SGID, and sticky bit do?',
            'answer': 'SUID (Set User ID, 4xxx): executable runs as file owner. E.g. /usr/bin/passwd runs as root. SGID (Set Group ID, 2xxx): on file: runs as group; on dir: new files inherit directory group. Sticky bit (1xxx): on dir (e.g. /tmp): only file owner can delete their files.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you find files with specific criteria using the find command?',
            'answer': 'find /path -name "*.log": by name. find / -type f -size +10M: files over 10 MB. find / -user john: owned by john. find / -perm 777: permission 777. find / -mtime -7: modified in last 7 days. -exec ls -lh {} \\;: execute command on results.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is an inode in Linux?',
            'answer': 'An inode is a data structure on disk that stores metadata about a file: permissions, owner, size, timestamps, and pointers to data blocks. The inode does NOT store the filename — that is stored in the directory entry. Each file has a unique inode number per filesystem.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Name common Linux filesystems and their key characteristics.',
            'answer': 'ext4: default for most Linux distros; journalling, large file/filesystem support. xfs: high performance, good for large files. btrfs: copy-on-write, snapshots, RAID. tmpfs: RAM-based, volatile. vfat/exFAT: cross-platform compatibility. Use df -T to view filesystem types.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 3. Process Management
    # -------------------------------------------------------------------------
    add_cards('Process Management', [
        {
            'question': 'What is the difference between a process and a thread?',
            'answer': 'A process is an independent program instance with its own memory space, PID, file descriptors. A thread is a lightweight execution unit within a process, sharing the same memory and resources. Linux uses POSIX threads (pthreads); kernel represents both as tasks.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe the Linux process states.',
            'answer': 'R: Running or runnable (in queue). S: Interruptible sleep (waiting for event). D: Uninterruptible sleep (I/O wait). Z: Zombie (finished but parent not called wait()). T: Stopped (by signal or debugger). I: Idle kernel thread.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you view and manage processes in Linux?',
            'answer': 'ps aux: snapshot of all processes. top or htop: real-time process monitor. kill PID: send SIGTERM. kill -9 PID: send SIGKILL (force). killall name: kill by name. nice -n 10 cmd: start with lower priority. renice 10 -p PID: change priority of running process.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a zombie process and how do you deal with it?',
            'answer': 'A zombie is a process that has finished execution but its parent hasn\'t called wait() to read its exit status. The zombie consumes a PID. Fix: find the parent (ps -o ppid= -p <zombie_pid>) and signal the parent, or if the parent is faulty, kill the parent.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you run a process in the background and manage it?',
            'answer': 'Append & to run in background: cmd &. jobs: list background jobs. fg %n: bring job n to foreground. bg %n: resume suspended job in background. Ctrl+Z: suspend foreground job. nohup cmd &: run immune to SIGHUP (survives terminal close).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are signals in Linux and name the most important ones?',
            'answer': 'Signals are software interrupts sent to processes. Key signals: SIGTERM (15): polite request to terminate. SIGKILL (9): forceful kill (cannot be caught). SIGHUP (1): hang up / reload config. SIGINT (2): interrupt (Ctrl+C). SIGSTOP (19): pause process. SIGCONT (18): resume.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is systemd and how do you use systemctl?',
            'answer': 'systemd is the init system (PID 1) on most modern Linux distros. systemctl commands: start/stop/restart/status service_name. enable/disable: enable/disable service at boot. list-units: show all active units. journalctl -u service: view service logs.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 4. Networking in Linux
    # -------------------------------------------------------------------------
    add_cards('Networking in Linux', [
        {
            'question': 'How do you view network interfaces and their IP addresses in Linux?',
            'answer': 'ip addr show (or ip a): preferred modern command. ifconfig: older command (net-tools package). ip link show: interface state. nmcli: NetworkManager CLI. ip route show: routing table.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you test network connectivity from Linux?',
            'answer': 'ping host: ICMP echo test (connectivity). traceroute/tracepath host: path to host. curl URL: test HTTP connectivity. nc -zv host port: test TCP port. nmap -p port host: port scan. ss -tunap: show active connections.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you configure a static IP address on a Linux system?',
            'answer': 'Using Netplan (Ubuntu): edit /etc/netplan/*.yaml, set addresses, gateway4, nameservers, then netplan apply. Using NetworkManager: nmcli con mod "eth0" ipv4.addresses "192.168.1.100/24" ipv4.gateway "192.168.1.1". Direct (temporary): ip addr add 192.168.1.100/24 dev eth0.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the /etc/hosts file and what is it used for?',
            'answer': '/etc/hosts maps hostnames to IP addresses locally, bypassing DNS. Checked before DNS resolution (typically). Used for: static name resolution, blocking domains (map to 0.0.0.0), development (map custom hostnames to localhost).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you configure DNS resolution in Linux?',
            'answer': '/etc/resolv.conf: nameserver <IP> entries (managed by systemd-resolved or NetworkManager). /etc/nsswitch.conf: controls resolution order (files dns). systemd-resolved: systemctl status systemd-resolved; resolvectl status. On Ubuntu, /etc/resolv.conf is a symlink to /run/systemd/resolve/stub-resolv.conf.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you use SSH to connect to a remote server and transfer files?',
            'answer': 'Connect: ssh user@host, ssh -p 2222 user@host (non-default port). Key auth: ssh-keygen (generate key pair), ssh-copy-id user@host (copy public key). File transfer: scp file user@host:/path, scp -r dir/ user@host:/path. sftp user@host: interactive file transfer.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is iptables and what are its main tables and chains?',
            'answer': 'iptables is the Linux kernel firewall/NAT tool. Tables: filter (packet filtering), nat (address translation), mangle (packet alteration). Chains: INPUT (incoming to local), OUTPUT (outgoing from local), FORWARD (through the machine), PREROUTING, POSTROUTING. Rules are processed in order; default policy applies if no rule matches.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you configure a basic firewall using ufw (Uncomplicated Firewall)?',
            'answer': 'ufw enable: enable firewall. ufw status verbose: show rules. ufw allow 22/tcp: allow SSH. ufw allow from 192.168.1.0/24: allow subnet. ufw deny 23: deny Telnet. ufw delete allow 80: remove rule. ufw reset: clear all rules. Default: deny incoming, allow outgoing.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 5. Shell Scripting
    # -------------------------------------------------------------------------
    add_cards('Shell Scripting', [
        {
            'question': 'What is the shebang line and why is it needed?',
            'answer': '#! (shebang) at the first line specifies the interpreter. E.g. #!/bin/bash tells the kernel to use bash. #!/usr/bin/env python3 uses the python3 found in PATH. Without it, the shell tries to interpret the file as shell commands.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do variables work in bash scripting?',
            'answer': 'Assignment: VAR=value (no spaces around =). Access: $VAR or ${VAR}. Read-only: readonly VAR. Export to child processes: export VAR. Special: $0 (script name), $1-$9 (arguments), $# (arg count), $? (last exit code), $$ (PID), $@ (all args).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Write a bash if-else statement that checks if a file exists.',
            'answer': 'if [ -f "/path/to/file" ]; then\n    echo "File exists"\nelif [ -d "/path/to/file" ]; then\n    echo "It\'s a directory"\nelse\n    echo "Not found"\nfi\nTest operators: -f (regular file), -d (directory), -e (exists), -r/-w/-x (readable/writable/executable).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Write a bash for loop that processes all .txt files in the current directory.',
            'answer': 'for file in *.txt; do\n    echo "Processing: $file"\n    # do something with $file\ndone\n\nC-style: for ((i=0; i<10; i++)); do echo $i; done\nLoop over array: for item in "${array[@]}"; do ... done',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between $() and `` (backticks) in bash?',
            'answer': 'Both perform command substitution — replace the expression with the command output. $() is preferred: readable, nestable ($(cmd1 $(cmd2))), handles special characters better. Backticks `` are older, harder to nest, and escape rules differ.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you handle errors in bash scripts?',
            'answer': 'set -e: exit on error. set -u: error on undefined variable. set -o pipefail: fail if any pipe command fails. set -x: debug/trace mode. Check exit codes: if ! command; then handle_error; fi. Trap: trap "cleanup" EXIT ERR.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Write a bash function that accepts arguments and returns a value.',
            'answer': 'greet() {\n    local name="$1"\n    local greeting="Hello, $name!"\n    echo "$greeting"  # return via stdout\n    return 0  # return code (0=success)\n}\n\nresult=$(greet "World")\necho "$result"\n\nNote: functions return exit codes (0-255), not arbitrary values. Use echo/stdout for string returns.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Write a bash script step that reads a configuration file line by line.',
            'answer': '',
            'hint': 'Use while read loop with input redirection',
            'difficulty': 'medium',
            'question_type': 'step_by_step',
            'uses_latex': False,
            'steps': [
                {'move': 'Create config file example', 'detail': 'config.txt contains: KEY=value pairs'},
                {'move': 'Read loop', 'detail': 'while IFS= read -r line; do'},
                {'move': 'Skip comments/blanks', 'detail': '  [[ "$line" =~ ^#.*$ ]] && continue; [[ -z "$line" ]] && continue'},
                {'move': 'Parse key=value', 'detail': '  key="${line%%=*}"; value="${line#*=}"; echo "Key: $key, Value: $value"'},
                {'move': 'Close loop with redirect', 'detail': 'done < config.txt'},
            ],
        },
    ])

    # -------------------------------------------------------------------------
    # 6. Package Management
    # -------------------------------------------------------------------------
    add_cards('Package Management', [
        {
            'question': 'Compare APT (Debian/Ubuntu) and DNF/YUM (RHEL/CentOS/Fedora) package managers.',
            'answer': 'APT: apt update (refresh repos), apt install pkg, apt remove pkg, apt upgrade, apt search keyword, apt list --installed. DNF/YUM: dnf install pkg, dnf remove pkg, dnf update, dnf search keyword. Both use package repositories and handle dependencies.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is a package repository and how do you add a new one on Ubuntu?',
            'answer': 'A repository is a server hosting packages. Ubuntu repos listed in /etc/apt/sources.list and /etc/apt/sources.list.d/. Add PPA: add-apt-repository ppa:user/repo. Add custom: echo "deb [signed-by=/etc/apt/keyrings/key.gpg] URL suite component" > /etc/apt/sources.list.d/custom.list. Then: apt update.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is Snap and how does it differ from APT packages?',
            'answer': 'Snap packages are containerised (bundle dependencies), work across distros, auto-update. APT packages use system libraries (lighter), distro-specific, manually updated. Snap commands: snap install pkg, snap list, snap refresh. Trade-off: snaps are larger, sometimes slower startup.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you install software from source code on Linux?',
            'answer': 'Classic configure-make-install: 1) tar -xzf package.tar.gz && cd package/. 2) ./configure (checks dependencies, generates Makefile). 3) make (compiles). 4) sudo make install (installs to /usr/local/). Cmake: cmake -DCMAKE_INSTALL_PREFIX=/usr/local . && make && sudo make install.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you list all installed packages and check if a package is installed?',
            'answer': 'Debian/Ubuntu: dpkg -l (list all), dpkg -l | grep nginx (search), dpkg -s nginx (show status), apt list --installed. RHEL/Fedora: rpm -qa (all packages), rpm -q nginx, dnf list installed. Also: which nginx to check if binary is in PATH.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 7. System Security
    # -------------------------------------------------------------------------
    add_cards('System Security', [
        {
            'question': 'What is the principle of least privilege and how does it apply in Linux?',
            'answer': 'Every user/process should have only the minimum permissions needed for its function. Linux application: use regular user accounts (not root), use sudo for specific elevated tasks, set restrictive file permissions, use chroot/containers for isolation, configure SELinux/AppArmor mandatory access control.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How does sudo work and how do you configure it?',
            'answer': 'sudo executes a command as another user (default: root) based on rules in /etc/sudoers (edit with visudo). Syntax: user host=(run_as) command. Example: john ALL=(ALL:ALL) ALL. Group: %admin ALL=(ALL) ALL. NOPASSWD: john ALL=(ALL) NOPASSWD: /usr/bin/systemctl.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is SELinux and what are its operating modes?',
            'answer': 'Security-Enhanced Linux: kernel-level mandatory access control (MAC). Every process and file has a security context; policies define allowed interactions. Modes: Enforcing (blocks and logs violations), Permissive (logs only, nothing blocked), Disabled (SELinux off). Check: getenforce. Set: setenforce 0|1. Config: /etc/selinux/config.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you harden SSH configuration?',
            'answer': 'Edit /etc/ssh/sshd_config: PermitRootLogin no, PasswordAuthentication no (key auth only), Port 2222 (non-default), AllowUsers user1 user2, MaxAuthTries 3, ClientAliveInterval 300. Restart: systemctl restart sshd. Also: use fail2ban to block repeated failed logins.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What do PAM (Pluggable Authentication Modules) do in Linux?',
            'answer': 'PAM provides a framework for authentication, authorisation, and session management. Config files in /etc/pam.d/. Modules (pam_unix, pam_ldap, pam_faillock) are stacked with control flags: required (must pass, continue), requisite (must pass, stop), sufficient (pass = done), optional.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What tools can you use to check for rootkits and system integrity in Linux?',
            'answer': 'rkhunter (Rootkit Hunter): scans for rootkits, backdoors, local exploits — rkhunter --check. chkrootkit: another rootkit scanner. AIDE (Advanced Intrusion Detection Environment): creates baseline of file hashes, detects changes — aide --check. Tripwire: commercial/open-source file integrity monitoring.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Explain log files in Linux and the role of journald.',
            'answer': 'Traditional logs: /var/log/syslog (general), /var/log/auth.log (authentication), /var/log/kern.log (kernel), /var/log/apache2/ (web server). journald (systemd): binary log storage, journalctl -f (follow), journalctl -u service, journalctl --since "1 hour ago", journalctl -p err (priority filter).',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])

    # -------------------------------------------------------------------------
    # 8. LFCA Exam Preparation
    # -------------------------------------------------------------------------
    add_cards('LFCA Exam Preparation', [
        {
            'question': 'What topics does the LFCA (Linux Foundation Certified IT Associate) exam cover?',
            'answer': 'LFCA domains: Linux Fundamentals (~20%), System Administration (~26%), Security (~10%), Networking (~20%), DevOps/Cloud (~17%), Containers & Virtualisation (~7%). Two-hour exam, multiple choice and performance-based. Passing score ~66%.',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is the difference between user space and kernel space?',
            'answer': 'Kernel space: where the kernel runs with full hardware access. User space: where user applications run with limited access. User programs access hardware through system calls (syscalls) — a controlled interface. Crash in user space ≠ system crash; crash in kernel space = kernel panic.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What is virtualisation and what is a hypervisor?',
            'answer': 'Virtualisation: creating virtual versions of hardware (VMs). Hypervisor: software that creates/manages VMs. Type 1 (bare-metal): runs directly on hardware — KVM, VMware ESXi, Hyper-V. Type 2 (hosted): runs on OS — VirtualBox, VMware Workstation. KVM is built into the Linux kernel.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are containers and how do they differ from VMs?',
            'answer': 'Containers: lightweight isolated environments sharing the host OS kernel. VMs: full OS in virtualised hardware. Containers: faster startup, less overhead, portable. Docker: container runtime. podman: rootless alternative. Containers use Linux namespaces and cgroups for isolation.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are cgroups and namespaces used for in Linux?',
            'answer': 'cgroups (control groups): limit and account for resource usage (CPU, memory, I/O, network) per group of processes. Used by containers and systemd. Namespaces: isolate system resources so processes in different namespaces have separate views of: PID, network, filesystem, IPC, UTS (hostname), user.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'Describe the Linux boot process in order.',
            'answer': '1) BIOS/UEFI firmware — hardware POST. 2) Bootloader (GRUB2) — loads kernel. 3) Kernel — decompresses, initialises hardware, mounts initramfs. 4) initramfs — temporary root, loads essential drivers. 5) PID 1 (systemd/init) — starts system services. 6) Target/runlevel — multi-user.target, graphical.target, etc.',
            'difficulty': 'hard',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What are the key DevOps/cloud concepts tested in LFCA?',
            'answer': 'CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions). Infrastructure as Code (Ansible, Terraform). Version control (Git: branch, commit, merge, PR). Cloud concepts: IaaS, PaaS, SaaS. Container orchestration: Kubernetes basics (pod, service, deployment). Monitoring: Prometheus, Grafana basics.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'What cron syntax runs a job every weekday at 9:15 AM?',
            'answer': '15 9 * * 1-5 /path/to/script.sh\nCron field order: minute hour day-of-month month day-of-week\n15 = 15th minute, 9 = 9 AM, * = any day, * = any month, 1-5 = Mon-Fri.\nView crontab: crontab -l. Edit: crontab -e. System cron: /etc/cron.d/ and /etc/crontab.',
            'difficulty': 'medium',
            'question_type': 'standard',
            'uses_latex': False,
        },
        {
            'question': 'How do you monitor system resources in Linux?',
            'answer': 'CPU/memory: top, htop, vmstat 1. Disk: df -h (filesystem usage), du -sh dir/ (directory size), iostat -x 1. Network: iotop, nethogs, iftop, ip -s link. Logs: journalctl -f, tail -f /var/log/syslog. Performance: sar (system activity reporter, part of sysstat package).',
            'difficulty': 'easy',
            'question_type': 'standard',
            'uses_latex': False,
        },
    ])


def reverse_fn(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0021_flashcards_power_systems'),
    ]

    operations = [
        migrations.RunPython(seed_flashcards, reverse_fn),
    ]
