#include <p24FJ128GB206.h>
#include <stdint.h>
#include "config.h"
#include "common.h"
#include "ui.h"
#include "usb.h"
#include "pin.h"
#include "spi.h"
#include "enc.h"
#include "md.h"

#define TOGGLE_LED1         1
#define TOGGLE_LED2         2
#define READ_SW1            3
#define ENC_WRITE_REG       4
#define ENC_READ_ANGLE      5
#define TOGGLE_LED3         8 
#define READ_SW2            9
#define READ_SW3            10

#define REG_MAG_ADDR        0x3FFE

_PIN *ENC_SCK, *ENC_MISO, *ENC_MOSI, *ENC_NCS;

void VendorRequests(void) {
    WORD32 address;
    WORD result;

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
        case READ_SW1:
            BD[EP0IN].address[0] = (uint8_t)sw_read(&sw1);
            BD[EP0IN].bytecount = 1;
            BD[EP0IN].status = 0xC8;
            break;
        case ENC_READ_ANGLE:
            result = enc_angle(&enc);
            BD[EP0IN].address[0] = result.b[0];
            BD[EP0IN].address[1] = result.b[1];
            BD[EP0IN].bytecount = 2;
            BD[EP0IN].status = 0xC8;
            break;
        case TOGGLE_LED3:
            led_toggle(&led3);
            BD[EP0IN].bytecount = 0;
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
        default:
            USB_error_flags |= 0x01;
    }
}

void VendorRequestsIn(void) {
    switch (USB_request.setup.bRequest) {
        default:
            USB_error_flags |= 0x01;
    }
}

void VendorRequestsOut(void) {
//    WORD32 address;
//
//    switch (USB_request.setup.bRequest) {
//        case ENC_WRITE_REGS:
//            enc_writeRegs(USB_request.setup.wValue.b[0], BD[EP0OUT].address, USB_request.setup.wLength.b[0]);
//            break;
//        default:
//            USB_error_flags |= 0x01;                    // set Request Error Flag
//    }
}

int16_t main(void) {
    init_clock();
    init_ui();
    init_pin();
    init_spi();
    init_enc();
    init_oc();
    init_md();

    InitUSB();
    while (USB_USWSTAT!=CONFIG_STATE) {
        ServiceUSB();
    }

    md_velocity(&mdp, 0x0fff, 0);
    while (1) {
        if (!sw_read(&sw1)) {
            md_run(&mdp);
        } else {
            md_brake(&mdp);
        }
        ServiceUSB();
    }
}
