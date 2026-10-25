#!/usr/bin/env python3
"""Verify a standalone research-platform design package and its canonical seed files.

Usage: cd Docs && python checks/validate_package.py
Static validation only: does NOT execute SQL, parse PlantUML with a renderer, or prove research claims.
"""
from __future__ import annotations
import hashlib
import json
import re
import uuid
from collections import defaultdict, Counter
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {
    'topics.yaml': 20,
    'topic_area_versions.yaml': 20,
    'concepts.yaml': 217,
    'concept_topic_assignments.yaml': 215,
    'concept_relations.yaml': 52,
    'methods.yaml': 12,
    'metrics.yaml': 12,
    'method_concept_links.yaml': 14,
    'concept_metric_links.yaml': 12,
}
UUID_KEYS = {
    'concepts.yaml': 'concept_id', 'concept_relations.yaml': 'relation_id',
    'methods.yaml': 'method_id', 'metrics.yaml': 'metric_id',
    'topic_area_versions.yaml': 'topic_version_id',
    'concept_topic_assignments.yaml': 'assignment_id',
}


def ensure(ok: bool, explanation: str):
    if not ok:
        raise ValueError(explanation)


def is_uuid(value):
    try:
        ensure(isinstance(value, str), 'ID is not a string')
        uuid.UUID(value)
        return True
    except (ValueError, TypeError, AttributeError):
        return False


def load_catalog(root: Path):
    return {name: yaml.safe_load((root / 'catalog' / name).read_text(encoding='utf-8'))
            for name in (*EXPECTED_COUNTS, 'relation_types.yaml')}


def check_catalog(data):
    for name, expected in EXPECTED_COUNTS.items():
        ensure(isinstance(data[name], list) and len(data[name]) == expected,
               f'{name}: expected {expected} entries, got {len(data[name])}')
    for name, key in UUID_KEYS.items():
        ids = [r[key] for r in data[name]]
        ensure(len(ids) == len(set(ids)), f'{name}: duplicate {key}')
        ensure(all(is_uuid(v) for v in ids), f'{name}: invalid UUID {key}')

    topics = data['topics.yaml']
    ensure(all(isinstance(t['area_id'],str) for t in topics), 'area_id must be string')
    topic_ids = {t['area_id'] for t in topics}
    ensure(len(topic_ids) == 20, 'duplicate topic identifiers')
    versions = data['topic_area_versions.yaml']
    v_ids = {v['topic_version_id'] for v in versions}
    ensure(all(v['area_id'] in topic_ids and v['revision_no'] >= 1 for v in versions),
           'topic version references nonexistent topic or invalid revision')
    ensure(len({(v['area_id'], v['revision_no']) for v in versions}) == len(versions),
           'topic revision collision')
    ensure({v['area_id'] for v in versions} == topic_ids, 'missing initial topic versions')

    concepts = data['concepts.yaml']
    c_ids = {c['concept_id'] for c in concepts}
    ensure(Counter(c['kind_code'] for c in concepts).keys() == {'S','M','F','C','R'},
           'concept kind vocabulary mismatch')
    ensure(sum(not c.get('auxiliary', False) for c in concepts) == 215 and
           sum(c.get('auxiliary', False) for c in concepts) == 2,
           'expected 215 primary + 2 auxiliary concepts')
    ensure(all('topic_id' not in c and 'area_id' not in c for c in concepts),
           'CONCEPT cannot hold a duplicated topic membership field')
    assign = data['concept_topic_assignments.yaml']
    ensure(len({(a['concept_id'], a['topic_version_id']) for a in assign}) == len(assign),
           'duplicate concept/topic membership')
    ensure(all(a['concept_id'] in c_ids and a['topic_version_id'] in v_ids for a in assign),
           'orphan concept/topic membership')
    primary_ids = {c['concept_id'] for c in concepts if not c.get('auxiliary', False)}
    ensure({a['concept_id'] for a in assign} == primary_ids,
           'every primary concept needs an initial classification; auxiliary concepts none')

    methods = {m['method_id'] for m in data['methods.yaml']}
    metrics = {m['metric_id'] for m in data['metrics.yaml']}
    types = data['relation_types.yaml']
    ensure(len({t['predicate'] for t in types}) == len(types), 'duplicate predicates')
    typed = {t['predicate']:t for t in types}
    def legal(predicate, subject, obj):
        ensure(predicate in typed, f'unknown predicate {predicate}')
        ensure(subject in typed[predicate]['subject_types'] and
               obj in typed[predicate]['object_types'],
               f'wrong endpoint domain for {predicate}: {subject} → {obj}')

    for r in data['concept_relations.yaml']:
        ensure(r['subject_concept_id'] in c_ids and r['object_concept_id'] in c_ids,
               'orphan concept relation')
        legal(r['predicate'], 'CONCEPT','CONCEPT')
        ensure(r.get('review_status') == 'curated_initial_candidate' and
               r.get('evidence_status') == 'not_yet_individually_verified',
               'seed relation must not masquerade as accepted evidence-backed knowledge')
    for r in data['method_concept_links.yaml']:
        ensure(r['method_id'] in methods and r['concept_id'] in c_ids,
               'orphan method-concept relation')
        legal(r['predicate'], 'METHOD','CONCEPT')
    for r in data['concept_metric_links.yaml']:
        ensure(r['metric_id'] in metrics and r['concept_id'] in c_ids,
               'orphan concept-metric relation')
        legal(r['predicate'], 'CONCEPT','METRIC')


def check_diagrams(text):
    blocks = text.split('@startuml')[1:]
    ensure(len(blocks) == text.count('@enduml') == 10, 'expected 10 balanced PlantUML diagrams')
    ensure('!include' not in text.lower(), 'external PlantUML dependency detected')
    # Same physical entity appears in multiple diagrams. Common fields must not change type.
    by_entity = defaultdict(lambda: defaultdict(set))
    for block in blocks:
        ensure('@enduml' in block, 'missing PlantUML end marker')
        entity_pattern = r'entity\s+"([^"\n]+)"\s+as\s+(\w+)\s*(?:#[0-9A-Fa-f]{6})?\s*\{(.*?)\n\}'
        entities = list(re.finditer(entity_pattern, block, flags=re.S))
        aliases = [m.group(2) for m in entities]
        ensure(len(aliases) == len(set(aliases)), 'duplicate entity alias in PlantUML block')
        for match in entities:
            entity = match.group(1)
            for line in match.group(3).splitlines():
                f = re.search(r'\b([a-z][a-z0-9_]*)\s*:\s*(UUID|TEXT|CHAR\(\d+\)|JSONB|INT|DECIMAL|DATE|TIMESTAMPTZ|BIGINT|BOOLEAN)', line)
                if f:
                    by_entity[entity][f.group(1)].add(f.group(2))
    for entity, fields in by_entity.items():
        for field, types in fields.items():
            ensure(len(types) == 1, f'inconsistent ER type {entity}.{field}: {types}')
    for e, key in {'CLAIM':'claim_id','EVIDENCE':'evidence_id','INTERVENTION':'intervention_id',
                   'METRIC':'metric_id','METHOD':'method_id','CONCEPT':'concept_id'}.items():
        ensure(by_entity[e][key] == {'UUID'}, f'incorrect canonical key type {e}.{key}')
    ensure(by_entity['PAPER_RESULT']['metric_id'] == {'UUID'},
           'PAPER_RESULT.metric_id must use METRIC UUID')
    ensure('METHOD_EFFECT' in by_entity, 'MISSING METHOD_EFFECT typed claim branch')
    ensure('request_hash' in by_entity['EXECUTION_REQUEST'] and
           'request_hash' in by_entity['EXECUTION_APPROVAL'] and
           'request_hash' in by_entity['EXECUTION_DISPATCH'],
           'approval and dispatch must bind to immutable request hash')


def check_links_and_contents(root):
    alltext=[]
    for md in root.rglob('*.md'):
        content=md.read_text(encoding='utf8')
        alltext.append(content)
        for match in re.finditer(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', content):
            url=match.group(1)
            if url.startswith(('http://','https://','#','mailto:')): continue
            ensure((md.parent / url.split('#')[0]).exists(), f'broken link {md}: {url}')
    for f in root.rglob('*'):
        if f.is_file() and f.suffix in ('.puml','.yaml','.json'):
            alltext.append(f.read_text(encoding='utf8'))
    joined='\n'.join(alltext)
    for pattern in (r'\blegacy_code\b', r'CONCEPT_LEGACY_CODE', r'\bC[0-9]{2}-[0-9]{2}\b'):
        ensure(not re.search(pattern, joined, re.I), f'old ID form remains: {pattern}')


def expected_file_hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*')
            if p.is_file()
            and '__pycache__' not in p.parts
            and p.suffix != '.pyc'
            and p.relative_to(root).as_posix() != 'checks/manifest.json'}


def check_manifest(root, manifest):
    expected=expected_file_hashes(root)
    observed={r['path']:r['sha256'] for r in manifest['files']}
    ensure(len(observed)==len(manifest['files']), 'duplicate manifest path')
    ensure(expected==observed, f'checksum/content manifest mismatch: missing={set(expected)-set(observed)} '
              f'extra={set(observed)-set(expected)} changed={set(expected)&set(observed) and [x for x in expected.keys()&observed.keys() if expected[x]!=observed[x]]}')
    ensure(manifest.get('file_count_excluding_manifest')==len(expected), 'manifest file count mismatch')


def validate(root=ROOT, include_manifest=True):
    ensure(root.name.lower() == 'docs', 'all files must be under the docs/ directory')
    ensure(not (root/'docs').exists(), 'deprecated nested docs/ directory found')
    expected_sections={'design','ontology','experiments','contracts','references','catalog','diagrams','examples','checks'}
    ensure(expected_sections <= {p.name for p in root.iterdir() if p.is_dir()},
           'missing one or more Docs/ sections')
    check_catalog(load_catalog(root))
    check_diagrams((root/'diagrams'/'knowledge_research_er.puml').read_text(encoding='utf8'))
    check_links_and_contents(root)
    if include_manifest:
        check_manifest(root, json.loads((root/'checks'/'manifest.json').read_text(encoding='utf8')))
    return True


if __name__=='__main__':
    validate()
    print('OK: 20 areas/versions, 217 concepts, 215 memberships, 52 relation candidates, 12 methods/metrics, 10 consistent diagrams, checked package hashes')
