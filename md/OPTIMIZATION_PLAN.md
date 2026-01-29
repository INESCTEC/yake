🎯 PLANO DE OTIMIZAÇÕES PRIORITÁRIAS
=====================================

Baseado no profiling executado, aqui estão as otimizações recomendadas
em ordem de prioridade (impacto vs esforço).

═══════════════════════════════════════════════════════════════════════

## 🥇 PRIORIDADE 1: ComposedWord.__init__ (17% do tempo)

### Problema Identificado
- 10,050 chamadas durante processamento
- 0.043s total (17% do tempo)
- Criação de objetos é cara

### Otimização 1.1: Adicionar __slots__
**Impacto esperado:** 15-25% melhoria
**Dificuldade:** Baixa
**Tempo:** 15 minutos

```python
# yake/data/composed_word.py

class ComposedWord:
    __slots__ = (
        'surface_forms', 'terms', 'term_occur_set', 'tf',
        'cand', 'sentence_ids', 'unique_term', 'stopword_count',
        'max_term_occur', '_cached_hash'
    )
    
    def __init__(self, term_list, surface_forms=None):
        self.surface_forms = surface_forms or []
        self.terms = term_list
        # ... resto do código
```

**Benefícios:**
- ✅ Reduz uso de memória (~40%)
- ✅ Acesso a atributos mais rápido (~10-20%)
- ✅ Sem mudança na API pública

**Atenção:**
- ⚠️ Não permite adicionar atributos dinâmicos
- ⚠️ Precisa listar TODOS os atributos usados

---

### Otimização 1.2: Lazy Evaluation de Propriedades
**Impacto esperado:** 10-15% melhoria
**Dificuldade:** Média
**Tempo:** 30 minutos

```python
class ComposedWord:
    __slots__ = (..., '_cached_surface_form', '_cached_unique_term')
    
    def __init__(self, term_list, surface_forms=None):
        self.terms = term_list
        self.surface_forms = surface_forms or []
        self._cached_surface_form = None
        self._cached_unique_term = None
    
    @property
    def surface_form(self):
        """Calcula apenas quando necessário"""
        if self._cached_surface_form is None:
            self._cached_surface_form = ' '.join(self.terms)
        return self._cached_surface_form
    
    @property
    def unique_term(self):
        """Calcula apenas quando necessário"""
        if self._cached_unique_term is None:
            self._cached_unique_term = '|'.join(sorted(set(self.terms)))
        return self._cached_unique_term
```

**Benefícios:**
- ✅ Evita cálculos desnecessários
- ✅ Cache automático de valores computados
- ✅ Compatível com __slots__

---

### Otimização 1.3: String Interning para Terms Comuns
**Impacto esperado:** 5-10% melhoria memória
**Dificuldade:** Baixa
**Tempo:** 10 minutos

```python
# yake/data/core.py

class DataCore:
    def __init__(self, ...):
        self._term_cache = {}  # Cache de termos
    
    def _intern_term(self, term):
        """Reutiliza strings idênticas"""
        if term not in self._term_cache:
            self._term_cache[term] = term
        return self._term_cache[term]
    
    def _generate_candidates(self, ...):
        # Usar termos internados
        terms = [self._intern_term(t) for t in candidate_terms]
        composed = ComposedWord(terms, ...)
```

**Benefícios:**
- ✅ Reduz duplicação de strings
- ✅ Melhora performance de comparações
- ✅ Menor uso de memória

═══════════════════════════════════════════════════════════════════════

## 🥈 PRIORIDADE 2: get_tag() (15% do tempo)

### Problema Identificado
- 3,600 chamadas
- 0.040s total (15% do tempo)
- Muitas chamadas repetidas para mesmas palavras

### Otimização 2.1: LRU Cache
**Impacto esperado:** 40-60% melhoria nesta função
**Dificuldade:** Muito Baixa
**Tempo:** 5 minutos

```python
# yake/data/utils.py
from functools import lru_cache

@lru_cache(maxsize=10000)
def get_tag(word):
    """
    Cache de tags para palavras já processadas.
    
    Nota: maxsize=10000 é suficiente para a maioria dos textos.
    Para textos muito grandes (>1M palavras), considere aumentar.
    """
    # ... código existente
```

**Benefícios:**
- ✅ MUITO simples - apenas 1 linha!
- ✅ Grande impacto (~10-15% do tempo total)
- ✅ Automatic eviction de entradas antigas

**Alternativa para textos MUITO grandes:**
```python
# Cache customizado com limite de memória
class TagCache:
    def __init__(self, max_size=50000):
        self._cache = {}
        self._max_size = max_size
    
    def get_tag(self, word):
        if word in self._cache:
            return self._cache[word]
        
        tag = _compute_tag(word)  # função original
        
        # Limpar cache se muito grande
        if len(self._cache) >= self._max_size:
            # Remover 20% das entradas mais antigas
            remove_count = self._max_size // 5
            for key in list(self._cache.keys())[:remove_count]:
                del self._cache[key]
        
        self._cache[word] = tag
        return tag
```

---

### Otimização 2.2: Otimizar Regex Patterns
**Impacto esperado:** 5-10% melhoria
**Dificuldade:** Média
**Tempo:** 20 minutos

```python
# yake/data/utils.py

# Pré-compilar patterns (mover para nível de módulo)
ALPHA_PATTERN = re.compile(r'[a-zA-Z]')
DIGIT_PATTERN = re.compile(r'\d')

def get_tag(word):
    # Usar patterns pré-compilados
    has_alpha = bool(ALPHA_PATTERN.search(word))
    has_digit = bool(DIGIT_PATTERN.search(word))
    
    # ... resto do código
```

═══════════════════════════════════════════════════════════════════════

## 🥉 PRIORIDADE 3: add_or_update_composedword (13% do tempo)

### Problema Identificado
- 10,050 chamadas
- 0.034s total (13% do tempo)
- Lookups em dicionário de candidatos

### Otimização 3.1: Usar defaultdict
**Impacto esperado:** 5-10% melhoria
**Dificuldade:** Baixa
**Tempo:** 15 minutos

```python
# yake/data/core.py
from collections import defaultdict

class DataCore:
    def __init__(self, ...):
        # Ao invés de dict normal
        self._candidates = defaultdict(lambda: None)
    
    def add_or_update_composedword(self, composed_word):
        """Versão otimizada"""
        unique_term = composed_word.unique_term
        
        existing = self._candidates.get(unique_term)
        if existing is None:
            self._candidates[unique_term] = composed_word
        else:
            existing.update_cand(composed_word)
```

---

### Otimização 3.2: Batch Updates
**Impacto esperado:** 10-15% melhoria
**Dificuldade:** Média/Alta
**Tempo:** 1 hora

```python
class DataCore:
    def _process_sentence(self, sentence, sentence_id):
        """Processa sentença com batch updates"""
        # Coletar todas as atualizações
        pending_updates = []
        
        for word_data in sentence:
            # ... processar palavra
            candidates = self._generate_candidates(...)
            pending_updates.extend(candidates)
        
        # Aplicar todas de uma vez
        self._batch_update_candidates(pending_updates)
    
    def _batch_update_candidates(self, candidates_list):
        """Atualiza múltiplos candidatos de uma vez"""
        # Agrupar por unique_term
        grouped = defaultdict(list)
        for cand in candidates_list:
            grouped[cand.unique_term].append(cand)
        
        # Aplicar updates agrupados
        for unique_term, cands in grouped.items():
            if unique_term in self._candidates:
                self._candidates[unique_term].merge_batch(cands)
            else:
                self._candidates[unique_term] = cands[0]
                for cand in cands[1:]:
                    self._candidates[unique_term].update_cand(cand)
```

═══════════════════════════════════════════════════════════════════════

## 🎯 PRIORIDADE 4: Tokenização (24% do tempo)

### Problema Identificado
- 24% do tempo em bibliotecas externas (segtok)
- Difícil de otimizar diretamente

### Otimização 4.1: Avaliar Tokenizers Alternativos
**Impacto esperado:** 20-50% melhoria (se trocar)
**Dificuldade:** Alta
**Tempo:** 2-4 horas

```python
# yake/data/utils.py

# Opção 1: spaCy (mais rápido, mas pesado)
def tokenize_sentences_spacy(text, language='en'):
    import spacy
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    doc = nlp(text)
    return [[token.text for token in sent] for sent in doc.sents]

# Opção 2: Stanza (bom compromisso)
def tokenize_sentences_stanza(text, language='en'):
    import stanza
    nlp = stanza.Pipeline(language, processors='tokenize')
    doc = nlp(text)
    return [[token.text for token in sent.tokens] for sent in doc.sentences]

# Opção 3: Regex simples (mais rápido, menos preciso)
def tokenize_sentences_simple(text):
    import re
    # Split por pontuação de fim de sentença
    sentences = re.split(r'[.!?]+', text)
    return [re.findall(r'\b\w+\b', sent) for sent in sentences if sent.strip()]
```

**Recomendação:**
- ⚠️ Trocar tokenizer é arriscado - afeta resultados
- ✅ Criar flag opcional para escolher tokenizer
- ✅ Benchmarkar com cada opção
- ✅ Validar que keywords extraídas são similares

---

### Otimização 4.2: Cache de Tokenização
**Impacto esperado:** Variável (depende de duplicação)
**Dificuldade:** Baixa
**Tempo:** 15 minutos

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def _tokenize_sentence_cached(sentence):
    """Cache para sentenças idênticas"""
    return word_tokenizer(sentence)

def tokenize_sentences(text, language='en'):
    sentences = split_sentences(text)
    return [_tokenize_sentence_cached(s) for s in sentences]
```

═══════════════════════════════════════════════════════════════════════

## 📊 RESUMO E ROADMAP

### Quick Wins (< 30 min, alto impacto)
1. ✅ **@lru_cache em get_tag()** → ~10-15% ganho
2. ✅ **__slots__ em ComposedWord** → ~15-20% ganho
3. ✅ **String interning** → ~5-10% ganho memória

### Ganhos Médios (30-60 min)
4. ✅ **Lazy evaluation** → ~10-15% ganho
5. ✅ **defaultdict para candidatos** → ~5-10% ganho
6. ✅ **Pré-compilar regex** → ~5% ganho

### Projetos Maiores (> 1 hora)
7. ⚠️ **Batch updates** → ~10-15% ganho (complexo)
8. ⚠️ **Tokenizer alternativo** → ~20-50% ganho (arriscado)

### Ganho Total Esperado
- **Quick wins:** ~30-45% melhoria
- **Ganhos médios:** +15-25% adicional
- **Projetos maiores:** +20-50% adicional (se bem sucedidos)
- **TOTAL POTENCIAL:** 50-100% melhoria

═══════════════════════════════════════════════════════════════════════

## 🚀 ORDEM DE IMPLEMENTAÇÃO RECOMENDADA

### Fase 1: Quick Wins (implementar hoje!)
```bash
1. Adicionar @lru_cache a get_tag()
2. Adicionar __slots__ a ComposedWord
3. Implementar string interning básico

# Validar
python benchmark_compare.py
```

### Fase 2: Refinamentos (próxima semana)
```bash
4. Lazy evaluation de propriedades
5. defaultdict para candidatos
6. Pré-compilar regex patterns

# Validar
python benchmark_compare.py
```

### Fase 3: Exploratória (se necessário)
```bash
7. Experimentar tokenizers alternativos
8. Implementar batch updates (se crítico)

# Validar extensivamente
python benchmark_compare.py
python tests/test_yake.py  # garantir mesmos resultados
```

═══════════════════════════════════════════════════════════════════════

## ⚠️ AVISOS IMPORTANTES

### O que NÃO fazer:
❌ Não otimizar `_update_cooccurrence` - apenas 9% e código complexo
❌ Não mexer em `SingleWord.update_h()` - apenas 1.5% do tempo
❌ Não otimizar prematuramente outras funções <5%

### Validação Obrigatória:
✅ Executar benchmark antes e depois
✅ Rodar testes unitários
✅ Comparar keywords extraídas (devem ser idênticas)
✅ Testar com textos de diferentes tamanhos

### Monitoramento:
📊 Use `benchmark_compare.py` após cada otimização
📊 Documente ganhos reais vs esperados
📊 Se ganho < 5%, considere reverter (não vale complexidade)

═══════════════════════════════════════════════════════════════════════

Quer que eu implemente alguma dessas otimizações agora? Recomendo começar
pelas Quick Wins - são simples, seguras e têm alto impacto! 🚀
