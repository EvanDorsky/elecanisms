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
#ifndef _MOTOR_H_
#define _MOTOR_H_

#include <stdint.h>
#include "timer.h"
#include "enc.h"
#include "md.h"
#include "common.h"

void init_motor(void);

typedef struct {
    _ENC *enc;
    _MD *md;

    WORD last_enc_pos;
    int8_t wrap_count;

    float pos;
    float pos_1;
    float vel;
    float vel_1;

    float vel_set;
    float vel_err;
} _MOTOR;

extern _MOTOR motor1, motor2;

void motor_init(_MOTOR *self, _ENC *enc, _MD *md, _TIMER *timer);
void motor_free();

#endif
