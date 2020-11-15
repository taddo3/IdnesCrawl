import unittest


class TaggerTestCases(unittest.TestCase):
    def test_get_lemmas(self):
        from src.tagger.tagger import Lemmatizer
        text_for_tagging = 'Častěji než před vyhlášením nouzového stavu si jídlo vyzvedává nebo nechává dovézt asi třetina Čechů. Na této formě stravování 90 procent lidí oceňuje pohodlí, pro 80 procent respondentů znamená hlavně dostupnost, rychlost a chuť objednaného jídla. Stravovací provozy musejí být od 14. října pro veřejnost uzavřené. Jídlo mohou prodávat přes rozvoz nebo výdejní okénka, která mohou fungovat mezi 06:00 a 20:00. Uvolňování v závislosti na vývoji nákazy by se mělo řídit modelem, který v pátek představilo ministerstvo zdravotnictví. Ve všech pěti stupních rizika bude ale provoz gastronomických zařízení částečně omezen.'
        lem = Lemmatizer('../../src/tagger/czech-morfflex-pdt-161115.tagger')
        lemmas = lem.get_lemmas(text_for_tagging)
        self.assertTrue(bool(lemmas))
        self.assertLessEqual(lemmas[1][1], lemmas[0][1])


if __name__ == '__main__':
    unittest.main()
