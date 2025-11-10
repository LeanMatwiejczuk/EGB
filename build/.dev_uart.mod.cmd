savedcmd_dev_uart.mod := printf '%s\n'   dev_uart.o | awk '!x[$$0]++ { print("./"$$0) }' > dev_uart.mod
