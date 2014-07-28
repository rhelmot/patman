def main(args, repo):
    if repo is not None:
        repo.done()

    if len(args) == 0:
        args = ['']
    elif args[0] not in helps:
        args[0] = ''

    print helps[args[0]]

helps = {
    '':
"""patman -- the patch manager

Usage: patman [<project name>] <command> [<arg1> [<arg2> ...]]

Commands:
    init [<project name>]   -- Create a new project based in the current directory
    snap <snapshot name>    -- Create a new snapshot for the project
    use <snapshot name>     -- Restore the state from an old snapshot
    list                    -- List existing snapshots
    status                  -- List changes made since last snapshot operation
    ignore <file>           -- Ignore a file for the next snapshot
    help <topic>            -- Get help for a command
"""
}
