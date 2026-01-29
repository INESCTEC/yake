#!/usr/bin/env python
# pylint: skip-file
# Cálculo manual de cobertura YAKE 2.0 (excluindo yake_0.6.0)

# Da saída do pytest --cov:
# yake/__init__.py: 5 stmts, 0 miss
# yake/core/Levenshtein.py: 44 stmts, 4 miss
# yake/core/__init__.py: 0 stmts, 0 miss
# yake/core/highlight.py: 162 stmts, 33 miss
# yake/core/yake.py: 195 stmts, 25 miss
# yake/data/__init__.py: 4 stmts, 0 miss
# yake/data/composed_word.py: 183 stmts, 33 miss
# yake/data/core.py: 176 stmts, 13 miss
# yake/data/single_word.py: 128 stmts, 18 miss
# yake/data/utils.py: 32 stmts, 1 miss

total_stmts = 5 + 44 + 0 + 162 + 195 + 4 + 183 + 176 + 128 + 32
total_miss = 0 + 4 + 0 + 33 + 25 + 0 + 33 + 13 + 18 + 1

coverage = ((total_stmts - total_miss) / total_stmts) * 100

print(f"📊 YAKE 2.0 Coverage (excluindo yake_0.6.0):")
print(f"   Total statements: {total_stmts}")
print(f"   Missed statements: {total_miss}")
print(f"   Coverage: {coverage:.2f}%")
