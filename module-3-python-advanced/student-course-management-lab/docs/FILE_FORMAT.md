# File Format Specification

## Overview

The Student Course Management System uses JSON format for data persistence. This document specifies the file formats for storing students, courses, and enrollments.

## File Structure

### Directory Layout

```
data/
├── students.json       # Student records
├── courses.json        # Course records
└── enrollments.json    # Enrollment records
```

---

## Student Data Format

### File: `students.json`

#### Structure
```json
{
  "students": [
    {
      "student_id": "string",
      "name": "string",
      "email": "string",
      "program": "string"
    }
  ],
  "metadata": {
    "version": "1.0",
    "last_updated": "ISO 8601 datetime",
    "count": "integer"
  }
}
```

#### Example
```json
{
  "students": [
    {
      "student_id": "S001",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "program": "Computer Science"
    },
    {
      "student_id": "S002",
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "program": "Software Engineering"
    }
  ],
  "metadata": {
    "version": "1.0",
    "last_updated": "2024-01-15T10:30:00Z",
    "count": 2
  }
}
```

#### Field Specifications

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `student_id` | string | Yes | Unique, non-empty | Student identifier |
| `name` | string | Yes | Non-empty, max 100 chars | Full name |
| `email` | string | Yes | Valid email format | Email address |
| `program` | string | Yes | Non-empty, max 50 chars | Academic program |

---

## Course Data Format

### File: `courses.json`

#### Structure
```json
{
  "courses": [
    {
      "course_code": "string",
      "name": "string",
      "credits": "integer",
      "instructor": "string"
    }
  ],
  "metadata": {
    "version": "1.0",
    "last_updated": "ISO 8601 datetime",
    "count": "integer"
  }
}
```

#### Example
```json
{
  "courses": [
    {
      "course_code": "CSC1234",
      "name": "Introduction to Programming",
      "credits": 3,
      "instructor": "Dr. Smith"
    },
    {
      "course_code": "MAT5678",
      "name": "Calculus I",
      "credits": 4,
      "instructor": "Prof. Johnson"
    }
  ],
  "metadata": {
    "version": "1.0",
    "last_updated": "2024-01-15T10:30:00Z",
    "count": 2
  }
}
```

#### Field Specifications

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `course_code` | string | Yes | Format: XXX1234, unique | Course identifier |
| `name` | string | Yes | Non-empty, max 100 chars | Course name |
| `credits` | integer | Yes | 1-6 range | Credit hours |
| `instructor` | string | Yes | Non-empty, max 100 chars | Instructor name |

---

## Enrollment Data Format

### File: `enrollments.json`

#### Structure
```json
{
  "enrollments": [
    {
      "student_id": "string",
      "course_code": "string",
      "grade": "float or null",
      "enrollment_date": "ISO 8601 datetime"
    }
  ],
  "metadata": {
    "version": "1.0",
    "last_updated": "ISO 8601 datetime",
    "count": "integer"
  }
}
```

#### Example
```json
{
  "enrollments": [
    {
      "student_id": "S001",
      "course_code": "CSC1234",
      "grade": 85.5,
      "enrollment_date": "2024-01-10T09:00:00Z"
    },
    {
      "student_id": "S001",
      "course_code": "MAT5678",
      "grade": null,
      "enrollment_date": "2024-01-10T09:05:00Z"
    },
    {
      "student_id": "S002",
      "course_code": "CSC1234",
      "grade": 92.0,
      "enrollment_date": "2024-01-11T10:00:00Z"
    }
  ],
  "metadata": {
    "version": "1.0",
    "last_updated": "2024-01-15T10:30:00Z",
    "count": 3
  }
}
```

#### Field Specifications

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `student_id` | string | Yes | Must exist in students | Reference to student |
| `course_code` | string | Yes | Must exist in courses | Reference to course |
| `grade` | float or null | No | 0-100 if set | Numeric grade |
| `enrollment_date` | string | Yes | ISO 8601 format | Date enrolled |

---

## Data Integrity Rules

### Referential Integrity

1. **Student Reference**
   - `enrollment.student_id` must exist in `students.json`
   - Orphaned enrollments should be flagged on load

2. **Course Reference**
   - `enrollment.course_code` must exist in `courses.json`
   - Orphaned enrollments should be flagged on load

3. **Unique Constraints**
   - Each `student_id` must be unique across all students
   - Each `course_code` must be unique across all courses
   - Each (student_id, course_code) pair must be unique in enrollments

### Data Validation

#### On Load
```python
def validate_on_load(data):
    """Validate data when loading from files."""
    
    # Check required fields
    # Validate data types
    # Check constraints
    # Verify referential integrity
    # Flag or repair inconsistencies
```

#### On Save
```python
def validate_on_save(data):
    """Validate data before saving to files."""
    
    # Ensure all required fields present
    # Validate data types and formats
    # Check business rules
    # Update metadata
```

---

## File Operations

### Reading Files

```python
import json
from pathlib import Path
from typing import Dict, Any

def read_json_file(file_path: Path) -> Dict[str, Any]:
    """Read and parse JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"students": [], "metadata": {"version": "1.0", "count": 0}}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}")
```

### Writing Files

```python
def write_json_file(file_path: Path, data: Dict[str, Any]) -> None:
    """Write data to JSON file with proper formatting."""
    from datetime import datetime
    
    # Update metadata
    if "metadata" not in data:
        data["metadata"] = {}
    data["metadata"]["last_updated"] = datetime.now().isoformat()
    data["metadata"]["version"] = "1.0"
    
    # Write with indentation for readability
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

---

## Backup and Recovery

### Backup Strategy

```python
def create_backup(file_path: Path) -> Path:
    """Create a backup of the data file."""
    from datetime import datetime
    import shutil
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".{timestamp}.bak")
    shutil.copy2(file_path, backup_path)
    return backup_path
```

### Recovery Procedure

1. **Detect corruption**: Catch `JSONDecodeError` on load
2. **Find latest backup**: Search for `.bak` files
3. **Restore backup**: Copy backup to main file
4. **Validate restored data**: Ensure integrity
5. **Log incident**: Record recovery action

---

## Migration and Versioning

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-01 | Initial format |

### Migration Path

When format changes:

```python
def migrate_data(data: Dict, from_version: str, to_version: str) -> Dict:
    """Migrate data between versions."""
    
    if from_version == "1.0" and to_version == "1.1":
        # Apply migration logic
        pass
    
    return data
```

---

## CSV Alternative Format

For users who prefer CSV:

### students.csv
```csv
student_id,name,email,program
S001,John Doe,john.doe@example.com,Computer Science
S002,Jane Smith,jane.smith@example.com,Software Engineering
```

### courses.csv
```csv
course_code,name,credits,instructor
CSC1234,Introduction to Programming,3,Dr. Smith
MAT5678,Calculus I,4,Prof. Johnson
```

### enrollments.csv
```csv
student_id,course_code,grade,enrollment_date
S001,CSC1234,85.5,2024-01-10T09:00:00Z
S001,MAT5678,,2024-01-10T09:05:00Z
S002,CSC1234,92.0,2024-01-11T10:00:00Z
```

**Note**: CSV format doesn't include metadata. Use JSON for production.

---

## Error Handling

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| File not found | First run or deleted file | Create empty file with structure |
| Invalid JSON | Manual edit error | Restore from backup |
| Missing fields | Version mismatch | Apply migration |
| Type mismatch | Data corruption | Validate and fix or skip |
| Orphaned records | Deleted reference | Remove or flag |

### Error Messages

```python
class FileFormatError(Exception):
    """Base exception for file format errors."""
    pass

class JSONParseError(FileFormatError):
    """JSON parsing failed."""
    pass

class ValidationError(FileFormatError):
    """Data validation failed."""
    pass

class ReferentialIntegrityError(FileFormatError):
    """Referential integrity violation."""
    pass
```

---

## Best Practices

### File Management
1. Always create backups before writing
2. Use atomic writes (write to temp, then rename)
3. Validate data before and after serialization
4. Handle encoding properly (UTF-8)
5. Set appropriate file permissions

### Data Integrity
1. Validate referential integrity on load
2. Maintain unique constraints
3. Use transactions for multi-file updates
4. Log all data modifications
5. Provide rollback capability

### Performance
1. Load data once at startup
2. Keep data in memory during operation
3. Batch writes to reduce I/O
4. Use incremental saves for large datasets
5. Consider streaming for very large files
