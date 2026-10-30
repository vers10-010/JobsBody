"""Resolve paths from preserved project records after a local folder move."""
from pathlib import Path, PureWindowsPath

PROJECT_ROOT = Path(__file__).resolve().parent
LEGACY_ROOT = PureWindowsPath(r'C:\Users\vers1\OneDrive\Documents\JobsBody')


def project_path(value):
    """Rebase only this project's old paths; leave external paths unchanged."""
    recorded = PureWindowsPath(value)
    try:
        relative = recorded.relative_to(LEGACY_ROOT)
    except ValueError:
        return Path(value)
    if '..' in relative.parts:
        raise ValueError(f'Project path contains parent traversal: {value}')
    target = PROJECT_ROOT.joinpath(*relative.parts)
    if not target.resolve().is_relative_to(PROJECT_ROOT):
        raise ValueError(f'Project path leaves the current root: {value}')
    return target
