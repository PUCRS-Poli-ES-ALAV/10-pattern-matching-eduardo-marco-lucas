import random
import string
import time
import pandas as pd

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

# ---------------- ALGORITMO INGÊNUO ----------------
def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    comparisons = 0
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            return i, i + 1, comparisons, (i + 1) * m
    return -1, n - m + 1, comparisons, (n - m + 1) * m

# ---------------- RABIN-KARP ----------------
def hash_horner(s, M, R, Q):
    h = 0
    for j in range(M):
        h = (h * R + ord(s[j])) % Q
    return h

def rabin_karp_no_rolling(text, pattern, R=256, Q=9973):
    m, n = len(pattern), len(text)
    pattern_hash = hash_horner(pattern, m, R, Q)
    comparisons = 0
    for i in range(n - m + 1):
        text_hash = hash_horner(text[i:i + m], m, R, Q)
        comparisons += 1
        if text_hash == pattern_hash:
            return i, i + 1, comparisons, (i + 1) * m
    return -1, n - m + 1, comparisons, (n - m + 1) * m

def rabin_karp_rolling(text, pattern, R=256, Q=9973):
    m, n = len(pattern), len(text)
    pattern_hash = hash_horner(pattern, m, R, Q)
    text_hash = hash_horner(text[:m], m, R, Q)
    RM = pow(R, m - 1, Q)
    comparisons = 1
    if text_hash == pattern_hash:
        return 0, 1, comparisons, m
    for i in range(1, n - m + 1):
        text_hash = (text_hash + Q - RM * ord(text[i - 1]) % Q) % Q
        text_hash = (text_hash * R + ord(text[i + m - 1])) % Q
        comparisons += 1
        if text_hash == pattern_hash:
            return i, i + 1, comparisons, (i + 1) * 2
    return -1, n - m + 1, comparisons, (n - m + 1) * 2

# ---------------- KMP ----------------
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    m, n = len(pattern), len(text)
    lps = compute_lps(pattern)
    i = j = 0
    comparisons = 0
    instructions = 0
    while i < n:
        comparisons += 1
        instructions += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j, i, comparisons, instructions
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1, i, comparisons, instructions

def testar_algoritmo(nome, funcao, texto, padrao):
    inicio = time.time()
    indice, iteracoes, comparacoes, instrucoes = funcao(texto, padrao)
    fim = time.time()
    return [nome, len(texto), len(padrao), indice, iteracoes, f"{comparacoes:,}", instrucoes, round(fim - inicio, 6)]

# Casos de teste
texto_pequeno = "ABCDCBDCBDACBDABDCBADF"
padrao_pequeno = "ADF"
texto_grande = generate_random_string(600_000)
padrao_grande = texto_grande[599_900:600_000]  # garante match no final

resultados = []

resultados.append(testar_algoritmo("Naive", naive_search, texto_pequeno, padrao_pequeno))
resultados.append(testar_algoritmo("Rabin–Karp (sem rolling hash)", rabin_karp_no_rolling, texto_pequeno, padrao_pequeno))
resultados.append(testar_algoritmo("Rabin–Karp (com rolling hash)", rabin_karp_rolling, texto_pequeno, padrao_pequeno))
resultados.append(testar_algoritmo("KMP", kmp_search, texto_pequeno, padrao_pequeno))

resultados.append(testar_algoritmo("Naive", naive_search, texto_grande, padrao_grande))
resultados.append(testar_algoritmo("Rabin–Karp (sem rolling hash)", rabin_karp_no_rolling, texto_grande, padrao_grande))
resultados.append(testar_algoritmo("Rabin–Karp (com rolling hash)", rabin_karp_rolling, texto_grande, padrao_grande))
resultados.append(testar_algoritmo("KMP", kmp_search, texto_grande, padrao_grande))

df = pd.DataFrame(resultados, columns=["ALGORITMO", "TEXTO", "PADRÃO", "ÍNDICE", "ITERAÇÕES", "COMPARAÇÕES", "INSTRUÇÕES", "TEMPO (s)"])

df.insert(1, "TAMANHO", ["Pequeno"] * 4 + ["Grande"]*4)

print(df)