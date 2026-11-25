"""Convert the K-theory data set of 2026-11-25 into the portal's data files.

    python scripts/import_ktp_dataset.py PATH_TO_THE_DATA_SET

The data set (tables, the code that produced them, logs, README) is kept by the authors and is not part of
this repository; only the data files written here are.  Rerun this script when the data set is replaced by
a newer one.  It writes

  ktp_l<N>.txt          K-theoretic Thom polynomial, push-forward version      (family KTp of the data set)
  ktp_ms0_l<N>.txt      K-theoretic Thom polynomial, MS0 version, where it     (family mstp0)
                        differs from the push-forward version
  ms_closure_l<N>.txt   motivic Segre Thom polynomial of the closure, a series (families ms and ms-block;
                        in z                                                    ms-block files are marked partial)

into data/contact/<ID>/ for contact singularities and into data/thom-boardman/Sigma<r>/ for the Thom-Boardman
classes Sigma^r.  The family aux of the data set is not a Thom polynomial and is not imported.

What a data file says about itself:
  source             the credit line (rule set by R. Rimanyi on 2026-11-25, see SOURCE_* below)
  formula-status     THM / MODEL / ARG / UNCHECKED, with a reference when the formula is in the literature
  expansion-status   THM / VER
  completeness       which coefficients the file claims to list
  dataset            the table of the data set the file was made from
Working notes of the data set (which generating function, which checks were run, internal references) are
deliberately left out of the data files.

Every file is read back after writing and compared with the data set, coefficient by coefficient.
"""
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tpplib import read_datafile, write_datafile, maple_name, parse_g, parse_ms, g_expr, ms_expr  # noqa: E402

ROOT = os.path.dirname(HERE)
DS_DATE = '2026-11-25'

# ---------------------------------------------------------------- credit lines
SOURCE_FR = 'L. M. Fehér, R. Rimányi: K theory Thom polynomials, in preparation, 2026'
SOURCE_RS = ('R. Rimányi, A. Szenes: Residues, Grothendieck polynomials, and K-theoretic Thom polynomials, '
             'Int. Math. Res. Not. IMRN, https://doi.org/10.1093/imrn/rnac345')
SOURCE_CLASSICAL = 'classical (reference to be added)'

VARS_G = ('gr[[lambda]] = double stable Grothendieck polynomial G_lambda, in the convention of Rimanyi-Szenes '
          '(see the Conventions page); gr[[]] = 1')
CONVENTION = 'TPP 2026-K'
KAZARIAN = 'M. Kazarian, Non-associative Hilbert scheme and Thom polynomials, arXiv:1712.09270'


def target(name):
    """(entity type, entity id) on the portal for a singularity name of the data set."""
    base = name[:-3] if name.endswith('bar') else name
    return ('thom-boardman', base) if base.startswith('Sigma') else ('contact', base)


def formula_status(e):
    tag, ref = e['formula']['tag'], e['formula']['ref']
    if tag == 'THM':
        if ref.startswith('Rimanyi-Szenes Thm 7.1'):
            return 'THM (theorem) -- K-theoretic Giambelli-Thom-Porteous formula (see Rimanyi-Szenes, Thm 7.1)'
        if ref.startswith('Rimanyi-Szenes Thm 8.1'):
            return 'THM (theorem) -- Rimanyi-Szenes, Thm 8.1 (residue formula)'
        if ref.startswith('Rimanyi-Szenes Thm 10.1'):
            return 'THM (theorem) -- Rimanyi-Szenes, Thm 10.1 (residue formula)'
        if ref.startswith('Feher-Rimanyi-Weber'):
            return 'THM (theorem) -- Feher-Rimanyi-Weber, Motivic Chern classes and K-theoretic stable envelopes, Thm 8.3'
        if ref.startswith('Morin product'):
            return ('THM (theorem) -- product formula for germs of one variable, where the closure is a linear subspace; '
                    'this is why only a block of partitions is given')
        raise SystemExit(f"{e['id']}: unknown theorem reference; add it to formula_status()")
    if tag == 'MODEL':
        return f'MODEL (resolution model, not refereed) -- Kazarian\'s resolution model ({KAZARIAN}), used in K-theory'
    if tag == 'ARG':
        return 'ARG (argued, not proved) -- details in the paper in preparation'
    if tag == 'HANDOUT-THM':
        return 'UNCHECKED (stated, not yet checked) -- details in the paper in preparation'
    raise SystemExit(f"{e['id']}: unknown formula tag {tag}")


def expansion_status(e):
    tag, how = e['expansion']['tag'], e['expansion']['how']
    if tag == 'THM':
        if how.startswith('Rimanyi-Szenes Thm 8.4'):
            return 'THM (theorem) -- Rimanyi-Szenes, Thm 8.4'
        return 'THM (theorem) -- a single Grothendieck polynomial'
    if tag == 'VER':
        return 'VER (computed and verified numerically) -- compared with the formula at random points'
    raise SystemExit(f"{e['id']}: unknown expansion tag {tag}")


def completeness(e):
    c = e['completeness']
    # the scope is kept; the remark on how the scope was established is a working note
    c = re.sub(r' \(the residue check on .*?is expected\)', ' (no term outside this range is expected)', c)
    return c


def source_for(e, etype, eid, sigma_alias):
    """The credit rule of 2026-11-25: everything is Feher-Rimanyi (in preparation), except the push-forward KTp of the
    classes Sigma^r (classical) and of A2 (Rimanyi-Szenes).  A contact singularity that is the open stratum of Sigma^r
    at this l (A1 for all l, I22 at l=0, C41 at l=2) has the same class as Sigma^r there, so it is classical too."""
    if e['family'] == 'KTp':
        if etype == 'thom-boardman' or eid == 'A1' or sigma_alias:
            return SOURCE_CLASSICAL
        if eid == 'A2':
            return SOURCE_RS
    return SOURCE_FR


def old_portal_info(path, new_table):
    """Was this entry on the old portal?  (Read from the file being replaced, or kept from a previous run.)"""
    if not os.path.exists(path):
        return {}
    h, a = read_datafile(path)
    if 'old-portal' in h:
        return {'old-portal': h['old-portal']}
    tex = next((x for n, x, s in a if n.endswith('_tex')), None)
    rf = h.get('retrieved-from', '')
    if tex is None:
        return {}
    if tex.strip() == '?':
        return {'old-portal': f'shown as "?" (unknown) on {rf}'}
    old = parse_old_tex(tex)
    # A3 at l=0 and l=1: the old page spreads the entry over two table cells and the November 2026 migration kept
    # only the first, so the migrated file is a part of the new table.  The complete old entries were compared with
    # the data set from the WordPress export of 2026-10-18: identical.
    if old == new_table or all(new_table.get(lam) == c for lam, c in old.items()):
        return {'old-portal': f'identical to the entry on {rf}'}
    raise SystemExit(f'{path}: the old portal entry differs from the data set; resolve by hand')


def parse_old_tex(tex):
    """'g_{1,1}+ 2g_{2} - ( 2g_{2,1}+g_{3} ) + g_{3,1}'  ->  {(1,1): 1, (2,): 2, (2,1): -2, (3,): -1, (3,1): 1}"""
    s = re.sub(r'=1$', '', tex.replace(' ', ''))
    out, sign_stack, sign, i = defaultdict(int), [1], 1, 0
    tok = re.compile(r'(\d*)g_\{([\d,]*)\}')
    while i < len(s):
        ch = s[i]
        if ch in '+-':
            sign = 1 if ch == '+' else -1
            i += 1
        elif ch == '(':
            sign_stack.append(sign_stack[-1] * sign)
            sign = 1
            i += 1
        elif ch == ')':
            sign_stack.pop()
            sign = 1
            i += 1
        else:
            m = tok.match(s, i)
            if not m:
                raise ValueError(f'cannot parse old KTp string at {s[i:i + 20]!r}')
            lam = tuple(int(x) for x in m.group(2).split(',') if x and int(x) > 0)
            out[lam] += sign_stack[-1] * sign * int(m.group(1) or 1)
            sign = 1
            i = m.end()
    return {k: v for k, v in out.items() if v}


def main():
    if len(sys.argv) < 2 or not os.path.exists(os.path.join(sys.argv[1], 'index.json')):
        raise SystemExit(__doc__)
    ds = os.path.abspath(sys.argv[1])
    index = json.load(open(os.path.join(ds, 'index.json'), encoding='utf-8'))
    by_id = {e['id']: e for e in index['entries']}
    tables = {}

    def table(e):
        if e['file'] not in tables:
            tables[e['file']] = {t['id']: t for t in json.load(open(os.path.join(ds, e['file']), encoding='utf-8'))['tables']}
        return tables[e['file']][e['id']]

    ms0_equal = {}
    for r in index['mstp0_equals_KTp']:
        if r['singularity'] == 'A2bar':
            lo, hi = r['l_range']
            for l in range(lo, hi + 1):
                ms0_equal[('A2', l)] = f'equal to this push-forward version (verified numerically for l = {lo}..{hi})'
        else:
            ms0_equal['Sigma'] = 'equal to this push-forward version (proved: determinantal varieties have rational singularities)'
    written, skipped = [], []
    for e in index['entries']:
        fam, l = e['family'], e['l']
        if fam == 'aux':
            skipped.append(e['id'])
            continue
        etype, eid = target(e['singularity'])
        folder = os.path.join(ROOT, 'data', etype, eid)
        t = table(e)
        mn = maple_name(eid)
        if fam in ('KTp', 'mstp0'):
            tab = {tuple(lam): c for lam, c in t['terms']}
            st = e                     # the record whose status is quoted
            sigma_alias = next((a for a in e['aliases'] if a.startswith('Sigma')), None) if etype == 'contact' else None
            if sigma_alias:            # the same locus as Sigma^r at this l: quote the status of the Sigma^r table
                st = by_id[f'KTp/{sigma_alias}/l{l}']
                assert {tuple(lam): c for lam, c in table(st)['terms']} == tab, e['id']
            if fam == 'KTp':
                fname, kind, name = f'ktp_l{l}.txt', 'ktp', f'KTp_{mn}_l{l}_grothendieck'
                title = f'K-theoretic Thom polynomial of {eid}, push-forward version, relative dimension l={l}'
                version = 'push-forward (the class of the structure sheaf of a resolution of the closure, pushed forward)'
            else:
                fname, kind, name = f'ktp_ms0_l{l}.txt', 'ktp_ms0', f'KTpMS0_{mn}_l{l}_grothendieck'
                title = f'K-theoretic Thom polynomial of {eid}, MS0 version, relative dimension l={l}'
                version = ('MS0 (the class mC_0 of the closure; the z^0 coefficient of the motivic Segre Thom polynomial '
                           'of the closure). Differs from the push-forward version for this singularity')
            path = os.path.join(folder, fname)
            h = {'title': title, 'entity': eid, 'kind': kind, 'l': l, 'codimension': e['codim'], 'locus': 'closure',
                 'version': version, 'terms': e['nterms'], 'degrees': f"{e['degree_min']}..{e['degree_max']}", 'variables': VARS_G}
            if fam == 'KTp':
                eq = ms0_equal.get((eid, l)) or (ms0_equal['Sigma'] if (etype == 'thom-boardman' or sigma_alias) else None)
                if eid == 'A1':
                    eq = 'equal to this push-forward version (the closure of A1 is the closure of Sigma^1)'
                if eq:
                    h['ms0-version'] = eq
                if e['aliases']:
                    h['same-closure-as'] = ', '.join(e['aliases']) + ' (at this l)'
            h['formula-status'] = formula_status(st)
            h['expansion-status'] = expansion_status(st)
            h['completeness'] = completeness(st)
            h['source'] = source_for(e, etype, eid, sigma_alias)
            if fam == 'KTp':
                h.update(old_portal_info(path, tab))
            h['dataset'] = f"data set of {DS_DATE}, table {e['id']}"
            h['convention'] = CONVENTION
            write_datafile(path, h, [(name, g_expr(tab), False)])
            assert parse_g(read_datafile(path)[1][0][1]) == tab, path
        else:                                   # ms, ms-block: series in z
            tab = {tuple(lam): cs for lam, cs in t['terms']}
            K = e['z_max']
            partial = fam == 'ms-block'
            fname, name = f'ms_closure_l{l}.txt', f'MS_{mn}_l{l}_closure_grothendieck'
            path = os.path.join(folder, fname)
            h = {'title': f'Motivic Segre Thom polynomial of the closure of {eid}, relative dimension l={l}'
                          + (f" (partial: only the partitions with {e['block']})" if partial else ''),
                 'entity': eid, 'kind': 'ms', 'l': l, 'codimension': e['codim'], 'locus': 'closure',
                 'computed-up-to-z-order': K}
            if partial:
                h['partial'] = f"only the partitions with {e['block']}"
            h['terms'] = e['nterms']
            h['nonzero-per-z-order'] = ', '.join(map(str, e['nonzero_per_order']))
            h['top-degree-per-z-order'] = ', '.join(map(str, e['top_degree_per_order']))
            h['variables'] = ('z = the parameter of the motivic class (y = -z/(1+z)); the coefficient of z^0 is the MS0 version of '
                              'the K-theoretic Thom polynomial; ' + VARS_G)
            h['formula-status'] = formula_status(e)
            h['expansion-status'] = expansion_status(e)
            h['completeness'] = completeness(e)
            h['source'] = source_for(e, etype, eid, None)
            h['dataset'] = f"data set of {DS_DATE}, table {e['id']}"
            h['convention'] = CONVENTION
            write_datafile(path, h, [(name, ms_expr(tab, K), False)])
            assert parse_ms(read_datafile(path)[1][0][1], K) == {lam: cs for lam, cs in tab.items() if any(cs)}, path
        written.append(os.path.relpath(path, ROOT).replace(os.sep, '/'))

    # old-portal files that the data set does not replace: same content, new syntax
    for eid, l, tab, extra in (('A0', 0, {(): 1}, {}), ('A0', 1, {(): 1}, {}),
                               ('III22', 1, {(3, 3): 1}, {'same-closure-as': 'the Thom-Boardman class Sigma2 (for l >= 1); see its page for l = 0..8',
                                                          'source': SOURCE_CLASSICAL})):
        path = os.path.join(ROOT, 'data', 'contact', eid, f'ktp_l{l}.txt')
        h, a = read_datafile(path)
        tex = next((x for n, x, s in a if n.endswith('_tex')), None)
        if tex is None:
            continue                            # already converted
        assert parse_old_tex(tex) == tab, path
        h2 = {k: v for k, v in h.items() if k not in ('format', 'variables')}
        h2['title'] = f'K-theoretic Thom polynomial of {eid}, push-forward version, relative dimension l={l}'
        h2['locus'] = 'closure'
        h2['version'] = 'push-forward (the class of the structure sheaf of a resolution of the closure, pushed forward)'
        h2['terms'] = 1
        h2['variables'] = VARS_G
        h2['convention'] = CONVENTION
        h2.update(extra)
        write_datafile(path, h2, [(f'KTp_{maple_name(eid)}_l{l}_grothendieck', g_expr(tab), False)])
        assert parse_g(read_datafile(path)[1][0][1]) == tab, path
        written.append(os.path.relpath(path, ROOT).replace(os.sep, '/') + '  (syntax normalised)')

    by = defaultdict(int)
    for w in written:
        by[w.split('/')[1] + ': ' + re.sub(r'_l\d+\.txt.*', '', w.split('/')[-1])] += 1
    print(f'{len(written)} files written and read back; {len(skipped)} tables not imported (family aux)')
    for k in sorted(by):
        print(f'  {k}: {by[k]}')


if __name__ == '__main__':
    main()
