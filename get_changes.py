from catalog import get_changed_bps_path

def main():
    for file in get_changed_bps_path():
        print(file)
    
if __name__ == "__main__":
    main()
