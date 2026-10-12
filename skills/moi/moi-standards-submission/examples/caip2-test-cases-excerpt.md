# Test cases: the form

From the draft `caip2.md` (reference format option A, names). Each case carries the reason it is valid or invalid. A reviewer reads this section first. `spec-lint.py` checks every case against the Syntax regex.

## Test Cases

### Valid

```
# devnet
moi:devnet

# The reserved mainnet reference
moi:mainnet

# A private deployment
moi:acme-internal

# Minimum-length reference
moi:x
```

### Invalid

```
moi:                 # empty reference
moi:DevNet           # uppercase characters
moi:dev net          # whitespace
moi:-devnet          # leading hyphen
moi:devnet-          # trailing hyphen
moi:dev_net          # underscore is not permitted
MOI:devnet           # uppercase namespace
moi:this-reference-is-far-too-long-to-be-valid   # exceeds 32 characters
```
