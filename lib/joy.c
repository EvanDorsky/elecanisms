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

#define JOY_MODE_WALL    0
#define JOY_MODE_SPRING  1
#define JOY_MODE_DAMPER  2
#define JOY_MODE_TEXTURE 3
#define JOY_MODE_FREE    4

#define JOY_MAX_SPEED 0xF000
#define JOY_MIN_SPEED 0x0200
// 360/(13.8096*16383)
#define JOY_SCALE 0.001591
// 360/13.8096
#define JOY_WRAP_ANG 26.069 // deg
#define JOY_ACONV(word) (float)word.i*JOY_SCALE
#define JOY_STALL 2.0 // Amps
#define JOY_R 5.0 // Ohms
#define JOY_V 12.0 // Volts
#define JOY_T 4e-3 // Sec

#define JOY_DUTY(f) max(0x0000, (uint16_t)min(f*65535, 65535))

_JOY joy;

float __vel_tmp = 0;
void __joy_wrap_detect(_JOY *self) {
    WORD raw_angle = (WORD)(-(enc_angle(&enc).i - self->zero_angle.i));
    if (self->last_enc_angle.i - raw_angle.i > 8192)
        self->wrap_count += 1;
    else if (self->last_enc_angle.i - raw_angle.i < -8192)
        self->wrap_count -= 1;

    self->last_enc_angle = raw_angle;

    self->angle_1 = self->angle;
    self->angle = JOY_ACONV(raw_angle) + JOY_WRAP_ANG*self->wrap_count;

    __vel_tmp = (self->angle - self->angle_1)/JOY_T;
    if (fabsf(__vel_tmp) > 1e5) { // overflow check
        self->vel = self->vel_1;
    } else {
        self->vel_1 = self->vel;
        self->vel = __vel_tmp;
    }
}

void __joy_spring(_JOY *self);
void __joy_wall(_JOY *self);
void __joy_damp(_JOY *self);

void __joy_loop(_TIMER *timer) {
    __joy_wrap_detect(&joy);

    if (joy.angle < 0) {
        led_on(&led3);
    } else {
        led_off(&led3);
    }

    switch (joy.mode) {
        case JOY_MODE_SPRING:
            __joy_spring(&joy);
            break;
        case JOY_MODE_WALL:
            __joy_wall(&joy);
            break;
        case JOY_MODE_DAMPER:
            __joy_damp(&joy);
            break;
        case JOY_MODE_TEXTURE:
            break;
        case JOY_MODE_FREE:
            md_speed(&md1, 0);
            break;
    }
}

void __joy_spring(_JOY *self) {
    self->cur_set = self->angle/45.0*JOY_STALL;

    md_velocity(&md1, JOY_DUTY(fabsf(self->cur_set*self->K)/JOY_STALL), sign(self->cur_set) < 0);
}

void __joy_wall(_JOY *self) {
    if (self->angle >= self->right) {
        md_velocity(&md1, JOY_MAX_SPEED, 0);
        led_on(&led2);
    }
    else if (self->angle <= self->left) {
        md_velocity(&md1, JOY_MAX_SPEED, 1);
        led_on(&led1);
    } else {
        led_off(&led1);
        led_off(&led2);
        md_speed(&md1, JOY_MIN_SPEED);
    }
}

float __vel = 0;
void __joy_damp(_JOY *self) {
    __vel = fabsf(self->vel);
    if (__vel > 20) {
        md_velocity(&md1, JOY_DUTY(__vel*self->B/1080.0), sign(self->vel) < 0);
    }
}

void init_joy(void) {
    joy_init(&joy, &timer4);
}

void joy_init(_JOY *self, _TIMER *timer) {
    self->mode = JOY_MODE_FREE;

    // spring
    self->K = 1.0;
    // damper
    self->B = 1.0;
    // wall
    self->left = -30;
    self->right = 30;

    self->timer = timer;
    self->zero_angle = enc_angle(&enc);
    self->current = 0;
    self->cur_set = 0;
    self->err = 0;

    self->vel = 0;
    self->vel_1 = 0;

    timer_every(self->timer, JOY_T, *__joy_loop);
}

void joy_free(_JOY *self) {
    
}