import sys
from check_if_unprocessed_newick_is_full_binary import find_closing_paren, split_top_level, check as check_binary


SPECIES = {
    "ecoli": [
        "ATCC8739", "HS", "BW2952", "DH10B", "MG1655", "W3110",
        "SSSs046", "B18BS512", "B4Sb227", "F2a301", "F2a2457T", "F5b8401",
        "IAI1", "SE11", "E24377A", "D1Sd197", "CB9615", "EDL933", "Sakai",
        "CFT073", "536", "S88", "APEC01", "UTI89", "ED1a", "E234869",
        "IAI39", "SMS35", "UMN026",
    ],
    "fish": [
        "NC_013564", "NC_013577", "NC_009459", "NC_009066", "NC_010205",
        "NC_012055", "NC_009067", "NC_009060", "NC_009059", "NC_009064",
        "NC_009065", "NC_011179", "NC_011177", "NC_011170", "NC_011169",
        "NC_011168", "NC_009058", "NC_011171", "NC_009057", "NC_013750",
        "NC_013663", "NC_009062", "NC_018814", "NC_018815", "NC_009063",
    ],
    "plant": [
        "vinifera", "grandis", "camaldule", "cacao", "raimondii",
        "clementin", "sinensis", "papaya", "rubella", "thalian",
        "lyrata", "halophilu", "rapa", "parvulum",
    ],
}


def leaf_name(s):
    """Extract the taxon name from a leaf token (strip branch length if present)."""
    return s.split(':')[0].strip()


def get_leaves(s, leaves):
    s = s.strip()
    if not s.startswith('('):
        leaves.append(leaf_name(s))
        return
    close = find_closing_paren(s, 0)
    for child in split_top_level(s[1:close]):
        get_leaves(child, leaves)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python validate_newick.py [{'/'.join(SPECIES)}] <file.newick>")
        sys.exit(1)

    dataset, path = sys.argv[1], sys.argv[2]
    if dataset not in SPECIES:
        print(f"Unknown dataset '{dataset}'. Choose from: {', '.join(SPECIES)}")
        sys.exit(1)

    with open(path) as f:
        content = f.read().strip()
    if content.endswith(';'):
        content = content[:-1].strip()

    ok = True

    # Check binary tree
    errors = []
    check_binary(content, errors)
    if errors:
        print(f"FAIL binary tree ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        ok = False
    else:
        print("PASS binary tree")

    # Check leaves
    leaves = []
    get_leaves(content, leaves)
    expected = set(SPECIES[dataset])
    found = set(leaves)

    missing = expected - found
    extra = found - expected
    if missing or extra:
        if missing:
            print(f"FAIL leaves — missing ({len(missing)}): {', '.join(sorted(missing))}")
        if extra:
            print(f"FAIL leaves — unexpected ({len(extra)}): {', '.join(sorted(extra))}")
        ok = False
    else:
        print(f"PASS leaves ({len(leaves)} species match)")

    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
