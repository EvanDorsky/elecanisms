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
#include "enc.h"

#define ENC_REG_MAG_ADDR 0x3FFE
#define ENC_REG_ANG_ADDR 0x3FFF
#define ENC_MASK     0x3FFF

_ENC enc;

WORD __enc_readReg(_ENC *self, WORD address) {
    WORD cmd, result;
    cmd.w = 0x4000|address.w; //set 2nd MSB to 1 for a read
    cmd.w |= parity(cmd.w)<<15; //calculate even parity

    pin_clear(self->NCS);
    spi_transfer(self->spi, cmd.b[1]);
    spi_transfer(self->spi, cmd.b[0]);
    pin_set(self->NCS);

    pin_clear(self->NCS);
    result.b[1] = spi_transfer(self->spi, 0);
    result.b[0] = spi_transfer(self->spi, 0);
    pin_set(self->NCS);
    return (WORD)(result.w & ENC_MASK);
}

void init_enc(void) {
    enc_init(&enc, &spi1, &D[1], &D[0], &D[2], &D[3], 0, &timer4);
}

void enc_init(_ENC *self, _SPI *spi, _PIN *MISO, _PIN *MOSI, _PIN *SCK, _PIN *NCS, uint8_t wrap_detect, _TIMER *timer) {
    self->spi = spi;
    self->MISO = MISO;
    self->MOSI = MOSI;
    self->SCK = SCK;
    self->NCS = NCS;

    self->wrap_detect = wrap_detect;
    self->timer = timer;

    pin_digitalOut(self->NCS);
    pin_set(self->NCS);

    spi_open(self->spi, self->MISO, self->MOSI, self->SCK, 2e6, 1);
}

void enc_free(_ENC *self) {

}

WORD enc_magnitude(_ENC *self) {
    return __enc_readReg(self, (WORD)ENC_REG_MAG_ADDR);
}

WORD enc_angle(_ENC *self) {
    return __enc_readReg(self, (WORD)ENC_REG_ANG_ADDR);
}