/* SPDX-License-Identifier: MIT
 * Original minimal startup; no vendor startup or legacy linker code copied.
 */
.syntax unified
.cpu cortex-m4
.thumb

.section .vectors,"a",%progbits
.balign 512
.global chimera_vectors
chimera_vectors:
  .word __stack_top
  .word Reset_Handler
  .word Trap_Handler /* NMI */
  .word Trap_Handler /* HardFault */
  .word Trap_Handler /* MemManage */
  .word Trap_Handler /* BusFault */
  .word Trap_Handler /* UsageFault */
  .word 0, 0, 0, 0
  .word Trap_Handler /* SVCall */
  .word Trap_Handler /* Debug monitor */
  .word 0
  .word Trap_Handler /* PendSV */
  .word Trap_Handler /* SysTick */
  /* ST F413 interrupt enumeration ends at external IRQ101. */
  .rept 102
  .word Trap_Handler
  .endr

.section .text.Reset_Handler,"ax",%progbits
.global Reset_Handler
.type Reset_Handler,%function
.thumb_func
Reset_Handler:
  cpsid i
  /* Legacy bootstub branches here without loading the application's MSP.
   * Future legacy signing replaces vector word zero with the image length.
   */
  movs r0, #0
  msr control, r0
  isb
  ldr r0, =__stack_top
  msr msp, r0
  bl chimera_reset
1: b 1b
.size Reset_Handler, .-Reset_Handler

.section .text.Trap_Handler,"ax",%progbits
.global Trap_Handler
.type Trap_Handler,%function
.thumb_func
Trap_Handler:
  cpsid i
  ldr r0, =__stack_top
  msr msp, r0
  bl chimera_fault
2: b 2b
.size Trap_Handler, .-Trap_Handler
