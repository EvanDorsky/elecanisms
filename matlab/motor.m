clear all
clc

s = tf('s');

K = 1e-2;
tau = 1e-3;
M = K/(tau*s+1);

Kp = 1;
L = tf(K, (1+K));
% L = 1/s;

c2d(L, 1e-2, 'matched')
