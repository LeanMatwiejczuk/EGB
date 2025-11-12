#include <linux/module.h>
#include <linux/export-internal.h>
#include <linux/compiler.h>

MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};



static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xc3a4d7fc, "serdev_device_set_parity" },
	{ 0x5403c125, "__init_waitqueue_head" },
	{ 0x9f222e1e, "alloc_chrdev_region" },
	{ 0xb06a91bd, "cdev_init" },
	{ 0x7db91808, "cdev_add" },
	{ 0x3d568d84, "class_create" },
	{ 0xa2e1228b, "device_create" },
	{ 0x28adaf0b, "__serdev_device_driver_register" },
	{ 0xfbc10eaa, "class_destroy" },
	{ 0x0bc5fb0d, "unregister_chrdev_region" },
	{ 0xa53f4e29, "memcpy" },
	{ 0x16ab4215, "__wake_up" },
	{ 0x90a48d82, "__ubsan_handle_out_of_bounds" },
	{ 0xa61fd7aa, "__check_object_size" },
	{ 0x092a35a2, "_copy_from_user" },
	{ 0xe54e0a6b, "__fortify_panic" },
	{ 0xf4ab5329, "serdev_device_write_buf" },
	{ 0xd272d446, "__stack_chk_fail" },
	{ 0x7851be11, "__SCT__might_resched" },
	{ 0x092a35a2, "_copy_to_user" },
	{ 0x7a5ffe84, "init_wait_entry" },
	{ 0xd272d446, "schedule" },
	{ 0x0db8d68d, "prepare_to_wait_event" },
	{ 0xc87f4bab, "finish_wait" },
	{ 0xf64ac983, "__copy_overflow" },
	{ 0x88b4fdc1, "device_destroy" },
	{ 0x6ce3748e, "cdev_del" },
	{ 0xb1835a42, "driver_unregister" },
	{ 0xd272d446, "__fentry__" },
	{ 0xe8213e80, "_printk" },
	{ 0xc97a84c8, "serdev_device_close" },
	{ 0xd272d446, "__x86_return_thunk" },
	{ 0xff2b0590, "serdev_device_open" },
	{ 0x396f048a, "serdev_device_set_baudrate" },
	{ 0x822a568c, "serdev_device_set_flow_control" },
	{ 0x70eca2ca, "module_layout" },
};

static const u32 ____version_ext_crcs[]
__used __section("__version_ext_crcs") = {
	0xc3a4d7fc,
	0x5403c125,
	0x9f222e1e,
	0xb06a91bd,
	0x7db91808,
	0x3d568d84,
	0xa2e1228b,
	0x28adaf0b,
	0xfbc10eaa,
	0x0bc5fb0d,
	0xa53f4e29,
	0x16ab4215,
	0x90a48d82,
	0xa61fd7aa,
	0x092a35a2,
	0xe54e0a6b,
	0xf4ab5329,
	0xd272d446,
	0x7851be11,
	0x092a35a2,
	0x7a5ffe84,
	0xd272d446,
	0x0db8d68d,
	0xc87f4bab,
	0xf64ac983,
	0x88b4fdc1,
	0x6ce3748e,
	0xb1835a42,
	0xd272d446,
	0xe8213e80,
	0xc97a84c8,
	0xd272d446,
	0xff2b0590,
	0x396f048a,
	0x822a568c,
	0x70eca2ca,
};
static const char ____version_ext_names[]
__used __section("__version_ext_names") =
	"serdev_device_set_parity\0"
	"__init_waitqueue_head\0"
	"alloc_chrdev_region\0"
	"cdev_init\0"
	"cdev_add\0"
	"class_create\0"
	"device_create\0"
	"__serdev_device_driver_register\0"
	"class_destroy\0"
	"unregister_chrdev_region\0"
	"memcpy\0"
	"__wake_up\0"
	"__ubsan_handle_out_of_bounds\0"
	"__check_object_size\0"
	"_copy_from_user\0"
	"__fortify_panic\0"
	"serdev_device_write_buf\0"
	"__stack_chk_fail\0"
	"__SCT__might_resched\0"
	"_copy_to_user\0"
	"init_wait_entry\0"
	"schedule\0"
	"prepare_to_wait_event\0"
	"finish_wait\0"
	"__copy_overflow\0"
	"device_destroy\0"
	"cdev_del\0"
	"driver_unregister\0"
	"__fentry__\0"
	"_printk\0"
	"serdev_device_close\0"
	"__x86_return_thunk\0"
	"serdev_device_open\0"
	"serdev_device_set_baudrate\0"
	"serdev_device_set_flow_control\0"
	"module_layout\0"
;

MODULE_INFO(depends, "");

MODULE_ALIAS("of:N*T*Ctd3_uart,EGB");
MODULE_ALIAS("of:N*T*Ctd3_uart,EGBC*");

MODULE_INFO(srcversion, "64E7453B36CE201B9853BC5");
