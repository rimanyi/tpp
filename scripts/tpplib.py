"""Shared helpers for the Thom Polynomial Portal repository.

Data-file format (one file per cell: entity x kind x l):

    # title: Thom polynomial of A2, relative dimension l=2
    # entity: A2
    # kind: tp
    # l: 2
    # codimension: 6
    # source: ...
    # ... more "# key: value" header lines ...
    Tp_A2_l2_monomial := 2*c[1]*c[5] +c[2]*c[4] +c[3]^2 +4*c[6]:
    Tp_A2_l2_schur := 8*s[[6]] +s[[3,3]] +2*s[[4,2]] +4*s[[5,1]]:

Header lines are comments for Maple ('#'), so `read "tp_l2.txt":` in Maple defines
the polynomials.  Each Maple assignment ends with ':'.  Expressions that are not
Maple expressions (TeX) are stored as Maple strings ("...").

K-theory (kinds ktp, ktp_ms0, ms): expansions in double stable Grothendieck polynomials,
written gr[[lambda]] like s[[lambda]] for Schur polynomials (gr is the name used by the Maple package
"Double stable Grothendieck polynomials" on the Downloads page: subs(GR[k,l], gr[lambda])):

    KTp_A2_l0_grothendieck :=          one line per degree |lambda|
    gr[[1,1]] +2*gr[[2]]
    -2*gr[[2,1]] -gr[[3]]
    +gr[[3,1]]
    :
    MS_A2_l0_closure_grothendieck :=   one block per order of z
    +z^0*( ... )
    +z^1*( ... )
    :
"""
import os
import re

HEADER_ORDER = ['title', 'entity', 'kind', 'l', 'codimension', 'locus', 'computed-up-to-degree', 'computed-up-to-z-order', 'partial',
                'version', 'ms0-version', 'same-closure-as', 'terms', 'degrees', 'nonzero-per-z-order', 'top-degree-per-z-order',
                'local-algebra', 'tp-degree', 'format', 'variables', 'formula-status', 'expansion-status', 'completeness',
                'source', 'old-portal', 'dataset', 'remark', 'note', 'convention', 'retrieved-from']

# ------------------------------------------------------------------ data files

def write_datafile(path, header, assignments):
    """header: dict (ordered); assignments: list of (maple_name, expression, is_string)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = []
    keys = [k for k in HEADER_ORDER if k in header] + [k for k in header if k not in HEADER_ORDER]
    for k in keys:
        v = header[k]
        if v is None or v == '':
            continue
        for i, part in enumerate(str(v).split('\n')):
            lines.append(f'# {k}: {part}' if i == 0 else f'#   {part}')
    lines.append('# Read into Maple with:  read "' + os.path.basename(path) + '":')
    for name, expr, is_string in assignments:
        if is_string:
            expr = '"' + expr.replace('\\', '\\\\').replace('"', '\\"') + '"'
        if '\n' in expr:
            lines.append(f'{name} :=\n{expr}\n:')
        else:
            lines.append(f'{name} := {expr}:')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')


ASSIGN_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*:=\s*(.*?)\s*:\s*$', re.S | re.M)


def read_datafile(path):
    """Return (header dict, list of (name, expression, is_string))."""
    header, body_lines = {}, []
    last = None
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('#'):
                m = re.match(r'#\s([A-Za-z0-9_-]+):\s?(.*)$', line)
                if m and not line.startswith('# Read into Maple'):
                    last = m.group(1)
                    header[last] = m.group(2)
                elif line.startswith('#   ') and last:
                    header[last] += '\n' + line[4:]
            else:
                body_lines.append(line)
    body = '\n'.join(body_lines)
    # split on assignments: NAME := ... :   (expression may span lines; ends with ':')
    starts = list(re.finditer(r'(?m)^([A-Za-z_][A-Za-z0-9_]*)\s*:=', body))
    result = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(body)
        name = m.group(1)
        chunk = body[m.end():end].strip()
        if chunk.endswith(':'):
            chunk = chunk[:-1].rstrip()
        is_string = chunk.startswith('"') and chunk.endswith('"')
        if is_string:
            chunk = chunk[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        result.append((name, chunk, is_string))
    return header, result


def max_tdeg(expr):
    ks = [int(k) for k in re.findall(r't\s*\^\s*(\d+)', expr)]
    return max(ks) if ks else None


def min_tdeg(expr):
    ks = [int(k) for k in re.findall(r't\s*\^\s*(\d+)', expr)]
    return min(ks) if ks else None

# ------------------------------------------------------------------ entity names

def maple_name(entity_id):
    """A Maple-safe identifier for an entity id (2A0+A2 -> M_2A0_A2)."""
    s = re.sub(r'[^A-Za-z0-9]', '_', entity_id)
    if not re.match(r'[A-Za-z]', s):
        s = 'M_' + s
    return s


SPECIAL_TEX = {
    'C510': r'\mathrm{C}_{5,10}', 'C511': r'\mathrm{C}_{5,11}',
    'EMPTY': r'\varnothing',
    'Sigma3-pencil': r'\textstyle\bigcup_{\lambda}(x^2-\lambda yz,\,y^2-\lambda xz,\,z^2-\lambda xy)',
}
SPECIAL_PLAIN = {'C510': 'C5,10', 'C511': 'C5,11', 'EMPTY': '∅', 'Sigma3-pencil': 'Σ³ pencil'}


def mono_tex(mid):
    if mid in SPECIAL_TEX:
        return SPECIAL_TEX[mid]
    m = re.fullmatch(r'([A-Z]+)(\d+)', mid)
    if m:
        return r'\mathrm{%s}_{%s}' % (m.group(1), m.group(2))
    if mid.startswith('ideal-'):
        return mid  # replaced by catalog tex
    return r'\mathrm{%s}' % mid


def mono_plain(mid):
    return SPECIAL_PLAIN.get(mid, mid)


def mono_html(mid):
    """Display name in HTML without MathJax: A<sub>2</sub>."""
    if mid in SPECIAL_PLAIN and mid not in ('C510', 'C511'):
        return SPECIAL_PLAIN[mid]
    if mid == 'C510':
        return 'C<sub>5,10</sub>'
    if mid == 'C511':
        return 'C<sub>5,11</sub>'
    m = re.fullmatch(r'([A-Z]+)(\d+)', mid)
    if m:
        return f'{m.group(1)}<sub>{m.group(2)}</sub>'
    return mid


def multi_parts(mid):
    """'2A0+A2' -> [(2,'A0'),(1,'A2')]"""
    if mid == 'EMPTY':
        return []
    out = []
    for p in mid.split('+'):
        m = re.fullmatch(r'(\d*)(.+)', p)
        out.append((int(m.group(1) or 1), m.group(2)))
    return out


def multi_tex(mid):
    if mid == 'EMPTY':
        return r'\varnothing'
    return '+'.join((str(k) if k > 1 else '') + mono_tex(n) for k, n in multi_parts(mid))


def multi_html(mid):
    if mid == 'EMPTY':
        return '∅'
    return '+'.join((str(k) if k > 1 else '') + mono_html(n) for k, n in multi_parts(mid))


def multi_slug(mid):
    return 'empty' if mid == 'EMPTY' else mid


# ------------------------------------------------------------------ Grothendieck expansions (K-theory)

def _gterm(lam, c):
    g = 'gr[[' + ','.join(map(str, lam)) + ']]'
    if c == 1:
        return '+' + g
    if c == -1:
        return '-' + g
    return ('+' if c > 0 else '-') + str(abs(c)) + '*' + g


def g_expr(tab):
    """{partition: integer} -> Maple expression, one line per degree, partitions in increasing order."""
    by = {}
    for lam in sorted(tab, key=lambda p: (sum(p), p)):
        if tab[lam]:
            by.setdefault(sum(lam), []).append(_gterm(lam, tab[lam]))
    s = '\n'.join(' '.join(by[n]) for n in sorted(by))
    return s[1:] if s.startswith('+') else s


def ms_expr(tab, K):
    """{partition: [c_0..c_K]} -> Maple expression  +z^0*( ... ) +z^1*( ... ) ..., one block per order of z."""
    blocks = []
    for k in range(K + 1):
        sub = {lam: cs[k] for lam, cs in tab.items() if cs[k]}
        if not sub:
            continue
        body = g_expr(sub)
        blocks.append(f'+z^{k}*(\n{body}\n)' if '\n' in body else f'+z^{k}*( {body} )')
    return '\n'.join(blocks)


G_TERM = re.compile(r'([+-]?)\s*(\d*)\s*\*?\s*gr\[\[([\d,\s]*)\]\]')


def parse_g(expr):
    """Inverse of g_expr."""
    out = {}
    for sign, coef, lam in G_TERM.findall(expr):
        lam = tuple(int(x) for x in lam.replace(' ', '').split(',') if x)
        out[lam] = out.get(lam, 0) + (-1 if sign == '-' else 1) * int(coef or 1)
    return {k: v for k, v in out.items() if v}


Z_BLOCK = re.compile(r'\+z\^(\d+)\*\((.*?)\)\s*(?=\+z\^|\Z)', re.S)


def ms_blocks(expr):
    """[(k, text of the block of z^k)] of an ms expression."""
    return [(int(k), body.strip()) for k, body in Z_BLOCK.findall(expr)]


def parse_ms(expr, K):
    """Inverse of ms_expr: {partition: [c_0..c_K]}."""
    out = {}
    for k, body in ms_blocks(expr):
        for lam, c in parse_g(body).items():
            out.setdefault(lam, [0] * (K + 1))[k] = c
    return out


def g_tex(expr, max_terms=40):
    """TeX of a Grothendieck expansion (None if it has more than max_terms terms)."""
    if len(G_TERM.findall(expr)) > max_terms:
        return None
    lines = []
    for ln in expr.strip().split('\n'):
        t = re.sub(r'gr\[\[([\d,\s]*)\]\]', lambda m: 'G_{' + (m.group(1).replace(' ', '') or r'\varnothing') + '}', ln.strip())
        t = re.sub(r'\s*([+-])', r' \1 ', t).replace('*', r'\,').strip()
        lines.append(t)
    if len(lines) == 1:
        return re.sub(r'^\+\s*', '', lines[0])
    lines[0] = re.sub(r'^\+\s*', '', lines[0])
    return r'\begin{aligned}' + r' \\ '.join('& ' + ln for ln in lines) + r'\end{aligned}'

# ------------------------------------------------------------------ Thom-Boardman classes

_SUP = str.maketrans('0123456789,', '⁰¹²³⁴⁵⁶⁷⁸⁹’')


def tb_symbol(tid):
    """'Sigma2' -> '2';  'Sigma2-1' -> '2,1'  (ids of Thom-Boardman classes: Sigma + the symbol, parts joined by '-')."""
    return tid[len('Sigma'):].replace('-', ',')


def tb_tex(tid):
    return r'\Sigma^{%s}' % tb_symbol(tid)


def tb_html(tid):
    return 'Σ<sup>%s</sup>' % tb_symbol(tid)


def tb_plain(tid):
    return 'Σ' + tb_symbol(tid).translate(_SUP)
