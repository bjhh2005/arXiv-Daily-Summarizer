# arXiv Daily Summarizer - Language Configuration

## Configuration

The setting controls the language of the email title and interface labels. Every
mode includes the original arXiv abstract. If `DEEPSEEK_API_KEY` is configured,
the email also includes an optional Chinese translation.

### Setting Language

Set the `EMAIL_LANGUAGE` environment variable:

```bash
# Chinese only (default)
export EMAIL_LANGUAGE=zh

# English only
export EMAIL_LANGUAGE=en

# Legacy bilingual value (uses English interface labels)
export EMAIL_LANGUAGE=both
```

Or in GitHub Secrets, add:
- Key: `EMAIL_LANGUAGE`
- Value: `zh`, `en`, or `both`

## Language Modes

### 1. Chinese Mode (`zh`) - DEFAULT
- Email title, labels, and UI in Chinese
- Original arXiv abstract and, when available, a Chinese translation
- This is the default if EMAIL_LANGUAGE is not set

### 2. English Mode (`en`)
- Email title, labels, and UI in English
- Original arXiv abstract and, when available, a Chinese translation

### 3. Bilingual Mode (`both`)
- Email title and labels in English (primary)
- Behaves like English mode for interface labels
- Retained for backward compatibility

## Examples

### Chinese Email
```
标题: arXiv 每日论文推送
日期提醒: 论文日期提醒
摘要: arXiv 原始摘要
翻译（可选）: 中文翻译
```

### English Email
```
Title: arXiv Daily Paper Digest
Date Notice: Date Notice
Summary: Original arXiv Abstract
Translation (optional): Chinese Translation
```

### Bilingual Email
```
Title: arXiv Daily Paper Digest
Date Notice: Date Notice
Summary: Original arXiv Abstract
Translation (optional): Chinese Translation
```

## Testing Locally

```bash
# Test Chinese
export EMAIL_LANGUAGE=zh
python fetch_papers.py

# Test English
export EMAIL_LANGUAGE=en
python fetch_papers.py

# Test Bilingual
export EMAIL_LANGUAGE=both
python fetch_papers.py
```

## Note

- AI translation is optional and is skipped when `DEEPSEEK_API_KEY` is absent
- Translation failures fall back to the original abstract without blocking email
- Default is Chinese (`zh`) if not specified
