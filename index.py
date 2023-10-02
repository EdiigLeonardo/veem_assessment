import os
import shutil
import sys
import time

def sync_folders(source_dir, replica_dir, log_file):
    try:
        # Check if source directory exists
        if not os.path.exists(source_dir):
            print(f"Source directory '{source_dir}' does not exist.")
            return

        # Create replica directory if it doesn't exist
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)

        # Synchronize the content of source and replica
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_dir, os.path.relpath(source_file, source_dir))

                # Copy or update files
                if not os.path.exists(replica_file) or os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                    shutil.copy2(source_file, replica_file)
                    print(f"Copied: {source_file} -> {replica_file}")
                elif os.path.getmtime(source_file) < os.path.getmtime(replica_file):
                    shutil.copy2(replica_file, source_file)
                    print(f"Updated: {replica_file} -> {source_file}")

        # Remove files in replica that don't exist in source
        for root, dirs, files in os.walk(replica_dir):
            for file in files:
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_dir, os.path.relpath(replica_file, replica_dir))
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    print(f"Removed: {replica_file}")

        # Log the operations to a log file
        with open(log_file, "a") as log:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"{timestamp} - Synchronization completed.\n")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python sync_folders.py <source_dir> <replica_dir> <log_file>")
        sys.exit(1)

    source_dir = sys.argv[1]
    replica_dir = sys.argv[2]
    log_file = sys.argv[3]

    while True:
        sync_folders(source_dir, replica_dir, log_file)
        time.sleep(3600)  # Synchronize every hour (3600 seconds)
