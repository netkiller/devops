# Git Merge Tools

    neo@MacBook-Pro-M2 ~/w/G/devops (master)> merge
    Netkiller git merge tools
    Usage: merge [options] <parameter>

    Options:
    -h, --help            show this help message and exit
    -w ~/workspace, --workspace=~/workspace
                            workspace ~/workspace
    -p PROJECT, --project=PROJECT
                            project directory
    -l /tmp/merge.log, --logfile=/tmp/merge.log
                            log file
    -d, --debug           debug

    Repository:
        -c https://git.netkiller.cn | git@git.netkiller.cn:exmaple.git, --clone=https://git.netkiller.cn | git@git.netkiller.cn:exmaple.git
                            clone branch
        -r 8547cb94, --reset=8547cb94
                            Reset current HEAD to the specified state
        -b master, --checkout=master
                            checkout branch

    Custom merge branch:
        -s development, --source=development
                            source
        -t testing, --to=testing
                            target

    Workflow merge development -> testing -> staging -> production(master):
        --testing           from development to testing
        --staging           from testing to staging
        --production        from staging to production(master)

    Create branch:
        -B mybranch, --branch=mybranch
                            create custom branch
        -f feature/0001, --feature=feature/0001
                            feature branch from development
        -H hotfix/0001, --hotfix=hotfix/0001
                            hotfix branch from master

    Homepage: http://www.netkiller.cn       Author: Neo <netkiller@msn.com>
    Help https://github.com/netkiller/devops/blob/master/doc/merge.md

## 合并 dev 到 test 分支

    neo@MacBook-Pro-M2 devops % merge -s dev -t test