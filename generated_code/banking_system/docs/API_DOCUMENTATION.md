# Banking System
**Version**: 1.0.0
**Generated**: 2025-12-28 06:41:05

---

## Architecture Overview

- **Total Domains**: 1
- **Total Classes**: 4
- **Total Relationships**: 1

## Domains

### Banking Domain
**Key Letter**: BD

Domain untuk sistem perbankan

**Classes in Banking Domain**:
- 🔄 **Account**: Rekening bank
- 🔄 **Transaction**: Transaksi keuangan
- 🔄 **Customer**: Nasabah bank

---

## Class Reference

### ParkingSlot

**Type**: class

Representasi fisik tempat parkir

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `SlotID` | uuid | - |
| `SlotNumber` | string | - |
| `Status` | state | - |

**Methods**:

- `parkvehicle()`: Transition from *Available* to *Occupied*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### Account

**Type**: class

Rekening bank

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `AccountID` | uuid | - |
| `AccountNumber` | string | - |
| `AccountType` | string | - |
| `Balance` | decimal | - |
| `Currency` | string | - |
| `CreatedDate` | datetime | - |
| `Status` | state | - |

**Methods**:

- `approve()`: Transition from *Pending* to *Active*
- `freeze()`: Transition from *Active* to *Frozen*
- `unfreeze()`: Transition from *Frozen* to *Active*
- `close()`: Transition from *Active* to *Closed*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### Transaction

**Type**: class

Transaksi keuangan

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `TransactionID` | uuid | - |
| `AccountID` | uuid | - |
| `Type` | string | - |
| `Amount` | decimal | - |
| `Description` | text | - |
| `Timestamp` | datetime | - |
| `Status` | state | - |

**Methods**:

- `process()`: Transition from *Pending* to *Processing*
- `complete()`: Transition from *Processing* to *Completed*
- `fail()`: Transition from *Processing* to *Failed*
- `reverse()`: Transition from *Completed* to *Reversed*

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

### Customer

**Type**: class

Nasabah bank

**Attributes**:

| Name | Type | Description |
|------|------|-------------|
| `CustomerID` | uuid | - |
| `FullName` | string | - |
| `Email` | email | - |
| `Phone` | string | - |
| `DateOfBirth` | date | - |
| `Address` | text | - |
| `KYCVerified` | boolean | - |

**Auto-generated Methods**:

- `__str__()`: String representation
- `to_dict()`: Serialize to dictionary
- `validate()`: Validate instance data

---

## Relationships

### Unknown: Unknown ↔ Unknown

**Type**: one_to_many

Account has many Transactions

- **Unknown** [1]  ← **Unknown** [1] 

---

## State Machines

### ParkingSlot State Machine

**Initial State**: Available

**States**:

- **Available**: No description
- **Occupied**: No description

**State Transitions**:

```
Available --[parkVehicle]--> Occupied
```

### Account State Machine

**Initial State**: Pending

**States**:

- **Pending**: No description
- **Active**: No description
- **Frozen**: No description
- **Closed**: No description

**State Transitions**:

```
Pending --[approve]--> Active
Active --[freeze]--> Frozen
Frozen --[unfreeze]--> Active
Active --[close]--> Closed
```

### Transaction State Machine

**Initial State**: Pending

**States**:

- **Pending**: No description
- **Processing**: No description
- **Completed**: No description
- **Failed**: No description
- **Reversed**: No description

**State Transitions**:

```
Pending --[process]--> Processing
Processing --[complete]--> Completed
Processing --[fail]--> Failed
Completed --[reverse]--> Reversed
```

---

## API Quick Reference

### Active Classes (with State Machines)

| Class | Initial State | Available Events |
|-------|---------------|------------------|
| **ParkingSlot** | Available | `parkVehicle` |
| **Account** | Pending | `freeze`, `approve`, `close` (+1 more) |
| **Transaction** | Pending | `process`, `complete`, `reverse` (+1 more) |

---

## Usage Examples

### Basic Usage

```python
from library import *

# Create ParkingSlot instance
obj = ParkingSlot()
print(obj.Status)

# Trigger event: parkVehicle
obj.parkvehicle()
print(obj.Status)

# Validate and serialize
if obj.validate():
    data = obj.to_dict()
    print(data)
```
