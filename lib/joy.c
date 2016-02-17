/*
** Copyright (c) 2016, Evan Dorsky
** All rights reserved.
**
** Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are met:
**
**     1. Redistributions of source code must retain the above copyright
**        notice, this list of conditions and the following disclaimer.
**     2. Redistributions in binary form must reproduce the above copyright
**        notice, this list of conditions and the following disclaimer in the
**        documentation and/or other materials provided with the distribution.
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
** AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
** IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
** ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
** LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
** CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
** SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
** INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
** CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
** ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
** POSSIBILITY OF SUCH DAMAGE.
*/
#include <p24FJ128GB206.h>
#include "joy.h"

#define JOY_MAX_SPEED 0xFFFF
#define JOY_MIN_SPEED 0x2000
// 360/(13.8096*16383)
#define JOY_SCALE 0.001591
// 360/13.8096
#define JOY_WRAP_ANG 26.069 // deg
#define JOY_ACONV(word) (float)word.i*JOY_SCALE
#define JOY_STALL 2.0 // Amps
#define JOY_R 5.0 // Ohms
#define JOY_V 12.0 // Volts

#define JOY_DUTY(f) min((uint16_t)(f*65535), 0xFFFF)

_JOY joy;

void __joy_wrap_detect(_JOY *self) {
    led_toggle(&led1);

    WORD raw_angle = (WORD)(-(enc_angle(&enc).i - self->zero_angle.i));
    if (self->last_enc_angle.i - raw_angle.i > 8192) {
        self->wrap_count += 1;
        led_toggle(&led2);
    } else if (self->last_enc_angle.i - raw_angle.i < -8192) {
        self->wrap_count -= 1;
        led_toggle(&led2);
    }

    self->last_enc_angle = raw_angle;
    self->angle = JOY_ACONV(raw_angle) + JOY_WRAP_ANG*self->wrap_count;
}

void __joy_loop(_TIMER *timer) {
    __joy_wrap_detect(&joy);

    if (joy.angle < 0) {
        led_on(&led3);
    } else {
        led_off(&led3);
    }

    joy.cur_set = joy.angle/45.0*JOY_STALL;
    joy.current = (pin_read(&A[0])/65535.0*3.3 - 1.65)/.75;

    joy.cur_err = joy.cur_set - joy.current;

    md_velocity(&md1, JOY_DUTY(fabsf(joy.cur_err*JOY_R/JOY_V)), fabsf(joy.cur_err)/joy.cur_err < 0);
}


void init_joy(void) {
    joy_init(&joy, &timer4);
}

void joy_init(_JOY *self, _TIMER *timer) {
    self->timer = timer;
    self->zero_angle = enc_angle(&enc);
    self->current = 0;
    self->cur_set = 0;
    self->cur_err = 0;

    timer_every(self->timer, 4e-3, *__joy_loop);
}

void joy_free(_JOY *self) {
    
}