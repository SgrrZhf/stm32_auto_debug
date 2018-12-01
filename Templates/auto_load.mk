
#####################################
# download and debug application 
#####################################
DEVICE = $DEVICE
IF = SWD
SPEED = 4000

.PHONY: debug
debug:
	gnome-terminal --title "CGDB" -- \
	cgdb -d \
	arm-none-eabi-gdb $$(BUILD_DIR)/$$(TARGET).elf

.PHONY: jlinkgdbserver
jlinkgdbserver:
	gnome-terminal --title "JLinkGDBServer" -- \
	JLinkGDBServer -device $$(DEVICE) -if $$(IF) -speed $$(SPEED)

.PHONY: load
load:
	JLinkExe -device $$(DEVICE) -CommanderScript commandfile.jlink

