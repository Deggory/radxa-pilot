/* SPDX-License-Identifier: MIT
 * Original conservative application-only layout. See BOARD_FLASH_CONTRACT.md.
 */
ENTRY(Reset_Handler)
MEMORY {
  /* Preserve bootstub below 0x08004000 and config at/above 0x08020000.
   * Leave 8-byte VERS trailer + 128-byte legacy signature outside raw image.
   */
  FLASH (rx) : ORIGIN = 0x08004000, LENGTH = 0x1C000 - 136
  RAM (rw) : ORIGIN = 0x20000000, LENGTH = 0x20000 - 8
}
PHDRS {
  flash PT_LOAD FLAGS(5);
  ram PT_LOAD FLAGS(6);
}
__stack_top = ORIGIN(RAM) + LENGTH(RAM);
__stack_bottom = __stack_top - 0x1000;
SECTIONS {
  .vectors : {
    KEEP(*(.vectors))
    . = ALIGN(512);
  } > FLASH :flash
  .text : {
    /* Pure protocol entry is retained for offline checks and future EP0 wiring.
     * Nothing calls it from the parked application in this increment.
     */
    KEEP(*(.text.chimera_control_read))
    KEEP(*(.text.chimera_can_*))
    KEEP(*(.text.chimera_usb_*))
    KEEP(*(.text.chimera_boot_read_facts))
    KEEP(*(.rodata.chimera_*))
    *(.text*) *(.rodata*)
    *(.glue_7) *(.glue_7t) *(.vfp11_veneer) *(.v4_bx)
    . = ALIGN(4);
  } > FLASH :flash
  .unsupported : { *(.iplt) *(.rel.iplt) *(.igot.plt) } > FLASH :flash
  .data : {
    __data_start = .;
    KEEP(*(.data.chimera_boot_magic))
    *(.data*)
    . = ALIGN(4);
    __data_end = .;
  } > RAM AT> FLASH :ram
  __data_load = LOADADDR(.data);
  __image_end = LOADADDR(.data) + SIZEOF(.data);
  .bss (NOLOAD) : {
    __bss_start = .;
    *(.bss*) *(COMMON)
    . = ALIGN(4);
    __bss_end = .;
  } > RAM :ram
  /* Stack needs no load segment. Its reservation is enforced by the assertion
   * below; adding a distant NOLOAD section can distort ELF physical extents.
   */
  .ARM.attributes 0 : { *(.ARM.attributes) }
  /DISCARD/ : { *(.comment) *(.note*) *(.eh_frame*) }
}
ASSERT(ADDR(.vectors) == 0x08004000, "FLASH vector start changed")
ASSERT(SIZEOF(.unsupported) == 0, "FLASH dynamic linkage is unsupported")
ASSERT(SIZEOF(.vectors) == 512, "FLASH vector table exceeds 512 bytes")
ASSERT(__image_end <= 0x08020000 - 136, "FLASH image overlaps legacy envelope/config")
ASSERT(__bss_end <= __stack_bottom, "RAM globals collide with reserved stack")
ASSERT(__stack_top == 0x2001FFF8, "RAM boot flag reservation changed")
