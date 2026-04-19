# ERRORS.md — VulnAI Runtime Error Log

<!-- RUNTIME LOG START -->

---

### [2026-04-19T08:56:06.884386+00:00] CeleryTaskError in apps.scans.tasks

**Message:** Agent crashed

**Context:**
  scan_id: c8b98a6a-de10-4c7f-b518-69fca1458133

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/scans/tasks.py", line 14, in run_scan_task
    agent.run_scan()
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1093, in __call__
    return self._mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1097, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1152, in _execute_mock_call
    raise effect
Exception: Agent crashed

```

**Status:** open

---

### [2026-04-19T08:56:21.463941+00:00] CeleryTaskError in apps.scans.tasks

**Message:** Agent crashed

**Context:**
  scan_id: 25eaffb7-57d9-41b9-afc3-08befb1e1235

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/scans/tasks.py", line 14, in run_scan_task
    agent.run_scan()
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1093, in __call__
    return self._mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1097, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1152, in _execute_mock_call
    raise effect
Exception: Agent crashed

```

**Status:** open

---

### [2026-04-19T08:56:37.175865+00:00] CeleryTaskError in apps.scans.tasks

**Message:** Agent crashed

**Context:**
  scan_id: f6165334-2569-43ca-bc5c-73942d0aa569

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/scans/tasks.py", line 14, in run_scan_task
    agent.run_scan()
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1093, in __call__
    return self._mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1097, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1152, in _execute_mock_call
    raise effect
Exception: Agent crashed

```

**Status:** open

---

### [2026-04-19T08:56:38.664061+00:00] ReportGenerationError in apps.reports.generator

**Message:** ['“non-existent-id” is not a valid UUID.']

**Context:**
  scan_id: non-existent-id

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2688, in to_python
    return uuid.UUID(**{input_form: value})
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/uuid.py", line 177, in __init__
    raise ValueError('badly formed hexadecimal UUID string')
ValueError: badly formed hexadecimal UUID string

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 12, in generate_report
    scan = Scan.objects.get(id=scan_id)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 623, in get
    clone = self._chain() if self.query.combinator else self.filter(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1436, in filter
    return self._filter_or_exclude(False, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1454, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1461, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1546, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1577, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1492, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1319, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 27, in __init__
    self.rhs = self.get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 341, in get_prep_lookup
    return super().get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 85, in get_prep_lookup
    return self.lhs.output_field.get_prep_value(self.rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2672, in get_prep_value
    return self.to_python(value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2690, in to_python
    raise exceptions.ValidationError(
django.core.exceptions.ValidationError: ['“non-existent-id” is not a valid UUID.']

```

**Status:** open

---

### [2026-04-19T08:56:38.671950+00:00] ReportGenerationError in apps.reports.generator

**Message:** 'Finding' object has no attribute 'get'

**Context:**
  scan_id: 766603f3-a884-40b7-8ca1-7f04fd373b10

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 16, in generate_report
    risk_score = calculate_risk_score(findings)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/utils/cvss_scorer.py", line 23, in calculate_risk_score
    cvss_score = getattr(finding, 'cvss_score', None) or finding.get('cvss_score')
AttributeError: 'Finding' object has no attribute 'get'

```

**Status:** open

---

### [2026-04-19T08:57:00.126845+00:00] CeleryTaskError in apps.scans.tasks

**Message:** Agent crashed

**Context:**
  scan_id: 987ab6b0-950a-49b4-bf00-d9071609b799

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/scans/tasks.py", line 14, in run_scan_task
    agent.run_scan()
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1093, in __call__
    return self._mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1097, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1152, in _execute_mock_call
    raise effect
Exception: Agent crashed

```

**Status:** open

---

### [2026-04-19T08:57:01.597277+00:00] ReportGenerationError in apps.reports.generator

**Message:** ['“non-existent-id” is not a valid UUID.']

**Context:**
  scan_id: non-existent-id

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2688, in to_python
    return uuid.UUID(**{input_form: value})
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/uuid.py", line 177, in __init__
    raise ValueError('badly formed hexadecimal UUID string')
ValueError: badly formed hexadecimal UUID string

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 12, in generate_report
    scan = Scan.objects.get(id=scan_id)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 623, in get
    clone = self._chain() if self.query.combinator else self.filter(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1436, in filter
    return self._filter_or_exclude(False, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1454, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1461, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1546, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1577, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1492, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1319, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 27, in __init__
    self.rhs = self.get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 341, in get_prep_lookup
    return super().get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 85, in get_prep_lookup
    return self.lhs.output_field.get_prep_value(self.rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2672, in get_prep_value
    return self.to_python(value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2690, in to_python
    raise exceptions.ValidationError(
django.core.exceptions.ValidationError: ['“non-existent-id” is not a valid UUID.']

```

**Status:** open

---

### [2026-04-19T08:57:01.603909+00:00] ReportGenerationError in apps.reports.generator

**Message:** 'Finding' object has no attribute 'get'

**Context:**
  scan_id: d21201e5-6978-41ba-9536-b34d5737fc79

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 16, in generate_report
    risk_score = calculate_risk_score(findings)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/utils/cvss_scorer.py", line 23, in calculate_risk_score
    cvss_score = getattr(finding, 'cvss_score', None) or finding.get('cvss_score')
AttributeError: 'Finding' object has no attribute 'get'

```

**Status:** open

---

### [2026-04-19T08:57:23.343887+00:00] ReportGenerationError in apps.reports.generator

**Message:** ['“non-existent-id” is not a valid UUID.']

**Context:**
  scan_id: non-existent-id

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2688, in to_python
    return uuid.UUID(**{input_form: value})
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/uuid.py", line 177, in __init__
    raise ValueError('badly formed hexadecimal UUID string')
ValueError: badly formed hexadecimal UUID string

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 12, in generate_report
    scan = Scan.objects.get(id=scan_id)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 623, in get
    clone = self._chain() if self.query.combinator else self.filter(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1436, in filter
    return self._filter_or_exclude(False, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1454, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1461, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1546, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1577, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1492, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1319, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 27, in __init__
    self.rhs = self.get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 341, in get_prep_lookup
    return super().get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 85, in get_prep_lookup
    return self.lhs.output_field.get_prep_value(self.rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2672, in get_prep_value
    return self.to_python(value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2690, in to_python
    raise exceptions.ValidationError(
django.core.exceptions.ValidationError: ['“non-existent-id” is not a valid UUID.']

```

**Status:** open

---

### [2026-04-19T08:57:23.350349+00:00] ReportGenerationError in apps.reports.generator

**Message:** 'Finding' object has no attribute 'get'

**Context:**
  scan_id: c6a5547b-edf2-4928-a1ed-2b10df22b62b

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 16, in generate_report
    risk_score = calculate_risk_score(findings)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/utils/cvss_scorer.py", line 23, in calculate_risk_score
    cvss_score = getattr(finding, 'cvss_score', None) or finding.get('cvss_score')
AttributeError: 'Finding' object has no attribute 'get'

```

**Status:** open

---

### [2026-04-19T08:57:40.578089+00:00] ReportGenerationError in apps.reports.generator

**Message:** ['“non-existent-id” is not a valid UUID.']

**Context:**
  scan_id: non-existent-id

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2688, in to_python
    return uuid.UUID(**{input_form: value})
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/uuid.py", line 177, in __init__
    raise ValueError('badly formed hexadecimal UUID string')
ValueError: badly formed hexadecimal UUID string

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 12, in generate_report
    scan = Scan.objects.get(id=scan_id)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 623, in get
    clone = self._chain() if self.query.combinator else self.filter(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1436, in filter
    return self._filter_or_exclude(False, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1454, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1461, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1546, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1577, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1492, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1319, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 27, in __init__
    self.rhs = self.get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 341, in get_prep_lookup
    return super().get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 85, in get_prep_lookup
    return self.lhs.output_field.get_prep_value(self.rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2672, in get_prep_value
    return self.to_python(value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2690, in to_python
    raise exceptions.ValidationError(
django.core.exceptions.ValidationError: ['“non-existent-id” is not a valid UUID.']

```

**Status:** open

---

### [2026-04-19T08:57:40.584214+00:00] ReportGenerationError in apps.reports.generator

**Message:** 'Finding' object has no attribute 'get'

**Context:**
  scan_id: 76309992-b4ad-4481-beb7-1d047df88e4e

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 16, in generate_report
    risk_score = calculate_risk_score(findings)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/utils/cvss_scorer.py", line 45, in calculate_risk_score
    v = getattr(f, 'cvss_score', None) or f.get('cvss_score')
AttributeError: 'Finding' object has no attribute 'get'

```

**Status:** open

---

### [2026-04-19T08:57:55.002312+00:00] ReportGenerationError in apps.reports.generator

**Message:** ['“non-existent-id” is not a valid UUID.']

**Context:**
  scan_id: non-existent-id

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2688, in to_python
    return uuid.UUID(**{input_form: value})
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/uuid.py", line 177, in __init__
    raise ValueError('badly formed hexadecimal UUID string')
ValueError: badly formed hexadecimal UUID string

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/reports/generator.py", line 12, in generate_report
    scan = Scan.objects.get(id=scan_id)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 623, in get
    clone = self._chain() if self.query.combinator else self.filter(*args, **kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1436, in filter
    return self._filter_or_exclude(False, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1454, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1461, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1546, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1577, in _add_q
    child_clause, needed_inner = self.build_filter(
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1492, in build_filter
    condition = self.build_lookup(lookups, col, value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/sql/query.py", line 1319, in build_lookup
    lookup = lookup_class(lhs, rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 27, in __init__
    self.rhs = self.get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 341, in get_prep_lookup
    return super().get_prep_lookup()
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/lookups.py", line 85, in get_prep_lookup
    return self.lhs.output_field.get_prep_value(self.rhs)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2672, in get_prep_value
    return self.to_python(value)
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/.venv/lib/python3.9/site-packages/django/db/models/fields/__init__.py", line 2690, in to_python
    raise exceptions.ValidationError(
django.core.exceptions.ValidationError: ['“non-existent-id” is not a valid UUID.']

```

**Status:** open

---

### [2026-04-19T08:57:55.953697+00:00] CeleryTaskError in apps.scans.tasks

**Message:** Agent crashed

**Context:**
  scan_id: 7763b105-a477-4720-983a-8a6458894186

**Traceback:**
```
Traceback (most recent call last):
  File "/Users/armankatia/Documents/DeepVulFinder/vulnai/apps/scans/tasks.py", line 14, in run_scan_task
    agent.run_scan()
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1093, in __call__
    return self._mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1097, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/unittest/mock.py", line 1152, in _execute_mock_call
    raise effect
Exception: Agent crashed

```

**Status:** open
