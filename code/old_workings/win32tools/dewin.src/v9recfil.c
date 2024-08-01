#include <v9dewin_ext.h>
/*
+   RECURSIVE FILTERING : F(Z) = (1+A*Z+AA*Z**2)/(1+B*Z+BB*Z**2)
+
+   ARGUMENTS
+   X : INPUT TIME SERIES
+   Y : OUTPUT TIME SERIES  (MAY BE EQUIVALENT TO X)
+   N : LENGTH OF X & Y
+   H : FILTER COEFFICIENTS ; H(1)=A, H(2)=AA, H(3)=B, H(4)=BB
+   NML : >0 ; FOR NORMAL  DIRECTION FILTERING
+       <0 ; FOR REVERSE DIRECTION FILTERING
+   uv  : past data and results saved
+
+   M. SAITO  (6/XII/75)
*/
int recfil(double * x, double * y, int n, double * h, int nml, double * uv)
{
    int     i, j, jd;
    double  a, aa, b, bb, u1, u2, u3, v1, v2, v3;
    if (n <= 0) {
        fprintf(stderr, "? (recfil) invalid input : n=%d ?\n", n);
        return 1;
    }
    if (nml >= 0) {
        j = 0;
        jd = 1;
    } else {
        j = n - 1;
        jd = (-1);
    }
    a = h[0];
    aa = h[1];
    b = h[2];
    bb = h[3];
    u1 = uv[0];
    u2 = uv[1];
    v1 = uv[2];
    v2 = uv[3];
    /****  FILTERING */
    for (i = 0; i < n; i++) {
        u3 = u2;
        u2 = u1;
        u1 = x[j];
        v3 = v2;
        v2 = v1;
        v1 = u1 + a * u2 + aa * u3 - b * v2 - bb * v3;
        y[j] = v1;
        j += jd;
    }
    uv[0] = u1;
    uv[1] = u2;
    uv[2] = v1;
    uv[3] = v2;
    return 0;
}
