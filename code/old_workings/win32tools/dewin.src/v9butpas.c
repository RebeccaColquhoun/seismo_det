#include <v9dewin_ext.h>
/*
+   BUTTERWORTH BAND PASS FILTER COEFFICIENT
+
+   ARGUMENTS
+   H : FILTER COEFFICIENTS
+   M : ORDER OF FILTER
+   GN  : GAIN FACTOR
+   N : ORDER OF BUTTERWORTH FUNCTION
+   FL  : LOW  FREQUENCY CUT-OFF  (NON-DIMENSIONAL)
+   FH  : HIGH FREQUENCY CUT-OFF
+   FS  : STOP BAND FREQUENCY
+   AP  : MAX. ATTENUATION IN PASS BAND
+   AS  : MIN. ATTENUATION IN STOP BAND
+
+   M. SAITO  (7/I/76)
*/
int butpas(double * h, int * m, double * gn, int * n, double fl, double fh, double fs, double ap, double as)
{
    double  wl, wh, ws, clh, op, ww, ts, os, pa, sa, cc, c, dp, g, fj, rr, tt, re, ri, a, wpc, wmc;
    int     k, l, j, i;
    struct {
        double  r;
        double  c;
    }       oj, aa, cq, r[2];
    if (fabs(fl) < fabs(fh))
        wl = fabs(fl) * PI;
    else
        wl = fabs(fh) * PI;
    if (fabs(fl) > fabs(fh))
        wh = fabs(fl) * PI;
    else
        wh = fabs(fh) * PI;
    ws = fabs(fs) * PI;
    if (wl == 0.0 || wl == wh || wh >= HP || ws == 0.0 || ws >= HP || (ws - wl) * (ws - wh) <= 0.0) {
        fprintf(stderr,
            "? (butpas) invalid input : fl=%14.6e fh=%14.6e fs=%14.6e ?\n",
            fl, fh, fs);
        *m = 0;
        *gn = 1.0;
        return 1;
    }
    /****  DETERMINE N & C */
    clh = 1.0 / (cos(wl) * cos(wh));
    op = sin(wh - wl) * clh;
    ww = tan(wl) * tan(wh);
    ts = tan(ws);
    os = fabs(ts - ww / ts);
    if (fabs(ap) < fabs(as))
        pa = fabs(ap);
    else
        pa = fabs(as);
    if (fabs(ap) > fabs(as))
        sa = fabs(ap);
    else
        sa = fabs(as);
    if (pa == 0.0)
        pa = 0.5;
    if (sa == 0.0)
        sa = 5.0;
    if ((*n = (int) (fabs(log(pa / sa) / log(op / os)) + 0.5)) < 2)
        *n = 2;
    cc = exp(log(pa * sa) / (double) (*n)) / (op * os);
    c = sqrt(cc);
    ww = ww * cc;
    dp = HP / (double) (*n);
    k = (*n) / 2;
    *m = k * 2;
    l = 0;
    g = fj = 1.0;
    for (j = 0; j < k; j++) {
        oj.r = cos(dp * fj) * 0.5;
        oj.c = sin(dp * fj) * 0.5;
        fj = fj + 2.0;
        aa.r = oj.r * oj.r - oj.c * oj.c + ww;
        aa.c = 2.0 * oj.r * oj.c;
        rr = sqrt(aa.r * aa.r + aa.c * aa.c);
        tt = atan(aa.c / aa.r);
        cq.r = sqrt(rr) * cos(tt / 2.0);
        cq.c = sqrt(rr) * sin(tt / 2.0);
        r[0].r = oj.r + cq.r;
        r[0].c = oj.c + cq.c;
        r[1].r = oj.r - cq.r;
        r[1].c = oj.c - cq.c;
        g = g * cc;
        for (i = 0; i < 2; i++) {
            re = r[i].r * r[i].r;
            ri = r[i].c;
            a = 1.0 / ((c + ri) * (c + ri) + re);
            g = g * a;
            h[l] = 0.0;
            h[l + 1] = (-1.0);
            h[l + 2] = 2.0 * ((ri - c) * (ri + c) + re) * a;
            h[l + 3] = ((ri - c) * (ri - c) + re) * a;
            l = l + 4;
        }
    }
    /****  EXIT */
    *gn = g;
    if (*n == (*m))
        return 0;
    /****  FOR ODD N */
    *m = (*m) + 1;
    wpc = cc * cos(wh - wl) * clh;
    wmc = (-cc) * cos(wh + wl) * clh;
    a = 1.0 / (wpc + c);
    *gn = g * c * a;
    h[l] = 0.0;
    h[l + 1] = (-1.0);
    h[l + 2] = 2.0 * wmc * a;
    h[l + 3] = (wpc - c) * a;
    return 0;
}
