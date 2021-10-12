#include <s4win2sac.h>
#include    <stdio.h>
#include <string.h>
void 
swap_header(_sac_header * ptHeader)
{
    int ia;
    swap4b((unsigned int *)&ptHeader->delta);
    swap4b((unsigned int *)&ptHeader->depmin);
    swap4b((unsigned int *)&ptHeader->depmax);
    swap4b((unsigned int *)&ptHeader->scale);
    swap4b((unsigned int *)&ptHeader->odelta);
    swap4b((unsigned int *)&ptHeader->b);
    swap4b((unsigned int *)&ptHeader->e);
    swap4b((unsigned int *)&ptHeader->o);
    swap4b((unsigned int *)&ptHeader->a);
    swap4b((unsigned int *)&ptHeader->rint1);
    swap4b((unsigned int *)&ptHeader->t0);
    swap4b((unsigned int *)&ptHeader->t1);
    swap4b((unsigned int *)&ptHeader->t2);
    swap4b((unsigned int *)&ptHeader->t3);
    swap4b((unsigned int *)&ptHeader->t4);
    swap4b((unsigned int *)&ptHeader->t5);
    swap4b((unsigned int *)&ptHeader->t6);
    swap4b((unsigned int *)&ptHeader->t7);
    swap4b((unsigned int *)&ptHeader->t8);
    swap4b((unsigned int *)&ptHeader->t9);
    swap4b((unsigned int *)&ptHeader->f);
    swap4b((unsigned int *)&ptHeader->resp0);
    swap4b((unsigned int *)&ptHeader->resp1);
    swap4b((unsigned int *)&ptHeader->resp2);
    swap4b((unsigned int *)&ptHeader->resp3);
    swap4b((unsigned int *)&ptHeader->resp4);
    swap4b((unsigned int *)&ptHeader->resp5);
    swap4b((unsigned int *)&ptHeader->resp6);
    swap4b((unsigned int *)&ptHeader->resp7);
    swap4b((unsigned int *)&ptHeader->resp8);
    swap4b((unsigned int *)&ptHeader->resp9);
    swap4b((unsigned int *)&ptHeader->stla);
    swap4b((unsigned int *)&ptHeader->stlo);
    swap4b((unsigned int *)&ptHeader->stel);
    swap4b((unsigned int *)&ptHeader->stdp);
    swap4b((unsigned int *)&ptHeader->evla);
    swap4b((unsigned int *)&ptHeader->evlo);
    swap4b((unsigned int *)&ptHeader->evel);
    swap4b((unsigned int *)&ptHeader->evdp);
    swap4b((unsigned int *)&ptHeader->runs1);
    swap4b((unsigned int *)&ptHeader->user0);
    swap4b((unsigned int *)&ptHeader->user1);
    swap4b((unsigned int *)&ptHeader->user2);
    swap4b((unsigned int *)&ptHeader->user3);
    swap4b((unsigned int *)&ptHeader->user4);
    swap4b((unsigned int *)&ptHeader->user5);
    swap4b((unsigned int *)&ptHeader->user6);
    swap4b((unsigned int *)&ptHeader->user7);
    swap4b((unsigned int *)&ptHeader->user8);
    swap4b((unsigned int *)&ptHeader->user9);
    swap4b((unsigned int *)&ptHeader->dist);
    swap4b((unsigned int *)&ptHeader->az);
    swap4b((unsigned int *)&ptHeader->baz);
    swap4b((unsigned int *)&ptHeader->gcarc);
    swap4b((unsigned int *)&ptHeader->rint2);
    swap4b((unsigned int *)&ptHeader->rint3);
    swap4b((unsigned int *)&ptHeader->depmen);
    swap4b((unsigned int *)&ptHeader->cmpaz);
    swap4b((unsigned int *)&ptHeader->cmpinc);
    for (ia=0; ia<11; ia++) {
        swap4b((unsigned int *)&ptHeader->runs2[ia]);
    }
    swap4b((unsigned int *)&ptHeader->nzyear);
    swap4b((unsigned int *)&ptHeader->nzjday);
    swap4b((unsigned int *)&ptHeader->nzhour);
    swap4b((unsigned int *)&ptHeader->nzmin);
    swap4b((unsigned int *)&ptHeader->nzsec);
    swap4b((unsigned int *)&ptHeader->nzmsec);
    swap4b((unsigned int *)&ptHeader->nvhdr);
    swap4b((unsigned int *)&ptHeader->iint1[0]);
    swap4b((unsigned int *)&ptHeader->iint1[1]);
    swap4b((unsigned int *)&ptHeader->npts);
    swap4b((unsigned int *)&ptHeader->iint2[0]);
    swap4b((unsigned int *)&ptHeader->iint2[1]);
    swap4b((unsigned int *)&ptHeader->iuns1[0]);
    swap4b((unsigned int *)&ptHeader->iuns1[1]);
    swap4b((unsigned int *)&ptHeader->iuns1[2]);
    swap4b((unsigned int *)&ptHeader->iftype);
    swap4b((unsigned int *)&ptHeader->idep);
    swap4b((unsigned int *)&ptHeader->iztype);
    swap4b((unsigned int *)&ptHeader->iuns2);
    swap4b((unsigned int *)&ptHeader->iinst);
    swap4b((unsigned int *)&ptHeader->istreg);
    swap4b((unsigned int *)&ptHeader->ievreg);
    swap4b((unsigned int *)&ptHeader->ievtyp);
    swap4b((unsigned int *)&ptHeader->iqual);
    swap4b((unsigned int *)&ptHeader->isynth);
    for (ia=0; ia<10; ia++) {
        swap4b((unsigned int *)&ptHeader->iuns3[ia]);
    }
    swap4b((unsigned int *)&ptHeader->leven);
    swap4b((unsigned int *)&ptHeader->lpspol);
    swap4b((unsigned int *)&ptHeader->lovrok);
    swap4b((unsigned int *)&ptHeader->lcalda);
    swap4b((unsigned int *)&ptHeader->luns1);
}
