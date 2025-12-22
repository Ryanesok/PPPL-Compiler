# Blog Management System
**Version**: 1.0.0
**Generated**: 2025-12-22 15:19:12

---

## Architecture Overview

- **Total Domains**: 1
- **Total Classes**: 4
- **Total Relationships**: 1

## Domains

### Content Domain
**Key Letter**: CD

Domain untuk manajemen konten blog

**Classes in Content Domain**:
- 🔄 **User**: User/Author dalam sistem blog
- 🔄 **Post**: Blog post/artikel
- 🔄 **Comment**: Komentar pada post
- 🔄 **Category**: Kategori untuk post

---

## Class Reference

### User

**Type**: class

User/Author dalam sistem blog

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `UserID` | uuid | - |
| `Username` | string | - |
| `Email` | email | - |
| `FullName` | string | - |
| `Bio` | text | - |
| `ProfileImage` | url | - |
| `JoinedDate` | datetime | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### Post

**Type**: class

Blog post/artikel

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `PostID` | uuid | - |
| `AuthorID` | uuid | - |
| `Title` | string | - |
| `Content` | text | - |
| `Excerpt` | string | - |
| `PublishedAt` | datetime | - |
| `ViewCount` | integer | - |
| `Status` | state | - |

**Methods**:

- `publish()`: Transition from *Draft* to *Published*
- `archive()`: Transition from *Published* to *Archived*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### Comment

**Type**: class

Komentar pada post

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `CommentID` | uuid | - |
| `PostID` | uuid | - |
| `UserID` | uuid | - |
| `Content` | text | - |
| `CreatedAt` | datetime | - |
| `IsApproved` | boolean | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### Category

**Type**: class

Kategori untuk post

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `CategoryID` | uuid | - |
| `Name` | string | - |
| `Description` | text | - |
| `Slug` | string | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

---

## Relationships

### Unknown: Unknown ↔ Unknown

**Type**: many_to_many

Posts belong to many Categories

- **Unknown** [1]  ← **Unknown** [1] 

---

## State Machines

### Post State Machine

**Initial State**: Draft

**States**:

- **Draft**: No description
- **Published**: No description
- **Archived**: No description

**State Transitions**:

```
Draft --[publish]--> Published
Published --[archive]--> Archived
```

---

## API Quick Reference

### Active Classes (with State Machines)

| Class | Initial State | Available Events |
|-------|---------------|------------------|
| **Post** | Draft | `publish`, `archive` |

---

## Usage Examples

### Basic Usage

```python
from library import *

# Create User instance
obj = User()
print(obj.Status)

# Validate and serialize
if obj.validate():
    data = obj.to_dict()
    print(data)
```
