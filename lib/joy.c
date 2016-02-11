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

#define JOY_SCALE 13.8096

_JOY joy;

void __joy_spring(_TIMER *timer) {
    led_toggle(&led3);

    float angle = joy_angle(&joy);
    md_velocity(&md1, (uint16_t)(abs(angle)*100), abs(angle)/angle < 0);
}

void init_joy(void) {
    joy_init(&joy, &timer3);
}

void joy_init(_JOY *self, _TIMER *timer) {
    enc_en_wrap_detect(&enc); 

    self->timer = timer;
    self->zero_angle = (float)enc_angle(&enc).w/13.8;
}

float joy_angle(_JOY *self) {
    return (float)enc_angle(&enc).w/13.8 - self->zero_angle;
}

void joy_en_spring(_JOY *self) {
    timer_every(self->timer, 5e-2, *__joy_spring);
}

void joy_free(_JOY *self) {
    
}