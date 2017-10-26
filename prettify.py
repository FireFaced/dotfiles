import platform
from subprocess import call
import sys
import os.path
import tempfile

LOS = platform.linux_distribution() 
OS = LOS[0]
VERSION = LOS[1]


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " \
                             "(or 'y' or 'n').\n")


installFish = query_yes_no('Install fish?', default='yes')
if installFish:
    if OS == 'Fedora':
        call(['sudo', 'dnf', '-y', 'install', 'fish', 'python3-pip', 'python3-devel', 'git'])
        call(['sudo', 'pip3', 'install', 'thefuck'])
    elif OS == 'CentOS':
        if '6' in VERSION:
            VERSION = 6
        elif '7' in VERSION:
            VERSION = 7
        call(['sudo', 'curl', '-Lo', '/etc/yum.repos.d/fish.repo',
              'https://download.opensuse.org/repositories/shells:fish:release:2/CentOS_' + str(
                  VERSION) + '/shells:fish:release:2.repo'])
        call(['sudo', 'yum', '-y', 'install', 'epel-release'])
        call(['sudo', 'yum', '-y', 'install', 'fish', 'python3-pip', 'python3-devel', 'git'])
        call(['sudo', 'pip3', 'install', 'thefuck'])
    elif OS == 'debian':
        if '9' in VERSION:
            VERSION = 9
        elif '8' in VERSION:
            VERSION = 8
        call(['echo', '"deb http://download.opensuse.org/repositories/shells:/fish:/release:/2/Debian_' + str(
            VERSION) + '.0/ /"', '| sudo tee -a /etc/apt.sources.list.d/fish.list'])
        call(['sudo', 'apt-get', 'update'])
        call(['sudo', 'apt-get', '-y', 'install', 'fish', 'python3-pip', 'python3-dev', 'git'])
        call(['sudo', 'pip3', 'install', 'psutil', 'thefuck'])
    elif OS == 'Ubuntu':
        call(['sudo', 'add-apt-repository', '-y', 'ppa:fish-shell/release-2'])
        call(['sudo', 'apt-get', 'update'])
        call(['sudo', 'apt-get', '-y', 'install', 'fish', 'python3-pip', 'python3-dev', 'git'])
        call(['sudo', 'pip3', 'install', 'psutil', 'thefuck'])
    else:
        print 'One of two things has happened:'
        print '1) I could not detect your OS'
        print 'or 2) I do not support installing packages on your distro/OS'
        print 'Either way, fish has not been installed. Please install it manually, and run the script again.'
        exit(1)
else:
    print 'Not installing fish.'
installNVIM = query_yes_no('Install neovim?', default='yes')
if installNVIM:
    if OS == 'Fedora':
        call(['sudo', 'dnf', '-y', 'install', 'neovim'])
    elif OS == 'CentOS':
        call(['sudo', 'yum', '-y', 'install', 'epel-release'])
        call(['sudo', 'curl', '-Lo', '/etc/yum.repos.d/dperson-neovim-epel-7.repo', 'https://copr.fedorainfracloud.org/coprs/dperson/neovim/repo/epel-7/dperson-neovim-epel-7.repo'])
        call(['sudo', 'yum', '-y', 'install', 'neovim'])
    elif OS == 'debian':
        call(['sudo', 'apt-get', '-y', 'install', 'neovim', 'python-neovim', 'python3-neovim'])
    elif OS == 'Ubuntu':
        call(['sudo', 'add-apt-repository', '-y', 'ppa:neovim-ppa/stable'])
        call(['sudo', 'apt-get', 'update'])
        call(['sudo', 'apt-get', 'install', 'neovim'])
    else:
        print 'One of two things has happened:'
        print '1) I could not detect your OS'
        print 'or 2) I do not support installing packages on your distro/OS'
        print 'Either way, neovim has not been installed. Please install it manually, and run the script again.'
        exit(1)
else:
    print 'Not installing neovim.'
tempdir = tempfile.mkdtemp()
call(['git', 'clone', 'https://github.com/FireFaced/dotfiles.git', tempdir])
configFish = query_yes_no('Install julian.demille fish configuration?', default='yes')
if configFish:
    call(['curl', '-Lo', os.path.expanduser('~/.config/fish/functions/fisher.fish'), '--create-dirs', 'https://git.io/fisher'])
    call(['cp', '-Rv', tempdir + '/.config/fish', os.path.expanduser('~/.config')])
    call(['fish', '-c', 'fisher'])
configNvim = query_yes_no('Install julian.demille neovim configuration?', default='yes')
if configNvim:
    call(['curl', '-fLo', os.path.expanduser('~/.local/share/nvim/site/autoload/plug.vim'), '--create-dirs',
          'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'])
    call(['cp', '-av', tempdir + '/.config/nvim', os.path.expanduser('~/.config')])
    call(['nvim', '+PlugInstall'])
