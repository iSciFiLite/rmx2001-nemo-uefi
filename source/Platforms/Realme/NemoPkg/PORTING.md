# NemoPkg porting record

There is no `NemoPkg` implementation yet. This file is a place to keep the port's board-specific acceptance gates; it must not be treated as a DSC/FDF or a working firmware package.

## Must be established before a device configuration is committed

1. Record RMX2001 model, board revision, firmware build, LK version, and boot path.
2. Capture the entry exception level, registers/arguments, device-tree pointer, cache/MMU state, and memory reservations from a real supported boot path.
3. Identify RAM ranges and reserved regions. Never infer a UEFI FD or stack address from the Android kernel load address.
4. Confirm whether the boot chain preserves a display framebuffer; document base, size, stride, pixel format, mode, and ownership lifetime before exposing GOP.
5. Establish how PSCI is invoked and validate secondary CPU startup with RMX2001 MPIDRs.
6. Implement and test read-only UFS Block I/O before connecting an OS root filesystem. Do not enable writes for initial bring-up.
7. Pin all EDK II/Mu dependencies and retain the exact source/dependency revisions in CI logs.
8. Test a recoverable non-install boot and verify stock recovery before considering an installation procedure.

## Shared MT6785 facts versus Nemo facts

MT6785 CPU/GIC/UFS facts are useful starting points for the SoC layer. Board-level RAM reservations, panel, NVT touch variant, power sequencing, UFS handoff, and bootloader state remain Nemo-specific. SALAA values must not be copied solely because both phones use MT6785.

## Current state

Only device metadata and documentation exist in this repository. No C/assembly driver, EDK II module, platform DSC/FDF, firmware binary, or build script is supplied. GitHub Actions checks repository claims only.
