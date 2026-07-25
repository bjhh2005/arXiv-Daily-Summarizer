import tempfile
import unittest
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

# Keep these unit tests independent from optional runtime dependencies.
sys.modules.setdefault(
    'arxiv',
    SimpleNamespace(
        Client=object,
        Search=lambda **kwargs: kwargs,
        SortCriterion=SimpleNamespace(SubmittedDate='submitted'),
        SortOrder=SimpleNamespace(Descending='descending'),
    ),
)
sys.modules.setdefault('openai', SimpleNamespace(OpenAI=object))

import fetch_papers


class PushHistoryTests(unittest.TestCase):
    def test_canonical_arxiv_id_ignores_revision_and_preserves_legacy_id(self):
        self.assertEqual(
            fetch_papers.canonical_arxiv_id(
                'https://arxiv.org/abs/hep-th/9901001v2'
            ),
            'hep-th/9901001',
        )

    def test_three_year_publication_window_uses_calendar_years(self):
        now = datetime(2026, 7, 25, 12, tzinfo=timezone.utc)
        self.assertTrue(
            fetch_papers.is_within_publication_window(
                datetime(2023, 7, 25, 12, tzinfo=timezone.utc), now
            )
        )
        self.assertFalse(
            fetch_papers.is_within_publication_window(
                datetime(2023, 7, 25, 11, 59, tzinfo=timezone.utc), now
            )
        )

    def test_sent_papers_are_merged_and_can_be_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            history_file = Path(directory) / 'sent_papers.json'
            paper = {
                'entry_id': 'https://arxiv.org/abs/2607.12345v1',
                'title': 'A useful paper',
                'published': datetime(2026, 7, 24, tzinfo=timezone.utc),
            }

            fetch_papers.record_sent_papers(
                [paper],
                history_file,
                sent_at=datetime(2026, 7, 25, tzinfo=timezone.utc),
            )
            history = fetch_papers.load_push_history(history_file)

            self.assertEqual(set(history), {'2607.12345'})
            self.assertEqual(history['2607.12345']['title'], 'A useful paper')

    def test_selection_skips_sent_and_out_of_window_papers(self):
        def result(entry_id, title, published):
            return SimpleNamespace(
                entry_id=entry_id,
                title=title,
                published=published,
                summary='A' * 200,
                authors=[SimpleNamespace(name='Author One')],
                pdf_url=f'{entry_id}.pdf',
                categories=['cs.AI'],
            )

        now = datetime.now(timezone.utc)
        results = [
            result('https://arxiv.org/abs/2607.00001v2', 'Already sent', now),
            result('https://arxiv.org/abs/2607.00002v1', 'Fresh and unseen', now),
            result(
                'https://arxiv.org/abs/2201.00003v1',
                'Outside the publication window',
                datetime(now.year - 4, 1, 1, tzinfo=timezone.utc),
            ),
        ]
        client = SimpleNamespace(results=lambda search: iter(results))

        with (
            patch.object(fetch_papers.arxiv, 'Client', return_value=client),
            patch.object(fetch_papers, 'CATEGORIES', ['cs.AI']),
            patch.object(fetch_papers, 'MAX_RESULTS', 5),
            patch('builtins.print'),
        ):
            papers = fetch_papers.get_latest_papers({'2607.00001'})

        self.assertEqual([paper['title'] for paper in papers], ['Fresh and unseen'])


if __name__ == '__main__':
    unittest.main()
