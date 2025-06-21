import os, sqlite3, hashlib
from icecream import ic

# Create Paths
cd = os.curdir
exported_dir: os.path = os.path.join(cd, "exported")
db_path: os.path = os.path.join(os.getenv("LOCALAPPDATA"), "Roblox", "rbx-storage.db")

# Create exported folder if its not already created.
if not os.path.isdir(exported_dir):
    os.makedirs(exported_dir)

# Create a connection to the db_path
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# View id and content, from the files table
cur.execute(f"SELECT id, content FROM files")

# Fetch the content viewed into a variable.
rows: list[tuple[str]] = cur.fetchall() # Rows will look like: [("Hash", "Content"), ("Hash", "Content")]

# Process Rows into a more readable format
database: dict[str: str] = {} # {Hash (str): Content}

for datarow in rows:
    # Process ("Hash", "Content") to {Hash (str): Content}
    hash_unconverted = datarow[0]
    
    # IDs will currently be gibberish if converted to UTF-8 currently
    # Using this method we convert the binary of (for example) f0ab61c
    # To the string value of "f0ab61c"
    hash = hashlib.md5(hash_unconverted).hexdigest()
    
    content = datarow[1]
    database[hash] = content


i=1 # Used in print(f"{i}: Ripped!") & Gets incremented every loop
for hash, content in database.items():
    # Creates the file path for exporteddir/hash (hash being a file and not another directory)
    path = os.path.join(exported_dir, hash)
    
    # Open the path (while creating it if not existing)
    with open(path, "wb") as f:
        # Write the content to the file
        try:
            f.write(content)
        except Exception as e:
            # If there is an error, we simply continue on and do not halt ripping.
            print(f"{i}: ERROR ({e})")
            continue
        
    print(f"{i}: Ripped!")
    i+=1

# Close connection (honestly unneeded)
conn.close()

print("Done")
