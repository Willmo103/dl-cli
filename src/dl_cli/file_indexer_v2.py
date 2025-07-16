#!/usr/bin/env python3
"""
file_indexer.py: Scan directories with ignore/include/match filters, collect file metrics,
identify top-level git repositories, and emit reports in Markdown, JSON, or YAML.
Supports JSON config for AllowedFiles (include globs) and Ignored (exclude globs), CLI overrides,
output redirection, and a --projects mode for per-repo JSON/YAML breakdowns (honoring .gitignore).
"""
import os
import fnmatch
import json
from collections import defaultdict
from datetime import datetime
from sqlite3 import connect
from models import RootModel, RootFileModel, RootFolderModel



class RootManager:
    """ Manages root directories and their files/folders in the database. """

