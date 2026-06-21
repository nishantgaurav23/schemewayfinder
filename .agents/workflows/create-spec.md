---
name: create-spec
description: Create spec.md and checklist.md for a SchemeWayfinder spec from roadmap.md. Use when starting a new numbered spec.
---

# /create-spec — Create spec docs for a SchemeWayfinder spec

Input: A spec ID and slug (e.g., `S1.1 scheme-corpus-loader`).

## Step 1: Resolve Identity
- Parse `spec_id` and `slug` from input.
- Read `roadmap.md` (Master Spec Index and active phase table) to extract:
  - Spec Location
  - Feature Summary
  - Implementation Location (code files)
  - Dependencies
  - Context/Notes

## Step 2: Create Specification Documents
Create the directory `specs/spec-{id}-{slug}/` and populate the following two files:

### spec.md
- **Overview**: Synthesize Feature and Notes from roadmap.
- **Dependencies**: List technical and logical dependencies.
- **Target Location**: Files/modules being created or modified.
- **Functional Requirements (FRs)**: Use the format:
  - **FR[N]**: Description
    - **Inputs**: Data structure or parameters.
    - **Outputs**: Expected return or side effect.
    - **Edge Cases**: Error handling, empty states, or constraints.
- **Tangible Outcomes**: Concrete, testable artifacts.
- **Test-Driven Requirements (TDD)**: Define the core test cases required before implementation.
  - *Note*: Mock external services (Gemini/Bhashini/Firestore/MCP server). For agent-based tasks, assert on structured state outputs.

### checklist.md
Standard workflow phases:
1. **Setup & Dependencies**: Environment prep and dependency installation.
2. **Tests First (TDD)**: Write unit/integration tests corresponding to FRs.
3. **Implementation**: Core logic development.
4. **Integration**: Wire into the orchestrator, register MCP tools, or finalize configuration.
5. **Verification**: Confirm outcomes, ensure no secrets/PII are committed, and update `roadmap.md`.

## Step 3: Roadmap Synchronization
- Update the status from `pending` to `spec-written` in BOTH the phase table and the Master Spec Index in `roadmap.md`.
- Ensure no other rows were inadvertently modified.

## Rules
- **Extract, don't invent**: Use ONLY the information provided in `roadmap.md`.
- **Traceability**: Every FR must map to at least one test in the TDD section.
- **Granularity**: Checklist items should be scoped for 15–30 minute completion blocks.
- **Pathing**: Ensure the spec folder structure aligns strictly with the roadmap's architectural definition.
- **Reporting**: Conclude by listing the created files and confirming the `roadmap.md` update.
