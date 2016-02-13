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

#define MOTOR_MIN_SPEED 0
#define MOTOR_MAX_SPEED 255
#define MOTOR_T         1e-2
// 360/(13.8096*16383)
#define MOTOR_SCALE 0.001591
// 360/13.8096
#define MOTOR_WRAP_ANG 26.069
#define MOTOR_ACONV(word) (float)word.i*MOTOR_SCALE

_MOTOR motor1, motor2;

void __motor_get_state(_MOTOR *self) {
    led_toggle(&led1);

    WORD raw_angle = (WORD)(enc_angle(&enc).i - self->zero_angle.i);
    if (self->last_enc_pos.i - raw_angle.i > 8192) {
        self->wrap_count += 1;
        led_toggle(&led2);
    } else if (self->last_enc_pos.i - raw_angle.i < -8192) {
        self->wrap_count -= 1;
        led_toggle(&led2);
    }

    self->last_enc_pos = raw_angle;

    self->pos_1 = self->pos;
    self->pos = MOTOR_ACONV(raw_angle) - MOTOR_WRAP_ANG*self->wrap_count;

    self->vel_1 = self->vel;
    self->vel = (self->pos - self->pos_1)/MOTOR_T;
}

// VERY VERY BAD
volatile _MOTOR *__ml_motor = NULL;
void __motor_loop(_TIMER *timer) {
    __motor_get_state(motor_loop_motor);

    __ml_motor->vel_err = __ml_motor->vel_set - __ml_motor->vel;

    uint16_t speed = min(max(fabsf(__ml_motor->vel_err), MOTOR_MIN_SPEED), MOTOR_MAX_SPEED);
    md_velocity(&md1, speed, fabsf(__ml_motor->vel)/__ml_motor->vel);
}

void init_motor(void) {
    __ml_motor = motor1;
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

    timer_every(self->timer, MOTOR_T, *__motor_loop); 
}

void motor_free(_MOTOR *self) {

}