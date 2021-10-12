#include <v9dewin_ext.h>
/*
+   BUTTERWORTH LOW PASS FILTER COEFFICIENT
+
+   ARGUMENTS
+   H : FILTER COEFFICIENTS
+   M : ORDER OF FILTER  (M=(N+1)/2)
+   GN  : GAIN FACTOR
+   N : ORDER OF BUTTERWORTH FUNCTION
+   FP  : PASS BAND FREQUENCY  (NON-DIMENSIONAL)
+   FS  : STOP BAND FREQUENCY
+   AP  : MAX. ATTENUATION IN PASS BAND
+   AS  : MIN. ATTENUATION IN STOP BAND
+
+   M. SAITO  (17/XII/75)
*/
int butlop(double * h, int * m, double * gn, int * n, double fp, double fs, double ap, double as)
{
    double  wp, ws, tp, ts, pa, sa, cc, c, dp, g, fj, c2, sj, tj, a;
    int     k, j;
    if (fabs(fp) < fabs(fs))
        wp = fabs(fp) * PI;
    else
        wp = fabs(fs) * PI;
    if (fabs(fp) > fabs(fs))
        ws = fabs(fp) * PI;
    else
        ws = fabs(fs) * PI;
    if (wp == 0.0 || wp == ws || ws >= HP) {
        fprintf(stderr, "? (butlop) invalid input : fp=%14.6e fs=%14.6e ?\n",
            fp, fs);
        return 1;
    }
    /****  DETERMINE N & C */
    tp = tan(wp);
    ts = tan(ws);
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
    if ((*n = (int) (fabs(log(pa / sa) / log(tp / ts)) + 0.5)) < 2)
        *n = 2;
    cc = exp(log(pa * sa) / (double) (*n)) / (tp * ts);
    c = sqrt(cc);
    dp = HP / (double) (*n);
    *m = (*n) / 2;
    k = (*m) * 4;
    g = fj = 1.0;
    c2 = 2.0 * (1.0 - c) * (1.0 + c);
    for (j = 0; j < k; j += 4) {
        sj = pow(cos(dp * fj), 2.0);
        tj = sin(dp * fj);
        fj = fj + 2.0;
        a = 1.0 / (pow(c + tj, 2.0) + sj);
        g = g * a;
        h[j] = 2.0;
        h[j + 1] = 1.0;
        h[j + 2] = c2 * a;
        h[j + 3] = (pow(c - tj, 2.0) + sj) * a;
    }
    /****  EXIT */
    *gn = g;
    if (*n % 2 == 0)
        return 0;
    /****  FOR ODD N */
    *m = (*m) + 1;
    *gn = g / (1.0 + c);
    h[k] = 1.0;
    h[k + 1] = 0.0;
    h[k + 2] = (1.0 - c) / (1.0 + c);
    h[k + 3] = 0.0;
    return 0;
}
