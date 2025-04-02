# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/01 13:51:47
@Author  :   47bwy
@Desc    :   None
'''



import os
import shutil
from tempfile import TemporaryDirectory


def copy_without_hidden(src, dest):
    """Copy files from src to dest, excluding hidden files and folders."""
    for root, dirs, files in os.walk(src):
        # Exclude hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        # Exclude hidden files
        files = [f for f in files if not f.startswith('.')]
        
        # Create corresponding directories in the destination
        dest_dir = os.path.join(dest, os.path.relpath(root, src))
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copy files
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dest_file)

# Create a temporary directory to hold the filtered files
with TemporaryDirectory() as temp_dir:
    copy_without_hidden('/Users/apri/Documents/selfSync', temp_dir)
    shutil.make_archive(
        base_name='/Users/apri/Downloads/selfSync',
        format='gztar',
        root_dir=temp_dir,
    )