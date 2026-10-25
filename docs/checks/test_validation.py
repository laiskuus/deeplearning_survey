"""Small negative tests for the package's structural validation rules (no database required)."""
import copy
import json
import unittest
from pathlib import Path
from validate_package import (ROOT, check_catalog, check_diagrams,
                              check_manifest, load_catalog)


class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=load_catalog(ROOT)
        cls.puml=(ROOT/'diagrams'/'knowledge_research_er.puml').read_text(encoding='utf8')

    def assert_catalog_bad(self, change):
        data=copy.deepcopy(self.base)
        change(data)
        with self.assertRaises(ValueError):check_catalog(data)

    def test_catalog_good(self):
        check_catalog(self.base)

    def test_missing_membership(self):
        self.assert_catalog_bad(lambda d: d['concept_topic_assignments.yaml'].pop())

    def test_topic_membership_duplicated_in_concept(self):
        self.assert_catalog_bad(lambda d: d['concepts.yaml'][0].update(topic_id='01'))

    def test_unknown_relation_endpoint(self):
        self.assert_catalog_bad(lambda d:d['concept_relations.yaml'][0].update(subject_concept_id=str(__import__('uuid').uuid4())))

    def test_wrong_predicate_domain(self):
        self.assert_catalog_bad(lambda d:d['method_concept_links.yaml'][0].update(predicate='is_a'))

    def test_duplicate_concept_id(self):
        self.assert_catalog_bad(lambda d:d['concepts.yaml'][1].update(concept_id=d['concepts.yaml'][0]['concept_id']))

    def test_diagrams_good(self):
        check_diagrams(self.puml)

    def test_diagrams_detect_inconsistent_id(self):
        broken=self.puml.replace(' * claim_id : UUID <<PK>>',' * claim_id : TEXT <<PK>>', 1)
        with self.assertRaises(ValueError):check_diagrams(broken)

    def test_manifest_detects_tampered_checksum(self):
        data=json.loads((ROOT/'checks'/'manifest.json').read_text())
        data['files'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):check_manifest(ROOT,data)


if __name__=='__main__': unittest.main(verbosity=2)
