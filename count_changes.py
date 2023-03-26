from catalog import get_changed_bps_path

def main():
    changed_files = get_changed_bps_path()
    return len(changed_files)
    
if __name__ == "__main__":
    print(main())
