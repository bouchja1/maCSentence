# macZentence API

Make a czech sentences from czech text input.

Z českého textu vrací pole českých vět :).

Všechno díky (díky, díky!) projektu [Centra zpracování přirozeného jazyka (MUNI, Brno)](https://nlp.fi.muni.cz/projekty/rozdelovac_vet/control.cgi).

### Running locally

* install node >= 10
* install dependencies with yarn

```
$ node index.js
```

## Usage

* POST http://localhost:3001/sentence

### Request
```
{
   "text":"Na další planetě bydlil pijan. Návštěva u něho byla velice krátká, ale malého prince hodně rozesmutnila. „Co tady děláš?“ řekl pijanovi, který seděl mlčky před řadou prázdných a řadou plných lahví. „Piji,“ odpověděl pochmurně pijan. „A proč piješ?“ zeptal se malý princ. „Abych zapomněl,“ řekl pijan. „Nač abys zapomněl?“ vyzvídal malý princ a užuž ho začínal litovat. „Abych zapomněl, že se stydím,“ přiznal se pijan a sklonil hlavu. „A zač se stydíš?“ vyptával se dále malý princ, protože by mu rád pomohl. „Stydím se, že piji!“ dodal pijan a nadobro se odmlčel. A malý princ zmaten odešel. Dospělí jsou rozhodně moc a moc zvláštní, říkal si v duchu cestou."
}
```

### Response

```
{
    "sentences": [
        "Na další planetě bydlil pijan.",
        "Návštěva u něho byla velice krátká, ale malého prince hodně rozesmutnila.",
        "„Co tady děláš?“ řekl pijanovi, který seděl mlčky před řadou prázdných a řadou plných lahví.",
        "„Piji,“ odpověděl pochmurně pijan.",
        "„A proč piješ?“ zeptal se malý princ.",
        "„Abych zapomněl,“ řekl pijan.",
        "„Nač abys zapomněl?“ vyzvídal malý princ a užuž ho začínal litovat.",
        "„Abych zapomněl, že se stydím,“ přiznal se pijan a sklonil hlavu.",
        "„A zač se stydíš?“ vyptával se dále malý princ, protože by mu rád pomohl.",
        "„Stydím se, že piji!“ dodal pijan a nadobro se odmlčel.",
        "A malý princ zmaten odešel.",
        "Dospělí jsou rozhodně moc a moc zvláštní, říkal si v duchu cestou.\n"
    ]
}
```
