#include <linux/module.h>
#include <linux/init.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/string.h>

// Etiqueta para el autor del modulo
#define AUTHOR	"EGB_GRUPO_2"

#define MSG_1 "get_sp"
#define MSG_2 "set_sp"
#define MSG_3 "get_err"
#define MSG_4 "set_err"
#define MSG_5 "set_mode"
#define MSG_6 "log"
#define MSG_7 "stop"
#define MSG_8 "start"

typedef char * system_msg_codes[8];
static system_msg_codes codes;

// Minor number del device
#define CHRDEV_MINOR	50
// Cantidad de devices para reservar
#define CHRDEV_COUNT	1

// Variable que guarda los major y minor numbers del char device
static dev_t chrdev_number;
// Variable que representa el char device
static struct cdev chrdev;
// Clase del char device
static struct class *chrdev_class;


// Buffer de datos para compartir entre usuario y kernel
static char shared_buffer[128];

/**
 * @brief Callback llamado cuando se lee del char device
*/
static ssize_t chr_dev_read(struct file *f, char __user *buff, size_t size, loff_t *off) {
    // Variables auxiliares
    int to_copy, not_copied, copied;
    // Si el offset es mayor que el tamaño del buffer, no hay mas datos para leer
    if (*off >= sizeof(shared_buffer)) { return 0; }
    // Reviso cuanto se puede leer
    to_copy = min(size, sizeof(shared_buffer) - *off);
    // Copio lo que hay en el dispositivo de caracteres y lo copio al usuario
    not_copied = copy_to_user(buff, shared_buffer + *off, to_copy);
    // Actualizo el offset
    *off += to_copy;
    // Calculo cuántos bytes se copiaron y devuelvo
    copied = to_copy - not_copied;
    printk(KERN_INFO "%s: Se leyo '%s' en el char device\n", AUTHOR, buff);
    return copied;
}

/**
 * @brief Callback llamado cuando se escribe el char device
*/
static ssize_t chr_dev_write(struct file *f, const char __user *buff, size_t size, loff_t *off) {
	// Variables auxiliares
	int to_copy, not_copied, copied;
	// Reviso si lo que se escribio excede al buffer
	to_copy = min(size, sizeof(shared_buffer));
	// Copio lo escrito al buffer y guardo la cantidad de bytes que no se copiaron
	not_copied = copy_from_user(shared_buffer, buff, to_copy);
	// Calculo cuantos bytes se copiaron
	copied = to_copy - not_copied;
	// Limpio los espacios despues del enter
	for(int i = 0; i < copied; i++) {
		if(shared_buffer[i] == '\n') {
			shared_buffer[i] = 0;
			break;
		}
	}
    for(int j = 0; j < 8; j++){
        if(strncmp(shared_buffer,codes[j],strlen(codes[j]))==0){
            printk(KERN_INFO "%s: RECIBIDO MENSAJE n°%d\n", AUTHOR, (j+1));
			printk(KERN_INFO "%s: %s\n", AUTHOR, shared_buffer);

			// ACA ENVIO POR UART	
        }
    } 
	// Muestro lo que se escribio en el kernel
	printk(KERN_INFO "%s: Se escribio '%s' en el char device\n", AUTHOR, shared_buffer);
	// Devuelvo la cantidad de bytes copiados	
	return copied;
}

/*#define MSG_1 "get_sp"
#define MSG_2 "set_sp"
#define MSG_3 "get_err"
#define MSG_4 "set_err"
#define MSG_5 "set_mode"
#define MSG_6 "log"
#define MSG_7 "stop"
#define MSG_8 "start"
 */

// Operaciones de archivos
static struct file_operations chrdev_ops = {
	.owner = THIS_MODULE,
    .read = chr_dev_read,
	.write = chr_dev_write
};

/**
 * @brief Se llama cuando el modulo se carga en el kernel
 * @return devuelve cero cuando la funcion termina con exito
*/


static int __init chrdev_init(void) {
	// Intento ver de reservar el char device
    codes[0] = MSG_1;
    codes[1] = MSG_2;
    codes[2] = MSG_3;
    codes[3] = MSG_4;
    codes[4] = MSG_5;
    codes[5] = MSG_6;
    codes[6] = MSG_7;
    codes[7] = MSG_8;
	if(alloc_chrdev_region(&chrdev_number, CHRDEV_MINOR, CHRDEV_COUNT, AUTHOR) < 0) {
		printk(KERN_ERR "%s: No se pudo crear el char device\n", AUTHOR);
		return -1;
	}
	// Mensaje informativo para ver el major y minor number
	printk(KERN_INFO
		"%s: Reservada una region para un char device con major %d y minor %d\n",
		AUTHOR,
		MAJOR(chrdev_number),
		MINOR(chrdev_number)
	);

	// Inicializo el char device con sus operaciones
	cdev_init(&chrdev, &chrdev_ops);
	// Asocio el char device con la region reservada
	if(cdev_add(&chrdev, chrdev_number, CHRDEV_COUNT) < 0) {
		unregister_chrdev_region(chrdev_number, CHRDEV_COUNT);
		printk(KERN_ERR "%s: No se pudo crear el char device\n", AUTHOR);
		return -1;
	}

	// Creo estructura de clase
	chrdev_class = class_create(AUTHOR);
	// Verifico si fue posible
	if(IS_ERR(chrdev_class)) {
		unregister_chrdev_region(chrdev_number, CHRDEV_COUNT);
		printk(KERN_ERR "%s: No se pudo crear la clase del char device\n", AUTHOR);
		return -1;
	}

	// Creo el archivo del char device
	if(IS_ERR(device_create(chrdev_class, NULL, chrdev_number, NULL, AUTHOR))) {
		class_destroy(chrdev_class);
		unregister_chrdev_region(chrdev_number, CHRDEV_COUNT);
		printk(KERN_ERR "%s: No se pudo crear el char device\n", AUTHOR);
		return -1;
	}

	printk(KERN_INFO "%s: Fue creado el char device\n", AUTHOR);
	return 0;
}

/**
 * @brief Se llama cuando el modulo se quita del kernel
 */
static void __exit chrdev_exit(void) {
	// Libero la zona del char device
	device_destroy(chrdev_class, chrdev_number);
	class_destroy(chrdev_class);
	unregister_chrdev_region(chrdev_number, CHRDEV_COUNT);
	cdev_del(&chrdev);
    printk(KERN_INFO "%s: Eliminado char device\n", AUTHOR);
}

// Registro la funcion de inicializacion y salida
module_init(chrdev_init);
module_exit(chrdev_exit);

// Informacion del modulo
MODULE_LICENSE("GPL");
MODULE_AUTHOR(AUTHOR);
MODULE_DESCRIPTION(".");
