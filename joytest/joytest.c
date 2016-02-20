#include <p24FJ128GB206.h>
#include <stdint.h>
#include "config.h"
#include "common.h"
#include "ui.h"
#include "usb.h"
#include "pin.h"
#include "spi.h"
#include "md.h"
#include "oc.h"
#include "enc.h"
#include "joy.h"

#define TOGGLE_LED1         1
#define TOGGLE_LED2         2
#define TOGGLE_LED3         8 
#define READ_SW1            3
#define READ_SW2            9
#define READ_SW3            10
#define ENC_READ_REG        5

#define JOY_SET_MODE        20
#define JOY_SET_K           21
#define JOY_SET_WALL_LEFT   22
#define JOY_SET_WALL_RIGHT  23

void VendorRequests(void) {
    WORD32 address;
    WORD result;
    WORD32 result32;
    WORD input;

    switch (USB_setup.bRequest) {
        case TOGGLE_LED1:
            led_toggle(&led1);
            BD[EP0IN].bytecount = 0;
            BD[EP0IN].status = 0xC8;
            break;
        case TOGGLE_LED2:
            led_toggle(&led2);
            BD[EP0IN].bytecount = 0;
            BD[EP0IN].status = 0xC8;
            break;
        case TOGGLE_LED3:
            led_toggle(&led3);
            BD[EP0IN].bytecount = 0;
            BD[EP0IN].status = 0xC8;
            break;
        case READ_SW1:
            BD[EP0IN].address[0] = (uint8_t)sw_read(&sw1);
            BD[EP0IN].bytecount = 1;
            BD[EP0IN].status = 0xC8;
            break;
        case READ_SW2:
            BD[EP0IN].address[0] = (uint8_t)sw_read(&sw2);
            BD[EP0IN].bytecount = 1;
            BD[EP0IN].status = 0xC8;
            break;
        case READ_SW3:
            BD[EP0IN].address[0] = (uint8_t)sw_read(&sw3);
            BD[EP0IN].bytecount = 1;
            BD[EP0IN].status = 0xC8;
            break;
        case ENC_READ_REG:
            result32 = (WORD32)joy.err;
            BD[EP0IN].address[0] = result32.b[0];
            BD[EP0IN].address[1] = result32.b[1];
            BD[EP0IN].bytecount = 2;
            BD[EP0IN].status = 0xC8;
            break;
        case JOY_SET_MODE:
            input = USB_setup.wValue;
            joy.mode = input.b[0];
            BD[EP0IN].address[0] = input.b[0];
            BD[EP0IN].address[1] = input.b[1];
            BD[EP0IN].bytecount = 2;
            BD[EP0IN].status = 0xC8;
            break;
        default:
            USB_error_flags |= 0x01;    // set Request Error Flag
    }
}

void VendorRequestsIn(void) {
    switch (USB_request.setup.bRequest) {
        default:
            USB_error_flags |= 0x01;
    }
}

void VendorRequestsOut(void) {

}

int16_t main(void) {
    init_clock();
    init_ui();
    init_pin();
    init_timer();
    init_oc();
    init_spi();
    init_enc();
    init_md();
    init_joy();

    InitUSB();
    while (USB_USWSTAT!=CONFIG_STATE) {
        ServiceUSB();
    }
    while (1) {
        ServiceUSB();
    }
}
