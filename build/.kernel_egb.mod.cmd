savedcmd_kernel_egb.mod := printf '%s\n'   kernel_egb.o | awk '!x[$$0]++ { print("./"$$0) }' > kernel_egb.mod
