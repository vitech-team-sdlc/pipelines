import sys
import tomlkit

def parse_value(value: str):
    """
    Attempt to parse the string into a more appropriate Python type
    (int, float, bool). Return string if parsing fails.
    """
    # Try integer
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return int(value)

    # Try float
    try:
        return float(value)
    except ValueError:
        pass

    # Try boolean
    if value.lower() in ("true", "false"):
        return value.lower() == "true"

    # Fallback to string
    return value

def update_toml_property(filename: str, key_path: str, new_value: str):
    """
    Update a property in a TOML file (preserving original structure/order).

    :param filename: Path to the TOML file.
    :param key_path: Dotted path to the key, e.g., "database.host".
    :param new_value: The new value to set (will attempt type-casting).
    """
    # Read and parse TOML while preserving structure
    with open(filename, "r", encoding="utf-8") as f:
        doc = tomlkit.parse(f.read())

    # Navigate to the correct section using dotted path
    keys = key_path.split(".")
    pointer = doc
    for k in keys[:-1]:
        pointer = pointer[k]

    # Update the final key
    final_key = keys[-1]
    pointer[final_key] = parse_value(new_value)

    # Write back with the same formatting
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(doc))

def main():
    # We expect three arguments: <TOML file> <property key path> <new_value>
    if len(sys.argv) != 4:
        print("Usage: python update_toml.py <toml_file> <property_key> <new_value>")
        print("Example: python update_toml.py config.toml database.port 5433")
        sys.exit(1)

    toml_file = sys.argv[1]
    property_key = sys.argv[2]
    new_value = sys.argv[3]

    update_toml_property(toml_file, property_key, new_value)

if __name__ == "__main__":
    main()
