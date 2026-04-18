import sys


def find_closing_paren(s, start):
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '(':
            depth += 1
        elif s[i] == ')':
            depth -= 1
            if depth == 0:
                return i
    return -1


def split_top_level(s):
    children = []
    depth = 0
    start = 0
    for i, c in enumerate(s):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif c == ',' and depth == 0:
            children.append(s[start:i].strip())
            start = i + 1
    children.append(s[start:].strip())
    return children


def check(s, errors):
    s = s.strip()
    if not s.startswith('('):
        return  # leaf node
    close = find_closing_paren(s, 0)
    children = split_top_level(s[1:close])
    if len(children) != 2:
        child_reprs = []
        for c in children:
            c = c.strip()
            label = c if not c.startswith('(') else f"({c[1:].split(',')[0].strip()},...)"
            child_reprs.append(label)
        errors.append(
            f"Internal node has {len(children)} children: [{', '.join(child_reprs)}]"
        )
    for child in children:
        check(child, errors)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_binary_newick.py <file.newick>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        content = f.read().strip()

    if content.endswith(';'):
        content = content[:-1].strip()

    errors = []
    check(content, errors)

    if errors:
        print(f"NOT a rooted binary tree ({len(errors)} issue(s) found):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("Valid rooted binary tree: every internal node has exactly 2 children.")


if __name__ == '__main__':
    main()
