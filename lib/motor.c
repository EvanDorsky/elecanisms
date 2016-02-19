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
#include "motor.h"

#define MOTOR_MIN_SPEED 0x0000
#define MOTOR_MAX_SPEED 0xF000
#define MOTOR_T         4e-3
#define MOTOR_SCALE 0.02197399744 // 360/16383
#define MOTOR_WRAP_ANG 360
#define MOTOR_ACONV(word) (float)word.i*MOTOR_SCALE

_MOTOR motor1, motor2;

float __vel_tmp = 0;
void __motor_get_state(_MOTOR *self) {
    WORD raw_angle = (WORD)-(enc_angle(&enc).i - self->zero_angle.i);
    if (self->last_enc_pos.i - raw_angle.i > 8192) {
        self->wrap_count += 1;
        led_toggle(&led2);
    } else if (self->last_enc_pos.i - raw_angle.i < -8192) {
        self->wrap_count -= 1;
        led_toggle(&led2);
    }

    self->last_enc_pos = raw_angle;

    self->pos_1 = self->pos;
    self->pos = MOTOR_ACONV(raw_angle) + MOTOR_WRAP_ANG*self->wrap_count;

    if (self->pos > 0)
        led_off(&led3);
    else
        led_on(&led3);

    __vel_tmp = (self->pos - self->pos_1)/MOTOR_T;
    if (fabsf(__vel_tmp) > 1e5) { // overflow check
        self->vel = self->vel_1;
    } else {
        self->vel_1 = self->vel;
        self->vel = __vel_tmp;
    }
}

// VERY VERY BAD
volatile _MOTOR *__ml_motor = NULL;
void __motor_loop(_TIMER *timer) {
    __motor_get_state(__ml_motor);
    led_toggle(&led1);

    __ml_motor->vel_err = __ml_motor->vel_set - __ml_motor->vel;

    __ml_motor->vel_set = __ml_motor->vel_set_1 + MOTOR_T*__ml_motor->vel_err;

    md_velocity(__ml_motor->md,
        clamp(fabsf(__ml_motor->vel_set), MOTOR_MIN_SPEED, MOTOR_MAX_SPEED),
        sign(__ml_motor->vel_set) < 0);

    __ml_motor->vel_set_1 = __ml_motor->vel_set;
}

void init_motor(void) {
    __ml_motor = &motor1;
    motor_init(&motor1, &enc, &md1, &timer3);
}

void motor_init(_MOTOR *self, _ENC *enc, _MD *md, _TIMER *timer) {
    self->enc = enc;
    self->md = md;
    self->pos = 0;
    self->pos_1 = 0;
    self->vel = 0;
    self->vel_1 = 0;

    self->vel_err = 0;
    self->vel_set = 100;
    self->vel_set_1 = 100;
    self->zero_angle = enc_angle(self->enc);

    self->timer = timer;
    timer_every(self->timer, MOTOR_T, *__motor_loop); 
}

void motor_free(_MOTOR *self) {

}