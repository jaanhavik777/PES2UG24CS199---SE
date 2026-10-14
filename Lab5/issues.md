| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection | Security (Bandit B605, High) | 43 | `os.system("cat " + file)` builds a shell command from a variable | Removed `os.system`; read the file with Python `open()` |
| Mutable default argument | Bug (Pylint W0102) | 11 | `equipment_list=[]` is shared across calls | Default `None`, create the list inside the function |
| Bare `except: pass` | Bug (E722, W0702, B110) | 27-28 | Silently hides all errors, including a wrong reservation ID | Explicit `if id not in reservations` check with a message |
| Files not closed / no encoding | Resource leak (R1732, W1514) | 35-37, 40-43 | `open()` without `with` or encoding; log file never closed | Used `with open(..., encoding="utf-8")` |
| No input validation | Logic bug (not tool-flagged) | 30-32, 49 | `"14-12"` gave -2 hours; `1530` (int) would crash `slot_hours` | Added `parse_slot` to check format and start < end |
| Double booking still accepted | Logic bug (not tool-flagged) | 13-18 | Conflict was logged but the booking went through anyway | Reject overlapping bookings with `ValueError` |
| Equipment stock unchecked | Logic bug (not tool-flagged) | 16-17 | Pool could go negative; unknown item gave `KeyError` | Check stock and name before decrementing |
| Global statement / naming | Style (W0603, C0103) | 9, 12, 39 | `global next_reservation`; `logConflicts` not snake_case | `itertools.count` for IDs; renamed to `log_conflicts` |
| Unused variables | Quality (F841, W0612) | 46, 47, 49 | `a`, `a_more`, `c` never used | Removed the assignments |
| Docstrings, f-strings, formatting | Style (C0114, C0116, C0209, C0206, E501, E302, E305, W292) | many | Missing docstrings, `%` formatting, long lines, blank lines | Added docstrings, f-strings, wrapped lines, PEP 8 spacing |
| `main()` runs on import | Quality | 59 | Module can't be imported without running | Added `if __name__ == "__main__":` |