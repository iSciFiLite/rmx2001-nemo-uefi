# Nemo UEFI — Realme 6 (RMX2001)

This repository is the separate bring-up record for the Realme 6, codename Nemo, using MediaTek MT6785 / Helio G90T. It was split from the historical `nemo` branch state at [commit `73875bb`](https://github.com/iSciFiLite/rmx2151-salaa-uefi/tree/73875bbf4866c7f4ce9b62532052bf87c5783213) so Nemo's board evidence, memory map, build state, and compatibility claims cannot be confused with SALAA. The legacy branch now contains only a migration notice.

**This repository does not yet contain a buildable UEFI firmware package. Nemo has not been booted with UEFI or HakiOS. Do not flash any SALAA image or reuse SALAA's configured FD, stack, or memory addresses.**

## At-a-glance status

| Area | Current record | Verified on Nemo? |
|---|---|---:|
| SoC | MT6785 / Helio G90T; same MT6785 family as SALAA's Helio G95 | No UEFI validation |
| UEFI platform package | No `NemoPkg.dsc` / FDF or complete source closure | No |
| Entry/handoff | Exact LK entry registers, exception level, arguments, and retained services not documented from a device trace | No |
| Memory map | No validated RAM ranges or reserved regions for firmware, stack, framebuffer, loader, and kernel | No |
| Display/GOP | Linux reference identifies a Novatek display path; no Nemo GOP driver or verified GOP handoff | No |
| UFS | MT6785 UFS is the intended storage; no Nemo UEFI UFS Block I/O driver or tested GPT read | No |
| PSCI/CPU start | Generic MT6785 CPU topology is recorded by HakiOS; firmware PSCI method and secondary start are unknown | No |
| Input/touch | Linux reference selects Novatek NVT SPI input; no UEFI driver | No |
| HakiOS compatibility | Required firmware services are not established | **No** |
| Build | No reproducible Nemo firmware build or image | No |
| CI | Repository/status audit only; no firmware compilation or emulation | Hosted audit only |

The machine-readable summary is [`nemo-hardware.conf`](nemo-hardware.conf). It intentionally records unknown addresses as unknown instead of copying values from SALAA or another MT6785 phone.

## What is done

- Established a dedicated public repository for RMX2001 UEFI work.
- Moved the Nemo-specific porting record out of the SALAA branch, retaining the historic branch as provenance: [`nemo` branch at commit `73875bbf4866c7f4ce9b62532052bf87c5783213`](https://github.com/iSciFiLite/rmx2151-salaa-uefi/tree/nemo).
- Recorded a device/SoC profile, known references, explicit HakiOS prerequisites, and a staged roadmap.
- Added GitHub Actions to audit the status documentation and prevent unverified firmware binaries from being mistaken for releases.

## What is not done

- No actual Nemo-specific SEC implementation, EDK II DSC/FDF, `DeviceBuild.py`, complete dependency list, or reproducible build workflow.
- No Nemo-specific memory discovery, RAM reservations, FD/stack placement, HOB construction, or verified bootloader handoff.
- No GOP/display driver or proven framebuffer address, format, stride, and lifetime.
- No UFS host/controller/PHY setup or UEFI Block I/O service.
- No PSCI test, secondary-core startup test, serial trace, UEFI shell, or recovery procedure.
- No board-revision-specific touch/input, keys, Wi-Fi, Bluetooth, audio, camera, sensor, or power drivers.
- No HakiOS loader/kernel boot and no physical device testing.

## HakiOS compatibility

HakiOS's EFI loader requires a valid AArch64 UEFI environment, consistent RAM/memory descriptors, GOP for display, PSCI for secondary CPUs, and UFS Block I/O to read the `xnusys` root. Device-specific RAM reservations must keep the firmware, stack, framebuffer, loader, and kernel from overlapping.

| Required service | Nemo status | Evidence needed to close |
|---|---|---|
| UEFI boot services | Not established | Reproducible firmware build and serial boot trace |
| Memory map / HOB handoff | Unknown | Capture real bootloader input and verify reservations on RMX2001 revisions |
| GOP | Not present or verified | Driver or proven inherited framebuffer; check address, pixel format, stride, mode, lifetime |
| PSCI | Unknown | Determine conduit/CPU IDs and confirm all secondary cores start |
| UFS Block I/O | Not present or verified | Driver plus read-only GPT/partition enumeration on Nemo |
| HakiOS loader and kernel | Not tested | Boot loader/kernel with captured UART and display logs |
| Recovery | No validated procedure | Test stock recovery/unbrick process before any install experiment |

**Answer: Nemo UEFI is not yet HakiOS-compatible or working.** The MT6785 loader/kernel profiles in [HakiOS MT6785](https://github.com/iSciFiLite/hakios-mt6785) configure a shared SoC path, but the UEFI services that path needs have not been delivered or verified for RMX2001.

The SALAA project is also not HakiOS-compatible today; see its [explicit firmware status](https://github.com/iSciFiLite/rmx2151-salaa-uefi#hakios-compatibility). Sharing MT6785 does not make one device's board package safe for another.

## Why MT6768 is a reference, not a donor package

The Helio G85 MT6768 donor is useful because it demonstrates HakiOS's MediaTek-oriented interfaces, XNU handoff, driver contracts, and read-only storage design. G90T, G95, and G85 are related MediaTek platforms, so those software patterns can shorten porting work. MT6785 is still a different SoC and board implementation: CPU cluster IDs, UFS instead of the donor's eMMC, Mali-G76 configuration/power, panel, touch controller, PMIC, and firmware handoff must be Nemo-specific. Donor register sequences are not enabled as substitutes for missing RMX2001 drivers.

## Board and source references

The following are public hardware/software references, not proof of UEFI support:

- [Realme 6 postmarketOS/Linux port](https://github.com/Hari-Pi/realme6-pmos-port) and its [Nemo device tree](https://github.com/Hari-Pi/realme6-pmos-port/blob/main/linux-realme-nemo/mt6785-realme-nemo.dts). Its status reports Linux reaching initramfs and USB SSH while display support remains incomplete.
- [Realme Nemo Android kernel repository](https://github.com/iSciFiLite/android_kernel_realme_nemo).
- [Nemo firmware/device-tree dump index](https://github.com/shub876/realme_rmx2001_dump). This is a large external dump repository; no firmware image was downloaded or copied into this project. A DTS memory range is a reference, not a verified UEFI load map.
- [SALAA UEFI project](https://github.com/iSciFiLite/rmx2151-salaa-uefi) for shared MT6785 research only; its fixed addresses and incomplete service set are not Nemo configuration.
- [HakiOS MT6785](https://github.com/iSciFiLite/hakios-mt6785) for the current loader/kernel side.

## Roadmap

| Stage | Deliverable / acceptance evidence | State |
|---|---|---|
| 1. Device facts | Identify RMX2001 board/revision; capture bootloader handoff, LK/FDT, UFS, panel, and input variants with source provenance | Started; exact handoff unknown |
| 2. Firmware source | Nemo-specific EDK II package and complete pinned dependency/source closure | Open |
| 3. Hosted build | Clean-runner UEFI build, archive build logs, inspect image sections and metadata | Open |
| 4. Safe early boot | Verify entry state, memory reservations, stack/FV placement, serial output, and recovery | Open; requires device |
| 5. Basic UEFI | Verify boot services, shell, device paths, runtime services, PSCI | Open; requires device |
| 6. Display | Establish or implement GOP and confirm framebuffer properties/lifetime | Open; requires device |
| 7. Storage | Add/validate UFS Block I/O; enumerate GPT read-only and confirm root partition | Open; requires device |
| 8. HakiOS | Boot HakiOS loader/kernel with logs and working display/storage | Open; requires device |
| 9. Release | Tested recovery instructions, source-to-binary provenance, signed-off device/revision matrix | Open |

No CI job can prove physical memory handoff, panel output, UFS signaling, or recovery on its own. Each hardware gate stays open until evidence for RMX2001 is published.

## GitHub Actions

The [Nemo status audit](https://github.com/iSciFiLite/rmx2001-nemo-uefi/actions/workflows/status-audit.yml) runs on pushes, pull requests, and manual dispatch. A [hosted run](https://github.com/iSciFiLite/rmx2001-nemo-uefi/actions/runs/41254374767) passed for commit `0ce8972`; it checks required status claims and ensures no generated firmware artifacts are tracked. It is not an EDK II build, emulator test, or hardware test. Firmware compilation will be added only when a complete Nemo platform package and reproducible upstream dependency set exist; calling the current documentation audit a firmware test would be misleading.

## License and safety

This repository contains documentation, metadata, and the audit workflow only; it contains no firmware implementation or proprietary device data. New documentation and metadata are offered under CC BY 4.0 (see [`LICENSE`](LICENSE)); the audit script is MIT-licensed (see [`LICENSE-CODE`](LICENSE-CODE)). External reference repositories retain their own licenses and attribution. Do not redistribute firmware dumps, signing keys, or proprietary blobs here.

Do not flash this repository. Preserve stock boot, vendor_boot, vbmeta, and recovery images. Establish and test the device's recovery route before any future firmware experiment.
