#include <string.h>
#include <stdlib.h>
#include <v9dewin_ext.h>
int get_filter(int sr, struct Filter * f)
{
    double  dt;
    dt = 1.0 / (double) sr;
    if (strcmp(f->kind, "LPF") == 0)
        butlop(f->coef, &f->m_filt, &f->gn_filt, &f->n_filt,
            f->fp * dt, f->fs * dt, f->ap, f->as);
    else if (strcmp(f->kind, "HPF") == 0)
        buthip(f->coef, &f->m_filt, &f->gn_filt, &f->n_filt,
            f->fp * dt, f->fs * dt, f->ap, f->as);
    else if (strcmp(f->kind, "BPF") == 0)
        butpas(f->coef, &f->m_filt, &f->gn_filt, &f->n_filt,
            f->fl * dt, f->fh * dt, f->fs * dt, f->ap, f->as);
    if (f->m_filt > MAX_FILT) {
        fputs("filter order exceeded limit\n", stderr);
        exit(1);
    }
    return 0;
}
