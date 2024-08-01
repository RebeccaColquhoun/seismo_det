#include <v9dewin_ext.h>
/*
+   RECURSIVE FILTERING IN SERIES
+
+   ARGUMENTS
+   X : INPUT TIME SERIES
+   Y : OUTPUT TIME SERIES  (MAY BE EQUIVALENT TO X)
+   N : LENGTH OF X & Y
+   H : COEFFICIENTS OF FILTER
+   M : ORDER OF FILTER
+   NML : >0 ; FOR NORMAL  DIRECTION FILTERING
+       <0 ;   REVERSE DIRECTION FILTERING
+   uv  : past data and results saved
+
+   SUBROUTINE REQUIRED : RECFIL
+
+   M. SAITO  (6/XII/75)
*/
int tandem(double * x, double * y, int n, double * h, int m, int nml, double * uv)
{
    int     i;
    if (n <= 0 || m <= 0) {
        fprintf(stderr, "? (tandem) invalid input : n=%d m=%d ?\n", n, m);
        return 1;
    }
    /****  1-ST CALL */
    recfil(x, y, n, h, nml, uv);
    /****  2-ND AND AFTER */
    if (m > 1)
        for (i = 1; i < m; i++)
            recfil(y, y, n, &h[i * 4], nml, &uv[i * 4]);
    return 0;
}
