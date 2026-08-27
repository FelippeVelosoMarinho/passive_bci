import json


def src(code: str) -> list[str]:
    lines = code.strip("\n").splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


DEFAULT_SEARCH_QUERY = (
    '("passive BCI" OR "passive brain-computer" OR pBCI OR "implicit BCI") '
    'AND (biomarker OR "spectral" OR "engagement index" OR "EEG feature" OR "quantitative") '
    'AND (validation OR reliability OR validity OR "cross-validation") '
    'AND (education OR learning OR pedagog OR classroom OR rehabilitation OR psychology OR "human-computer")'
)

CELL_SYNTHESIS = src(
    r"""
def _labels(text, patterns: dict[str, str]) -> list[str]:
    found = []
    for label, pattern in patterns.items():
        if re.search(pattern, text):
            found.append(label)
    return found


def extract_synthesis_variables(text):
    text = str(text).lower()

    channels = [
        ch.upper()
        for ch in ["fp1", "fp2", "af3", "af4", "f3", "f4", "cz", "p3", "p4", "o1", "o2"]
        if re.search(rf"\b{ch}\b", text)
    ]

    biomarker_patterns = {
        "Razão Beta/Alfa (β/α)": r"beta[\s/-]?alpha|β/α|beta-alpha",
        "Potência Teta": r"\btheta power\b|\btheta band\b",
        "Índice de Engajamento": r"engagement index",
        "Potência Espectral": r"spectral power|power spectral|psd",
        "Conectividade/Coerência": r"connectivity|coherence|plv|pli",
        "Entropia/Complexidade": r"entropy|complexity|hjorth",
        "Assimetria Frontal": r"frontal asymmetry|faa",
    }
    biomarkers = _labels(text, biomarker_patterns)

    construction = _labels(text, {
        "Normalização/Baseline": r"baseline|normaliz|z-score|standardiz",
        "Janela temporal/sliding": r"sliding window|time window|epoch",
        "Feature engineering": r"feature extraction|feature engineering|handcraft",
        "Índice composto": r"composite index|combined index|ratio",
    })

    validation = _labels(text, {
        "Cross-validation": r"cross-validation|k-fold|leave-one-out",
        "Test-retest/Confiabilidade": r"test-retest|reliability|icc|intraclass",
        "AUC/ROC": r"\bauc\b|roc curve|receiver operating",
        "Correlação/Ground truth": r"correlation|ground truth|criterion validity|concurrent validity",
        "Estudo ecológico": r"ecological validity|in the wild|real-world|classroom study",
    })

    ground_truth = _labels(text, {
        "Desempenho/Task": r"task performance|accuracy|response time|reaction time",
        "Autorrelato/Questionário": r"questionnaire|self-report|nasa-tlx|panas",
        "Observação/Expert": r"observ|expert rating|teacher rating",
        "Aprendizagem/Outcome": r"learning outcome|test score|grade|retention",
        "Clínico/FUNCIONAL": r"clinical scale|functional outcome|fugl-meyer|motor recovery",
    })

    domain_patterns = {
        "Pedagogia": r"education|learning|pedagog|classroom|student|school|tutor|instruction|mooc|e-learning",
        "Reabilitação": r"rehabilitation|therapy|stroke|motor recovery|clinical trial|patient",
        "Psicologia": r"psycholog|cognitive state|emotion|motivation|attention|flow state",
        "IHC/Adaptação": r"human-computer|interface|adaptive system|user interface|feedback loop|usability",
        "Neuroergonomia": r"neuroergonomic|operator|pilot|workload|atc|driving",
    }
    domains = _labels(text, domain_patterns)

    pedagogy_app = _labels(text, {
        "Feedback adaptativo": r"adaptive feedback|personalized feedback|real-time feedback",
        "Tutoria/Sistema inteligente": r"intelligent tutoring|its\b|tutoring system",
        "Serious game/Ambiente virtual": r"serious game|virtual learning|simulation-based learning",
        "Monitoramento em aula": r"in-class|during lecture|online lecture|remote learning",
    })

    hci = _labels(text, {
        "Loop fechado": r"closed-loop|closed loop",
        "Calibração individual": r"calibration|personalized model|subject-specific",
        "Interpretabilidade": r"interpretab|explainab|transparen",
        "Carga cognitiva da interface": r"extraneous load|interface design|cognitive load theory",
    })

    transfer = []
    if domains.count("Pedagogia") and domains.count("Reabilitação"):
        transfer.append("Pedagogia + Reabilitação no mesmo estudo")
    if re.search(r"transfer|generaliz|cross-domain|cross domain", text):
        transfer.append("Menção explícita de transferência/generalização")
    if re.search(r"rehabilitation", text) and re.search(r"education|learning|classroom", text):
        transfer.append("Ponte reabilitação → educação")

    return pd.Series([
        ", ".join(channels) if channels else "Não especificado",
        ", ".join(biomarkers) if biomarkers else "Não especificado",
        ", ".join(construction) if construction else "Não detalhado no resumo",
        ", ".join(validation) if validation else "Não detalhado no resumo",
        ", ".join(ground_truth) if ground_truth else "Não especificado",
        ", ".join(domains) if domains else "Não especificado",
        ", ".join(pedagogy_app) if pedagogy_app else "Não aplicável / não mencionado",
        ", ".join(hci) if hci else "Não mencionado",
        ", ".join(transfer) if transfer else "Sem evidência no resumo",
    ])


SYNTHESIS_COLUMNS = [
    "Canais_EEG",
    "Biomarcador_Quantitativo",
    "Construcao_Biomarcador",
    "Validacao",
    "Ground_Truth",
    "Dominio_Aplicacao",
    "Aplicacao_Pedagogica",
    "Aspectos_IHC",
    "Transferibilidade",
]

if "Status_Triagem" in df_screen.columns and not df_screen.empty:
    df_included = df_screen[df_screen["Status_Triagem"] == "INCLUÍDO (Pré-seleção)"].copy()
else:
    df_included = df_screen.iloc[0:0].copy()

if not df_included.empty:
    df_included[SYNTHESIS_COLUMNS] = df_included.apply(
        lambda r: extract_synthesis_variables(f"{r['title']} {r['abstract']}"), axis=1
    )
    df_included = df_included.sort_values(
        by=["Prioridade_Pedagogia", "Score"],
        ascending=[True, False],
        key=lambda s: s.map({"Alta": 0, "Média": 1, "Baixa": 2, "—": 3}) if s.name == "Prioridade_Pedagogia" else s,
    )
    df_included.to_excel("Matriz_Mapeamento_PRISMA.xlsx", index=False)
    print("Arquivo 'Matriz_Mapeamento_PRISMA.xlsx' gerado com sucesso!")
    print("\n--- PRIORIDADE PEDAGÓGICA (pré-incluídos) ---")
    print(df_included["Prioridade_Pedagogia"].value_counts())

print("\n--- FLUXOGRAMA PRISMA-ScR (DADOS) ---")
print(f"Identificados: {len(df_raw)}")
print(f"Duplicatas Removidas: {len(df_raw) - len(df_screen)}")
print(f"Triados por Título/Resumo: {len(df_screen)}")
print(f"Excluídos: {len(df_screen) - len(df_included)}")
print(f"Incluídos para Leitura Completa: {len(df_included)}")
"""
)

notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Revisão sistemática: Passive BCI e biomarcadores quantitativos\n",
                "\n",
                "**Escopo:** uso de *passive BCI* na **construção e validação** de biomarcadores EEG quantitativos, "
                "com ênfase em **pedagogia** e transferência a partir de experiências em **reabilitação**, "
                "incluindo aspectos de **IHC** (feedback adaptativo, calibração, interpretabilidade).\n",
                "\n",
                "Fluxo: busca (OpenAlex + PubMed) → deduplicação → triagem (PCC alinhado ao escopo) → "
                "matriz de síntese PRISMA-ScR.\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["### Célula 1: Dependências e configuração\n"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": src(
                f"""
# Dependências: source .venv/bin/activate && pip install -r requirements.txt
# Kernel: Python (passive_bci)

import os
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests
from dotenv import load_dotenv
from pyzotero import zotero
from rapidfuzz import fuzz

load_dotenv(Path.cwd() / ".env")

ZOTERO_USER_ID = os.getenv("ZOTERO_USER_ID", "").strip()
ZOTERO_API_KEY = os.getenv("ZOTERO_API_KEY", "").strip()
ZOTERO_LIBRARY_TYPE = os.getenv("ZOTERO_LIBRARY_TYPE", "user").strip() or "user"
COLLECTION_KEY = os.getenv("COLLECTION_KEY", "").strip()

SEARCH_QUERY = os.getenv(
    "SEARCH_QUERY",
    {DEFAULT_SEARCH_QUERY!r},
).strip()
SEARCH_LIMIT = int(os.getenv("SEARCH_LIMIT", "80"))
SEARCH_SOURCES = [
    s.strip().lower()
    for s in os.getenv("SEARCH_SOURCES", "openalex,pubmed").split(",")
    if s.strip()
]
PUSH_TO_ZOTERO = os.getenv("PUSH_TO_ZOTERO", "true").strip().lower() in {{"1", "true", "yes"}}
SCREENING_MIN_SCORE = int(os.getenv("SCREENING_MIN_SCORE", "5"))
OPENALEX_MAILTO = os.getenv("OPENALEX_MAILTO", "passive_bci@local.dev").strip()
NCBI_EMAIL = os.getenv("NCBI_EMAIL", OPENALEX_MAILTO).strip()
HTTP_TIMEOUT = 45

print("Ambiente configurado.")
print(f"Query: {{SEARCH_QUERY}}")
print(f"Fontes: {{SEARCH_SOURCES}} | limite={{SEARCH_LIMIT}} | score mínimo={{SCREENING_MIN_SCORE}}")
"""
            ),
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Célula 2: Busca automatizada (OpenAlex + PubMed)\n",
                "> Query orientada a: passive BCI + biomarcador quantitativo + validação + "
                "(pedagogia | reabilitação | psicologia | IHC).\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": src(
                r"""
def _clean_doi(doi: str) -> str:
    doi = (doi or "").strip()
    if doi.lower().startswith("https://doi.org/"):
        doi = doi.split("doi.org/", 1)[-1]
    return doi.strip()


def search_openalex(query: str, limit: int) -> list[dict]:
    records = []
    per_page = min(50, limit)
    cursor = "*"
    headers = {"User-Agent": f"passive_bci/1.0 (mailto:{OPENALEX_MAILTO})"}

    while len(records) < limit:
        url = (
            "https://api.openalex.org/works"
            f"?search={quote(query)}"
            f"&per_page={per_page}"
            f"&cursor={quote(cursor)}"
            f"&mailto={quote(OPENALEX_MAILTO)}"
        )
        resp = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
        for work in payload.get("results", []):
            doi = _clean_doi(work.get("doi") or "")
            abstract = ""
            inv = work.get("abstract_inverted_index") or {}
            if inv:
                positions = []
                for word, idxs in inv.items():
                    for i in idxs:
                        positions.append((i, word))
                abstract = " ".join(w for _, w in sorted(positions))

            year = work.get("publication_year")
            primary = work.get("primary_location") or {}
            records.append({
                "key": f"oa:{work.get('id', '').rsplit('/', 1)[-1]}",
                "title": work.get("display_name") or "",
                "abstract": abstract,
                "publicationYear": str(year) if year else "",
                "doi": doi,
                "itemType": "journalArticle",
                "url": primary.get("landing_page_url")
                or (f"https://doi.org/{doi}" if doi else work.get("id", "")),
                "source": "openalex",
            })
            if len(records) >= limit:
                break

        cursor = (payload.get("meta") or {}).get("next_cursor")
        if not cursor:
            break
        time.sleep(0.2)

    return records[:limit]


def search_pubmed(query: str, limit: int) -> list[dict]:
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = (
        f"{base}/esearch.fcgi?db=pubmed&retmode=json"
        f"&retmax={limit}&term={quote(query)}&email={quote(NCBI_EMAIL)}"
    )
    search = requests.get(search_url, timeout=HTTP_TIMEOUT)
    search.raise_for_status()
    ids = (search.json().get("esearchresult") or {}).get("idlist") or []
    if not ids:
        return []

    fetch_url = (
        f"{base}/efetch.fcgi?db=pubmed&retmode=xml"
        f"&id={','.join(ids)}&email={quote(NCBI_EMAIL)}"
    )
    fetch = requests.get(fetch_url, timeout=HTTP_TIMEOUT)
    fetch.raise_for_status()
    root = ET.fromstring(fetch.text)

    records = []
    for article in root.findall(".//PubmedArticle"):
        medline = article.find("MedlineCitation")
        pmid = (medline.findtext("PMID") or "").strip() if medline is not None else ""
        art = medline.find("Article") if medline is not None else None
        title = (art.findtext("ArticleTitle") or "") if art is not None else ""

        abstract_nodes = art.findall(".//AbstractText") if art is not None else []
        abstract_parts = []
        for node in abstract_nodes:
            label = node.attrib.get("Label")
            text = "".join(node.itertext()).strip()
            abstract_parts.append(f"{label}: {text}" if label else text)
        abstract = " ".join(abstract_parts)

        year = ""
        if art is not None:
            year = (
                art.findtext("Journal/JournalIssue/PubDate/Year")
                or (art.findtext("Journal/JournalIssue/PubDate/MedlineDate") or "")[:4]
            )

        doi = ""
        for idn in article.findall(".//ArticleId"):
            if idn.attrib.get("IdType") == "doi":
                doi = _clean_doi(idn.text or "")
                break

        records.append({
            "key": f"pmid:{pmid}",
            "title": title,
            "abstract": abstract,
            "publicationYear": year,
            "doi": doi,
            "itemType": "journalArticle",
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
            "source": "pubmed",
        })

    return records


all_records = []
for src_name in SEARCH_SOURCES:
    try:
        if src_name == "openalex":
            found = search_openalex(SEARCH_QUERY, SEARCH_LIMIT)
        elif src_name == "pubmed":
            found = search_pubmed(SEARCH_QUERY, SEARCH_LIMIT)
        else:
            print(f"Fonte ignorada: {src_name}")
            continue
        print(f"{src_name}: {len(found)} resultados")
        all_records.extend(found)
    except Exception as e:
        print(f"Falha em {src_name}: {e}")

df_search = pd.DataFrame(all_records)
if df_search.empty:
    df_search = pd.DataFrame(
        columns=["key", "title", "abstract", "publicationYear", "doi", "itemType", "url", "source"]
    )
print(f"Total bruto das buscas: {len(df_search)}")
df_search.head(3)
"""
            ),
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Célula 3: Corpus (`df_raw`) e envio opcional ao Zotero\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": src(
                """
def push_search_to_zotero(df: pd.DataFrame) -> int:
    if df.empty or not ZOTERO_USER_ID or not ZOTERO_API_KEY:
        return 0

    zot = zotero.Zotero(ZOTERO_USER_ID, ZOTERO_LIBRARY_TYPE, ZOTERO_API_KEY)
    created = 0
    payload = []

    for _, row in df.iterrows():
        payload.append({
            "itemType": "journalArticle",
            "title": str(row.get("title") or "")[:1000],
            "abstractNote": str(row.get("abstract") or "")[:10000],
            "DOI": str(row.get("doi") or ""),
            "url": str(row.get("url") or ""),
            "date": str(row.get("publicationYear") or ""),
            "collections": [COLLECTION_KEY] if COLLECTION_KEY else [],
            "tags": [
                {"tag": "passive_bci_biomarker_review"},
                {"tag": str(row.get("source") or "search")},
            ],
        })
        if len(payload) == 50:
            zot.create_items(payload)
            created += len(payload)
            payload = []
            time.sleep(0.3)

    if payload:
        zot.create_items(payload)
        created += len(payload)
    return created


df_raw = df_search.copy()

if PUSH_TO_ZOTERO and not df_raw.empty:
    try:
        n = push_search_to_zotero(df_raw)
        print(f"Zotero: {n} itens enviados.")
    except Exception as e:
        print(f"Zotero push falhou ({e}). Triagem segue com df_search.")

print(f"Total em df_raw: {len(df_raw)}")
"""
            ),
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["### Célula 4: Deduplicação (DOI + fuzzy matching)\n"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": src(
                """
def deduplicate_records(df):
    initial_count = len(df)
    if initial_count == 0:
        print("Nada para deduplicar.")
        return df.copy()

    df = df.copy()
    df["doi_clean"] = df["doi"].fillna("").astype(str).str.lower().str.strip()
    df_dedup = pd.concat([
        df[df["doi_clean"] == ""],
        df[df["doi_clean"] != ""].drop_duplicates(subset=["doi_clean"], keep="first"),
    ], ignore_index=False)

    indices_to_drop = set()
    titles = df_dedup["title"].fillna("").tolist()
    idx_list = df_dedup.index.tolist()

    for i in range(len(titles)):
        if idx_list[i] in indices_to_drop or not titles[i]:
            continue
        for j in range(i + 1, len(titles)):
            if idx_list[j] in indices_to_drop or not titles[j]:
                continue
            if fuzz.ratio(titles[i].lower(), titles[j].lower()) >= 90:
                indices_to_drop.add(idx_list[j])

    df_dedup = df_dedup.drop(index=list(indices_to_drop)).drop(columns=["doi_clean"])
    print(f"Registros brutos: {initial_count}")
    print(f"Duplicatas removidas: {initial_count - len(df_dedup)}")
    print(f"Únicos: {len(df_dedup)}")
    return df_dedup.reset_index(drop=True)


df_screen = deduplicate_records(df_raw)
"""
            ),
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Célula 5: Triagem alinhada ao escopo da revisão\n",
                "\n",
                "**Critérios mínimos (título/resumo):**\n",
                "1. Passive BCI (ou equivalente implícito)\n",
                "2. Biomarcador quantitativo **ou** procedimento de validação\n",
                "3. Score ≥ limiar + sem exclusões (BCI ativo, motor imagery, etc.)\n",
                "\n",
                "**Prioridade pedagógica:** Alta (pedagogia explícita) | Média (psicologia/IHC/educação genérica) | Baixa (outros domínios)\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": src(
                r"""
# --- Passive BCI (obrigatório) ---
PATTERNS_PASSIVE = {
    r"\bpassive bci\b": 4,
    r"\bpbci\b": 4,
    r"\bpassive brain[\s-]?computer\b": 4,
    r"\bimplicit bci\b": 3,
    r"\bpassive brain interface\b": 3,
}

# --- Biomarcadores quantitativos ---
PATTERNS_BIOMARKER = {
    r"\bbiomarker\b|\bbio-marker\b": 3,
    r"beta[\s/-]?alpha|β/α": 4,
    r"\bspectral (power|index|ratio|feature)\b": 3,
    r"\bengagement index\b": 3,
    r"\beeg feature\b|\bneurophysiological (marker|indicator)\b": 3,
    r"\bquantitative\b.*\b(eeg|neural|brain)\b": 2,
    r"\bprefrontal\b.*\b(eeg|activity|power)\b": 2,
}

# --- Construção / validação ---
PATTERNS_VALIDATION = {
    r"\bvalidation\b|\bvalidity\b": 3,
    r"\breliability\b|\btest-retest\b|\bintraclass\b|\bicc\b": 3,
    r"\bcross-validation\b|\bk-fold\b": 2,
    r"\bground truth\b|\bcriterion validity\b": 3,
    r"\becological validity\b|\breal-world study\b": 2,
}

# --- Domínios (pedagogia com peso maior) ---
PATTERNS_PEDAGOGY = {
    r"\beducation\b|\beducational\b": 4,
    r"\blearning\b|\be-learning\b|\belearning\b": 4,
    r"\bpedagog\b|\bteaching\b|\bteacher\b|\bstudent\b": 4,
    r"\bclassroom\b|\bschool\b|\bcurriculum\b": 4,
    r"\btutoring\b|\bintelligent tutoring\b": 3,
    r"\bmooc\b|\bonline course\b": 3,
}

PATTERNS_REHAB = {
    r"\brehabilitation\b|\brehab\b": 3,
    r"\btherapy\b|\bclinical\b|\bpatient\b": 2,
    r"\bstroke\b|\bmotor recovery\b": 2,
}

PATTERNS_PSYCH = {
    r"\bpsycholog\b": 2,
    r"\bcognitive (state|load|engagement)\b": 2,
    r"\bmotivation\b|\battention\b|\bflow\b": 2,
}

PATTERNS_HCI = {
    r"\bhuman-computer\b|\bhci\b": 3,
    r"\badaptive (system|interface|feedback)\b": 3,
    r"\buser interface\b|\binteraction design\b": 2,
    r"\bclosed-loop\b|\bfeedback loop\b": 2,
    r"\busability\b|\buser experience\b": 2,
}

PATTERNS_NEUROERG = {
    r"\bneuroergonomic\b": 1,
    r"\bmental workload\b|\boperator\b|\bpilot\b": 1,
}

PATTERNS_EXCLUSION = {
    r"\bmotor imagery\b": -6,
    r"\bactive bci\b|\bexplicit bci\b": -6,
    r"\bprosthesis\b|\bexoskeleton\b|\bspell(er|ing)\b": -5,
    r"\bseizure\b|\bepilepsy\b": -4,
    r"\bfnirs\b|\bfmri\b|\bmri\b": -3,
}


def _score_patterns(text, patterns: dict) -> tuple[int, list[str]]:
    score = 0
    hits = []
    for pattern, weight in patterns.items():
        if re.search(pattern, text):
            score += weight
            hits.append(pattern.replace(r"\b", ""))
    return score, hits


def _primary_domain(text) -> str:
    domain_scores = {
        "Pedagogia": _score_patterns(text, PATTERNS_PEDAGOGY)[0],
        "Reabilitação": _score_patterns(text, PATTERNS_REHAB)[0],
        "Psicologia": _score_patterns(text, PATTERNS_PSYCH)[0],
        "IHC": _score_patterns(text, PATTERNS_HCI)[0],
        "Neuroergonomia": _score_patterns(text, PATTERNS_NEUROERG)[0],
    }
    best = max(domain_scores, key=domain_scores.get)
    return best if domain_scores[best] > 0 else "Indeterminado"


def _pedagogy_priority(text, domain: str) -> str:
    ped_score = _score_patterns(text, PATTERNS_PEDAGOGY)[0]
    if ped_score >= 4:
        return "Alta"
    if ped_score >= 2 or domain in {"Psicologia", "IHC"} or re.search(r"\blearning\b", text):
        return "Média"
    if domain in {"Reabilitação", "Neuroergonomia", "Indeterminado"}:
        return "Baixa"
    return "Média"


def evaluate_paper(title, abstract):
    text = f"{str(title)} {str(abstract)}".lower()

    passive_score, passive_hits = _score_patterns(text, PATTERNS_PASSIVE)
    biomarker_score, biomarker_hits = _score_patterns(text, PATTERNS_BIOMARKER)
    validation_score, validation_hits = _score_patterns(text, PATTERNS_VALIDATION)

    ped_score, _ = _score_patterns(text, PATTERNS_PEDAGOGY)
    rehab_score, _ = _score_patterns(text, PATTERNS_REHAB)
    psych_score, _ = _score_patterns(text, PATTERNS_PSYCH)
    hci_score, _ = _score_patterns(text, PATTERNS_HCI)
    neuro_score, _ = _score_patterns(text, PATTERNS_NEUROERG)

    exclusion_reasons = []
    exclusion_penalty = 0
    for pattern, weight in PATTERNS_EXCLUSION.items():
        if re.search(pattern, text):
            exclusion_penalty += weight
            exclusion_reasons.append(pattern.replace(r"\b", ""))

    total = (
        passive_score + biomarker_score + validation_score
        + ped_score + rehab_score + psych_score + hci_score + neuro_score
        + exclusion_penalty
    )

    matched = passive_hits + biomarker_hits + validation_hits
    domain = _primary_domain(text)
    priority = _pedagogy_priority(text, domain)

    if passive_score == 0:
        status = "EXCLUÍDO"
        motivo = "Sem passive BCI no título/resumo"
    elif biomarker_score == 0 and validation_score == 0:
        status = "EXCLUÍDO"
        motivo = "Sem biomarcador quantitativo nem validação"
    elif exclusion_penalty <= -6:
        status = "EXCLUÍDO"
        motivo = "BCI ativo / motor imagery / fora do escopo"
    elif total < SCREENING_MIN_SCORE:
        status = "EXCLUÍDO"
        motivo = f"Score {total} abaixo do limiar ({SCREENING_MIN_SCORE})"
    else:
        status = "INCLUÍDO (Pré-seleção)"
        motivo = ""

    return pd.Series([
        total, status, domain, priority,
        ", ".join(dict.fromkeys(matched)),
        ", ".join(exclusion_reasons) or motivo,
    ])


if df_screen.empty:
    print("Sem registros para triagem.")
else:
    df_screen[[
        "Score", "Status_Triagem", "Dominio_Principal",
        "Prioridade_Pedagogia", "Termos_Detectados", "Motivo_Exclusao",
    ]] = df_screen.apply(
        lambda r: evaluate_paper(r["title"], r["abstract"]), axis=1
    )
    print("--- RESULTADO DA PRÉ-TRIAGEM ---")
    print(df_screen["Status_Triagem"].value_counts())
    print("\n--- DOMÍNIO PRINCIPAL ---")
    print(df_screen["Dominio_Principal"].value_counts())
    print("\n--- PRIORIDADE PEDAGÓGICA (incluídos) ---")
    inc = df_screen[df_screen["Status_Triagem"] == "INCLUÍDO (Pré-seleção)"]
    if not inc.empty:
        print(inc["Prioridade_Pedagogia"].value_counts())
"""
            ),
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Célula 6: Matriz de síntese PRISMA-ScR\n",
                "> Colunas alinhadas às questões da revisão: biomarcador, construção, validação, "
                "ground truth, domínio, pedagogia, IHC e transferibilidade.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": CELL_SYNTHESIS,
        },
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python (passive_bci)",
            "language": "python",
            "name": "passive_bci",
        },
        "language_info": {
            "name": "python",
            "version": "3.10.12",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 2,
}

with open("triagem_zotero_prisma.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=1, ensure_ascii=False)

print("Notebook 'triagem_zotero_prisma.ipynb' criado com sucesso!")
