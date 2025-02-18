#!/usr/bin/env python

import os
from unittest import TestCase, main

from g2p import make_g2p
from g2p.exceptions import MalformedMapping
from g2p.log import LOGGER
from g2p.mappings import Mapping
from g2p.tests.public import __file__ as public_data
from g2p.transducer import Transducer


class LexiconTransducerTest(TestCase):
    def test_lexicon_mapping(self):
        """Test loading a lexicon mapping directly in the constructor."""
        with self.assertLogs(LOGGER, level="INFO"):
            m = Mapping(
                type="lexicon",
                case_sensitive=False,
                out_delimiter=" ",
                alignments=os.path.join(
                    os.path.dirname(public_data), "mappings", "hello.aligned.txt"
                ),
            )
        self.assertEqual(m.mapping, [])
        self.assertEqual(m.kwargs["type"], "lexicon")
        t = Transducer(m)
        tg = t("hello")
        self.assertEqual(tg.output_string, "HH EH L OW ")
        self.assertEqual(
            tg.edges, [(0, 0), (0, 1), (1, 3), (1, 4), (2, 6), (3, 6), (4, 8), (4, 9)]
        )
        tg = t("you're")
        self.assertEqual(tg.output_string, "Y UH R ")
        self.assertEqual(
            tg.edges,
            [(0, 0), (1, 2), (1, 3), (2, 2), (2, 3), (3, 4), (4, 5), (5, 5)],
        )
        # These alignments are somewhat bogus, hence the name
        tg = t("bogus")
        self.assertEqual(tg.input_string, "bogus")
        self.assertEqual(tg.output_string, "")
        self.assertEqual(
            tg.edges,
            [(0, None), (1, None), (2, None), (3, None), (4, None)],
        )
        self.assertEqual(
            tg.substring_alignments(),
            [("bogus", "")],
        )
        tg = t("bogus")
        tg += t("hello")
        self.assertEqual(tg.input_string, "bogushello")
        self.assertEqual(tg.output_string, "HH EH L OW ")
        self.assertEqual(
            tg.edges,
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
                (5, 1),
                (6, 3),
                (6, 4),
                (7, 6),
                (8, 6),
                (9, 8),
                (9, 9),
            ],
        )
        self.assertEqual(
            tg.substring_alignments(),
            [("bogush", "HH"), ("e", "EH"), ("ll", "L"), ("o", "OW")],
        )
        tg = t("hello")
        tg += t("bogus")
        tg += t("you're")
        tg += t("bogus")
        self.assertEqual(tg.input_string, "hellobogusyou'rebogus")
        self.assertEqual(
            tg.edges,
            [
                (0, 0),
                (0, 1),
                (1, 3),
                (1, 4),
                (2, 6),
                (3, 6),
                (4, 8),
                (4, 9),
                (5, 9),
                (6, 9),
                (7, 9),
                (8, 9),
                (9, 9),
                (10, 11),
                (11, 13),
                (11, 14),
                (12, 13),
                (12, 14),
                (13, 15),
                (14, 16),
                (15, 16),
                (16, 16),
                (17, 16),
                (18, 16),
                (19, 16),
                (20, 16),
            ],
        )
        self.assertEqual(
            tg.substring_alignments(),
            [
                ("h", "HH"),
                ("e", "EH"),
                ("ll", "L"),
                ("obogus", "OW"),
                ("y", "Y"),
                ("ou", "UH"),
                ("'", " "),
                ("rebogus", "R"),
            ],
        )

    def test_load_lexicon_mapping(self):
        """Test loading a lexicon mapping through a config file."""
        with self.assertLogs(LOGGER, level="INFO"):
            m = Mapping(
                os.path.join(
                    os.path.dirname(public_data), "mappings", "lexicon_config.yaml"
                )
            )
        self.assertEqual(m.mapping, [])
        self.assertEqual(m.kwargs["type"], "lexicon")
        t = Transducer(m)
        tg = t("hello")
        self.assertEqual(tg.output_string, "HH EH L OW ")
        self.assertEqual(
            tg.edges, [(0, 0), (0, 1), (1, 3), (1, 4), (2, 6), (3, 6), (4, 8), (4, 9)]
        )

    def test_bad_lexicon_mapping(self):
        """Test failure to load alignments."""
        with self.assertRaises(MalformedMapping), self.assertLogs(LOGGER, level="INFO"):
            _ = Mapping(
                os.path.join(
                    os.path.dirname(public_data), "mappings", "bad_lexicon_config.yaml"
                )
            )

    def test_eng_lexicon(self):
        """Test the cached eng to eng-ipa lexicon as a Mapping."""
        m = Mapping(in_lang="eng", out_lang="eng-ipa")
        self.assertEqual(m.kwargs["type"], "lexicon")
        t = Transducer(m)
        tg = t("hello")
        self.assertEqual(tg.output_string, "hʌloʊ")
        self.assertEqual(tg.edges, [(0, 0), (1, 1), (2, 2), (3, 2), (4, 3), (4, 4)])
        tg = t("you're")
        self.assertEqual(tg.output_string, "jʊɹ")
        self.assertEqual(tg.edges, [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
        tg = t("change")
        self.assertEqual(tg.output_string, "tʃeɪndʒ")
        self.assertEqual(tg.input_string, "change")
        self.assertEqual(
            tg.edges,
            [
                (0, 0),
                (0, 1),
                (1, 1),
                (2, 2),
                (2, 3),
                (3, 4),
                (4, 5),
                (4, 6),
                (5, 6),
            ],
        )
        tg = t("chain")
        # These aligments are weird but they are the ones EM gave us
        # (and the ones that our arbitrary assignment of deletions to
        # adjacent outputs gives us, too...)
        self.assertEqual(tg.output_string, "tʃeɪn")
        self.assertEqual(tg.input_string, "chain")
        self.assertEqual(tg.edges, [(0, 0), (0, 1), (1, 1), (2, 2), (3, 3), (4, 4)])
        tg = t("xtra")
        self.assertEqual(tg.output_string, "ɛkstɹʌ")
        self.assertEqual(tg.input_string, "xtra")
        self.assertEqual(tg.edges, [(0, 0), (0, 1), (0, 2), (1, 3), (2, 4), (3, 5)])
        pe = tg.pretty_edges()
        self.assertEqual(
            pe,
            [("x", "ɛ"), ("x", "k"), ("x", "s"), ("t", "t"), ("r", "ɹ"), ("a", "ʌ")],
        )

    def test_eng_transducer(self):
        """Test the cached eng to eng-ipa lexicon from make_g2p
        ."""
        transducer = make_g2p("eng", "eng-arpabet")
        tg = transducer("hello")
        self.assertEqual(tg.output_string, "HH AH L OW ")

        # since we tokenize by default now, this works:
        self.assertEqual(
            transducer("hello my friend").output_string, "HH AH L OW  M AY  F R EH N D "
        )


if __name__ == "__main__":
    main()
