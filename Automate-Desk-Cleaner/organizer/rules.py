# rules.py

# Maps extensions to main categories
EXTENSION_MAP = {
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.jpg': 'Photos',
    '.jpeg': 'Photos',
    '.png': 'Photos',
    '.exe': 'Software',
    '.mp4': 'Media',
}

# Sub-categorization rules by keyword
KEYWORD_MAP = {
    'Documents': {
        'StudyMaterial': ['notes', 'lecture', 'assignment','unit'],
        'OtherDocs': []
    },
    'Photos': {
        'Screenshots': ['screenshot', 'ss','download'],
        'Junk': ['whatsapp', 'status'],
        'Important': []
    }
}
