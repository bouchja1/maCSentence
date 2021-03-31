# 🇨🇿 maCSentence API

- Make Czech sentences from Czech input text.
- Run this project in a Docker container and use it as an API for your project.

Z českého textu na vstupu vrátí pole českých vět :).

Všechno díky (fakt díky!) projektu [Centra zpracování přirozeného jazyka (FI MUNI, Brno)](https://nlp.fi.muni.cz/projekty/rozdelovac_vet/control.cgi). Autorem rozdělovače (celá složka [separator](separator) zde v projektu) je práce Mgr. Petra Machovce.

### Install

* install node >= 10
* install dependencies with yarn

#### Run it locally: 

```
$ node index.js
```

#### Or you can use Docker:

```
$ docker build -t macsentence .
$ docker run -i -t --rm --env-file=./.env -p=3001:3001 --name="macsentence" macsentence
```

Or the same as above with makefile that is a part of the project:

```
$ make build
$ make run
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
